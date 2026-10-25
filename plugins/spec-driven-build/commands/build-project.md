---
description: Build the approved plan milestone by milestone (refuses until PLAN.md is approved)
argument-hint: "[first milestone, e.g. 01] [--unattended]"
---
<task>Build the project from its approved plan, starting at milestone ${ARGUMENTS:-01}.</task>

<check>Read .claude/plan-approval.json and PLAN.md. If the approval file is missing, or
PLAN.md's status isn't APPROVED, say so and stop: the user approves with
! python3 scripts/approve_plan.py --by "<name>". Never approve it yourself.</check>

<loop>For each milestone in milestones/README.md, in order, follow its PROMPTS.md: start,
plan (gate G1), tests first in Mode B (gate G2), scaffold, one module per step, verify,
review (gate G3), learn. Commit when /verify is green (gate G4). At each gate, stop and
wait for me, unless I passed --unattended. Then record the decision as an assumption in
the milestone's plan and carry on.</loop>

<stop>Stop at the first milestone whose /verify you can't get green, or at a SPEC
contradiction. Report the failing check, the SPEC line, and what you'd change. A change to
the plan itself (scope, milestones, decisions) goes back to the user and needs a new
approval.</stop>
