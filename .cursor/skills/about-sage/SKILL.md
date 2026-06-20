---
name: about-sage
description: Brief overview of the Sage SDLC agent system and each agent's role. Use when the user asks what Sage is, how it works, or about Sage agents.
disable-model-invocation: true
---

# About Sage

When invoked, give a short overview of Sage, then the agent table below. Keep it brief. Do not dump Agents.md or phase workflows unless asked.

## What Sage is

Sage is an SDLC agent orchestration system. Specialized agents run phases of software delivery (plan, design, architect, build, qa, devops, release) in order. An orchestrator routes work by workflow profile, writes handoffs between phases, and stores run artifacts under `runs/<run-id>/`. Each agent reads [Agents.md](../../Agents.md) first, then its role file in `agents/`.

## Agents

| Agent              | What it does                                              | Primary role        |
|--------------------|-----------------------------------------------------------|---------------------|
| Sage Orchestrator  | Runs the pipeline, picks profile, enforces gates          | Orchestrate         |
| Sage Planner       | Clarifies requirements; `plan.md` in **full** or **steps** format | Plan                |
| Sage Designer      | UI/UX specs, components, asset structure                  | Design              |
| Sage Architect     | Schemas, boundaries, deployment impact, test strategy     | Architect           |
| Sage Engineer      | Full-stack implementation, tests, wiring                  | Build               |
| Sage QA            | Tests, lint, verification against plan                    | Verify              |
| Sage DevOps        | Docker, CDN sync, nginx, deploy prep                      | Package             |
| Sage Release       | Commits, branches, PRs                                    | Ship                |
| Sage Status        | Reports run phase, profile, gates, next command           | Status              |
| Sage Handoff       | Writes or validates phase handoff documents               | Handoff             |
| Sage Init          | Bootstraps ./runs/ and project Sage config                | Init                |

## Slash commands

Each phase agent maps to a `/sage-*` command. Use **`/sage-plan steps`** when the problem is unfamiliar (plain breakdown). Use **`/sage-plan`** or **`/sage-plan full`** for the handoff-ready spec. Start a run with `/sage-orchestrator`.

Skills live in `.cursor/skills/` and must match the Skills mirror table in [Agents.md](../../Agents.md). One skill folder per registry row; no orphan skills.

For profile paths and global rules, point to [Agents.md](../../Agents.md) and [workflows/profiles.md](../../workflows/profiles.md).
