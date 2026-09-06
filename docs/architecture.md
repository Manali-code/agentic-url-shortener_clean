# Architecture

## Overview

This project is structured around two parallel layers:

1. Application layer: FastAPI service for URL shortening and redirect flows.
2. Orchestration layer: agent-driven workflow describing the software delivery lifecycle.

## Components

- API: handles short URL creation, redirect, and analytics
- Database: SQLAlchemy models with SQLite/PostgreSQL flexibility
- Orchestrator: requirements, architecture, implementation, testing, docs, and release agents
- Governance: approval gate and policy engine for release readiness

## Design principles

- modular service boundaries
- stateless orchestration logic
- explicit approval checkpoints
- test-first validation workflow
- easy containerized deployment
