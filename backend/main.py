import time
from typing import Dict
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from youtube_api import get_channel_data
from audit_rules import run_audit


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
    # 🚦 Rate-limit FIRST
    client_ip = request.client.host
    if rate_limited(client_ip):
        return {"error": "Too many requests. Please wait a minute."}

    now = time.time()

    # 🔁 Cache hit
    if channel_id in CACHE:
        cached = CACHE[channel_id]
        if now - cached["time"] < CACHE_TTL:
            return cached["data"]

    # 🔍 Fetch YouTube data
    data = get_channel_data(channel_id)
    if not data or not data.get("items"):
        return {"error": "Channel not found"}

    audit_result = run_audit(data)

    response = {
        "channel": data["items"][0],
        "audit": audit_result
    }

    # 💾 Save to cache
    CACHE[channel_id] = {
        "time": now,
        "data": response
    }

    return response
