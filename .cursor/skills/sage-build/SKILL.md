---
name: sage-build
description: Sage SDLC phase 4 — run backend and frontend build in parallel.
disable-model-invocation: true
---

# sage-build

You are **Sage Orchestrator** coordinating parallel build.

1. Read [Agents.md](../../Agents.md).
2. Read [agents/sage-orchestrator.md](../../agents/sage-orchestrator.md).
3. Read [agents/sage-backend.md](../../agents/sage-backend.md) and [agents/sage-frontend.md](../../agents/sage-frontend.md).
4. Read `runs/<run-id>/design.md`, `runs/<run-id>/architecture.md`, and `runs/<run-id>/handoffs/architect-to-build.md`.

Delegate backend and frontend work (use Task subagents in parallel when available):

- Backend → `build-backend.md` + `handoffs/build-backend-to-qa.md`
- Frontend → `build-frontend.md` + `handoffs/build-frontend-to-qa.md`

Update manifest when both complete. Tell user: run `/sage-qa`.
