---
name: add-{{FILL: thing}}
description: {{FILL: one sentence: what this adds, and the request wording that should trigger it, e.g. "Use when a request adds a new external tool or integration."}}
---

# Add {{FILL: thing}}

<!-- A use-case skill captures a change you expect to repeat. Copy this folder to
     .claude/skills/add-<thing>/ and fill it in. Good ones are short (20–40 lines) and
     name exact files, decisions, tests and docs. Examples from the worked project:
     add-policy-rule, add-tool-check, add-golden-case, add-workflow-node,
     new-prompt-version, investigate-decision. -->

{{FILL: one or two sentences on why this change is risky, so the reader takes the steps seriously.}}

1. **Decide first.** {{FILL: the question to ask if the request doesn't say, e.g. required or optional; reject or escalate. Record the answer in CLAUDE.md › Clarifications.}}
2. **The source of truth.** {{FILL: which file holds the rule or contract; who owns it.}}
3. **The code.** {{FILL: the files to touch, in order, and the pattern to follow (name an existing example).}}
4. **Failure handling.** {{FILL: every fault kind it must handle, and the status or reason code for each.}}
5. **Tests.** {{FILL: the test file; the cases: OK path, each fault, both sides of each threshold.}}
6. **Eval.** {{FILL: a golden case per meaningful outcome, expected answer from the rules, never from running the system.}}
7. **Document.** {{FILL: the row in architecture/failure-modes.md, the ADR if a decision was made, the code map.}}
8. **Verify.** `/verify`. {{FILL: the invariant that must still hold, e.g. a failure never turns a reject into an accept.}}
