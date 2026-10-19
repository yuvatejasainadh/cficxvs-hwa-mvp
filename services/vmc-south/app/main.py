import os
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="CloudForge South Detector — AASIST-L", version="0.1.0")
MODEL_STATUS = os.getenv("MODEL_STATUS", "not_configured")

class DetectRequest(BaseModel):
    request_id: str = Field(min_length=1)
    audio_reference: str = Field(min_length=1)
    language: str | None = None

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "vmc-south",
            "model_status": MODEL_STATUS, "inference_ready": False}

@app.post("/v1/detect")
def detect(request: DetectRequest):
    # TODO(Varun): load the evaluated/versioned South Indian AASIST-L artifact.
    # TODO: implement the agreed preprocessing and genuine inference.
    return {
        "request_id": request.request_id,
        "status": "NOT_IMPLEMENTED",
        "model_id": "aasist-l-south",
        "model_version": None,
        "detector_evidence": None,
        "limitations": ["South Indian AASIST-L artifact/inference is not integrated."]
    }
