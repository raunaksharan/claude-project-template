---
name: write-plan
description: Use when a milestone, rule, tool or change is clear enough to build, before touching code. Writes a small test-first plan in docs/plans/ from the milestone's SPEC.md. Adapted from obra/superpowers writing-plans (MIT).
---

# Write the plan

Write the plan for an engineer who hasn't seen this repo. They can write idiomatic code
once they know the exact names, the exact tests and the order. What they can't know is
what you decided, so write that down. (Adapted from obra/superpowers `writing-plans`; see
THIRD_PARTY_NOTICES.md.)

**Save to:** `docs/plans/milestone-NN-<short-name>.md` (or `docs/plans/<date>-<change>.md`
outside a milestone). Commit it with the work.

## Header

```markdown
# <What this builds> plan

**Goal:** one sentence.
**Spec:** milestones/NN-*/SPEC.md (and the ADR or source of truth, if any)
**Tests that prove it:** the files and test names (Mode A), or the ACs and the test
files you will write (Mode B)
**Constraints:** the CLAUDE.md rules that apply; the files not to touch
**Assumptions:** anything the spec left open and how you resolved it

## Review focus
The two or three failure modes from architecture/failure-modes.md this work touches, and
the behaviour the domain owner would expect for each.
```

## Tasks

Bottom-up: pure functions first, then the code that calls them. One task per module, or
per function when a module is big. Each task:

```markdown
### Task N: <module or function>
**Files:** create or modify `src/...`; tests `tests/test_...py`
**Interfaces:** consumes <exact names from earlier tasks or the seed>; produces <exact
names and signatures from SPEC.md that later code imports>
**ACs covered:** AC-NN.k, ...
- [ ] Run the named tests and watch them fail (or error at import).
- [ ] Implement the smallest code that satisfies the spec.
- [ ] Run the tests; then the whole suite.
- [ ] Lint clean; commit with a message that says why.
```

Then stop and show the plan. Build only after it's approved, or, unattended, after
writing your assumptions into it.

<rules>
- Names and signatures come from SPEC.md exactly; other code and the tests import them.
- Every AC maps to a task. An AC no task covers is a gap: say so.
- No task for a later milestone's feature (karpathy-guidelines §2).
</rules>
