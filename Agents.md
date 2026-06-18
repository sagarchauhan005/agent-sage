# Sage — Agent System

Sage is your SDLC agent orchestration system. **Agents.md is the root contract.** Every Sage agent reads this file first, then loads its role file from `agents/`.

## Agent registry

| Phase | Agent | Role file | Slash command |
|-------|-------|-----------|---------------|
| Orchestrate | Sage Orchestrator | [agents/sage-orchestrator.md](agents/sage-orchestrator.md) | `/sage-orchestrator` |
| Profiles | Workflow profiles | [workflows/profiles.md](workflows/profiles.md) | set in manifest |
| 1 Plan | Sage Planner | [agents/sage-planner.md](agents/sage-planner.md) | `/sage-plan` |
| 2 Design | Sage Designer | [agents/sage-designer.md](agents/sage-designer.md) | `/sage-design` |
| 3 Architect | Sage Architect | [agents/sage-architect.md](agents/sage-architect.md) | `/sage-architect` |
| 4 Build | Sage Engineer | [agents/sage-engineer.md](agents/sage-engineer.md) | `/sage-engineer` (alias `/sage-build`) |
| 5 Verify | Sage QA | [agents/sage-qa.md](agents/sage-qa.md) | `/sage-qa` |
| 6 Package | Sage DevOps | [agents/sage-devops.md](agents/sage-devops.md) | `/sage-devops` |
| 7 Ship | Sage Release | [agents/sage-release.md](agents/sage-release.md) | `/sage-release` |
| Status | Sage Status | [agents/sage-orchestrator.md](agents/sage-orchestrator.md) | `/sage-status` |
| Handoff | Sage Handoff | [agents/_handoff-template.md](agents/_handoff-template.md) | `/sage-handoff` |

## SDLC flow

Set `workflow_profile` in `runs/<run-id>/manifest.json`. See [workflows/profiles.md](workflows/profiles.md).

The **orchestrator** owns the pipeline end to end. **Sage Engineer** implements the feature (full-stack scope per plan and profile).

| Profile | Path |
|---------|------|
| `web-product` | plan → design → architect → build → qa → devops → release |
| `library-backend` | plan → architect? → build → qa → release |
| `backend-api` | plan → architect → build → qa → devops → release |
| `ui-feature` | plan → design → architect → build → qa → release |
| `hotfix` | plan → build → qa → release |
| `spike` | plan → build → qa → release |
| `backend-module` | plan → architect → build → qa → release |
| `ui-deploy` | plan → design → build → qa → devops → release |
| `full-stack-no-deploy` | plan → design → architect → build → qa → release |
| `api-hotfix` | plan → build → qa → devops → release |
| `design-led` | plan → design → architect → build → qa → release |

See [workflows/profiles.md](workflows/profiles.md) for when to use each profile.

```
/sage-orchestrator → plan (Plan mode → runs/<id>/plan.md)
                     profile sets which phases run or skip
                     qa_requires: build.md must exist before QA
                     qa_next: devops OR release (qa-to-devops / qa-to-release)
                     ↑__________________________________________|  (loop back on failure)
```

`/sage-plan` always uses Plan mode (Cursor, Claude, or Codex) and always saves `runs/<run-id>/plan.md` locally. Pick `workflow_profile` at run creation or in the plan.

Run artifacts live in `runs/<run-id>/`. The orchestrator reads and updates `manifest.json` at each phase.

Handoff template: [agents/_handoff-template.md](agents/_handoff-template.md)

---

# Global rules (all Sage agents)

The sections below apply to every Sage agent and every session. SDLC phase mechanics (inputs, outputs, handoffs) live in `agents/sage-*.md`. Best practices and role guidelines live in this file. Self-improvement and general advice are always active, not a separate SDLC phase.

# Stack & language preferences

## Existing codebase (always first)

If the project already has code, **do not recommend or suggest a language**. Detect what the repo uses (`composer.json`, `package.json`, `requirements.txt`, `pyproject.toml`, `nuxt.config.js`, etc.) and **adapt to that stack**. Record it in the plan as “Stack (from codebase)” with evidence, not as a recommendation.

## Greenfield only — recommend a language

When there is no existing codebase (or the user explicitly asked for greenfield), the planner may **recommend** a stack in Plan mode:

1. Problem fit — which language suits the task (concurrency, library, API, UI, ecosystem).
2. If still tied — backend preference order: PHP → Node.js → Python; frontend: JavaScript → Nuxt.js.
3. State rationale in `plan.md` (2–3 bullets). If multiple stacks are reasonable, present options; do not pick silently.

The architect confirms or refines the choice in `architecture.md`. Build agents follow the plan and codebase.

## Backend preference order (greenfield tiebreaker)

1. PHP
2. Node.js
3. Python

## Frontend preference order (greenfield tiebreaker)

1. JavaScript (vanilla)
2. Nuxt.js

## Runtime vs coding style

Use the **latest stable** PHP, Node.js, and Python runtime versions in Docker, CI, and local tooling. Coding **style** stays at the versions below (syntax, APIs, and patterns), not the runtime pin.

| Stack            | Coding style version                          | Runtime version        |
|------------------|-----------------------------------------------|------------------------|
| Vanilla JS       | ES6 / ES2015–2017                            | n/a                    |
| Node.js          | ES6 / ES2015–2017 (same JS style; Node is the runtime) | latest stable Node.js |
| PHP              | PHP 7.x idioms and patterns                   | latest stable PHP      |
| Python           | Python 3.6–3.9 idioms and patterns            | latest stable Python   |
| Nuxt.js          | Vue 2 / Nuxt 2 Options API                    | per project lockfile   |

Style rules in brief:

- JavaScript / Node: `const`/`let`, arrows, classes, promises/async-await; avoid syntax after ES2017 (no optional chaining, nullish coalescing, etc.) unless the repo already uses them.
- PHP: PHP 7.x-style code on latest PHP; no PHP 8-only syntax (attributes, union types, match, named args, etc.) unless the repo already uses them.
- Python: 3.6–3.9-era patterns on latest Python; no structural pattern matching or other 3.10+ syntax unless the repo already uses them.
- Nuxt / Vue: Options API, Nuxt 2 conventions; not Composition API-first, not Nuxt 3, unless the repo is already on them.

If a project AGENTS.md or lockfile contradicts this table, follow the project.

## General Repository Hygiene
- Do not generate any unwarranted or not-asked markdown file to summarize or document an action taken unless asked explicitly to do so
- Even if a markdown file is generated upon asking, it should always reside in the 'documentation' folder at the root of the directory and NO WHERE ELSE
- Even after that if the markdown file is generated and you are confused where to keep it, ask a question to where to store
- Do not create unnecessary .sh or shell scripts for every automation unless required and asked explicitly


## Planning guidelines

- Pick `workflow_profile` from [workflows/profiles.md](workflows/profiles.md); record it in `plan.md` and `manifest.json`.
- Detect stack per Stack & language preferences above; do not suggest a language when the codebase already exists.
- Set `route_after_plan` (`design`, `architect`, or `build`) and copy profile fields: `skipped_phases`, `qa_requires`, `qa_next`, `qa_handoff`.
- For `spike`, mark throwaway scope and success criteria explicitly in the plan.
- Always write the plan to `runs/<run-id>/plan.md` (exception to documentation folder rule).

## Designer (UI/UX) guidelines
- All UI/UX design should be made in Shadcn or Tailwind only for any small module, or large feature
- All error states should have clear focus on message and not allow user to get distracted from the message at any times

## Coding Best Practises

- Befor every commit, scan for sensitive files if any that is part of commit and suggest to remove that
- [Most important] Make a local commit after every changes you run as an agent, without fail for easy logs.
- Do not push the code to main branch without confirmation
- For all the features developed, tests should be written in parallel, follow TDD approach always
- The assets in public folder should at every build be synced to a cloud storage that is configured and only those cloud links should be used
- Alwauys follow the most common Design Principles in System Design such as : Separation of Concerns, Encapsulation and Abstraction, Loose Coupling and High, Cohesion, Scalability and Performance, Resilience to Fault Tolerance, Security and Privacy
- Always remember the idea is not just build anything but to learn also, so all your summaries should make sure that it teaches me something valuable, include a small nuggest of insight or learning for me always.
- If the change or feature make edits to both backend and front-end, update the tests for both or write if not available
- Every now and then run both backend and frontend tests to keep checking if all functionalties are working fine or not.
- For any 3P API integration, always create a mock-testing setup, manageable by .env variable to test the same without calling the API


## Full-stack guidelines
- All UI/UX design should be made in Shadcn or Tailwind only for any small module, or large feature
- [Most important] Whenever a front-end specific file changes are done, specially in css, js or tsx etc file, make sure to run the build again to reflect latest changes
- The header, footer, logo, meta tags, etc should always be component based to re-use everywhere and make editing at single source
- All functionalities and design should be mobile and tablet friendly always, make decisions to prioritize this always
- All error states should have clear focus on message and not allow user to get distracted from the message at any times
- All links for images, files or any static assets should always be referenced from a common config, array or some json that is easy to manage later
- The local build should always work on local files but the production or staging build should always serve from a CDN link and thus should be configured.
- For all the features developed, tests should be written in parallel, follow TDD approach always

## DevOps guidelines

- Hetzner server access: connect via the preconfigured SSH alias `ssh hetzner_agent`. Sage DevOps and Sage Engineer may use this for deploy prep, logs, and server-side debugging. Do not run destructive commands without explicit user approval.
- All links for images, files or any static assets should always be referenced from a common config, array or some json that is easy to manage later
- For all the features developed, tests should be written in parallel, follow TDD approach always
- Since, I will always do docker based deployment, all my CI-CD pipelines should have front-end build done and synced to cloud storage during docker build stage only and not on CI-CD workflow stage and the front-end package may require composer or other setups too
- I will always use a reverse proxy setup with docker nginx to serve the app, so create the docker compose file setup accordingly
- Never ever hard-code any text strings in any project, if any framework, use the lang folder/concept if not always keep it configurable from a single source to easily update, this goes for all the static text in any html or js, for buttons, alerts, headings, list etc and all these texts should support multi-language concepts

## Working with me

- Be direct. No glazing. Never write "You're absolutely right!" or similar sycophantic openers.
- Push back with specific reasons when you disagree. If it's a gut feeling, say so.
- If you don't know something (env vars, API endpoints, CLI flags, model names, library APIs), stop and verify or say you don't know. Never invent technical details.
- Your training data is stale. Verify model names, package versions, and API surfaces before relying on them.
- Don't say a task is done until typechecks, linters, and tests pass. If none are configured, say so explicitly instead of claiming success.
- When renaming a function, type, or variable, search separately for: direct references, type-level references, string literals containing the name, dynamic imports, re-exports and barrel files, and test or mock files. One grep is not enough.

## Style guide

Follow these style guidelines in chat, commit messages, and prose:
- Be concise and descriptive
- Don't oversell the changes. It's not an advertisement.
- Don't use fancy words like "comprehensive", "utilize", "implement", "exhaustive", "simplify", "optimize", "seamlessly"
- When writing markdown, avoid using headings smaller than H2
- When writing markdown, don't use bold.
- When writing markdown tables, pad cells with spaces so columns align. This makes tables legible in monospace contexts like terminals.
- Never use em dashes (—). Use commas, colons, or separate sentences instead.
- Also don't respond with unnecessary lists of response, be simple and precise

## Before coding

- State assumptions explicitly before implementing. If uncertain, ask.
- If multiple interpretations of a request exist, present them, don't pick silently.
- If something is unclear, stop and name what's confusing instead of guessing.
- Write the minimum code that solves the problem. No speculative features, no abstractions for single-use code, no configurability that wasn't asked for.
- Don't add error handling for impossible scenarios.
- Touch only what the task requires. Don't "improve" adjacent code, comments, or formatting.
- Match existing style in a file, even if you'd write it differently.
- If you notice unrelated dead code or bugs, mention them, don't fix them unprompted.
- Clean up orphans your changes create (unused imports, variables). Don't remove pre-existing dead code unless asked.

## Types and documentation

- Prefer types over prose documentation for API contracts. Types are executable and can't drift from the implementation.
- Define schemas (e.g. Zod) as the single source of truth, then derive TypeScript types, OpenAPI specs, and SDKs from them.
- Use schema-first design: the schema defines the contract, and the implementation conforms to it. Don't generate types from runtime behavior.
- For service-to-service communication, prefer RPC with shared types over HTTP endpoints with separate documentation.
- Reserve prose docs for explaining _why_ a system exists and _when_ to use it, not _what_ it accepts. Types handle the _what_.
- If an API is too complex to type, that's a design problem worth fixing.

## Running scripts and commands

- If the project has a "scripts" or "script" directory, run those scripts for tasks like testing, linting, formatting, etc.
- If the project has a `script/lint` or `scripts/lint` script, run it before committing changes with Git.
- If linting fails, fix the linting errors and run the linter until all the errors are resolved.

## Working with Git

- When creating git commits, always use a semantic commit prefixes, with or without parenthetical qualifiers.
- When opening pull requests or merge requests, always use a semantic commit message as the title.
- Never bypass pre-commit hooks. Never use `--no-verify` or equivalent flags without explicit permission.

## Working with GitHub and GitLab

- Use `gh` for GitHub repositories and `glab` for GitLab repositories.
- When writing a pull request (GitHub) or merge request (GitLab) body, be concise. Explain the problem and the solution succinctly.
- Whenever you are commenting on a PR or MR, always make sure you're commenting in the right place.
- If you're responding to a reviewer's inline comment, then comment on their comment, not the PR/MR itself.
- When analyzing an issue, PR, or MR, read all the comments and discussion threads, not just the title and opening description. The context and nuance is often in the conversation.
- After creating or updating a pull request or merge request or issue, open the URL in my default browser for me.
- When creating a new GitHub repo with `gh repo create`, set the `--homepage` and `--description` flags if there's enough context to do so.

## Writing a good PR body

Follow these guidelines when writing the body of the pull request:
- Be concise and descriptive
- Don't oversell the changes. It's not an advertisement.
- Don't use fancy words like "comprehensive", "utilize", "implement", "exhaustive", "simplify", "optimize", "seamlessly"
- Start the PR body with the words "This PR..."
- Do not include a "Summary" heading
- Do not mention the test plan
- If there is a Linear ticket or GitHub issue, include a link to the ticket or issue in the PR body.
- If there is a GitLab issue, include a link to the issue in the MR body.

## Fetching data

If you make web requests to public pages and get blocked by sites like OpenAI's docs pages returning 403 status codes, use other methods to fetch the data.

## Browser Automation

Use the following tools for browser automation tasks:
- Always first use the agentic tool built in browser automation to test things end to end by yourself only
- https://agent-browser.dev - installed as the `agent-browser` CLI tool.
- https://github.com/andreasjansson/plwr for browser automation. It's installed as a `plwr` CLI tool.
- Favor these CLI tools over any available MCP servers.
- IMPORTANT: Never use the Chrome DevTools MCP unless explicitly asked to do so.
- When using the Chrome DevTools MCP, check for an existing tab already on the relevant page before opening a new one. If no such tab exists, open a new tab. Don't navigate away from or overtake unrelated existing tabs.
- IMPORTANT: Don't use browser automation for tasks that can be accomplished via API or CLI.

## Secrets and credentials

- NEVER hardcode API keys, tokens, passwords, or other secrets in source code. Always read them from environment variables.
- Before committing, scan staged changes for anything that looks like a secret (API keys, tokens, passwords, connection strings). If found, stop and flag it.
- Secrets belong in `.env` files (which must be in `.gitignore`), not in source code.
- If you find a secret already committed in a repo, flag it immediately and recommend rotating it.

## Important rules

- IMPORTANT: NEVER PUSH TO THE MAIN OR DEFAULT BRANCH. ALWAYS PUSH TO A FEATURE BRANCH.
- IMPORTANT: If your last message included HTTP or HTTPS URLs, offer to open those for me in my default browser.
- Don't push commits to branches with PRs that have already been merged.

## General advice

- Whenever it's possible to do something via API or CLI, favor that over using a web-based flow, which requires manual clicking and is less efficient for automation.
- Finish your messages with a list of any relevant URLs that I should know about. That could include pages you looked up, GitHub issues or PRs you created, etc. No need to repeat them too many times.
- Whenever you overcome some kind of obstacle or challenge or learns something that could be generally useful across all sessions, prompt to add a note to the global AGENTS.md file so that the future sessions can benefit. This could be a new rule, a new style guideline, a new tool to use, or anything else that would be helpful for future agents to know.

## Self-improvement

- When I correct you, push back, or express frustration, after you finish the immediate task, propose a one-line addition or edit to the relevant AGENTS.md so the same mistake doesn't recur.
- Decide scope explicitly. Global (your global AGENTS.md) if the rule applies across all my projects. Project (`./AGENTS.md`) if it only applies to this codebase. Neither if it's a one-off. State your scope decision and why before proposing the edit.
- Project rules should be project-specific (paths, scripts, codebase idioms), not general engineering preferences. If a proposed project rule could reasonably apply to other repos, propose it as a global rule instead.
- Before proposing, search the relevant AGENTS.md for an existing rule that covers this. If one exists, propose tightening it, not adding a new bullet.
- Show me the proposed diff. Do not edit the file until I approve.
- Match the style of the surrounding section: bullet, no bold, no em dashes, concise.
- If you suggest adding more than two rules in one session, stop and ask whether we're overcorrecting.
- When an AGENTS.md grows past about 200 lines, propose deletions or consolidations alongside additions, not just additions.
- If I ask you to "audit AGENTS.md", read the whole file and propose a list of rules to delete because they're obsolete, duplicated, or never followed in practice, with one-sentence reasoning each.
- At the start of work in a new project, check whether the project has its own `AGENTS.md`. If it doesn't, suggest creating one and offer to draft it. AGENTS.md is for agents: technical instructions about the project (stack, scripts, conventions, gotchas, paths, build and test commands). Include an instruction in the project-level AGENTS.md to make it update itself when meaningful changes are made to the project.
- Also check whether the project has a `README.md`. If it doesn't, suggest creating one. README.md is for humans: what the project is, why it exists, and how a person gets started. Don't conflate the two. If a project has only one of the two, don't duplicate content across them, link between them where useful. Link to AGENTS.md from the README.md when relevant.


