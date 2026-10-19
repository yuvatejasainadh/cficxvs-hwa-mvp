# CloudForge MVP — HackWithAditya

A lean HackVersion workspace for the CloudForge × VoiceShield MVP.

## MVP flow

VoiceShield Android/Web → existing gateway (if configured) → CloudForge API/orchestrator → LID → selected detector → shared result.

The initial local scaffold provides:
- `vmc-lid`: Open Vakgyata language-identification service scaffold.
- `vmc-south`: South Indian AASIST-L integration placeholder for Varun's validated model artifact.
- `vmc-english`: English/fallback AASIST-L integration placeholder.
- `orchestrator`: minimal API to coordinate the service path.
- Docker Compose for local development.

**Important:** Scaffolds are not completed inference services. Detector services return explicit `NOT_IMPLEMENTED` responses until real model inference is integrated. Never present placeholders as model predictions.

## Team ownership

- Yuvateja — orchestrator, contracts, routing, end-to-end integration.
- Varun — fine-tune/evaluate AASIST-L for the agreed South Indian scope; deliver versioned artifact and inference interface.
- Pallavi — Open Vakgyata LID service and Docker packaging.
- Varshu — English AASIST-L / fallback service and Docker packaging.

## Quick start

1. Copy `.env.example` to `.env` and review values.
2. Start the scaffold services:

   ```bash
   docker compose up --build
   ```

3. Check service health:
   - Orchestrator: `http://localhost:8000/healthz`
   - LID: `http://localhost:8001/healthz`
   - South detector: `http://localhost:8002/healthz`
   - English detector: `http://localhost:8003/healthz`

4. OpenAPI docs: `http://localhost:8000/docs`

The scaffold health endpoints indicate process health only; they do not prove that model inference is ready.

## API sketch

- `GET /healthz` — process health.
- `POST /v1/analyze` — accepts a JSON request with a language hint and audio reference. File upload/audio storage and the final contract must be agreed before integration.
- `GET /v1/jobs/{job_id}` — placeholder contract for future asynchronous job lifecycle.

See `contracts/` and `docs/api-contract.md`.

## Before claiming MVP completion

- [ ] Load the real Open Vakgyata artifact and validate labels against the model card.
- [ ] Implement and validate real South Indian AASIST-L inference.
- [ ] Implement and validate English/fallback AASIST-L inference.
- [ ] Freeze preprocessing, model I/O, response schema and routing policy.
- [ ] Add authenticated gateway integration and job lifecycle/Redis if required by final acceptance criteria.
- [ ] Run real end-to-end tests using supported recordings through the entire pipeline.
- [ ] Document model versions, evaluation evidence, limitations and license constraints.

## License note

Review the Open Vakgyata model's non-commercial license before commercial use. Model weights should not be committed to Git unless licensing and repository-size policy explicitly allow it.
