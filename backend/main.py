from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from youtube_api import get_channel_data
from audit_rules import run_audit

app = FastAPI()

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
    data = get_channel_data(channel_id)

    if not data or not data.get("items"):
        return {"error": "Channel not found"}

    audit_result = run_audit(data)

    return {
        "channel": data["items"][0],
        "audit": audit_result
    }
