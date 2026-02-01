from fastapi import FastAPI
from youtube_api import get_channel_data
from audit_rules import run_audit

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/channel")
def channel(channel_id: str):
    return get_channel_data(channel_id)

@app.get("/audit")
def audit(channel_id: str):
    data = get_channel_data(channel_id)
    audit_result = run_audit(data)
    return {
        "channel": data["items"][0],
        "audit": audit_result
    }
