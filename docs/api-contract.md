# Initial API Contract — Draft

This contract is a scaffold and must be reviewed/frozen by the team before integration.

- `GET /healthz`: process health only.
- `POST /v1/analyze`: initial JSON request with `request_id`, `audio_reference`, optional `language_hint`, and optional `client_id`.
- `POST /v1/language/identify`: LID service contract draft.
- `POST /v1/detect`: detector service contract draft.
- `GET /v1/jobs/{job_id}`: future job status; currently not implemented.

Outstanding decisions:
1. Upload bytes vs controlled audio reference.
2. Authentication between gateway and services.
3. Audio format, duration and payload limits.
4. Exact language label mapping and confidence semantics.
5. Detector score semantics and model versions.
6. Job persistence/Redis requirement and retry/timeout behavior.
7. Whether optional WSS updates are in scope.
