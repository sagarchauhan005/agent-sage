# Workflow profiles

Parent: [Agents.md](../Agents.md)
Workflow: [feature-sdlc.yaml](./feature-sdlc.yaml)

Set `workflow_profile` in `runs/<run-id>/manifest.json` when creating a run. The **orchestrator** owns the pipeline end to end. **Sage Full-stack** (`/sage-fullstack`) is the agent that writes both backend and frontend code.

## Terminology


| Term             | Meaning                                                         |
| ---------------- | --------------------------------------------------------------- |
| **Orchestrator** | Routes the SDLC pipeline (`/sage-orchestrator`)                 |
| **Full-stack**   | Build agent for backend + frontend together (`/sage-fullstack`) |
| **web-product**  | Profile for a full web feature pipeline (uses full-stack build) |


## Profiles


| Profile           | Use when                | Build agent            | QA requires     | After QA |
| ----------------- | ----------------------- | ---------------------- | --------------- | -------- |
| `web-product`     | UI + API + deploy       | `/sage-fullstack`      | build-fullstack | devops   |
| `library-backend` | Library, CLI, algorithm | `/sage-build-backend`  | build-backend   | release  |
| `backend-api`     | API/service with deploy | `/sage-build-backend`  | build-backend   | devops   |
| `ui-feature`      | Frontend-heavy          | `/sage-build-frontend` | build-frontend  | release  |


## Pipelines


| Profile           | Path                                                              |
| ----------------- | ----------------------------------------------------------------- |
| `web-product`     | plan → design → architect → **fullstack** → qa → devops → release |
| `library-backend` | plan → architect? → build-backend → qa → release                  |
| `backend-api`     | plan → architect → build-backend → qa → devops → release          |
| `ui-feature`      | plan → design → architect → build-frontend → qa → release         |


## Example — web product feature

```json
{
  "workflow_profile": "web-product",
  "route_after_plan": "design",
  "skipped_phases": ["build-backend", "build-frontend"],
  "qa_requires": ["build-fullstack"],
  "qa_next": "devops",
  "qa_handoff": "qa-to-devops.md"
}
```

Commands: `/sage-plan` → `/sage-design` → `/sage-architect` → `/sage-fullstack` → `/sage-qa` → `/sage-devops` → `/sage-release`

## Manifest fields (profile-driven)


| Field              | Source                                                                   |
| ------------------ | ------------------------------------------------------------------------ |
| `workflow_profile` | User or planner at run creation                                          |
| `skipped_phases`   | Copied from profile; may add `architect` if routing plan → build-backend |
| `qa_requires`      | Copied from profile                                                      |
| `qa_next`          | `devops` or `release` from profile                                       |
| `qa_handoff`       | `qa-to-devops.md` or `qa-to-release.md`                                  |


## Rules

- Orchestrator owns the pipeline. Full-stack owns dual-layer implementation only.
- Never skip `plan`, `qa`, or `release`.
- Only skip phases listed in `skipped_phases` for the active profile.
- QA runs only after all phases in `qa_requires` have artifacts on disk.
- If `qa_next` is `release`, write `handoffs/qa-to-release.md`, not `qa-to-devops.md`.

