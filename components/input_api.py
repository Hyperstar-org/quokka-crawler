from datetime import datetime

def fill_profile_data(data):
    author_data = data.get('author', {})
    _form = {
        "name": author_data.get('nickname', ""),
        "username":  author_data.get('uniqueId', ""),
        "email": f"{author_data.get('uniqueId', '')}@gmail.com",
        "bio": author_data.get("signature", ""),
        "profile_url": f"https://www.tiktok.com/{author_data.get('uniqueId', '')}",
        "avatar_url": "",
        "location": "",
        "date_last_post": datetime.fromtimestamp(data['create_time']).strftime("%Y-%m-%d %H:%M:%S"),
        "fake_follower_rate": 0,
        "avg_engagement_by_day": "",
        "avg_posting_time": "",
        "platform_ids": [
            "fa6b5bf2-5154-487a-9482-168fdacef1ae"
        ],
        "category_ids": [
            "9e7d2d14-6fbd-4930-ad69-72c851967f78"
        ],
        "metrics": {
            "follower_count": author_data.get('followerCount', ""),
            "engagement_rate": data.get('engagement_rate', ""),
            "active_status": True
        },
        "platform_metrics": [
        ]
    }
    return _form