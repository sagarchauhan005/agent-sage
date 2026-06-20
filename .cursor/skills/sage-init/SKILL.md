---
name: sage-init
description: Bootstrap a new repo for Sage SDLC — creates ./runs/, optional ./Agents.md, .sage-project.json. Use as the first command in a new project before /sage-plan or /sage-orchestrator.
disable-model-invocation: true
---

# sage-init

You are **Sage Init**. Prepare the current workspace for Sage runs.

## Prerequisites

If `$HOME/.sage/install.json` is missing, stop. Tell the user to run global install first:

```bash
npx agent-sage install --all
# or: cd /path/to/agent-sage && ./scripts/install.sh --all
```

## Steps

1. Read [agents/sage-init.md](../../agents/sage-init.md).
2. Use workspace root as the project directory.
3. Create `./runs/` and `./runs/.gitkeep` if missing.
4. Write `./.sage-project.json` with:
   - `initialized_at` (ISO 8601)
   - `sage_home`: `$HOME/.sage`
   - `sage_version` from `$HOME/.sage/VERSION`
   - `local_agents_md`: whether `./Agents.md` exists in the project
   - `next_command`: `sage-orchestrator` (default)
5. **Agents.md** — unless the user asked to skip local copy (`--no-agents-md`):
   - If `./Agents.md` is missing, copy `$HOME/.sage/Agents.md` → `./Agents.md`
   - If `./Agents.md` exists, compare SHA256 to `$HOME/.sage/install.json` → `agents_md_sha256`
   - If different, refresh from `$HOME/.sage/Agents.md` (fixes stale copies after global updates)
   - If the user asked to keep local customizations, do not overwrite
   - Record `agents_md_sha256` in `./.sage-project.json`
5. **CLAUDE.md** — if `./CLAUDE.md` is missing and `$HOME/.sage/CLAUDE.md` exists, copy it to `./CLAUDE.md`
6. Do not create `./runs/<run-id>/` yet.

## Report

Tell the user:

- What was created or already present
- Whether `./Agents.md` is a fresh copy, pre-existing, or skipped
- Whether `./CLAUDE.md` was copied (if applicable)
- Next: `/sage-orchestrator` (recommended) or `/sage-plan`

## CLI alternative

```bash
npx agent-sage init
# or: /path/to/agent-sage/scripts/install.sh --project .
```
