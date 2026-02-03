import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI()

# This is what you set in Render Environment Variables
VALID_API_KEY = os.getenv("AUTH_KEY", "your-secret-key")

class DetectionRequest(BaseModel):
    message: str
    audio_url: str

# 1. ADD THIS: This handles GET requests to the main URL
@app.get("/")
def home():
    return {"status": "Server is alive. Use POST /detect for API calls."}

# 2. THIS IS THE TARGET: Ensure the tester is hitting this with POST
@app.post("/detect")
async def detect_voice(request: DetectionRequest, x_api_key: str = Header(None)):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid x-api-key")

    return {
        "status": "success",
        "prediction": "Real",
        "confidence_score": 0.95,
        "language": "en"
    }
