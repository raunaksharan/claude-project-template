"""Start a new project from template/.

    python3 scripts/new_project.py --name adas-agent-factory --package adas_factory \
            --cli adas --dest ../adas-agent-factory [--kit vendored|plugin]

Copies template/ into --dest, renames __PACKAGE__ paths, and fills {{PROJECT}},
{{PACKAGE}} and {{CLI}}. Every {{FILL: …}} is left for the architect; check_ready.py lists them.

--kit vendored (default) copies the spec-driven-build plugin's skills and commands into
the project's .claude/, so it works offline, in headless runs and in untrusted folders.
--kit plugin instead registers the fde-project-kit marketplace and enables the plugin in
.claude/settings.json, so every project shares one copy.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
TEMPLATE = HERE / "template"
PLUGIN = HERE / "plugins" / "spec-driven-build"
MARKETPLACE = "fde-project-kit"
MARKETPLACE_REPO = "raunaksharan/claude-project-template"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--name", required=True, help="project name, e.g. adas-agent-factory")
    ap.add_argument("--package", required=True, help="Python package, e.g. adas_factory")
    ap.add_argument("--cli", required=True, help="CLI command, e.g. adas")
    ap.add_argument("--dest", required=True)
    ap.add_argument("--kit", choices=["vendored", "plugin"], default="vendored",
                    help="copy the process skills and commands in, or enable the plugin")
    ap.add_argument("--with-kit", action="store_true",
                    help="also copy kit/ (starter branches from reference code; for teaching)")
    ap.add_argument("--no-git", action="store_true", help="don't run git init")
    a = ap.parse_args()

    dest = Path(a.dest).resolve()
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"{dest} exists and is not empty")
    shutil.copytree(TEMPLATE, dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    if not a.with_kit:
        shutil.rmtree(dest / "kit", ignore_errors=True)
    for p in sorted(dest.rglob("*__PACKAGE__*"), key=lambda p: -len(p.parts)):
        p.rename(p.with_name(p.name.replace("__PACKAGE__", a.package)))
    values = {"{{PROJECT}}": a.name, "{{PACKAGE}}": a.package, "{{CLI}}": a.cli}
    for f in dest.rglob("*"):
        if f.is_file():
            try:
                text = f.read_text()
            except UnicodeDecodeError:
                continue
            new = text
            for k, v in values.items():
                new = new.replace(k, v)
            if new != text:
                f.write_text(new)
    (dest / ".claude/hooks/lint.sh").chmod(0o755)
    if a.kit == "vendored":
        for sub in ("skills", "commands"):
            shutil.copytree(PLUGIN / sub, dest / ".claude" / sub, dirs_exist_ok=True)
        shutil.copy2(PLUGIN / "THIRD_PARTY_NOTICES.md", dest / ".claude/skills/THIRD_PARTY_NOTICES.md")
    else:
        settings_path = dest / ".claude/settings.json"
        settings = json.loads(settings_path.read_text())
        settings["extraKnownMarketplaces"] = {
            MARKETPLACE: {"source": {"source": "github", "repo": MARKETPLACE_REPO}}}
        settings["enabledPlugins"] = {f"spec-driven-build@{MARKETPLACE}": True}
        settings_path.write_text(json.dumps(settings, indent=2) + "\n")
    if not a.no_git:
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=dest, check=True)
    print(f"created {dest}")
    print(f"next: fill the plan-phase files (PLAN-PHASE.md), then "
          f"python3 {HERE / 'scripts/check_ready.py'} {dest}")


if __name__ == "__main__":
    main()
