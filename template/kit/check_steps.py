"""Check that each milestone's PROMPTS.md can be built in the order it gives (optional tool).

    python3 kit/check_steps.py 03      # one milestone
    python3 kit/check_steps.py all

For each milestone, in a temporary worktree of the reference code (`base` in
kit/milestones.json):

1. **Scaffold:** every function and method in the built modules raises
   NotImplementedError, except constructors, which only store their arguments (what the
   scaffold step of PROMPTS.md produces). No test file may
   then fail to import, except those in `_config.allowed_collection_errors`.
2. **Steps:** for each step in steps.json, restore the reference code for the step's
   files (keeping `still_stubbed` names stubbed) and run the step's tests. Every selected
   test must pass. Later steps' code stays stubbed.

A failing step means the prompt pack asks for something its tests can't show yet: fix
the order in PROMPTS.md and steps.json, not the tests.
"""

from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_ALL = json.loads((ROOT / "kit/milestones.json").read_text())
LESSONS = {k: v for k, v in _ALL.items() if not k.startswith("_")}
STEPS = {k: v for k, v in json.loads((ROOT / "kit/steps.json").read_text()).items()
         if not k.startswith("_")}
# test files that can't collect until some step's code exists (say so in PROMPTS.md)
ALLOWED_COLLECTION_ERRORS = {k: set(v) for k, v in
                             _ALL["_config"].get("allowed_collection_errors", {}).items()}


def stub(source: str, qualnames: set[str] | None) -> str:
    """Replace the bodies of the named functions (all functions and methods if None)."""
    lines = source.splitlines(keepends=True)
    edits = []

    def walk(node: ast.AST, prefix: str) -> None:
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.ClassDef):
                walk(ch, f"{prefix}{ch.name}.")
            elif isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)):
                q = f"{prefix}{ch.name}"
                # a scaffold keeps constructors (they only store their arguments)
                if (qualnames is None and ch.name != "__init__") or (
                        qualnames is not None and q in qualnames):
                    body = ch.body
                    has_doc = (isinstance(body[0], ast.Expr)
                               and isinstance(body[0].value, ast.Constant)
                               and isinstance(body[0].value.value, str))
                    start = body[1].lineno if has_doc and len(body) > 1 else (
                        None if has_doc else body[0].lineno)
                    if start is not None:
                        indent = " " * body[0].col_offset
                        edits.append((start - 1, ch.end_lineno,
                                      f"{indent}raise NotImplementedError\n"))
                if qualnames is not None:
                    walk(ch, f"{q}.")  # nested functions can be named explicitly

    walk(ast.parse(source), "")
    for s, e, new in sorted(edits, reverse=True):
        lines[s:e] = [new]
    return "".join(lines)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = {**os.environ, "UV_SYSTEM_CERTS": "1"}
    env.pop("UV_NATIVE_TLS", None)
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)


def pytest(wt: Path, tests: list[str], k: str | None) -> tuple[bool, str]:
    cmd = ["uv", "run", "pytest", "-o", "addopts=", "-q", "-p", "no:cacheprovider", *tests]
    if k:
        cmd += ["-k", k]
    r = run(cmd, wt)
    last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
    return r.returncode == 0 and " passed" in last, last


def check(n: str) -> bool:
    cfg = LESSONS[n]
    ref = {p: subprocess.run(["git", "show", f"{cfg['base']}:{p}"], cwd=ROOT, check=True,
                             capture_output=True, text=True).stdout for p in cfg["build"]}
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        wt = Path(tmp) / "wt"
        subprocess.run(["git", "worktree", "add", "-q", "--detach", str(wt), cfg["base"]],
                       cwd=ROOT, check=True)
        try:
            run(["uv", "sync", "-q", "--all-groups"], wt)
            for p, src in ref.items():
                (wt / p).write_text(stub(src, None))
            r = run(["uv", "run", "pytest", "-o", "addopts=", "-q", "-p", "no:cacheprovider",
                     "--collect-only"], wt)
            errors = {line.split()[1].split("::")[0] for line in r.stdout.splitlines()
                      if line.startswith("ERROR ")}
            bad = errors - ALLOWED_COLLECTION_ERRORS.get(n, set())
            print(f"milestone {n} scaffold: "
                  + ("imports cleanly" if not bad else f"collection errors in {sorted(bad)}")
                  + (f" (allowed: {sorted(errors & ALLOWED_COLLECTION_ERRORS.get(n, set()))})"
                     if errors - bad else ""))
            ok &= not bad
            restored: set[str] = set()
            for step in STEPS[n]:
                restored |= set(step["restore"])
                still: dict[str, set[str]] = {}
                for s in step.get("still_stubbed", []):
                    f, q = s.split("::")
                    still.setdefault(f, set()).add(q)
                for p, src in ref.items():
                    if p in restored:
                        (wt / p).write_text(stub(src, still[p]) if p in still else src)
                    else:
                        (wt / p).write_text(stub(src, None))
                passed, last = pytest(wt, step["tests"], step.get("k"))
                extra = ""
                for c in step.get("commands", []) if passed else []:
                    r = run(c["cmd"].split(), wt)
                    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
                    passed &= r.returncode == 0 and c.get("expect", "") in tail
                    extra += f"; {c['cmd']}: {tail}"
                print(f"  {'ok  ' if passed else 'FAIL'} {step['step']}: {last}{extra}")
                ok &= passed
        finally:
            subprocess.run(["git", "worktree", "remove", "--force", str(wt)], cwd=ROOT)
    return ok


if __name__ == "__main__":
    which = sys.argv[1]
    targets = list(LESSONS) if which == "all" else [which]
    results = [check(t) for t in targets]
    sys.exit(0 if all(results) else 1)
