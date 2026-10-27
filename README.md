# CloudForge Intelligence Core for VoiceShield (CFIC × VS)

**TEAM SAIL · HackWithAditya 2026**  
**Primary theme:** Cybersecurity, FinTech & Digital Trust  
**Technical differentiator:** Language-aware AI infrastructure for voice security  
**Repository:** https://github.com/yuvatejasainadh/cficxvs-hwa-mvp

> **Project in one line:** CFIC is the shared inference and orchestration layer for VoiceShield that identifies the language of incoming audio, routes it to an appropriate validated audio-spoofing detector, and returns a consistent, traceable result.

---

## 1. Problem Statement

AI-generated speech, voice cloning, and audio spoofing can undermine trust in voice-based communication and identity checks. At the same time, integrating language identification and specialized detection models separately into every client can duplicate routing logic, fragment service interfaces, and make model updates harder to manage.

**VoiceShield needs a unified, language-aware inference layer** that can identify the language of an audio request, select an appropriate validated detector, and return a consistent result through one interface. It must also handle uncertain language predictions, unsupported languages, invalid audio, and model-service failures explicitly rather than silently selecting an unsuitable model or returning fabricated scores.

CFIC addresses this infrastructure problem by coordinating language identification and specialized audio-spoofing detection behind a common API.

## 2. Proposed Solution

CFIC separates VoiceShield client integrations from the model-serving layer. A central orchestrator validates and coordinates each request, calls the language-identification service, applies an explicit routing policy, invokes the selected detector, and returns a normalized result with request and model metadata where available.

The project combines:
- **Cybersecurity:** supports VoiceShield's audio-spoofing analysis workflow.
- **Multilingual AI:** uses language identification to inform detector selection.
- **Cloud engineering:** separates services into containerized components with defined contracts.
- **Responsible inference:** makes unsupported cases and failures explicit and distinguishes real model outputs from prototype mocks.

CFIC is infrastructure for audio-spoofing detection; it is **not itself a new detection model**, and a detector score must not be interpreted as a calibrated fraud probability unless evaluation supports that interpretation.

## 3. Target Users

- VoiceShield Android and web application users.
- VoiceShield application and backend developers.
- Product teams integrating voice-analysis functionality into their applications or services.

## 4. Architecture and Fixed Model Scope

The HackVersion has **exactly three model services**. The orchestrator coordinates them and is not a fourth model.

1. **Open-Vakgyata LID** — language identification.
2. **VMC-South fine-tuned AASIST-L** — audio-spoofing detection for the validated South Indian language scope.
3. **AASIST-L English/fallback** — English detection and only those fallback cases explicitly approved by the routing policy.

```text
VoiceShield Android / Web
          |
          | HTTPS / REST
          v
CFIC API + Orchestrator
          |
          | Internal model-service calls
          v
Open-Vakgyata Language Identification
          |
          v
Explicit, confidence-aware routing policy
          |
          +------------------------------+
          |                              |
          v                              v
VMC-South fine-tuned AASIST-L    AASIST-L English/fallback
          |                              |
          +---------------+--------------+
                          v
             Normalized analysis result
                          |
                          v
                 VoiceShield client
```

### Routing principles

- Confident language result within the South model's validated scope → VMC-South.
- Confident English result → English detector when enabled by policy.
- Low-confidence language result → documented abstain, retry, or specifically approved fallback behavior.
- Unsupported language → explicit unsupported response unless an approved, evaluated route exists.
- LID or detector failure → controlled error; never guess a language or fabricate a score.
- Mock mode, if used for the MVP demonstration, must be visibly labelled in the response and demo.

### Protocol boundary

The initial repository scaffold uses HTTP/FastAPI interfaces. The HackVersion target is HTTPS/REST from VoiceShield to CFIC and versioned protobuf/gRPC for internal orchestrator-to-model calls. This is a planned integration boundary, **not a claim that the current scaffold already uses gRPC**. Any migration must be implemented deliberately, with shared contracts and tests updated together.

## 5. MVP and HackVersion: Different Delivery Targets

| Area | MVP / Level 1 prototype | HackVersion / complete target |
|---|---|---|
| Purpose | Reproducible prototype demonstrating the request-to-result flow | Fully integrated, cloud-hosted inference pipeline |
| Models | Real components where integrated; mocks allowed only when clearly labelled | All three actual model services |
| Routing | Demonstrate explicit routing and controlled failure behavior | Real LID-driven routing to the validated detector |
| API | Shared request/result contract and working prototype path | HTTPS API integrated with VoiceShield |
| Internal calls | Current scaffold interfaces, documented honestly | Agreed protobuf/gRPC contracts |
| Deployment | Reproducible local Docker Compose setup | Cloud deployment using tested, versioned containers |
| Evidence | Tests and demo clearly distinguish implemented features from mocks | End-to-end real-audio evidence and model evaluation/limitations |

**Release rule:** Do not describe the system as a fully working HackVersion until actual model inference, routing, VoiceShield integration, and cloud deployment have been demonstrated end to end.

## 6. Technology Stack

The initial scaffold uses:

- **Python** — service implementation.
- **FastAPI** — HTTP APIs for the orchestrator and model-service scaffolds.
- **Docker** — containerization.
- **Docker Compose** — local multi-service development.
- **JSON Schema** — initial request/response contracts.
- **pytest** — automated tests.

Target components and requirements:
- Open-Vakgyata model artifact/runtime for LID.
- Validated fine-tuned AASIST-L artifact for VMC-South.
- Actual AASIST-L artifact/runtime for the English/fallback service.
- Versioned protobuf/gRPC contracts for internal model calls in the HackVersion.
- HTTPS and deployment-appropriate authentication for external VoiceShield-to-CFIC traffic.
- Cloud container hosting for the completed HackVersion.

The precise cloud provider, hardware/GPU requirements, dependency versions, model revisions, and environment variables must be documented from the tested deployment before submission. Do not infer them from this README.

## 7. Repository Structure

```text
cficxvs-hwa-mvp/
├── README.md
├── .env.example
├── docker-compose.yml
├── Makefile
├── contracts/
│   ├── analyze-request.schema.json
│   ├── analyze-result.schema.json
│   └── README.md
├── services/
│   ├── orchestrator/
│   ├── vmc-lid/
│   ├── vmc-south/
│   └── vmc-english/
├── tests/
└── docs/
```

The structure above is a high-level map. Check the current repository for the exact files and test dependencies.

## 8. Quick Start: Local Prototype

### Prerequisites

- Git.
- Docker Desktop or Docker Engine with Docker Compose.
- Python 3.11 or a compatible Python environment if running tests outside containers.

### Clone and start

```bash
git clone https://github.com/yuvatejasainadh/cficxvs-hwa-mvp.git
cd cficxvs-hwa-mvp
```

Create a local environment file.

**Windows CMD**
```cmd
copy .env.example .env
```

**PowerShell, Linux, or macOS**
```bash
cp .env.example .env
```

Review `.env` and configure any required values before starting:

```bash
docker compose up --build
```

If the repository's current Compose configuration exposes these ports, the local endpoints are:

| Service | Endpoint |
|---|---|
| Orchestrator | `http://localhost:8000` |
| LID service | `http://localhost:8001` |
| South detector service | `http://localhost:8002` |
| English detector service | `http://localhost:8003` |

Health endpoints, if enabled by the current service implementation:
- `http://localhost:8000/healthz`
- `http://localhost:8001/healthz`
- `http://localhost:8002/healthz`
- `http://localhost:8003/healthz`

Orchestrator API documentation, if enabled:
- `http://localhost:8000/docs`

Stop the local services:

```bash
docker compose down
```

**Important:** A successful container start or process-health response does not prove that model weights are loaded or that inference is working. Verify the current implementation and model-readiness behavior before using these endpoints as evidence in a submission.

## 9. Tests and Validation

Install test dependencies using the repository's current test requirements file, if present, then run:

```bash
python -m pytest tests -q
```

Run commands from a clean clone before relying on them in the submission. Update this section if the actual repository uses a different test path or setup command.

### Required validation layers

1. **Unit tests** — validate routing, validation, and error-handling functions.
2. **Contract tests** — verify request and response schemas.
3. **Model component tests** — use known recordings to verify each real model service.
4. **Integration tests** — verify the orchestrator's calls to LID and the selected detector.
5. **End-to-end tests** — demonstrate VoiceShield → CFIC → LID → detector → normalized result.

### Required behavior matrix

| Scenario | Expected behavior |
|---|---|
| Supported South language, confident LID | Invoke South detector only if that language is validated |
| English, confident LID | Invoke English detector when enabled by policy |
| Unsupported language | Explicit unsupported response or approved documented policy |
| Low-confidence LID | Documented abstain/retry/approved fallback; no arbitrary routing |
| Invalid or corrupt audio | Controlled validation error |
| LID unavailable or times out | Controlled service error; no guessed language |
| Detector unavailable or times out | Controlled service error; no fabricated score |
| Mock inference | Clearly label the response as mocked/demo output |
| Real inference | Identify actual model/version and inference status where available |

## 10. HackWithAditya Submission Readiness

The project submission should include the required team/member details and project title, problem statement, target users, abstract/project document, working prototype, feature and limitation list, GitHub repository with reproducible setup steps, a demo video under five minutes, and the actual tech stack, hardware/runtime requirements, and dependencies.

### Judging alignment

- **Problem relevance:** explain the voice-spoofing and digital-trust problem.
- **Prototype credibility:** demonstrate a real request, actual outputs, tests, and clearly labelled mocks.
- **48-hour feasibility:** keep the three-model scope fixed and the baseline runnable.
- **Technical clarity:** explain the API contract, routing policy, service boundaries, failure behavior, and score limitations.
- **Originality:** clearly distinguish TEAM SAIL's architecture and implementation from external models, libraries, templates, and adapted code.

For Level 2, the organizers will announce **two mandatory enhancements and one optional stretch goal** at the event. Do not assume or invent those requirements in advance. Keep a clean baseline, assign clear owners, test incrementally, and make coherent commits to the shared repository at least every three hours during the on-site build.

## 11. Demo Plan: Under Five Minutes

1. **0:00–0:30 — Problem:** why VoiceShield needs a common, language-aware inference layer.
2. **0:30–1:00 — Architecture:** show the three model services and explicit routing policy.
3. **1:00–2:00 — Live request:** submit a prepared, non-sensitive test recording and show request ID, language result, route, and output status.
4. **2:00–3:00 — Engineering evidence:** show containers, tests, contracts, and the real inference path that exists in the current build.
5. **3:00–4:00 — Failure/limitations:** demonstrate invalid audio or an unsupported/low-confidence case; explain how mocks are labelled.
6. **4:00–5:00 — Value and close:** state what is implemented, what is validated, what remains, and why the system can be extended during the 48-hour challenge.

Record the actual current build. Never imply that mocked inference is real. Do not show credentials, private audio, secrets, or sensitive dataset information.

## 12. Security, Privacy, and Model Limitations

- Never commit API keys, credentials, tokens, private endpoints, or secrets.
- Use environment variables and deployment secret stores for configuration.
- Do not commit model weights unless license terms, artifact size, and distribution requirements permit it.
- Verify and document each model's source, version/revision, license, supported language scope, and limitations.
- Review the Open-Vakgyata model license before any commercial use.
- Document audio retention and deletion behavior before processing real user recordings.
- Avoid logging raw audio or sensitive personal information.
- Apply input size/duration limits, timeouts, and appropriate request validation.
- Keep internal gRPC services on a private network in the deployed HackVersion; expose only the secured external API.
- Distinguish process health from model readiness.
- Do not call an uncalibrated spoof score a probability of fraud or proof that a caller is a scammer.
- Clearly label any mocked model output as `MOCKED_FOR_DEMO` or an equivalent explicit status.

## 13. Team Responsibilities

### Yuvateja Sainadh Kasukurthi — Systems Architect and Integration Lead
- Own overall CFIC architecture, shared contracts, orchestration, routing, result normalization, and failure behavior.
- Coordinate integration with the existing VoiceShield gateway where available.
- Run end-to-end validation and prepare the technical demo.
- Maintain the scope and ensure the implementation matches the submitted claims.

### Padavala Varun Ranga Rao — South Detector / MLOps
- Fine-tune and evaluate the agreed South-scope AASIST-L model.
- Deliver a versioned artifact and reproducible inference entry point.
- Document preprocessing, supported languages, evaluation evidence, thresholds, and limitations.
- Coordinate containerization and the detector service interface.

### Koduru Pallavi — Language Identification Service
- Integrate and containerize the actual Open-Vakgyata LID artifact/runtime.
- Validate labels, preprocessing, language coverage, health/readiness, and error behavior.
- Document model provenance, license, and limitations.

### Gude Kanaka Sri Varshini — English Detector and Cloud Integration Support
- Package the agreed English AASIST-L detector path.
- Validate preprocessing and inference against known test recordings.
- Support gateway/request-validation tests and deployment readiness.
- Document model limitations and unsupported-language behavior.

All members should be able to explain their component, tests, contracts, dependencies, external model/code sources, and which features are real, mocked, or planned.

## 14. AI, External Code, and Originality Disclosure

HackWithAditya permits coding assistants and AI APIs subject to disclosure. Before submission, TEAM SAIL must complete an accurate disclosure of:
- AI tools used, what they assisted with, and human review/testing performed.
- External libraries and frameworks, versions, purposes, and licenses.
- External model names, sources, revisions, licenses/usage terms, supported languages, and known limitations.
- Code copied or adapted from documentation, examples, repositories, or templates.
- Each team member's ownership and understanding of their submitted work.

Do not claim external model weights, libraries, or adapted code as original work. Ensure the team can explain every submitted component.

## 15. Feature Status and Project Honesty

Use one of these statuses for each feature in the submission and demo:

- `IMPLEMENTED_AND_TESTED`
- `IMPLEMENTED_NOT_FULLY_VALIDATED`
- `MOCKED_FOR_PROTOTYPE`
- `PLANNED_NOT_IMPLEMENTED`

A directory, Dockerfile, API route, schema, health endpoint, or mock response alone does not prove that real model inference is complete.

**Current implementation status must be verified against the actual repository before submission.** Update the status below based on tested evidence; do not leave a scaffold described as a fully operational pipeline.

| Capability | Status | Evidence / notes |
|---|---|---|
| Common API and request/result contracts | To verify | Link tests or demo evidence |
| Open-Vakgyata real LID inference | To verify | Record model revision and test evidence |
| VMC-South real AASIST-L inference | To verify | Record artifact version and evaluation evidence |
| English AASIST-L real inference | To verify | Record artifact version and evaluation evidence |
| Real LID-driven routing | To verify | Link integration test |
| Controlled unsupported/error paths | To verify | Link tests or demo evidence |
| Cloud-hosted end-to-end VoiceShield flow | To verify | Record deployment and real-audio test evidence |

## 16. Roadmap

### Phase 1 — Reproducible MVP
- Freeze shared request/result contracts and routing rules.
- Ensure a clean checkout starts locally.
- Test request validation, request IDs, and controlled errors.
- Label any mocked inference explicitly.

### Phase 2 — Real model services
- Integrate and validate Open-Vakgyata LID.
- Integrate and validate the fine-tuned South AASIST-L detector.
- Integrate and validate the English AASIST-L detector.
- Add model-readiness checks and model/version metadata.

### Phase 3 — End-to-end HackVersion
- Implement real LID-driven routing and normalized results.
- Finalize internal protobuf/gRPC contracts and external HTTPS integration.
- Deploy tested, versioned containers to the cloud.
- Verify the complete VoiceShield-to-CFIC-to-detector-to-VoiceShield path.

### Phase 4 — Level 2 enhancement challenge
- Preserve a clean, runnable baseline.
- Convert the exact organizer brief into acceptance criteria.
- Complete both mandatory enhancements before attempting the optional stretch.
- Test, integrate, document, and demonstrate the actual changes.

### Future productionization
Further detector groups, broader telephony/VoIP integration, autoscaling, and high availability are future extensions, not part of the fixed three-model HackVersion scope.

---

## 17. Project Identity

- **Project:** CloudForge Intelligence Core for VoiceShield
- **Short name:** CFIC × VS
- **Team:** TEAM SAIL
- **Hackathon:** HackWithAditya 2026
- **Primary theme:** Cybersecurity, FinTech & Digital Trust
- **Technical differentiator:** Language-aware AI routing
- **Repository:** https://github.com/yuvatejasainadh/cficxvs-hwa-mvp

**Security is the problem we solve; multilingual intelligence is how we make the solution more capable.**
