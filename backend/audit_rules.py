def run_audit(channel_data):
    stats = channel_data["items"][0]["statistics"]

    subs = int(stats.get("subscriberCount", 0))
    views = int(stats.get("viewCount", 0))
    videos = int(stats.get("videoCount", 0))

    audit = {}

    # Rule 1: Subscriber health
    if subs >= 100000:
        audit["subscriber_health"] = {
            "status": "Good",
            "message": "Strong subscriber base."
        }
    else:
        audit["subscriber_health"] = {
            "status": "Needs Improvement",
            "message": "Try to increase subscriber engagement."
        }

    # Rule 2: Upload volume
    if videos >= 100:
        audit["content_volume"] = {
            "status": "Good",
            "message": "Healthy number of videos."
        }
    else:
        audit["content_volume"] = {
            "status": "Low",
            "message": "Upload more videos consistently."
        }

    # Rule 3: Views per video
    avg_views = views / videos if videos else 0
    if avg_views >= 1000:
        audit["view_efficiency"] = {
            "status": "Good",
            "message": "Videos attract good average views."
        }
    else:
        audit["view_efficiency"] = {
            "status": "Low",
            "message": "Work on thumbnails, titles, and SEO."
        }

    return audit
