import os
import requests
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI()

# Use Environment Variable from Render Settings
VALID_AUTH_KEY = os.getenv("AUTH_KEY", "default-secret-key")

class DetectionRequest(BaseModel):
    message: str
    audio_url: str

@app.get("/")
def health():
    return {"status": "Service is online"}

@app.post("/detect")
async def detect_voice(request: DetectionRequest, authorization: str = Header(None)):
    if authorization != VALID_AUTH_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # Check if URL is valid
        audio_response = requests.get(request.audio_url, timeout=10)
        audio_response.raise_for_status()

        # Mock result
        return {
            "status": "success",
            "test_message": request.message,
            "prediction": "Real",
            "confidence_score": 0.99,
            "language": "Multi-Language-Detected",
            "error": None
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
