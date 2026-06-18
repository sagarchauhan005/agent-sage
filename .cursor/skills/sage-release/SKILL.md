---
name: sage-release
description: Sage SDLC phase 7 — commit, branch, open PR, complete run (from devops or QA).
disable-model-invocation: true
---

# sage-release

You are **Sage Release**.

1. Read [Agents.md](../../Agents.md) — follow **Working with Git**, **Secrets and credentials**, **Important rules**, and related global rules.
2. Read [agents/sage-release.md](../../agents/sage-release.md).
3. Read `runs/<run-id>/manifest.json`.
4. Read inputs based on profile:
   - devops ran → `deploy-report.md` + `handoffs/devops-to-release.md`
   - devops skipped → `test-report.md` + `handoffs/qa-to-release.md`

Scan for secrets and stop for user approval before push and PR per Agents.md.

Produce `runs/<run-id>/release-report.md`. Write `handoffs/release-complete.md`.

Mark manifest `phase: done`.
