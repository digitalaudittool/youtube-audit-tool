import os
import requests

API_KEY = os.getenv("YOUTUBE_API_KEY")

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
CHANNELS_URL = "https://www.googleapis.com/youtube/v3/channels"


def get_channel_data(query: str):
    if not API_KEY:
        return None

    q = query.strip()

    # 1️⃣ If handle is provided, try forHandle (BEST & OFFICIAL)
    if q.startswith("@"):
        r = requests.get(
            CHANNELS_URL,
            params={
                "part": "snippet,statistics",
                "forHandle": q,
                "key": API_KEY,
            },
            timeout=10,
        ).json()

        if r.get("items"):
            return r

    # 2️⃣ Fallback: Search API (name / text)
    search = requests.get(
        SEARCH_URL,
        params={
            "part": "snippet",
            "q": q.replace("@", ""),
            "type": "channel",
            "maxResults": 1,
            "key": API_KEY,
        },
        timeout=10,
    ).json()

    if not search.get("items"):
        return None

    channel_id = search["items"][0]["snippet"]["channelId"]

    # 3️⃣ Fetch by channel ID
    channel = requests.get(
        CHANNELS_URL,
        params={
            "part": "snippet,statistics",
            "id": channel_id,
            "key": API_KEY,
        },
        timeout=10,
    ).json()

    return channel if channel.get("items") else None
