import json
import asyncio
import re
import os
import logging
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor

from apify_client import ApifyClient

from components.helpers import get_request_data_async, input_data_to_api
from components.constants import (
    headers, params_keyword, cookies,
    params_detail, params_comment,
    data_dir, params_reply
)
from components.input_api import fill_profile_data


class TikTokScraper:
    """
    Advanced TikTok data scraper with robust multithreading support.

    Features:
    - Concurrent video and comment extraction
    - Configurable scraping parameters
    - Detailed error handling
    - Comprehensive metadata collection
    """

    def __init__(self,
                 apify_client,
                 keyword: str,
                 max_influencers: int = 100,
                 max_workers: int = 10,
                 log_level: int = logging.INFO,
                 ):
        """
        Initialize TikTok scraper with configurable parameters.

        :param keyword: Search keyword for TikTok content
        :param max_influencers: Maximum number of influencers to scrape
        :param max_workers: Number of concurrent threads
        :param log_level: Logging verbosity level
        """
        self.logger = self._setup_logger(log_level)
        self.kw = keyword
        self.total_data = []
        self.offset = 0
        self.limit = 20
        self._client = apify_client
        self.max_influencers = max_influencers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def _setup_logger(self, log_level: int) -> logging.Logger:
        """
        Configure and return a logger for the scraper.

        :param log_level: Logging verbosity
        :return: Configured logger instance
        """
        logger = logging.getLogger('TikTokScraper')
        logger.setLevel(log_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def calculate_engagement_rate(likes: int, comments: int, shares: int, views: int) -> float:
        """
        Calculate engagement rate percentage.

        :param likes: Number of likes
        :param comments: Number of comments
        :param shares: Number of shares
        :param views: Number of views
        :return: Engagement rate percentage
        """
        return (likes + comments + shares) / views * 100 if views > 0 else 0

    async def get_author_metadata(self, author_unique_id: str) -> Dict:
        """
        Retrieve detailed metadata for a specific TikTok author.

        :param author_unique_id: Unique identifier for the author
        :return: Author's metadata dictionary
        """
        url = f'https://www.tiktok.com/@{author_unique_id}'
        pattern = r'(?<="stats":)([^}]*)'

        try:
            text = await get_request_data_async(
                url=url,
                headers=headers,
                cookies=cookies,
                params=params_keyword
            )
            match = re.search(pattern, text)
            stats_json = match.group(0) + "}"
            return json.loads(stats_json)
        except Exception as e:
            self.logger.error(f"Error fetching author metadata: {e}")
            return {}

    async def extract_influencers(self) -> List[Dict]:
        """
        Extract influencer data from TikTok search results.

        :return: List of extracted influencer data
        """
        url = 'https://www.tiktok.com/api/search/item/full/'

        while len(self.total_data) < self.max_influencers:
            try:
                params_keyword.update({
                    'keyword': self.kw,
                    'offset': self.offset,
                    'limit': self.limit
                })

                data = await get_request_data_async(
                    url=url,
                    headers=headers,
                    cookies=cookies,
                    params=params_keyword
                )

                data_list = json.loads(data)
                tasks = []

                for item in data_list['item_list']:
                    task = self.process_video_item(item)
                    tasks.append(task)

                await asyncio.gather(*tasks)

                if len(self.total_data) >= self.max_influencers:
                    break

                self.offset += self.limit

            except Exception as e:
                self.logger.error(f"Data extraction error: {e}")
                break

        return self.total_data

    async def process_video_item(self, item: Dict):
        """
        Process a single video item with concurrent comment extraction.

        :param item: Video item dictionary
        """
        try:
            engagement_rate = self.calculate_engagement_rate(
                likes=item['stats']['diggCount'],
                shares=item['stats']['shareCount'],
                views=item['stats']['playCount'],
                comments=item['stats']['commentCount']
            )

            author_stats = await self.get_author_metadata(
                author_unique_id=item['author'].get('uniqueId')
            )

            processed_item = {
                'author': {**item['author'], **author_stats},
                'video': item['video'],
                'description': item['desc'],
                'id': item['id'],
                'create_time': item['createTime'],
                'hashtags': item.get('textExtra', []),
                'engagement_rate': engagement_rate,
                'stats': item['stats']
            }

            comments = await self.extract_comments(
                video_id=item['id'],
                unique_id=item['author']['uniqueId']
            )
            processed_item['comments'] = comments

            await self.save_video_data(processed_item)
        except Exception as e:
            self.logger.error(f"Video processing error: {e}")

    async def extract_comments(self, video_id: str, unique_id: str) -> List[Dict]:
        """
        Extract comments for a specific video with reply handling.

        :param video_id: Unique video identifier
        :param unique_id: Author's unique identifier
        :return: List of comments with replies
        """
        total_comments = []
        cursor, limit = 0, 20

        while True:
            try:
                params = params_comment.copy()
                params.update({
                    'aweme_id': video_id,
                    'cursor': cursor,
                    'limit': limit
                })

                comments = await self.extract_comment_batch(params, unique_id)

                if not comments:
                    break

                total_comments.extend(comments)
                cursor += limit

                if len(total_comments) >= 100:  # Limit total comments
                    break

            except Exception as e:
                self.logger.error(f"Comment extraction error: {e}")
                break

        return total_comments

    async def extract_comment_batch(self, params: Dict, unique_id: str) -> List[Dict]:
        """
        Extract a batch of comments with concurrent reply processing.

        :param params: Request parameters
        :param unique_id: Author's unique identifier
        :return: List of processed comments
        """
        url = 'https://www.tiktok.com/api/comment/list/'

        data = await get_request_data_async(
            url=url,
            headers=headers,
            cookies=cookies,
            params=params
        )

        comment_data = json.loads(data)
        comments = comment_data.get('comments', [])

        # Mark author's comments and process replies concurrently
        processed_comments = []
        for comment in comments:
            comment['is_author_reply'] = comment['user']['unique_id'] == unique_id
            comment['replies'] = await self.extract_comment_replies(comment, unique_id)
            processed_comments.append(comment)

        return processed_comments

    async def extract_comment_replies(self, comment: Dict, unique_id: str) -> List[Dict]:
        """
        Extract replies for a specific comment.

        :param comment: Parent comment dictionary
        :param unique_id: Author's unique identifier
        :return: List of comment replies
        """
        comment_id = comment.get('cid', '')
        video_id = comment.get('aweme_id', '')
        reply_count = comment.get('reply_comment_total', 0)

        if reply_count <= 4:
            return comment.get('reply_comment', [])

        replies = []
        cursor = 0

        while True:
            new_replies, cursor = await self.fetch_comment_replies(
                comment_id, video_id, str(cursor), unique_id
            )

            if not new_replies:
                break

            replies.extend(new_replies)
            cursor += 1

        return replies

    async def fetch_comment_replies(self, comment_id: str, video_id: str,
                                    cursor: str, unique_id: str) -> Tuple[List[Dict], str]:
        """
        Fetch replies for a specific comment.

        :param comment_id: Parent comment ID
        :param video_id: Video ID
        :param cursor: Pagination cursor
        :param unique_id: Author's unique identifier
        :return: Tuple of replies and new cursor
        """
        url = "https://www.tiktok.com/api/comment/list/reply/"
        params = params_reply.copy()
        params.update({
            'comment_id': comment_id,
            'item_id': video_id,
            'cursor': cursor
        })

        data = await get_request_data_async(
            url=url,
            headers=headers,
            cookies=cookies,
            params=params
        )

        reply_data = json.loads(data)
        comments = reply_data.get('comments', [])

        # Mark author's replies
        processed_replies = [
            {**comment, 'is_author_reply': comment['user']['unique_id'] == unique_id}
            for comment in comments
        ]

        return processed_replies, reply_data.get('cursor', '')

    async def save_video_data(self, item: Dict):
        """
        Save video data to JSON file with thread pool.

        :param item: Video data dictionary
        """
        # await asyncio.get_event_loop().run_in_executor(
        #     self.executor,
        #     self._save_video_sync,
        #     item
        # )
        await self._save_video_sync(item=item)

    async def push_data_to_api(self, json_data):
        url = "https://dev.quokkaai.org/api/v1/influencers/"
        input_data_to_api(url, json=json_data)




    async def _save_video_sync(self, item: Dict):
        """
        Synchronous method to save video data to file.

        :param item: Video data dictionary
        """
        try:
            # result = await self._client.push_data(item)
            json_data = fill_profile_data(data=item)
            await self.push_data_to_api(json_data)
            self.logger.info(f"Saved {item['id']} data successfully.")
        except Exception as e:
            self.logger.error(f"Error saving video data: {e}")

