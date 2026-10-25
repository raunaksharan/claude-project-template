---
description: Independent review of the current diff against this repo's rules
---
<task>Get an independent review of the current work, using the review-and-learn skill.</task>

<reviewer>
A subagent that has not seen this session. Give it CLAUDE.md, ARCHITECTURE.md,
architecture/failure-modes.md, the milestone's SPEC.md, and the output of `git diff`
(staged and unstaged). Without git, give it the milestone's modules (listed in SPEC.md)
and any other file you changed.
</reviewer>

<check>
1. Breaks of the CLAUDE.md rules.
2. Edits to tests (Mode A), evals, thresholds, reference data or golden-case expectations.
3. ACs with no test; missing tests for new branches and both sides of every threshold.
4. Code beyond what the spec asked for.
5. Personal data in prompts, messages or traces.
</check>

<output>Findings ranked by severity, each with file:line and why it matters. Don't fix
anything. Then wait: I'll decide which findings to act on, and /learn records the
lessons.</output>
