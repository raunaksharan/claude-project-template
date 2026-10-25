"""Approve PLAN.md: a human act, run by the user, not by Claude.

In Claude Code, type it with the ! prefix so it runs as you:
    ! python3 scripts/approve_plan.py --by "Your Name"

It checks that PLAN.md has no FILL markers left, sets its status line to APPROVED, and writes
.claude/plan-approval.json with your name, the time and a hash of PLAN.md. The plan-gate hook
lets Claude write to the build paths only while that hash matches. Edit PLAN.md later and it
must be approved again. `--revoke` removes the approval.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "PLAN.md"
APPROVAL = ROOT / ".claude" / "plan-approval.json"
STATUS = re.compile(r"^\*\*Status:\*\*.*$", re.M)


def plan_hash(text: str) -> str:
    # the status line is excluded, so writing APPROVED into it doesn't change the hash
    return hashlib.sha256(STATUS.sub("**Status:**", text).encode()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--by", help="who approves")
    ap.add_argument("--revoke", action="store_true")
    a = ap.parse_args()
    if a.revoke:
        APPROVAL.unlink(missing_ok=True)
        PLAN.write_text(STATUS.sub("**Status:** DRAFT", PLAN.read_text(), count=1))
        print("approval revoked; PLAN.md is DRAFT")
        return 0
    if not a.by:
        ap.error("--by is required")
    text = PLAN.read_text()
    if "{" * 2 in text:
        print("PLAN.md still has FILL markers; finish the plan first", file=sys.stderr)
        return 1
    when = dt.datetime.now().astimezone().isoformat(timespec="minutes")
    text = STATUS.sub(f"**Status:** APPROVED by {a.by} on {when}", text, count=1)
    PLAN.write_text(text)
    APPROVAL.write_text(json.dumps({"by": a.by, "at": when, "plan_sha256": plan_hash(text)},
                                   indent=2) + "\n")
    print(f"PLAN.md approved by {a.by}. Claude may now build: /build-project")
    return 0


if __name__ == "__main__":
    sys.exit(main())
