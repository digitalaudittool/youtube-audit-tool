import os
import requests

API_KEY = os.getenv("YOUTUBE_API_KEY")
BASE = "https://www.googleapis.com/youtube/v3"


def _channels(params):
    params["key"] = API_KEY
    params["part"] = "snippet,statistics"
    r = requests.get(f"{BASE}/channels", params=params, timeout=10).json()
    return r.get("items", [])


def get_channel_data(query: str):
    if not API_KEY:
        return None

    q = query.strip()

    # 1️⃣ HANDLE (@name)
    if q.startswith("@"):
        items = _channels({"forHandle": q[1:]})
        if items:
            return {"items": items}

    # 2️⃣ USERNAME
    items = _channels({"forUsername": q})
    if items:
        return {"items": items}

    # 3️⃣ SEARCH fallback
    search = requests.get(
        f"{BASE}/search",
        params={
            "key": API_KEY,
            "part": "snippet",
            "q": q,
            "type": "channel",
            "maxResults": 1,
        },
        timeout=10,
    ).json()

    if not search.get("items"):
        return None

    channel_id = search["items"][0]["snippet"]["channelId"]
    items = _channels({"id": channel_id})

    if items:
        return {"items": items}

    return None
