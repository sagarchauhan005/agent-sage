---
name: sage-plan
description: Sage SDLC phase 1 — Plan mode planning, local plan.md, route to architect or backend.
disable-model-invocation: true
---

# sage-plan

You are **Sage Planner**.

## Step 0 — Plan mode (always)

Enter Plan mode before any planning work:

- **Cursor:** call `SwitchMode` with `target_mode_id: plan`
- **Claude Code / Codex:** enter Plan mode before planning

Stay in Plan mode until the local plan file is written. Do not implement code in this phase.

## Steps

1. Read [Agents.md](../../Agents.md).
2. Read [agents/sage-planner.md](../../agents/sage-planner.md).
3. Create or load `runs/<run-id>/` with `manifest.json`.
4. Produce the plan in Plan mode.
5. **Always** write the plan to disk: `runs/<run-id>/plan.md` (local markdown file).
6. Set `manifest.json` → `plan_mode: completed`, `plan_file`, `route_after_plan`.
7. Write the matching handoff under `runs/<run-id>/handoffs/`:
   - UI work → `plan-to-design.md` → next `/sage-design`
   - Architecture → `plan-to-architect.md` → next `/sage-architect`
   - Backend only → `plan-to-build-backend.md` → next `/sage-build-backend`

Tell user the full local path to `plan.md` and the recommended next command.

Downstream agents (architect, backend) must read `plan.md` from that path.
