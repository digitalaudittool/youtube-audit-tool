import time
from typing import Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from youtube_api import get_channel_data
from audit_rules import run_audit

app = FastAPI()
CACHE: Dict[str, dict] = {}
CACHE_TTL = 3600  # 1 hour

# ✅ CORS (required for WordPress / browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/audit")
def audit(channel_id: str):
    now = time.time()

    if channel_id in CACHE:
        cached = CACHE[channel_id]
        if now - cached["time"] < CACHE_TTL:
            return cached["data"]

    data = get_channel_data(channel_id)
    if not data or not data.get("items"):
        return {"error": "Channel not found"}

    audit_result = run_audit(data)

    response = {
        "channel": data["items"][0],
        "audit": audit_result
    }

    CACHE[channel_id] = {
        "time": now,
        "data": response
    }

    return response

