---
name: sage-run
description: Sage SDLC full run — start a feature from plan through release.
disable-model-invocation: true
---

# sage-run

You are **Sage Orchestrator** running a full SDLC pipeline.

1. Read [Agents.md](../../Agents.md).
2. Read [agents/sage-orchestrator.md](../../agents/sage-orchestrator.md).
3. Read [workflows/feature-sdlc.yaml](../../workflows/feature-sdlc.yaml).

Create a new run folder: `runs/<YYYY-MM-DD>-<feature-slug>/` with `manifest.json`.

**Phase 1 must use Plan mode** and write `runs/<run-id>/plan.md` before continuing.

Execute phases in order:

| Order | Command | Agent file |
|-------|---------|------------|
| 1 | sage-plan | agents/sage-planner.md |
| 2 | sage-design | agents/sage-designer.md |
| 3 | sage-architect | agents/sage-architect.md |
| 4 | sage-build-backend + sage-build-frontend | agents/sage-backend.md + agents/sage-frontend.md |
| 5 | sage-qa | agents/sage-qa.md |
| 6 | sage-devops | agents/sage-devops.md |
| 7 | sage-release | agents/sage-release.md |

At each phase:

- Load the agent file + prior handoffs
- Produce the phase artifact
- Write handoff to `runs/<run-id>/handoffs/`
- Update `manifest.json`
- Stop at gates (push, PR, deploy) for user approval

On QA failure, loop back to the failing build phase.

On release complete, mark run `phase: done`. Apply Self-improvement rules from Agents.md if learnings surfaced.

Include a learning nugget in each phase summary per Agents.md.
