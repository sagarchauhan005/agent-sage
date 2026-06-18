---
name: sage-status
description: Sage SDLC — show run profile, phase, skips, gates, and next command.
disable-model-invocation: true
---

# sage-status

You are **Sage Orchestrator** in status mode.

1. Read [Agents.md](../../Agents.md).
2. Read [agents/sage-orchestrator.md](../../agents/sage-orchestrator.md).
3. Read [workflows/profiles.md](../../workflows/profiles.md).
4. Find the active run in `runs/` (latest modified or user-specified).
5. Read `manifest.json` and list handoffs and artifacts.

Report:

- Run ID and feature
- `workflow_profile`
- `skipped_phases`
- `qa_requires` and whether each artifact exists (especially `build.md` before QA)
- `qa_next` and `qa_handoff`
- Current phase and status
- Completed phases
- Gate status (push, pr, deploy)
- Next recommended `/sage-*` command
- Missing artifacts or blockers
