# Workflow profiles

Parent: [Agents.md](../Agents.md)
Workflow: [feature-sdlc.yaml](./feature-sdlc.yaml)

Set `workflow_profile` in `runs/<run-id>/manifest.json` when creating a run. The **orchestrator** owns the pipeline end to end. **Sage Engineer** (`/sage-engineer`) implements the feature (full-stack scope per plan and profile).

## Terminology

| Term             | Meaning                                        |
| ---------------- | ---------------------------------------------- |
| **Orchestrator** | Routes the SDLC pipeline (`/sage-orchestrator`) |
| **Engineer**     | Single build agent (`/sage-engineer`)          |

## All profiles

| Profile                 | Pipeline                                              | Skipped phases          | After QA | When to use |
| ----------------------- | ----------------------------------------------------- | ----------------------- | -------- | ----------- |
| `web-product`           | plan → design → architect → build → qa → devops → release | —                   | devops   | UI + API + deploy |
| `library-backend`       | plan → architect? → build → qa → release              | design, devops          | release  | Library, CLI, algorithm |
| `backend-api`           | plan → architect → build → qa → devops → release      | design                  | devops   | API/service with deploy |
| `ui-feature`            | plan → design → architect → build → qa → release    | devops                  | release  | Frontend-heavy feature |
| `hotfix`                | plan → build → qa → release                           | design, architect, devops | release | One-line fix, typo, config tweak, dependency patch |
| `spike`                 | plan → build → qa → release                           | design, architect, devops | release | Time-boxed prototype; plan marks throwaway scope |
| `backend-module`        | plan → architect → build → qa → release               | design, devops          | release  | Shared lib/package with arch doc, no deploy |
| `ui-deploy`             | plan → design → build → qa → devops → release         | architect               | devops   | UI needing CDN/Docker; no formal architecture doc |
| `full-stack-no-deploy`  | plan → design → architect → build → qa → release      | devops                  | release  | Full feature on branch/PR; hosting unchanged |
| `api-hotfix`            | plan → build → qa → devops → release                  | design, architect       | devops   | Production API fix with deploy |
| `design-led`            | plan → design → architect → build → qa → release      | devops                  | release  | UI-heavy + formal API contract in architecture |

Build command for all profiles: `/sage-engineer` (alias `/sage-build`). QA requires: `build` (`build.md` on disk).

## Similar profiles — how to choose

| Pair | Difference |
|------|------------|
| `ui-feature` vs `design-led` vs `full-stack-no-deploy` | Same pipeline (no devops). Use `design-led` when a formal API contract in `architecture.md` matters; `ui-feature` for UI-heavy work; `full-stack-no-deploy` when naming intent as “PR only, hosting unchanged”. |
| `hotfix` vs `spike` | Same path. Use `spike` when the plan marks throwaway/prototype scope and success criteria; `hotfix` for a small production fix. |
| `library-backend` vs `backend-module` | Both skip design and devops. `library-backend` allows skipping architect when the plan is exhaustive (`architect?` in path). `backend-module` always includes architect for a shared lib/package with an architecture doc. |

## Profile selection guide

```
Need UI spec?              → include design (not hotfix/spike/api-hotfix)
Need architecture doc?     → include architect (not hotfix/spike/ui-deploy/api-hotfix)
Need Docker/CDN deploy?    → qa_next: devops (web-product, backend-api, ui-deploy, api-hotfix)
Tiny / known change?       → hotfix or api-hotfix (with deploy if api-hotfix)
Prototype / throwaway?     → spike
Full web app + deploy?     → web-product
```

## Example — hotfix

```json
{
  "workflow_profile": "hotfix",
  "route_after_plan": "build",
  "skipped_phases": ["design", "architect", "devops"],
  "qa_requires": ["build"],
  "qa_next": "release",
  "qa_handoff": "qa-to-release.md"
}
```

Commands: `/sage-plan` → `/sage-engineer` → `/sage-qa` → `/sage-release`

## Example — ui-deploy

```json
{
  "workflow_profile": "ui-deploy",
  "route_after_plan": "design",
  "skipped_phases": ["architect"],
  "qa_requires": ["build"],
  "qa_next": "devops",
  "qa_handoff": "qa-to-devops.md"
}
```

After design, designer writes `design-to-build.md` (architect skipped). Commands: `/sage-plan` → `/sage-design` → `/sage-engineer` → `/sage-qa` → `/sage-devops` → `/sage-release`

## Manifest fields (profile-driven)

| Field              | Source                                                          |
| ------------------ | --------------------------------------------------------------- |
| `workflow_profile` | User or planner at run creation                                 |
| `skipped_phases`   | Copied from profile; may add `architect` if routing plan → build |
| `qa_requires`      | Always `[build]` for all profiles                               |
| `qa_next`          | `devops` or `release` from profile                              |
| `qa_handoff`       | `qa-to-devops.md` or `qa-to-release.md`                         |

## Rules

- Orchestrator owns the pipeline. Engineer owns implementation only.
- Never skip `plan`, `build`, `qa`, or `release`.
- Only skip phases listed in `skipped_phases` for the active profile.
- QA runs only after `build.md` exists.
- If `architect` is in `skipped_phases`, design hands off to build (`design-to-build.md`), not architect.
- If `qa_next` is `release`, write `handoffs/qa-to-release.md`, not `qa-to-devops.md`.
