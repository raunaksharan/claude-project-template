# Worked example 2: adas-agent-factory (the template's proof run)

This is a small agent platform: an "agent factory" modelled on a production
agent-platform design. Its first agent triages ADAS emergency-braking events.

- An LLM agent gathers evidence through a governed tool gateway and proposes.
- Deterministic rules decide.
- Every write waits for a safety engineer's approval and is re-authorized at execution.
- Runs are durable: leases, checkpoints, crash recovery.
- New agent versions ship only through an eval gate and a canary.

**How it was built:**
1. The architect filled only the plan-phase files: 4 ADRs (the first is "no LLM in the
   vehicle control loop"), 16 failure modes, and 5 milestone specs with 128 acceptance
   criteria.
2. Headless Claude Code then wrote all the tests and code in Mode B, with no one
   answering its questions.
3. 146 hidden acceptance tests, written from the specs before the build, graded it:
   **146/146**.

The builder wrote 304 tests of its own, and `adas eval` passes 13/13 golden tasks.

What the builder caught in the plan, now part of `PLAN-PHASE.md`:
- an acceptance-criterion example that contradicted its own error table;
- a later milestone that silently changed an earlier milestone's rule;
- a mutation drill that couldn't fail.

The repo has `pilot/README.md`, `pilot/FINDINGS.md` and `pilot/hidden-acceptance/`.

**Also tested: `/plan-project` itself.** It ran on a fresh objective (CoolWatch,
data-center cooling-alert triage), with a simulated user answering four rounds of
questions and then saying "fill the rest yourself".
- It produced 4 ADRs, 7 milestones, 3 use-case skills, 31 golden cases and 17 open
  assumptions, then stopped at "Okay, I'm good. This is the plan."
- It refused to build on "skip the approval formality", and the hook blocked a forced
  write to `src/`.
