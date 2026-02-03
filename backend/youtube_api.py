import os
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"


def get_channel_data(query: str):
    if not YOUTUBE_API_KEY:
        return None

    # 1️⃣ Try search (handle / name)
    search = requests.get(
        SEARCH_URL,
        params={
            "part": "snippet",
            "q": query,
            "type": "channel",
            "maxResults": 1,
            "key": YOUTUBE_API_KEY,
        },
        timeout=10,
    ).json()

    channel_id = None
    if search.get("items"):
        channel_id = search["items"][0]["snippet"]["channelId"]

    # 2️⃣ If search failed, try forUsername
    if not channel_id:
        channel = requests.get(
            CHANNELS_URL,
            params={
                "part": "snippet,statistics",
                "forUsername": query.replace("@", ""),
                "key": YOUTUBE_API_KEY,
            },
            timeout=10,
        ).json()

        if channel.get("items"):
            return channel

        return None

    # 3️⃣ Fetch channel by ID
    channel = requests.get(
        CHANNELS_URL,
        params={
            "part": "snippet,statistics",
            "id": channel_id,
            "key": YOUTUBE_API_KEY,
        },
        timeout=10,
    ).json()

    return channel if channel.get("items") else None
