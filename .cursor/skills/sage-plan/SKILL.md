---
name: sage-plan
description: Sage SDLC phase 1 — Plan mode, stack detection, local plan.md, route next phase.
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

1. Read [Agents.md](../../Agents.md) — follow all global rules.
2. Read [agents/sage-planner.md](../../agents/sage-planner.md).
3. Read [workflows/profiles.md](../../workflows/profiles.md).
4. Create or load `runs/<run-id>/` with `manifest.json`.
5. Set stack in `plan.md` per Agents.md **Stack & language preferences**.
6. Set `workflow_profile` from [workflows/profiles.md](../../workflows/profiles.md).
7. Copy profile defaults: `skipped_phases`, `qa_requires`, `qa_next`, `qa_handoff`.
8. Produce the plan in Plan mode.
9. **Always** write the plan to disk: `runs/<run-id>/plan.md`.
10. Write the matching handoff:
   - UI profiles (`ui-feature`, `web-product`, `ui-deploy`, `full-stack-no-deploy`, `design-led`) → `plan-to-design.md` → `/sage-design`
   - Architecture profiles → `plan-to-architect.md` → `/sage-architect`
   - Build-only profiles (`hotfix`, `spike`, `api-hotfix`) → `plan-to-build.md` → `/sage-engineer`
   - `library-backend` direct build → `plan-to-build.md` → `/sage-engineer` (add `architect` to `skipped_phases`)

Tell user the local path to `plan.md`, the profile, stack section used, and the next command.
