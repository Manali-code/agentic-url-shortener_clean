# Brownfield Scenario

Integrate a URL shortener into an existing service platform. Priorities:

## Before/after impact analysis

Before integration, existing authentication and analytics own request identity and
event persistence. The shortener should add a URL mapping and redirect path without
duplicating either concern. After integration, the service layer calls the existing
auth boundary, writes a mapping plus analytics event, and exposes stats through the
same observability pipeline.

## Orchestration and rollback

The requirements agent captures compatibility constraints; architecture identifies
the mapping migration and data-flow touch points; implementation is followed by
testing and documentation as independent dependency-ready steps. A migration or
implementation failure restores the pre-step state, records a rollback, and retries
only within the graph's bounded budget. Release still requires tests, docs, security
review, and explicit approval.

## Validation and risks

The critical checks are auth preservation, idempotent backfill, redirect correctness,
analytics continuity, and migration rollback. The risk register includes schema
drift, duplicate short codes, partial backfills, and downtime during index creation.
