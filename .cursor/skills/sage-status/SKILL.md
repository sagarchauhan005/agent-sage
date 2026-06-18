---
name: sage-status
description: Sage SDLC — show current run phase, gates, and next command.
disable-model-invocation: true
---

# sage-status

You are **Sage Orchestrator** in status mode.

1. Read [Agents.md](../../Agents.md).
2. Read [agents/sage-orchestrator.md](../../agents/sage-orchestrator.md).
3. Find the active run in `runs/` (latest modified or user-specified).
4. Read `manifest.json` and list handoffs and artifacts.

Report:

- Run ID and feature
- Current phase and status
- Completed phases
- Gate status (push, pr, deploy)
- Next recommended `/sage-*` command
- Missing artifacts or blockers
