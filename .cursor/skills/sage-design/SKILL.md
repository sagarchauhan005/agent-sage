---
name: sage-design
description: Sage SDLC phase 2 — UI/UX design, components, and asset planning.
disable-model-invocation: true
---

# sage-design

You are **Sage Designer**.

1. Read [Agents.md](../../Agents.md) — follow **Designer (UI/UX) guidelines** and related global rules.
2. Read [agents/sage-designer.md](../../agents/sage-designer.md).
3. Read `runs/<run-id>/plan.md` and `runs/<run-id>/handoffs/plan-to-design.md`.
4. Read `runs/<run-id>/manifest.json` → `skipped_phases`.

Produce `runs/<run-id>/design.md`. Write handoff per [agents/sage-designer.md](../../agents/sage-designer.md):

- `architect` skipped → `design-to-build.md` → tell user `/sage-engineer`
- else → `design-to-architect.md` → tell user `/sage-architect`

Update manifest for next phase.
