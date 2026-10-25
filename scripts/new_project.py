"""Start a new project from template/.

    python3 scripts/new_project.py --name adas-agent-factory --package adas_factory \
            --cli adas --dest ../adas-agent-factory

Copies template/ into --dest, renames __PACKAGE__ paths, and fills {{PROJECT}},
{{PACKAGE}} and {{CLI}}. Every {{FILL: …}} is left for the architect; check_ready.py lists them.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
TEMPLATE = HERE / "template"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--name", required=True, help="project name, e.g. adas-agent-factory")
    ap.add_argument("--package", required=True, help="Python package, e.g. adas_factory")
    ap.add_argument("--cli", required=True, help="CLI command, e.g. adas")
    ap.add_argument("--dest", required=True)
    ap.add_argument("--no-git", action="store_true", help="don't run git init")
    a = ap.parse_args()

    dest = Path(a.dest).resolve()
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"{dest} exists and is not empty")
    shutil.copytree(TEMPLATE, dest, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
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
    if not a.no_git:
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=dest, check=True)
    print(f"created {dest}")
    print(f"next: fill the plan-phase files (PLAN-PHASE.md), then "
          f"python3 {HERE / 'scripts/check_ready.py'} {dest}")


if __name__ == "__main__":
    main()
