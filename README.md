# Agentic URL Shortener

A production-style prototype for an agentic software engineering system built around a URL shortener service. The project combines a working FastAPI application with a structured orchestration layer that models requirements, architecture, implementation, testing, documentation, governance, and release readiness.

## Objective

This project demonstrates how an AI-assisted engineering workflow can move from a vague requirement to a reviewable engineering outcome using explicit sequencing, state tracking, policy guardrails, approval gates, and validation checkpoints.

## Tech stack

- FastAPI
- SQLAlchemy
- SQLite/PostgreSQL
- Pytest
- LangChain / LangGraph patterns
- OpenAI / Azure OpenAI integration readiness
- Pydantic
- Docker
- GitHub Actions

## Core requirements addressed

- Requirement understanding and decomposition
- Architecture and implementation planning
- End-to-end service execution
- Automated validation
- Documentation and release readiness
- Governance and approval gates
- Workflow state tracking and dependency graph orchestration

## Workflow model

The orchestration layer includes a dependency-aware graph:

1. Requirements
2. Architecture
3. Implementation
4. Testing
5. Documentation
6. Release

Each stage is tracked with explicit dependencies and gating logic. The workflow supports approval checkpoints, retry handling, and state transitions that emulate a controlled agentic SDLC.

## Quick start

1. Create a virtual environment.
2. Install dependencies:
   `python -m pip install -r requirements.txt`
3. Start the app:
   `python -m uvicorn app.main:app --reload`
4. Visit the API docs:
   `http://127.0.0.1:8000/docs`

## Example usage

- POST `/shorten` with JSON: `{ "url": "https://example.com" }`
- GET `/r/{short_code}` to redirect
- GET `/stats/{short_code}` to inspect analytics

## Structure

- `app/`: application code and persistence layer
- `orchestrator/`: dependency graph, workflow state, metrics, governance, and agent stubs
- `tests/`: automated validation
- `docs/`: architecture and process notes
- `scenarios/`: greenfield, brownfield, and ambiguous requirements
- `.github/workflows/ci.yml`: CI pipeline stub

## Governance and risk posture

This prototype makes the following safeguards explicit:

- approval required before release actions
- policy validation for tests, documentation, and approval requirements
- retry and failure tracking via workflow metrics
- stateful execution that preserves context between stages
- runtime boundaries to reduce uncontrolled autonomy

## Limitations

This is still a prototype and intentionally models the SDLC orchestration pattern rather than a full production multi-agent runtime. It demonstrates controlled autonomy and governance but does not yet include a fully externalized orchestration engine, persistent workflow state storage, or production-grade agent runtime integrations.

## Documentation set

- [docs/architecture.md](docs/architecture.md)
- [docs/orchestration.md](docs/orchestration.md)
- [docs/decisions.md](docs/decisions.md)
- [docs/final_engineering_summary.md](docs/final_engineering_summary.md)
- [scenarios/greenfield.md](scenarios/greenfield.md)
- [scenarios/brownfield.md](scenarios/brownfield.md)
- [scenarios/ambiguous.md](scenarios/ambiguous.md)
