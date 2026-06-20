#!/usr/bin/env python3
"""Generate global Sage skills with ~/.sage paths (not repo-relative links)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

PATHS_HEADER = """\
## Sage paths (global install)

- **SAGE_HOME:** `$HOME/.sage`
- **Workspace:** current project root (where you run the command)
- **Root contract:** read `./Agents.md` at workspace root if present, else `$HOME/.sage/Agents.md`
- **Role files:** `$HOME/.sage/agents/<name>.md`
- **Workflows:** `$HOME/.sage/workflows/`
- **Run templates:** `$HOME/.sage/runs/_plan-template.md`, `_plan-steps-template.md`, `_manifest-template.json`
- **Run artifacts:** always under `./runs/<run-id>/` in the workspace (create the folder if missing)

"""

LINK_REPLACEMENTS: list[tuple[str, str]] = [
    (
        r"\[Agents\.md\]\(\../../Agents\.md\)",
        "`$HOME/.sage/Agents.md` (prefer `./Agents.md` at workspace root if present)",
    ),
    (
        r"\[workflows/profiles\.md\]\(\../../workflows/profiles\.md\)",
        "`$HOME/.sage/workflows/profiles.md`",
    ),
    (
        r"\[workflows/feature-sdlc\.yaml\]\(\../../workflows/feature-sdlc\.yaml\)",
        "`$HOME/.sage/workflows/feature-sdlc.yaml`",
    ),
    (
        r"\[runs/_plan-template\.md\]\(\../../runs/_plan-template\.md\)",
        "`$HOME/.sage/runs/_plan-template.md`",
    ),
    (
        r"\[runs/_plan-steps-template\.md\]\(\../../runs/_plan-steps-template\.md\)",
        "`$HOME/.sage/runs/_plan-steps-template.md`",
    ),
    (
        r"\[runs/_manifest-template\.json\]\(\../../runs/_manifest-template\.json\)",
        "`$HOME/.sage/runs/_manifest-template.json`",
    ),
    (
        r"\[agents/_handoff-template\.md\]\(\../../agents/_handoff-template\.md\)",
        "`$HOME/.sage/agents/_handoff-template.md`",
    ),
]

AGENT_LINK = re.compile(
    r"\[agents/([a-z0-9_.-]+\.md)\]\(\../../agents/([a-z0-9_.-]+\.md)\)"
)


def transform_body(body: str) -> str:
    for pattern, replacement in LINK_REPLACEMENTS:
        body = re.sub(pattern, replacement, body)

    body = AGENT_LINK.sub(
        r"`$HOME/.sage/agents/\1`",
        body,
    )

    # Workspace-relative run paths (avoid double ./ prefix)
    body = re.sub(r"(?<![./])`runs/", "`./runs/", body)
    body = re.sub(r"(?<![./])runs/<", "./runs/<", body)
    body = re.sub(r" in `runs/`", " in `./runs/`", body)
    body = re.sub(r" in `runs/", " in `./runs/", body)

    return body


def transform_skill(content: str) -> str:
    if "## Sage paths (global install)" in content:
        return content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return PATHS_HEADER + transform_body(content)

    frontmatter = parts[1]
    body = parts[2]
    if body.startswith("\n"):
        body = body[1:]

    title_end = body.find("\n\n")
    if title_end == -1:
        return f"---{frontmatter}---\n\n{PATHS_HEADER}{transform_body(body)}"

    title_block = body[: title_end + 2]
    rest = body[title_end + 2 :]
    return f"---{frontmatter}---\n\n{title_block}{PATHS_HEADER}{transform_body(rest)}"


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: generate-global-skills.py <source-skills-dir> <output-dir>", file=sys.stderr)
        return 1

    source_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for skill_md in sorted(source_dir.glob("*/SKILL.md")):
        skill_name = skill_md.parent.name
        out_skill_dir = output_dir / skill_name
        out_skill_dir.mkdir(parents=True, exist_ok=True)
        raw = skill_md.read_text(encoding="utf-8")
        out_skill_dir.joinpath("SKILL.md").write_text(
            transform_skill(raw),
            encoding="utf-8",
        )
        count += 1

    print(f"Generated {count} skills in {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
