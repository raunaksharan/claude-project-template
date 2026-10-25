---
description: Plan a milestone before writing any code (clarify, then a test-first plan)
argument-hint: "<milestone number, e.g. 03>"
---
<task>Plan milestone $ARGUMENTS. Don't write code yet.</task>

<read>
CLAUDE.md (Context, Scope, Plan, Rules, Clarifications, Learnings from PRs);
ARCHITECTURE.md; milestones/$ARGUMENTS-*/SPEC.md and PROMPTS.md; the failure modes the
SPEC names; the tests it names (Mode A).
</read>

<steps>
1. Use the clarify-before-building skill. Ask me, one at a time, about anything the spec
   leaves open that would change the code, and record each answer under Clarifications.
2. Use the write-plan skill. Save the plan to docs/plans/milestone-$ARGUMENTS-<name>.md:
   goal, the tests or ACs that prove it, review focus (failure modes), and one task per
   module, bottom-up, each with the exact names from SPEC.md and the ACs it covers.
3. List what you will not touch: the files under "Don't touch" in CLAUDE.md, and any
   module not in this milestone's SPEC.md.
</steps>

<stop>Show the plan and wait for me to approve or change it. If nobody can answer (an
unattended run), answer the open questions from SPEC.md, CLAUDE.md, ARCHITECTURE.md and
the existing code, write each answer as an assumption in the plan, and treat the plan as
approved.</stop>
