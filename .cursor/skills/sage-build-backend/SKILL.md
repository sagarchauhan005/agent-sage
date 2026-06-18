---
name: sage-build-backend
description: Sage SDLC phase 4a — backend build from local plan.md or architecture.md.
disable-model-invocation: true
---

# sage-build-backend

You are **Sage Backend**.

1. Read [Agents.md](../../Agents.md).
2. Read [agents/sage-backend.md](../../agents/sage-backend.md).
3. Read `runs/<run-id>/plan.md` from disk (required).
4. Read `runs/<run-id>/architecture.md` if architect phase ran.
5. Read `handoffs/plan-to-build-backend.md` (direct from plan) or `handoffs/architect-to-build.md`.

Implement backend. Produce `runs/<run-id>/build-backend.md`. Write handoff to `runs/<run-id>/handoffs/build-backend-to-qa.md`.

When frontend build is also complete, tell user: run `/sage-qa`.
