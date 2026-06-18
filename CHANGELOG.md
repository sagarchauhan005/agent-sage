# Changelog

Versions track `install/VERSION`, bumped by `scripts/install.sh`. Follows semver: patch for fixes/docs, minor for new features, major for breaking changes to the manifest schema or run layout.

## 1.1.0

- `runs/.current` pointer to resolve the active run across phases (Agents.md, orchestrator, planner, status, all phase agents).
- `runs/_manifest-template.schema.json` — formal JSON Schema for `manifest.json`.
- Concrete decision rule for `library-backend`'s `architect_optional` (agents/sage-planner.md).
- `scripts/check-consistency.py` — verifies profile tables in Agents.md, workflows/profiles.md, sage-orchestrator.md, and sage-planner.md agree with `workflows/feature-sdlc.yaml`, and that the Skills mirror table matches `.cursor/skills/`.
- `scripts/tests/` — pytest coverage for `generate-global-skills.py`.
- `.github/workflows/ci.yml` — runs the consistency check, pytest suite, and shellcheck on `install.sh`.
- CDN env var convention (`CDN_PROVIDER`, `CDN_BUCKET`, `CDN_BASE_URL`) in Agents.md Coding Best Practises.
- Root `CLAUDE.md` so Claude Code auto-loads the root contract.
- `LICENSE` (MIT).
- `runs/` template files now gitignored in this tool repo; only `_*` templates are tracked.

## 1.0.1

- `/sage-init` agent and skill — bootstraps `./runs/` and `.sage-project.json` for a new project.
- `scripts/install.sh --project` gained `--no-agents-md` / `--copy-agents-md`.

## 1.0.0

- Initial Sage SDLC agent system: orchestrator, seven phase agents, eleven workflow profiles, global install script.
