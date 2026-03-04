def run_audit(channel_data):
    stats = channel_data["items"][0]["statistics"]
    published = channel_data["items"][0]["snippet"]["publishedAt"]

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

        # Rule 4: Channel Activity
    audit["channel_activity"] = {
        "status": "Active" if videos >= 50 else "Inactive",
        "message": (
            "Channel shows healthy publishing activity."
            if videos >= 50
            else "Channel has very few uploads. Increasing activity may improve growth."
        )
    }

    # Rule 5: Channel Age Strength
from datetime import datetime

channel_year = int(published[:4])
current_year = datetime.utcnow().year
age = current_year - channel_year

audit["channel_age_strength"] = {
    "status": "Strong" if age >= 5 else "New",
    "message": (
        "Channel has strong historical presence."
        if age >= 5
        else "Channel is relatively new. Growth may take time."
    )
}

    return audit
