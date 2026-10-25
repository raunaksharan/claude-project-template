---
description: (Mode B) Write the milestone's tests from its acceptance criteria, before any code
argument-hint: "<milestone number, e.g. 03>"
---
<task>Write the tests for milestone $ARGUMENTS from the acceptance criteria in
milestones/$ARGUMENTS-*/SPEC.md. No implementation code.</task>

<method>Use the tdd-module skill (Mode B). One or more tests per AC, named for the
behaviour, with the AC id in the docstring. Use the exact values, names and messages from
the SPEC. Cover both sides of every threshold, the value exactly on it, and missing,
empty and malformed input. Use the seed's fixtures and mocks; inject the clock and
randomness. Put them in the test files the SPEC names, or tests/test_<module>.py.</method>

<check>Run them: each must fail with NotImplementedError or an import error, never pass,
and never fail for a reason in the test itself. Make a table: AC id → test names. Any AC
you couldn't test, say why.</check>

<stop>Show the table and the test files, and wait for my approval. After approval these
tests are the answer key: change one later only by asking me, with the SPEC line it
contradicts. Unattended: treat them as approved, and list any doubtful AC as an
assumption in the plan.</stop>
