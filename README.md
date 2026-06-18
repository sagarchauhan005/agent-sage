# Agent Sage

**Agent Sage** is an SDLC orchestration system for AI coding agents (Cursor, Claude Code, Codex). It turns ad-hoc agent sessions into a repeatable pipeline: plan → design → architect → build → QA → devops → release — with profile-aware phase skipping, structured handoffs, and a single root contract.

## What it does

- **Routes work through phase agents** — each phase has a role file, slash command, and expected artifacts on disk.
- **Skips phases by profile** — hotfixes skip design and architect; UI deploys skip architect; library work skips design and devops. Plan, build, QA, and release always run.
- **Keeps one source of truth** — [`Agents.md`](Agents.md) holds global rules (stack preferences, coding practices, gates). Phase agents inherit from it; they do not duplicate best practices.
- **Persists run state locally** — every feature run lives under `runs/<run-id>/` with `manifest.json`, phase artifacts, and handoff markdown between agents.
- **Enforces gates** — push, PR, and deploy require explicit user approval before Release or DevOps proceed.

## Quick start

1. Copy or clone this repo into your project (or use it as the project root).
2. Read [`Agents.md`](Agents.md) — the root contract for all agents.
3. Start a run with `/sage-orchestrator` or go straight to `/sage-plan`.
4. Pick a **workflow profile** (see [`workflows/profiles.md`](workflows/profiles.md)) — e.g. `web-product`, `hotfix`, `ui-deploy`.
5. Follow the next `/sage-*` command the orchestrator or phase agent tells you.

### Example — hotfix

```bash
/sage-plan      → writes runs/<id>/plan.md (Plan mode)
/sage-engineer  → implements fix, writes build.md
/sage-qa        → tests, writes test-report.md
/sage-release   → commit, branch, PR (with your approval)
```

### Example — full web feature

```bash
/sage-plan → /sage-design → /sage-architect → /sage-engineer → /sage-qa → /sage-devops → /sage-release
```

## Slash commands

| Command | Phase |
|---------|-------|
| `/sage-orchestrator` | Create or resume a run; route the pipeline |
| `/sage-status` | Read-only snapshot of run state |
| `/sage-plan` | Plan mode → local `plan.md` |
| `/sage-design` | UI/UX spec |
| `/sage-architect` | Schemas and system design |
| `/sage-engineer` | Full-stack implementation (alias `/sage-build`) |
| `/sage-qa` | Lint and tests |
| `/sage-devops` | Docker, CDN, nginx packaging |
| `/sage-release` | Commit, push, PR |
| `/sage-handoff` | Write or validate a phase handoff |

Skills live in [`.cursor/skills/sage-*/`](.cursor/skills/). Cursor loads them when you invoke the matching slash command.

## Repository layout

```
Agents.md                 # Root contract — read first
agents/                   # Phase agent role files (sage-planner, sage-engineer, …)
workflows/
  feature-sdlc.yaml       # Machine-readable profile definitions
  profiles.md             # Human guide — when to use each profile
runs/                     # Per-feature run artifacts (manifest, plan, handoffs)
.cursor/
  rules/sage-system.mdc   # Always-on Cursor rule
  skills/sage-*/          # Slash command definitions
```

## Workflow profiles

Eleven profiles control which phases run. Common ones:

| Profile | Use when |
|---------|----------|
| `web-product` | UI + API + deploy |
| `hotfix` | Small fix, no design/architect |
| `ui-deploy` | New UI with CDN/Docker, no architecture doc |
| `library-backend` | Library/CLI, optional architect |
| `spike` | Time-boxed throwaway prototype |

Full list and routing rules: [`workflows/profiles.md`](workflows/profiles.md).

## Design principles

1. **Agents.md is the root** — global rules live there; agents reference sections by name.
2. **Artifacts on disk, not chat** — downstream agents read `runs/<run-id>/` files, not conversation history.
3. **Orchestrator owns the pipeline** — Sage Engineer implements; Release owns git push/PR.
4. **Profile-driven skips** — never skip plan, build, QA, or release.
5. **Handoffs are explicit** — templated markdown in `runs/<run-id>/handoffs/`.

## License

Use and adapt freely for your own agent workflows. Customize `Agents.md` for your stack, gates, and team preferences.
