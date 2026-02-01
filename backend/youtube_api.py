import os
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_channel_data(channel_id: str):
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "snippet,statistics",
        "id": channel_id,
        "key": YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params, timeout=10)
    return response.json()
