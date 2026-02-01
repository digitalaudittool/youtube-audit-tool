from fastapi import FastAPI
from youtube_api import get_channel_data
from audit_rules import run_audit

app = FastAPI()

@app.get("/")
def health():
    return {"status": "Backend running"}

@app.get("/channel")
def channel(channel_id: str):
    data = get_channel_data(channel_id)
    return data

@app.get("/audit")
def audit(channel_id: str):
    channel_data = get_channel_data(channel_id)
    audit_result = run_audit(channel_data)
    return {
        "channel": channel_data,
        "audit": audit_result
    }
