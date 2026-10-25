"""Is a project ready to hand to Claude? The plan phase's definition of ready.

    python3 scripts/check_ready.py ../my-project            # all checks
    python3 scripts/check_ready.py ../my-project --no-kit   # ignore kit/ (not using it)

Fails (exit 1) while any {{FILL…}} marker is left or a required part is missing:
- CLAUDE.md has its sections and chooses one test mode (A or B);
- ARCHITECTURE.md has sections 1–14, and invariants;
- at least one ADR, and a failure-modes table with F1;
- a milestone map, and per milestone a SPEC.md (Public API, Behaviour, Acceptance
  criteria with AC ids) and a PROMPTS.md with XML-tagged prompts;
- .mcp.json parses, and the process skills are vendored or the plugin is enabled;
- .claude/commands/verify.md lists real checks.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CLAUDE_SECTIONS = ["## Context", "## Scope", "## Plan", "## Commands", "## Rules",
                   "## How to work", "## Don't touch", "## Code map", "## Skills and commands",
                   "## MCP servers and plugins", "## Clarifications", "## Learnings from PRs"]
SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules", ".pytest_cache", ".ruff_cache"}


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    no_kit = "--no-kit" in sys.argv
    root = Path(args[0] if args else ".").resolve()
    problems: list[str] = []

    def need(cond: bool, msg: str) -> None:
        if not cond:
            problems.append(msg)

    # 1. unfilled markers
    for f in sorted(root.rglob("*")):
        if not f.is_file() or SKIP_DIRS & set(f.relative_to(root).parts):
            continue
        rel = f.relative_to(root)
        if no_kit and rel.parts[0] == "kit":
            continue
        if rel.parts[:2] == (".claude", "skills") and "_use-case-skill-template" in rel.parts:
            continue  # the template stays a template
        if rel.parts[:2] == ("milestones", "01-example"):
            continue  # reported below if it's the only milestone
        try:
            lines = f.read_text().splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(lines, 1):
            if "{{" in line:
                problems.append(f"unfilled: {rel}:{i}: {line.strip()[:90]}")

    # 2. CLAUDE.md
    claude = root / "CLAUDE.md"
    text = claude.read_text() if claude.exists() else ""
    need(bool(text), "missing CLAUDE.md")
    for s in CLAUDE_SECTIONS:
        need(s in text, f"CLAUDE.md: missing section '{s}'")
    plan = text.split("## Plan", 1)[-1].split("\n## ", 1)[0]
    modes = [m for m in ("Mode A", "Mode B") if m in plan]
    need(len(modes) == 1, "CLAUDE.md › Plan: choose exactly one test mode (Mode A or Mode B)")

    # 3. ARCHITECTURE.md
    arch = root / "ARCHITECTURE.md"
    atext = arch.read_text() if arch.exists() else ""
    need(bool(atext), "missing ARCHITECTURE.md")
    for n in range(1, 15):
        need(re.search(rf"^## {n}\. ", atext, re.M) is not None,
             f"ARCHITECTURE.md: missing section {n}")
    need(re.search(r"^\| I1 \|", atext, re.M) is not None, "ARCHITECTURE.md: no invariant I1")

    # 4. architecture/
    adrs = [p for p in (root / "architecture/adr").glob("*.md") if not p.name.startswith("0000")]
    need(bool(adrs), "architecture/adr: no ADR besides the template")
    fm = root / "architecture/failure-modes.md"
    need(fm.exists() and re.search(r"^\| F1 \|", fm.read_text(), re.M) is not None,
         "architecture/failure-modes.md: no F1 row")
    need((root / "architecture/requirements.md").exists(), "missing architecture/requirements.md")

    # 5. milestones
    mdirs = sorted(p for p in (root / "milestones").glob("[0-9][0-9]-*") if p.is_dir())
    real = [p for p in mdirs if p.name != "01-example"]
    need(bool(real), "milestones/: no milestone folders besides 01-example")
    if real and (root / "milestones/01-example").exists():
        problems.append("milestones/01-example: delete the example folder")
    for d in real:
        spec, prompts = d / "SPEC.md", d / "PROMPTS.md"
        s = spec.read_text() if spec.exists() else ""
        need(bool(s), f"{d.name}: missing SPEC.md")
        need("Public API" in s, f"{d.name}/SPEC.md: no Public API")
        need("Behaviour" in s, f"{d.name}/SPEC.md: no Behaviour")
        need(re.search(r"\bAC-\d+\.\d+", s) is not None,
             f"{d.name}/SPEC.md: no acceptance criteria (AC-NN.k)")
        p = prompts.read_text() if prompts.exists() else ""
        need("<task>" in p and "<done_when>" in p,
             f"{d.name}/PROMPTS.md: missing or has no XML-tagged prompts")
    mr = root / "milestones/README.md"
    need(mr.exists() and re.search(r"^\| 0?1 \|", mr.read_text(), re.M) is not None,
         "milestones/README.md: no milestone map")

    # 6. MCP config parses; the process skills are present, vendored or as the plugin
    import json as _json
    mcp = root / ".mcp.json"
    try:
        need("mcpServers" in _json.loads(mcp.read_text()), ".mcp.json: no mcpServers key")
    except (OSError, ValueError):
        problems.append(".mcp.json: missing or not valid JSON")
    settings = root / ".claude/settings.json"
    stext = settings.read_text() if settings.exists() else ""
    need((root / ".claude/skills/tdd-module/SKILL.md").exists() or "spec-driven-build@" in stext,
         "process skills: neither vendored in .claude/skills nor the plugin enabled")

    # 7. verify command
    v = root / ".claude/commands/verify.md"
    need(v.exists() and re.search(r"^\s*1\. \S", v.read_text(), re.M) is not None,
         ".claude/commands/verify.md: no checks listed")

    if problems:
        print(f"NOT READY: {len(problems)} problem(s) in {root}\n")
        print("\n".join(f"- {p}" for p in problems))
        return 1
    print(f"READY: {root} has every plan-phase file filled in. Hand it to Claude: "
          f"/start-milestone {real[0].name[:2]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
