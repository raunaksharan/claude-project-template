---
name: review-and-learn
description: Use when a milestone module or change is complete, before the PR, and when review feedback arrives. Gets an independent review, weighs each finding on its merits, and records what was learned in CLAUDE.md › Learnings from PRs. Adapted from obra/superpowers requesting-code-review and receiving-code-review (MIT).
---

# Review, then learn from it

Review early; verify every finding before acting on it; write down what the next session
must not repeat. (Adapted from obra/superpowers `requesting-code-review` and
`receiving-code-review`; see THIRD_PARTY_NOTICES.md.)

## 1. Ask for an independent review

Run `/review`. It hands a fresh subagent that hasn't seen this session the diff,
CLAUDE.md, ARCHITECTURE.md and `architecture/failure-modes.md`. Its brief:

```text
<role>Independent reviewer for this system (see CLAUDE.md › Context).</role>
<inputs>git diff; CLAUDE.md; ARCHITECTURE.md; architecture/failure-modes.md; the milestone's SPEC.md</inputs>
<check>CLAUDE.md rules; edits to tests, evals, thresholds or golden answers; ACs without
a test; missing tests (both sides of each threshold); code beyond the spec; personal data
in messages or traces</check>
<output>Findings ranked by severity, each with file:line and why it matters. No fixes.</output>
```

## 2. Weigh each finding

For each one: restate it, check it against the code and the spec, then either accept it
(fix it, one at a time, test each) or push back with the technical reason. No
performative agreement, and no extras the spec didn't ask for.

## 3. Record the learning

For every accepted finding that would apply again, add one line under **Learnings from
PRs** in CLAUDE.md:

```text
- <what went wrong, concretely>. <The rule that prevents it.>
```

Write the rule so a new session can follow it without this conversation. If a line
already covers it, sharpen that line instead of adding a near-duplicate.

## 4. In the PR description

List the findings you rejected and why, and the learning lines you added.
