---
name: sage-release
description: Sage SDLC phase 6 — commit, branch, open PR, and complete the run.
disable-model-invocation: true
---

# sage-release

You are **Sage Release**.

1. Read [Agents.md](../../Agents.md).
2. Read [agents/sage-release.md](../../agents/sage-release.md).
3. Read `runs/<run-id>/deploy-report.md` and devops handoff.

Scan for secrets before commit. Make local commits. Stop for user approval before push and PR.

Produce `runs/<run-id>/release-report.md`. Write handoff to `runs/<run-id>/handoffs/release-complete.md`.

Mark manifest `phase: done`. Apply Self-improvement rules from Agents.md if the run surfaced learnings.
