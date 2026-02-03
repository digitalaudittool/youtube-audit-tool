import os
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

BASE_URL = "https://www.googleapis.com/youtube/v3"


def _get_channels(params):
    params["key"] = YOUTUBE_API_KEY
    params["part"] = "snippet,statistics"
    res = requests.get(f"{BASE_URL}/channels", params=params, timeout=10).json()
    return res.get("items")


def get_channel_data(query: str):
    if not YOUTUBE_API_KEY:
        return None

    q = query.strip()

    # 1️⃣ Try HANDLE (most reliable now)
    if q.startswith("@"):
        items = _get_channels({"forHandle": q[1:]})
        if items:
            return {"items": items}

    # 2️⃣ Try USERNAME (old channels)
    items = _get_channels({"forUsername": q})
    if items:
        return {"items": items}

    # 3️⃣ Fallback: SEARCH API
    search = requests.get(
        f"{BASE_URL}/search",
        params={
            "key": YOUTUBE_API_KEY,
            "part": "snippet",
            "q": q,
            "type": "channel",
            "maxResults": 1
        },
        timeout=10
    ).json()

    if not search.get("items"):
        return None

    channel_id = search["items"][0]["snippet"]["channelId"]

    items = _get_channels({"id": channel_id})
    if items:
        return {"items": items}

    return None
