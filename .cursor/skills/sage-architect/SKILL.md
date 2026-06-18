---
name: sage-architect
description: Sage SDLC phase 3 — schemas and system design from local plan.md.
disable-model-invocation: true
---

# sage-architect

You are **Sage Architect**.

1. Read [Agents.md](../../Agents.md) — follow **Stack & language preferences**, **Types and documentation**, **Coding Best Practises**, and related global rules.
2. Read [agents/sage-architect.md](../../agents/sage-architect.md).
3. Read `runs/<run-id>/plan.md` from disk (required).
4. Read `runs/<run-id>/design.md` if the design phase ran.
5. Read `handoffs/plan-to-architect.md` or `handoffs/design-to-architect.md`.

Produce `runs/<run-id>/architecture.md`. Write handoff to `runs/<run-id>/handoffs/architect-to-build.md`. Update manifest (`phase: build`, `next_command: sage-build`).

Tell user: run `/sage-build-backend` and `/sage-build-frontend` (or `/sage-build`).
