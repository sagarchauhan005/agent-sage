# Agent Sage

SDLC orchestration for AI coding agents (Cursor, Claude Code, Codex). Turn ad-hoc agent sessions into a repeatable pipeline: plan, design, architect, build, QA, devops, release.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![npm version](https://img.shields.io/npm/v/agent-sage.svg)](https://www.npmjs.com/package/agent-sage)

**Repo:** https://github.com/sagarchauhan005/agent-sage

## What it does

- Routes work through phase agents, each with a role file, slash command, and artifacts on disk
- Skips phases by workflow profile (hotfix, ui-deploy, library-backend, and others)
- Keeps one root contract in [`Agents.md`](Agents.md) that every agent inherits
- Persists run state under `runs/<run-id>/` with manifest, handoffs, and phase outputs
- Enforces gates before push, PR, or deploy

Plan, build, QA, and release always run. Design, architect, and devops are profile-dependent.

## Install

Requires **bash**, **python3**, and **Node.js 18+**.

```bash
npx agent-sage install --all    # once per machine
cd your-project
npx agent-sage init             # ./runs/, Agents.md, CLAUDE.md
```

Global install: `npm install -g agent-sage`, then `sage install --all` and `sage init`.

From a git clone:

```bash
git clone https://github.com/sagarchauhan005/agent-sage.git
cd agent-sage
./scripts/install.sh --all
./scripts/install.sh --project /path/to/your-app
```

### What gets installed

| Location                  | Contents                                              |
| ------------------------- | ----------------------------------------------------- |
| `~/.sage/`                | Agents.md, agents/, workflows/, templates, skills     |
| `~/.cursor/skills/sage-*` | Symlinks when Cursor is selected                      |
| `~/.claude/skills/sage-*` | Symlinks when Claude Code is selected                 |
| `~/.codex/skills/sage-*`  | Symlinks when Codex is selected                       |
| `./runs/` (per project)   | Feature run artifacts (`manifest.json`, handoffs, …)  |

## Usage

Start in any bootstrapped project:

```bash
/sage-orchestrator    # create or resume a run
/sage-plan            # jump straight to planning (Plan mode)
/sage-status          # snapshot of current run
```

Pick a **workflow profile** in the plan or manifest. See [`workflows/profiles.md`](workflows/profiles.md).

### Hotfix example

```
/sage-plan → /sage-engineer → /sage-qa → /sage-release
```

### Full web feature

```
/sage-plan → /sage-design → /sage-architect → /sage-engineer → /sage-qa → /sage-devops → /sage-release
```

## Agents

| Agent              | Slash command        | Primary role  |
| ------------------ | -------------------- | ------------- |
| Sage Orchestrator  | `/sage-orchestrator` | Orchestrate   |
| Sage Planner       | `/sage-plan`         | Plan          |
| Sage Designer      | `/sage-design`       | Design        |
| Sage Architect     | `/sage-architect`    | Architect     |
| Sage Engineer      | `/sage-engineer`     | Build         |
| Sage QA            | `/sage-qa`           | Verify        |
| Sage DevOps        | `/sage-devops`       | Package       |
| Sage Release       | `/sage-release`      | Ship          |
| Sage Init          | `/sage-init`         | Bootstrap     |
| Sage Status        | `/sage-status`       | Status        |
| Sage Handoff       | `/sage-handoff`      | Handoff       |

Full registry and skills mirror: [`Agents.md`](Agents.md).

## CLI reference

```bash
sage install [--all | --cursor | --claude | --codex]
sage init [DIR] [--no-agents-md]
sage status
sage uninstall
```

## Repository layout

```
Agents.md              # Root contract — read first
agents/                # Phase agent role files
workflows/             # Profiles (YAML + human guide)
runs/                  # Run templates (artifacts live per project)
.cursor/skills/        # Slash command skill definitions
bin/sage.js            # npm CLI entry
scripts/install.sh     # Global installer
examples/              # Worked hotfix run
```

Worked example: [`examples/hotfix-rate-limit-message/`](examples/hotfix-rate-limit-message/).

## Workflow profiles

| Profile              | Use when                          |
| -------------------- | --------------------------------- |
| `web-product`        | UI + API + deploy                 |
| `hotfix`             | Small fix, no design/architect    |
| `ui-deploy`          | UI with CDN/Docker, no architect  |
| `library-backend`    | Library/CLI, optional architect   |
| `spike`              | Time-boxed throwaway prototype    |

All eleven profiles: [`workflows/profiles.md`](workflows/profiles.md).

## Design principles

1. **Agents.md is the root** — global rules live there; agents reference sections by name
2. **Artifacts on disk, not chat** — downstream agents read `runs/<run-id>/`, not conversation history
3. **Orchestrator owns the pipeline** — Engineer implements; Release owns git push/PR
4. **Profile-driven skips** — never skip plan, build, QA, or release
5. **Handoffs are explicit** — templated markdown in `runs/<run-id>/handoffs/`

## Contributing

1. Fork and clone the repo
2. Run `./scripts/check-consistency.py` before opening a PR
3. Bump `install/VERSION` for releases (synced to `package.json` on pack)

## Versioning and publish

Semver tracked in `install/VERSION`. See [`CHANGELOG.md`](CHANGELOG.md).

```bash
# maintainer release
npm publish
```

## License

MIT — see [`LICENSE`](LICENSE). Fork freely. Customize `Agents.md` for your stack, gates, and team preferences.
