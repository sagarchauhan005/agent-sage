import importlib.util
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "generate-global-skills.py"
spec = importlib.util.spec_from_file_location("generate_global_skills", SCRIPT_PATH)
ggs = importlib.util.module_from_spec(spec)
sys.modules["generate_global_skills"] = ggs
spec.loader.exec_module(ggs)


def test_transform_body_rewrites_agents_md_link():
    body = "Read [Agents.md](../../Agents.md) first."
    out = ggs.transform_body(body)
    assert "../../Agents.md" not in out
    assert "$HOME/.sage/Agents.md" in out


def test_transform_body_rewrites_agent_role_file_link():
    body = "See [agents/sage-planner.md](../../agents/sage-planner.md)."
    out = ggs.transform_body(body)
    assert "../../agents/sage-planner.md" not in out
    assert "$HOME/.sage/agents/sage-planner.md" in out


def test_transform_body_makes_run_paths_workspace_relative():
    body = "Write to `runs/<run-id>/plan.md` and check `runs/.current`."
    out = ggs.transform_body(body)
    assert "`./runs/<run-id>/plan.md`" in out
    assert "`./runs/.current`" in out
    # Already-prefixed paths must not get a double ./ prefix.
    assert "././runs/" not in out


def test_transform_body_handles_runs_dir_phrases():
    assert "in `./runs/`" in ggs.transform_body("Create the folder in `runs/`")
    assert "in `./runs/<run-id>/handoffs/`" in ggs.transform_body(
        "Write the handoff in `runs/<run-id>/handoffs/`"
    )


def test_transform_skill_inserts_paths_header_once():
    content = (
        "---\nname: sage-plan\ndescription: test\n---\n\n"
        "# sage-plan\n\n"
        "Read [Agents.md](../../Agents.md).\n"
    )
    out = ggs.transform_skill(content)
    assert out.count("## Sage paths (global install)") == 1
    assert "$HOME/.sage/Agents.md" in out
    # Frontmatter and title stay before the inserted header.
    assert out.index("# sage-plan") < out.index("## Sage paths (global install)")


def test_transform_skill_is_idempotent():
    content = (
        "---\nname: sage-plan\ndescription: test\n---\n\n"
        "# sage-plan\n\n"
        "## Sage paths (global install)\n\nalready transformed\n"
    )
    assert ggs.transform_skill(content) == content


def test_transform_skill_without_frontmatter_still_gets_header():
    content = "# sage-plan\n\nRead [Agents.md](../../Agents.md).\n"
    out = ggs.transform_skill(content)
    assert "## Sage paths (global install)" in out
    assert "$HOME/.sage/Agents.md" in out


def test_main_generates_one_skill_per_source_folder(tmp_path):
    source_dir = tmp_path / "skills"
    out_dir = tmp_path / "out"
    for name in ["sage-plan", "sage-qa"]:
        skill_dir = source_dir / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: test\n---\n\n# {name}\n\nbody\n"
        )

    # main() reads argv directly, so call it with argv patched.
    old_argv = sys.argv
    try:
        sys.argv = ["generate-global-skills.py", str(source_dir), str(out_dir)]
        rc = ggs.main()
    finally:
        sys.argv = old_argv

    assert rc == 0
    assert (out_dir / "sage-plan" / "SKILL.md").exists()
    assert (out_dir / "sage-qa" / "SKILL.md").exists()
    generated = (out_dir / "sage-plan" / "SKILL.md").read_text()
    assert "## Sage paths (global install)" in generated


def test_main_requires_two_arguments(capsys):
    old_argv = sys.argv
    try:
        sys.argv = ["generate-global-skills.py", "only-one-arg"]
        rc = ggs.main()
    finally:
        sys.argv = old_argv
    assert rc == 1
    assert "Usage:" in capsys.readouterr().err
