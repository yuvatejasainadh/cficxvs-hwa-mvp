import os
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="CloudForge LID — Open Vakgyata", version="0.1.0")
MODEL_ID = os.getenv("MODEL_ID", "onecxi/open-vakgyata")
MODEL_REVISION = os.getenv("MODEL_REVISION", "main")

class IdentifyRequest(BaseModel):
    request_id: str = Field(min_length=1)
    audio_reference: str = Field(min_length=1)

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "vmc-lid",
            "model_id": MODEL_ID, "model_revision": MODEL_REVISION,
            "inference_ready": False}

@app.post("/v1/language/identify")
def identify(request: IdentifyRequest):
    # TODO(Pallavi): load the actual HF model, resolve audio_reference safely,
    # preprocess/resample to the model's required format, and return real labels.
    return {
        "request_id": request.request_id,
        "status": "NOT_IMPLEMENTED",
        "model_id": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "language": None,
        "scores": None,
        "limitations": ["Open Vakgyata inference has not been integrated in this scaffold."]
    }
