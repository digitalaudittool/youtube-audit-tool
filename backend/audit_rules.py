def run_audit(channel_data):
    stats = channel_data["items"][0]["statistics"]

    subscribers = int(stats.get("subscriberCount", 0))
    views = int(stats.get("viewCount", 0))
    videos = int(stats.get("videoCount", 0))

    audit = {}

    # Rule 1: Subscriber health
    audit["subscriber_health"] = {
        "status": "Good" if subscribers >= 100000 else "Needs Improvement",
        "message": (
            "Strong subscriber base."
            if subscribers >= 100000
            else "Focus on consistency and audience engagement."
        )
    }

    # Rule 2: Content volume
    audit["content_volume"] = {
        "status": "Good" if videos >= 100 else "Low",
        "message": (
            "Healthy number of videos."
            if videos >= 100
            else "Upload more content consistently."
        )
    }

    # Rule 3: View efficiency
    avg_views = views / videos if videos else 0
    audit["view_efficiency"] = {
        "status": "Good" if avg_views >= 1000 else "Low",
        "message": (
            "Videos attract good average views."
            if avg_views >= 1000
            else "Improve thumbnails, titles, and SEO."
        )
    }

    return audit
