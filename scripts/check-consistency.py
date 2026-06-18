#!/usr/bin/env python3
"""Check that profile and skills-mirror tables agree with workflows/feature-sdlc.yaml.

workflows/feature-sdlc.yaml is canonical. This script re-derives the expected
values from it and diffs them against the markdown tables in Agents.md,
workflows/profiles.md, agents/sage-orchestrator.md, and agents/sage-planner.md,
plus the Skills mirror table against actual .cursor/skills/ folders.

No third-party dependencies (works without pyyaml installed).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ARROW = " → "
EMPTY_MARKERS = {"none", "—", "-", ""}


def fail(errors, msg):
    errors.append(msg)


def parse_profiles(yaml_text):
    """Minimal parser for the flat `profiles:` block in feature-sdlc.yaml."""
    block_match = re.search(r"^profiles:\n(.*?)^phases:\n", yaml_text, re.S | re.M)
    if not block_match:
        raise ValueError("could not find profiles: block in feature-sdlc.yaml")
    block = block_match.group(1)

    profiles = {}
    entries = re.split(r"\n(?=  [a-z][a-z0-9-]*:\n)", block)
    for entry in entries:
        name_match = re.match(r"  ([a-z][a-z0-9-]*):", entry)
        if not name_match:
            continue
        name = name_match.group(1)

        def field(key, default=None):
            m = re.search(rf"^    {key}:\s*(.+?)\s*(?:#.*)?$", entry, re.M)
            return m.group(1).strip() if m else default

        phases_raw = field("phases", "[]")
        phases = [p.strip() for p in phases_raw.strip("[]").split(",") if p.strip()]

        skipped_raw = field("skipped_phases", "[]")
        skipped = [p.strip() for p in skipped_raw.strip("[]").split(",") if p.strip()]

        qa_requires_raw = field("qa_requires", "[]")
        qa_requires = [p.strip() for p in qa_requires_raw.strip("[]").split(",") if p.strip()]

        profiles[name] = {
            "phases": phases,
            "skipped_phases": skipped,
            "qa_requires": qa_requires,
            "qa_next": field("qa_next", ""),
            "qa_handoff": field("qa_handoff", ""),
            "default_route_after_plan": field("default_route_after_plan", ""),
            "architect_optional": field("architect_optional", "false") == "true",
        }
    return profiles


def extract_table(text, header_contains):
    """Return list of rows (each a list of cell strings) for the markdown table
    whose header line contains `header_contains`."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and header_contains in line:
            start = i
            break
    if start is None:
        raise ValueError(f"could not find table header containing {header_contains!r}")

    rows = []
    for line in lines[start + 2:]:
        if not line.strip().startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def cell_name(cell):
    return cell.strip("`")


def normalize_list_cell(cell):
    if cell.strip() in EMPTY_MARKERS:
        return set()
    return {p.strip().strip("`") for p in cell.split(",") if p.strip()}


def pipeline_string(phases, architect_optional):
    parts = []
    for p in phases:
        if architect_optional and p == "architect":
            parts.append("architect?")
        else:
            parts.append(p)
    return ARROW.join(parts)


def check_agents_md_sdlc_flow(profiles, text, errors):
    rows = extract_table(text, "| Profile | Path |")
    seen = set()
    for cells in rows:
        if len(cells) < 2:
            continue
        name = cell_name(cells[0])
        if name not in profiles:
            continue
        seen.add(name)
        expected = pipeline_string(profiles[name]["phases"], profiles[name]["architect_optional"])
        actual = cells[1].strip()
        if actual != expected:
            fail(errors, f"Agents.md SDLC flow: {name!r} expected {expected!r}, found {actual!r}")
    missing = set(profiles) - seen
    if missing:
        fail(errors, f"Agents.md SDLC flow: missing rows for {sorted(missing)}")


def check_profiles_md(profiles, text, errors):
    rows = extract_table(text, "| Profile ")
    seen = set()
    for cells in rows:
        if len(cells) < 4:
            continue
        name = cell_name(cells[0])
        if name not in profiles:
            continue
        seen.add(name)
        p = profiles[name]
        expected_pipeline = pipeline_string(p["phases"], p["architect_optional"])
        actual_pipeline = cells[1].strip()
        if actual_pipeline != expected_pipeline:
            fail(errors, f"profiles.md pipeline: {name!r} expected {expected_pipeline!r}, found {actual_pipeline!r}")

        expected_skipped = set(p["skipped_phases"])
        actual_skipped = normalize_list_cell(cells[2])
        if actual_skipped != expected_skipped:
            fail(errors, f"profiles.md skipped_phases: {name!r} expected {expected_skipped}, found {actual_skipped}")

        expected_after_qa = p["qa_next"]
        actual_after_qa = cells[3].strip().strip("`")
        if actual_after_qa != expected_after_qa:
            fail(errors, f"profiles.md After QA: {name!r} expected {expected_after_qa!r}, found {actual_after_qa!r}")
    missing = set(profiles) - seen
    if missing:
        fail(errors, f"profiles.md: missing rows for {sorted(missing)}")


def check_orchestrator_md(profiles, text, errors):
    rows = extract_table(text, "| Profile | Skipped phases | Build command | QA requires | QA next |")
    seen = set()
    for cells in rows:
        if len(cells) < 5:
            continue
        name = cell_name(cells[0])
        if name not in profiles:
            continue
        seen.add(name)
        p = profiles[name]

        expected_skipped = set(p["skipped_phases"])
        actual_skipped = normalize_list_cell(cells[1])
        if actual_skipped != expected_skipped:
            fail(errors, f"sage-orchestrator.md skipped_phases: {name!r} expected {expected_skipped}, found {actual_skipped}")

        expected_qa_requires = set(p["qa_requires"])
        actual_qa_requires = normalize_list_cell(cells[3])
        if actual_qa_requires != expected_qa_requires:
            fail(errors, f"sage-orchestrator.md qa_requires: {name!r} expected {expected_qa_requires}, found {actual_qa_requires}")

        expected_qa_next = p["qa_next"]
        actual_qa_next = cells[4].strip().strip("`")
        if actual_qa_next != expected_qa_next:
            fail(errors, f"sage-orchestrator.md qa_next: {name!r} expected {expected_qa_next!r}, found {actual_qa_next!r}")
    missing = set(profiles) - seen
    if missing:
        fail(errors, f"sage-orchestrator.md: missing rows for {sorted(missing)}")


def check_planner_md(profiles, text, errors):
    rows = extract_table(text, "| Profile | When | Default route after plan |")
    seen = set()
    for cells in rows:
        if len(cells) < 3:
            continue
        name = cell_name(cells[0])
        if name not in profiles:
            continue
        seen.add(name)
        expected_route = profiles[name]["default_route_after_plan"]
        actual_route_cell = cells[2].strip()
        if expected_route and expected_route not in actual_route_cell:
            fail(errors, f"sage-planner.md default route: {name!r} expected to mention {expected_route!r}, found {actual_route_cell!r}")
    missing = set(profiles) - seen
    if missing:
        fail(errors, f"sage-planner.md: missing rows for {sorted(missing)}")


def check_skills_mirror(text, errors):
    rows = extract_table(text, "| Skill folder | Slash command | Agent file |")
    documented = set()
    for cells in rows:
        if len(cells) < 1:
            continue
        documented.add(cell_name(cells[0]))

    skills_dir = ROOT / ".cursor" / "skills"
    actual = {p.name for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("_")}

    missing_from_docs = actual - documented
    missing_from_disk = documented - actual
    if missing_from_docs:
        fail(errors, f"Skills mirror: folders on disk but not in Agents.md table: {sorted(missing_from_docs)}")
    if missing_from_disk:
        fail(errors, f"Skills mirror: rows in Agents.md table with no folder on disk: {sorted(missing_from_disk)}")


def main():
    errors = []

    yaml_text = (ROOT / "workflows" / "feature-sdlc.yaml").read_text()
    profiles = parse_profiles(yaml_text)

    agents_md = (ROOT / "Agents.md").read_text()
    profiles_md = (ROOT / "workflows" / "profiles.md").read_text()
    orchestrator_md = (ROOT / "agents" / "sage-orchestrator.md").read_text()
    planner_md = (ROOT / "agents" / "sage-planner.md").read_text()

    check_agents_md_sdlc_flow(profiles, agents_md, errors)
    check_profiles_md(profiles, profiles_md, errors)
    check_orchestrator_md(profiles, orchestrator_md, errors)
    check_planner_md(profiles, planner_md, errors)
    check_skills_mirror(agents_md, errors)

    if errors:
        print(f"FAIL: {len(errors)} consistency error(s)\n")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK: {len(profiles)} profiles consistent across Agents.md, profiles.md, "
          f"sage-orchestrator.md, sage-planner.md; skills mirror consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
