import os
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="CloudForge English/Fallback Detector — AASIST-L", version="0.1.0")
MODEL_STATUS = os.getenv("MODEL_STATUS", "not_configured")

class DetectRequest(BaseModel):
    request_id: str = Field(min_length=1)
    audio_reference: str = Field(min_length=1)
    language: str | None = None

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "vmc-english",
            "model_status": MODEL_STATUS, "inference_ready": False}

@app.post("/v1/detect")
def detect(request: DetectRequest):
    # TODO(Varshu): wire the existing English AASIST-L artifact/runtime.
    # Do not use this route as a universal fallback for unsupported languages
    # until that behavior has been explicitly evaluated and approved.
    return {
        "request_id": request.request_id,
        "status": "NOT_IMPLEMENTED",
        "model_id": "aasist-l-english",
        "model_version": None,
        "detector_evidence": None,
        "limitations": ["English AASIST-L inference is not integrated in this scaffold."]
    }
