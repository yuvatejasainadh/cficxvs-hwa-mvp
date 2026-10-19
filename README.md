# CloudForge Intelligence Core for VoiceShield (CFIC × VS)

### HackWithAditya · MVP / HackVersion

**A common distributed intelligence infrastructure for VoiceShield across mobile applications, web applications, APIs, SDKs, telephony, and VoIP integrations.**

---

## 1. Project Overview

**CloudForge Intelligence Core for VoiceShield (CFIC × VS)** is a distributed intelligence infrastructure designed to provide a common, modular, and extensible processing layer for VoiceShield's voice impersonation and deepfake detection capabilities.

The platform aims to separate application-facing integrations from AI inference services. Instead of requiring every client application to implement its own language identification, model selection, and inference orchestration, CFIC provides a shared API and coordinated service pipeline.

For the HackWithAditya MVP, the project focuses on establishing a practical, testable end-to-end path from an audio analysis request to a structured detection result.

The implementation begins with a limited, validated inference path rather than attempting to deploy every planned model, region, or integration at once.

### Core objectives

- Establish a common API contract for VoiceShield clients.
- Identify the language of a supported audio recording.
- Route supported requests to an appropriate validated detector.
- Coordinate inference through a central orchestrator.
- Return consistent, structured analysis results.
- Keep model services modular and independently deployable.
- Establish a foundation for future distributed deployment and multi-channel integration.

---

## 2. Problem Statement

VoiceShield may be integrated into different environments, including Android applications, web applications, APIs, SDKs, telephony, and VoIP systems.

Without a shared intelligence layer, each integration may need to manage its own inference requests, model interfaces, routing rules, and response handling. This can lead to duplicated integration logic, inconsistent responses, and difficulty replacing or upgrading individual models.

**CFIC × VS addresses this architectural challenge by introducing a common orchestration and inference interface between VoiceShield clients and specialized AI services.**

The MVP will validate this architecture through a controlled audio-analysis pipeline, with explicit handling of unsupported inputs, unavailable services, and inference failures.

---

## 3. MVP Architecture

```text
VoiceShield Android / Web
          |
          v
Existing VoiceShield API Gateway
(if configured)
          |
          v
CloudForge API / Orchestrator
          |
          v
Language Identification (LID)
          |
          v
Routing Policy
          |
          +----------------------+
          |                      |
          v                      v
South Indian Detector     English Detector
(VM2_SOUTH)               (VM2_ENGLISH / fallback)
          |                      |
          +-----------+----------+
                      |
                      v
             Result Aggregation
                      |
                      v
          Structured Analysis Result
                      |
                      v
          VoiceShield Android / Web
```

The English detector is a separate service in the initial scaffold. Whether it is used as a fallback for a particular language must be determined by the validated routing policy; unsupported languages must not silently receive misleading predictions.

The architecture describes the intended pipeline. The current repository contains service scaffolds, not a fully operational inference pipeline.

### Proposed service responsibilities

| Component | Responsibility |
|---|---|
| VoiceShield clients | Submit analysis requests and consume results |
| Existing API gateway | Authentication, request validation, rate limiting, and secure forwarding, if configured |
| Orchestrator | Coordinate service calls, routing, errors, and result aggregation |
| VM1_LID | Identify the language of supported audio |
| VM2_SOUTH | Provide validated South Indian-scope anti-spoofing inference |
| VM2_ENGLISH | Provide validated English-scope anti-spoofing inference |
| Shared contracts | Standardize request and response formats |

---

## 4. Technology Stack

The initial scaffold uses the following technologies:

- **Python** — service implementation
- **FastAPI** — HTTP APIs for the orchestrator and model services
- **Docker** — service containerization
- **Docker Compose** — local multi-service development
- **JSON Schema** — shared request and response contract definitions
- **pytest** — automated scaffold and contract tests

### Planned integration components

The following are integration targets, not claims that they are already implemented:

- Open Vakgyata for language identification
- A validated AASIST-L artifact for the South Indian detector
- A validated AASIST-L artifact or explicitly approved English-only detector path
- Existing VoiceShield API gateway
- Redis and background workers if asynchronous job processing is required by the finalized acceptance criteria
- Cloud deployment and service-to-service security as later implementation milestones

The initial scaffold uses HTTP/FastAPI interfaces. Any change to gRPC or protobuf should be agreed upon and reflected in the shared contracts before implementation diverges across team members.

---

## 5. Repository Structure

```text
cficxvs-hwa-mvp/
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
├── Makefile
│
├── contracts/
│   ├── analyze-request.schema.json
│   ├── analyze-result.schema.json
│   └── README.md
│
├── services/
│   ├── orchestrator/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       └── main.py
│   │
│   ├── vmc-lid/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       └── main.py
│   │
│   ├── vmc-south/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       └── main.py
│   │
│   └── vmc-english/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── app/
│           └── main.py
│
├── tests/
│   └── test_scaffold_contract.py
│
└── docs/
    ├── architecture.md
    ├── api-contract.md
    ├── team-assignments.md
    └── local-setup.md
```

This layout is intended to keep the API, model services, contracts, tests, and documentation separated so each team member can work on an assigned component without modifying unrelated services.

---

## 6. Team Responsibilities

### Yuvateja Sainadh Kasukurthi — Applied AI Engineer, Systems Architect & Cloud Infrastructure Architect

**Primary ownership: CFIC architecture and end-to-end integration**

- Define and maintain the overall MVP architecture.
- Finalize shared request and result contracts.
- Implement orchestrator routing and result aggregation.
- Coordinate the LID-to-detector service path.
- Define job lifecycle and error-handling behavior.
- Integrate the existing VoiceShield gateway where available.
- Define Android and web adapter requirements.
- Coordinate local infrastructure and deployment planning.
- Perform end-to-end tests after the real model services are integrated.
- Prepare the technical demonstration and document limitations.

### Padavala Varun Ranga Rao — MLOps Architect & ML Infrastructure Engineer

**Primary ownership: South Indian detector**

- Fine-tune and evaluate AASIST-L for the agreed South Indian scope.
- Define audio preprocessing, sample-rate requirements, and model input/output.
- Deliver a versioned model artifact and reproducible inference entry point.
- Provide baseline evaluation evidence.
- Document supported languages, limitations, and threshold-calibration status.
- Coordinate a stable interface for integration with the orchestrator.

### Koduru Pallavi — Cloud Engineer

**Primary ownership: Open Vakgyata language-identification service**

- Package the Open Vakgyata LID service in Docker.
- Integrate the actual model artifact and inference runtime.
- Validate model labels against the model card.
- Define and test audio preprocessing and service input/output.
- Add health checks, startup validation, configuration, and useful logs.
- Document language coverage, model limitations, and readiness status.
- Review the model license before any commercial use.

### Gude Kanaka Sri Varshini — Cloud Engineer

**Primary ownership: English detector and gateway integration support**

- Package the agreed English AASIST-L detector or approved fallback path.
- Define the service interface and audio preprocessing requirements.
- Validate inference behavior using known test recordings.
- Support gateway integration and request-validation tests.
- Test HTTPS request submission and result retrieval where configured.
- Support WebSocket integration only if it is included in the agreed MVP scope.
- Document detector limitations and unsupported-language behavior.

**Shared rule:** Agree on the service contract, audio format, preprocessing, error schema, and model readiness criteria before merging the components.

---

## 7. Local Development

### Prerequisites

- Git
- Docker Desktop with Docker Compose
- Python 3.11 or a compatible Python environment for running tests directly

### Start the services

Clone the repository and enter its directory:

```bash
git clone https://github.com/yuvatejasainadh/cficxvs-hwa-mvp.git
cd cficxvs-hwa-mvp
```

Create the local environment file:

**Windows CMD**
```cmd
copy .env.example .env
```

**PowerShell, Linux, or macOS**
```bash
cp .env.example .env
```

Review the environment values and start the services:

```bash
docker compose up --build
```

### Local service endpoints

| Service | Local endpoint |
|---|---|
| Orchestrator | `http://localhost:8000` |
| LID | `http://localhost:8001` |
| South detector | `http://localhost:8002` |
| English detector | `http://localhost:8003` |

Health checks:

- `http://localhost:8000/healthz`
- `http://localhost:8001/healthz`
- `http://localhost:8002/healthz`
- `http://localhost:8003/healthz`

Orchestrator API documentation:

`http://localhost:8000/docs`

**Important:** These health checks currently indicate process health only. They do not prove that model weights are loaded or that inference is operational.

Stop the services with:

```bash
docker compose down
```

---

## 8. Testing

Install the test dependencies:

```bash
python -m pip install -r tests/requirements.txt
```

Run the current scaffold tests:

```bash
python -m pytest tests -q
```

The scaffold tests validate the initial structure and contract behavior. They do not prove that the real LID model or detector models are accurate or integrated.

### Required validation layers

1. **Unit tests** — validate individual functions and service behavior.
2. **Contract tests** — verify that services follow the shared request and response schemas.
3. **Component tests** — validate each real model service using known recordings.
4. **Integration tests** — verify communication between the orchestrator, LID, and selected detector.
5. **End-to-end tests** — submit a supported recording through the complete client-to-result path.

End-to-end completion must be demonstrated with actual model inference, not only mocked responses or successful health checks.

---

## 9. MVP Acceptance Criteria

The MVP should not be considered complete until the following are demonstrated:

- [ ] Android and web integrations follow the agreed shared API contract.
- [ ] Valid requests receive the agreed request or job identifier.
- [ ] Invalid or unauthorized requests are rejected when gateway authentication is configured.
- [ ] The real LID model identifies supported test recordings correctly enough for the documented acceptance criteria.
- [ ] A supported recording completes the validated LID-to-detector inference path.
- [ ] Detector responses follow the shared result schema.
- [ ] Unsupported inputs, malformed audio, timeouts, and service failures produce controlled errors.
- [ ] Routing does not silently apply an unvalidated detector to unsupported languages.
- [ ] Model versions, preprocessing, evaluation evidence, and limitations are documented.
- [ ] Integration and end-to-end tests pass against the real services.
- [ ] The demonstration distinguishes implemented features from future work.

---

## 10. Scope Boundaries

### Included in the initial HackVersion

- A common API contract
- A minimal orchestrator
- One real language-identification service
- One validated South Indian detector path
- A separately defined English detector path
- Docker-based local development
- Basic automated tests
- Controlled failure handling
- A demonstrable end-to-end analysis flow

### Deferred unless explicitly required

- All seven planned VM/model groups
- Full RIAS/TCED implementation
- Production-grade autoscaling and high availability
- Broad live-call, telephony, and VoIP integration
- Full production AWS/EKS deployment
- Unvalidated scam classification
- Any model routing path that lacks evaluation evidence

The HackVersion prioritizes a working, explainable, validated pipeline over the number of services or technologies displayed in the architecture.

---

## 11. Security, Privacy, and Model Limitations

- Never commit API keys, credentials, private endpoints, or secrets to Git.
- Keep environment-specific settings in local environment files and deployment secret stores.
- Do not commit model weights unless licensing, repository size, and distribution requirements permit it.
- Review the Open Vakgyata model's non-commercial license before commercial use.
- Document audio retention and deletion behavior before processing real user recordings.
- Avoid logging raw audio or sensitive personal data.
- Do not treat a healthy service process as proof that model inference is ready.
- Do not describe a deepfake score as proof that a caller is a scammer.
- Document detector thresholds and calibration status instead of presenting unvalidated scores as reliable probabilities.

Voice impersonation detection and scam classification are different tasks. CFIC × VS must report only what the integrated and evaluated models support.

---

## 12. Future Roadmap

### Phase 1 — Scaffold and contracts
- [x] Create the initial service structure.
- [x] Define initial request/result schemas.
- [x] Add Docker-based local development.
- [ ] Freeze service interfaces and routing rules.

### Phase 2 — Real model integration
- [ ] Integrate and validate Open Vakgyata.
- [ ] Integrate the agreed South Indian AASIST-L artifact.
- [ ] Integrate and validate the English detector path.
- [ ] Add model readiness checks.

### Phase 3 — Orchestration and integration
- [ ] Implement real LID-to-detector routing.
- [ ] Implement consistent result aggregation and error handling.
- [ ] Integrate the existing gateway where available.
- [ ] Add job lifecycle and Redis workers if required by the final acceptance criteria.

### Phase 4 — Validation and demonstration
- [ ] Run component and contract tests.
- [ ] Run end-to-end tests with supported recordings.
- [ ] Record evaluation evidence and known limitations.
- [ ] Demonstrate the working VoiceShield-to-CFIC pipeline.

### Phase 5 — Future productionization
- Evaluate cloud deployment and service-to-service security.
- Add further validated detector groups as justified.
- Explore broader application, SDK, telephony, and VoIP integrations.
- Evaluate scaling, resilience, observability, and operational requirements.

---

## 13. Project Status

**Current status: Initial scaffold created; real inference integration pending.**

The repository establishes the starting structure for the CloudForge Intelligence Core for VoiceShield HackWithAditya MVP. The API services and contracts provide a foundation for parallel development, but the real model artifacts, routing pipeline, gateway integration, and end-to-end inference must be implemented and validated before the project can be described as a functioning MVP.

---

## 14. Project Identity

**Project name:** CloudForge Intelligence Core for VoiceShield  
**Short name:** CFIC × VS  
**Repository:** `cficxvs-hwa-mvp`  
**Program:** HackWithAditya  
**Core focus:** Distributed intelligence infrastructure for voice impersonation detection  
**Primary objective:** A common, modular, validated AI inference path for VoiceShield integrations

---

*CloudForge Intelligence Core for VoiceShield — one coordinated intelligence layer, multiple integration surfaces, and a validated path from audio input to analysis result.*
