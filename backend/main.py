import time
from typing import Dict
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.youtube_api import get_channel_data
from backend.audit_rules import run_audit


# --------------------
# App
# --------------------
app = FastAPI()

# --------------------
# CORS (required for WordPress / browser)
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Cache (STEP 2A)
# --------------------
CACHE: Dict[str, dict] = {}
CACHE_TTL = 3600  # 1 hour

# --------------------
# Rate limit (STEP 2B)
# --------------------
REQUESTS: Dict[str, list] = {}
RATE_LIMIT = 20      # max requests
RATE_WINDOW = 60     # per 60 seconds


def rate_limited(ip: str) -> bool:
    now = time.time()
    window = REQUESTS.get(ip, [])
    window = [t for t in window if now - t < RATE_WINDOW]

    if len(window) >= RATE_LIMIT:
        return True

    window.append(now)
    REQUESTS[ip] = window
    return False


# --------------------
# Routes
# --------------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/audit")
def audit(channel_id: str, request: Request):
    now = time.time()
    ip = request.client.host

    # ---- RATE LIMIT ----
    history = REQUESTS.get(ip, [])
    history = [t for t in history if now - t < RATE_WINDOW]

    if len(history) >= RATE_LIMIT:
        return {
            "error": "Rate limit exceeded. Please wait and try again."
        }

    history.append(now)
    REQUESTS[ip] = history
    # --------------------

    # ---- CACHE ----
    if channel_id in CACHE:
        cached = CACHE[channel_id]
        if now - cached["time"] < CACHE_TTL:
            return cached["data"]

    data = get_channel_data(channel_id)
    if not data or not data.get("items"):
        return {"error": "Channel not found"}

    audit_result = run_audit(data)

stats = data["items"][0]["statistics"]
snippet = data["items"][0]["snippet"]

subs = int(stats.get("subscriberCount", 0))
views = int(stats.get("viewCount", 0))
videos = int(stats.get("videoCount", 0))

avg_views = views / videos if videos else 0
views_per_sub = views / subs if subs else 0

published = snippet["publishedAt"]
channel_year = int(published[:4])

response = {
    "channel": data["items"][0],

    "summary": {
        "subscribers": subs,
        "views": views,
        "videos": videos,
        "avg_views": int(avg_views),
        "views_per_subscriber": round(views_per_sub, 2),
        "channel_age_year": channel_year
    },

    "audit": audit_result
}

    CACHE[channel_id] = {
        "time": now,
        "data": response
    }

    return response

