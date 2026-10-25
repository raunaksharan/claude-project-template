---
description: Build one module from the milestone's SPEC.md, test-first, then verify
argument-hint: "<path, e.g. src/pkg/tools/gateway.py>"
---
<task>Build $ARGUMENTS.</task>

<spec>The section for $ARGUMENTS in the current milestone's SPEC.md
(milestones/NN-*/SPEC.md): purpose, public API (exact names and signatures), behaviour,
exact messages, acceptance criteria.</spec>

<method>Use the tdd-module skill and follow the karpathy-guidelines skill. Run the module's
tests and watch them fail, write the smallest code that satisfies the spec, then run the
whole suite. Keep the module docstring, extended to explain why.</method>

<constraints>
- Don't edit the files CLAUDE.md lists under "Don't touch".
- Only the names the spec lists are public; nothing for a later milestone.
- If the spec is unclear, stop and ask (clarify-before-building); record the answer.
</constraints>

<done_when>The module's tests pass, the suite has no new failures, and lint is clean.
Then show me the diff summary and suggest /verify.</done_when>
