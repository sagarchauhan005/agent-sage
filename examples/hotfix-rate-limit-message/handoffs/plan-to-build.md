# Sage Handoff Template

## Handoff: Sage Planner → Sage Engineer

- Run ID: 2026-06-18-rate-limit-message
- Phase completed: plan
- Next phase: build
- Next slash command: `/sage-engineer`

### Goal

Stop the 429 rate-limit response from leaking the internal `userId`.

### Completed

- [x] plan.md written with three-layer onion (condensed, hotfix profile)
- [x] `workflow_profile: hotfix` set; `design`, `architect`, `devops` added to `skipped_phases`

### Assumptions

- Leak is confined to `src/middleware/rateLimit.js` line 42, confirmed by grep

### Out of scope

- Rate limit thresholds, storage backend, retry-after logic

### Open questions

- None

### Artifacts

| File | Description |
|------|-------------|
| `runs/2026-06-18-rate-limit-message/plan.md` | Full plan |

### Files changed

- None yet — plan phase only

### Gates

| Gate | Status |
|------|--------|
| User approval required | n/a at this phase |

### Blockers

- None

### Instructions for next agent

Implement the fix per Layer 3 (single response-builder change), add T-1 through T-3, run the suite, write `build.md`.
