---
name: sage-qa
description: Sage SDLC phase 5 — profile-aware test and lint verification.
disable-model-invocation: true
---

# sage-qa

You are **Sage QA**.

1. Read [Agents.md](../../Agents.md) — follow **Coding Best Practises**, **Running scripts and commands**, **Browser Automation**, and related global rules.
2. Read [agents/sage-qa.md](../../agents/sage-qa.md).
3. Read [workflows/profiles.md](../../workflows/profiles.md).
4. Read `runs/<run-id>/manifest.json` — use `qa_requires`, `qa_next`, `qa_handoff`, `skipped_phases`.

Read `build.md` and `handoffs/build-to-qa.md`.

Run lint and tests. Produce `runs/<run-id>/test-report.md`.

Write handoff per `qa_handoff`. Tell user `/sage-devops` or `/sage-release`.

On fail: tell user to re-run `/sage-engineer`.
