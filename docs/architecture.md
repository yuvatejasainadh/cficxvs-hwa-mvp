# MVP Architecture

## Initial path

Existing VoiceShield clients → existing gateway (integration to be confirmed) → orchestrator → LID → language-aware route → detector → shared result.

## Services

- `orchestrator`: request coordination; currently scaffold-only.
- `vmc-lid`: Open Vakgyata LID; currently scaffold-only.
- `vmc-south`: South Indian AASIST-L; awaits Varun's validated artifact.
- `vmc-english`: English AASIST-L; awaits Varshu's runtime integration.

## Deferred

Seven-VM coverage, RIAS, TCED, Kubernetes/EKS, production autoscaling, broad live-call integration.

## Non-negotiable truthfulness

Health checks only indicate process health. A model is inference-ready only after artifact loading and real inference tests pass. A spoof score is not scam classification.
