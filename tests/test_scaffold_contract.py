from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def test_request_schema_has_required_fields():
    schema = json.loads((ROOT / "contracts/analyze-request.schema.json").read_text())
    assert set(schema["required"]) == {"request_id", "audio_reference"}

def test_result_schema_does_not_claim_scam_assessment_by_default():
    schema = json.loads((ROOT / "contracts/analyze-result.schema.json").read_text())
    assert "NOT_ASSESSED" in schema["properties"]["scam_risk_assessment"]["enum"]

def test_all_services_have_dockerfiles():
    for service in ("orchestrator", "vmc-lid", "vmc-south", "vmc-english"):
        assert (ROOT / "services" / service / "Dockerfile").exists()
