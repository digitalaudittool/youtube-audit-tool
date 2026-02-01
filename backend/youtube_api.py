import os
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def get_channel_data(channel_id_or_query: str):
    if not YOUTUBE_API_KEY:
        return {"error": "API key not configured"}

    # If user passes full channel ID
    if channel_id_or_query.startswith("UC"):
        channel_id = channel_id_or_query
    else:
        # Search channel by name
        search_response = requests.get(
            YOUTUBE_SEARCH_URL,
            params={
                "part": "snippet",
                "q": channel_id_or_query,
                "type": "channel",
                "maxResults": 1,
                "key": YOUTUBE_API_KEY
            },
            timeout=10
        ).json()

        if not search_response.get("items"):
            return {"error": "Channel not found"}

        channel_id = search_response["items"][0]["snippet"]["channelId"]

    # Fetch channel statistics
    channel_response = requests.get(
        YOUTUBE_CHANNEL_URL,
        params={
            "part": "snippet,statistics",
            "id": channel_id,
            "key": YOUTUBE_API_KEY
        },
        timeout=10
    ).json()

    if not channel_response.get("items"):
        return {"error": "Channel data not available"}

    return channel_response["items"][0]
