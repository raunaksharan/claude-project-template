# Milestones

<!-- PLAN-PHASE.md step 5. Four to eight milestones, bottom-up: domain and deterministic
     core first, then AI pieces, then orchestration, then evaluation and operations.
     Each must be shippable and testable on its own. -->

| # | Milestone | Builds (Claude writes) | Seed (given) | Closes failure modes | Acceptance command |
|---|---|---|---|---|---|
| 01 | {{FILL}} | {{FILL: modules}} | {{FILL: types, data, mocks, wiring}} | {{FILL: F-numbers}} | {{FILL}} |

Each milestone folder has:

- `SPEC.md`: the contract. Public API, behaviour, exact messages, acceptance criteria.
- `PROMPTS.md`: how to build it with Claude Code, one XML-tagged prompt per module.
- In Mode A, the tests the SPEC names, which ship in `tests/`.
