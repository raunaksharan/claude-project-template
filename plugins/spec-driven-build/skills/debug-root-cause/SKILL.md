---
name: debug-root-cause
description: Use on any failing test, wrong outcome, unexpected escalation or error, before proposing a fix. Finds the root cause from the error, the audit trail and the trace. Adapted from obra/superpowers systematic-debugging (MIT).
---

# Find the root cause before fixing anything

A symptom fix is a failure. (Adapted from obra/superpowers `systematic-debugging`; see
THIRD_PARTY_NOTICES.md.)

## 1. Investigate

- **Read the whole error,** including the test name and the first traceback line that is
  this project's code.
- **Reproduce it** with the smallest command: one test (`-k name`), or one unit of work
  through the CLI with the same injected faults.
- **Look at what the system records:** the outcome's reason codes and audit trail, and
  the trace if there is one (which step failed, how many attempts, how long).
- **Check what changed:** `git diff`, `git log -3`.

## 2. Compare

Find the working example: a passing case, the behaviour in SPEC.md, or a reference tag
(`git diff <tag> -- <file>`).

## 3. One hypothesis at a time

State it, test it with the smallest change or print, and confirm or drop it before the
next one.

## 4. Fix, then prove it

Write or name the test that reproduces the bug (`tdd-module`), fix the cause, then run
`verify-before-done`. If the bug taught something general, use `review-and-learn` to add
it to CLAUDE.md › Learnings from PRs.

<rules>
- Three failed fixes in a row: stop, and question the assumption, not the code.
- Never "fix" by loosening a threshold, an expectation or a test.
</rules>
