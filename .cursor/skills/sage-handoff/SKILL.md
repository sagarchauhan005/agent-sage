---
name: sage-handoff
description: Sage SDLC — write or validate a profile-aware phase handoff.
disable-model-invocation: true
---

# sage-handoff

You are **Sage Orchestrator** writing a handoff.

1. Read [Agents.md](../../Agents.md).
2. Read [agents/_handoff-template.md](../../agents/_handoff-template.md).
3. Read [workflows/profiles.md](../../workflows/profiles.md).
4. Read the current run manifest and phase artifacts.

Respect `skipped_phases` — do not hand off to a skipped phase.

Fill in the handoff template completely. Save to `runs/<run-id>/handoffs/<from>-to-<to>.md`.

For QA completion, use `qa_handoff` from manifest (`qa-to-devops.md` or `qa-to-release.md`).

Update `manifest.json` with next phase and `agents.next_command`.

Tell user which `/sage-*` command to run next.
