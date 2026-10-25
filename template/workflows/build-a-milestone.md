# Build a milestone with Claude Code

**When:** every milestone in `milestones/README.md`. This is the core loop.

## Steps

| Step | You type | Claude uses | You check (gate) |
|---|---|---|---|
| 1. Start | `/start-milestone NN` | — | What's red, and why |
| 2. Clarify | `/clarify <the module>` (only if something's open) | `clarify-before-building` | Each answer is a line in CLAUDE.md › Clarifications |
| 3. Plan | `/plan-milestone NN` | `write-plan` | **G1:** the plan in `docs/plans/` goes bottom-up, maps every AC to a task, names the failure modes, and touches nothing from a later milestone |
| 4. Tests (Mode B) | `/write-tests NN` | `tdd-module` | **G2:** every AC has a test; both sides of each threshold; messages match the SPEC |
| 5. Scaffold | the scaffold prompt in PROMPTS.md | — | Tests fail one by one, not at import |
| 6. Build | `/build-module src/<pkg>/<path>.py`, one per module | `tdd-module`, `karpathy-guidelines` | It ran the tests red first, then green. Read the diff |
| 7. Debug (if red) | describe the failure | `debug-root-cause` | It found a cause before changing code |
| 8. Verify | `/verify` | `verify-before-done` | The real numbers |
| 9. Review | `/review` | `review-and-learn` | **G3:** accept or reject each finding, with a reason |
| 10. Learn | `/learn <what went wrong>` | `review-and-learn` | One new line in CLAUDE.md › Learnings from PRs; a SPEC fix if the spec was the gap |
| 11. Merge | — | — | **G4:** the PR explains the decisions in the author's own words |

A good build prompt has this shape (PROMPTS.md has one per module):

```text
<task>Build src/<pkg>/<module>.py: <the public names></task>
<spec>milestones/NN-<slug>/SPEC.md, section "<module>"</spec>
<tests><the narrowest test command></tests>
<constraints>No new dependency. Don't edit tests. Only the names SPEC.md lists.</constraints>
<done_when>Those tests pass, the suite has no new failures, lint is clean.</done_when>
```

## Unattended (headless) runs

`claude -p "<prompt>" --permission-mode acceptEdits` runs the same loop without a
human. The commands then record open questions as assumptions in the plan instead of
waiting. Review those assumptions afterwards: each one is a spec gap to close.

## Done when

`/verify` is green, and the PR has the plan, the rejected findings with their reasons,
the learning lines and the author's explanation.
