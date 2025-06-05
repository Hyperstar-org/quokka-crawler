"""Module defines the main entry point for the Apify Actor.

Feel free to modify this file to suit your specific needs.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

from __future__ import annotations

import json

from apify import Actor, Configuration
from bs4 import BeautifulSoup
from decouple import config

from components.helpers import logger
from components.scraper import TikTokScraper

DATASETS_NAME = "tiktok"


async def main() -> None:
    """Define a main entry point for the Apify Actor.

    This coroutine is executed using `asyncio.run()`, so it must remain an asynchronous function for proper execution.
    Asynchronous execution is required for communication with Apify platform, and it also enhances performance in
    the field of web scraping significantly.
    """
    async with Actor:
        dataset_client = await Actor.open_dataset(name=DATASETS_NAME,
                                                  force_cloud=False)

        logger.info("Dataset ID:", dataset_client._id)  # or dataset_client.id if available

        actor_input = await Actor.get_input() or {'keyword': 'k-beauty'}
        keyword = "#" + actor_input.get('keyword')
        max_influencers = actor_input.get('max_influencers', 50)

        scraper = TikTokScraper(keyword=keyword, max_influencers=max_influencers,
                                apify_client=dataset_client)

        await scraper.extract_influencers()


