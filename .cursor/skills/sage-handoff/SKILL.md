---
name: sage-handoff
description: Sage SDLC — write or validate a phase handoff between agents.
disable-model-invocation: true
---

# sage-handoff

You are **Sage Orchestrator** writing a handoff.

1. Read [Agents.md](../../Agents.md).
2. Read [agents/_handoff-template.md](../../agents/_handoff-template.md).
3. Read the current run manifest and phase artifacts.

Fill in the handoff template completely. Save to `runs/<run-id>/handoffs/<from>-to-<to>.md`.

Update `manifest.json` with next phase and `agents.next_command`.

Tell user which `/sage-*` command to run next.
