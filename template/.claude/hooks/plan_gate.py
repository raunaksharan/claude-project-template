#!/usr/bin/env python3
"""PreToolUse hook: no writes to the build paths until PLAN.md is approved by a human.

Exit 2 sends the message to Claude and blocks the tool call; exit 0 allows it.
The build paths and the approval file are below. Approval is checked by hash, so
editing PLAN.md after approval blocks the build again until it is re-approved.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

BUILD_PATHS = ("src/", "tests/")
root = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
data = json.load(sys.stdin)
tool_input = data.get("tool_input", {})
target = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
if not target:
    sys.exit(0)
try:
    rel = Path(target).resolve().relative_to(root).as_posix()
except ValueError:
    sys.exit(0)
if not rel.startswith(BUILD_PATHS):
    sys.exit(0)

plan, approval = root / "PLAN.md", root / ".claude" / "plan-approval.json"
ok = False
if plan.exists() and approval.exists():
    text = re.sub(r"^\*\*Status:\*\*.*$", "**Status:**", plan.read_text(), flags=re.M)
    try:
        ok = json.loads(approval.read_text()).get("plan_sha256") == hashlib.sha256(
            text.encode()).hexdigest()
    except ValueError:
        ok = False
if ok:
    sys.exit(0)
print(f"Blocked: {rel} is a build path, and PLAN.md is not approved (or changed since it was). "
      "Finish /plan-project, show the user PLAN.md, and stop. The user approves it by running: "
      '! python3 scripts/approve_plan.py --by "<name>". Never approve it yourself.',
      file=sys.stderr)
sys.exit(2)
