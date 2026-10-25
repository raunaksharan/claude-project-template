# CLAUDE.md: {{PROJECT}}

{{FILL: one paragraph. What the system is, for whom, and your job in this repo (e.g. "help ship code that passes the tests and the eval, and that the team can explain").}}

## Context

- **The business.** {{FILL: two or three sentences. Point to `architecture/requirements.md` and say read it first.}}
- **The decisions already made** are the ADRs in `architecture/adr/`: {{FILL: one phrase per ADR, with its number}}. Failure modes F1–Fn are in `architecture/failure-modes.md`. The one-page view is `ARCHITECTURE.md`.
- **The sources of truth:** {{FILL: where thresholds, reference data and expected outcomes live}}.
- **Where a milestone is specified:** `milestones/NN-*/SPEC.md` (what to build: public API, behaviour, exact messages, acceptance criteria) and `PROMPTS.md` (how to build it with you). The milestone map is `milestones/README.md`.

## Scope

- **In scope:** {{FILL}}
- **Out of scope; don't add them:** {{FILL: say it plainly, e.g. UI, multi-region, billing, real cloud services}}
- **Per milestone:** build only what that milestone's SPEC.md lists. Code for a later milestone waits for that milestone, even when it would be easy now.

## Plan

Before writing code for anything bigger than a one-line fix:

1. Read the milestone's SPEC.md, its acceptance criteria and the tests named in it.
2. Write the plan (`/plan-milestone NN`): the files you'll touch, the order (bottom-up: pure functions first), the test that proves each step, and the failure mode it adds or closes.
3. Ask about anything the spec leaves open. Record the answer under Clarifications.
4. Tests: **{{FILL: Mode A — the acceptance tests ship with the milestone; never edit them. | Mode B — write the tests first from the acceptance criteria with `/write-tests`, one or more per AC, and stop for approval before writing code.}}**
5. Build one module at a time; run its tests after each; run `/verify` at the end.

## Commands

```bash
{{FILL: install}}                 # install
{{FILL: lint}}                    # lint
{{FILL: test}}                    # all tests (fast, offline)
{{FILL: run one unit of work}}    # e.g. one case, with its trace
{{FILL: eval}}                    # golden cases + release gates (from milestone N)
```

Everything runs offline on deterministic mocks. Never require an API key or a network service for tests.

## Rules of this system (never break these)

{{FILL: the invariants from ARCHITECTURE.md § 2, as numbered imperatives, each with the reason in one sentence. For example:
1. **The model proposes; code decides.** ...
2. **Escalate, never guess.** ...
3. **Typed results at every boundary.** ...
4. **Provider-agnostic.** Nothing outside `src/{{PACKAGE}}/llm/` imports a model SDK.
5. **Fault injection is a feature.** Faults are refused when `APP_ENV=production`.
6. **Everything is audited.** Append-only.
7. **No personal data in prompts, messages or traces.**}}

## How to work here

These follow the `karpathy-guidelines` skill, applied to this repo.

- **Think before coding.** State your assumptions. If the request is ambiguous, ask, or present the options. Asking is part of doing the job well.
- **Plan first** for anything bigger than a one-line fix: the files you'll touch, the tests that prove it, and the failure mode it adds (if any).
- **Simplicity first.** Write the code this milestone needs and nothing for later milestones. No new dependency without saying why.
- **Surgical changes.** Touch only what the task needs. Don't reformat unrelated code. Flag dead code you notice rather than deleting it.
- **Goal-driven.** Turn the task into a test that fails, make it pass, then run `/verify`. You're done when every check in `/verify` is green.

## Don't touch without being asked

- {{FILL: tests/ (Mode A) and evals/. Make failing tests pass by fixing the code, not the tests.}}
- {{FILL: thresholds and rule tables — business commitments, not tuning knobs}}
- {{FILL: golden-case expectations — they come from the rules, never from running the system}}
- {{FILL: reference data}}

## Code map

| Area | Where | Milestone |
|---|---|---|
| {{FILL}} | `src/{{PACKAGE}}/{{FILL}}` | {{FILL}} |

## Skills and commands

| When | Command | Skill(s) |
|---|---|---|
| Starting a milestone | `/start-milestone NN` | — |
| Something is unclear | `/clarify <task>` | `clarify-before-building` |
| Before code | `/plan-milestone NN` | `clarify-before-building`, `write-plan` |
| Tests first (Mode B) | `/write-tests NN` | `tdd-module` |
| Writing a module | `/build-module <path>` | `tdd-module`, `karpathy-guidelines` |
| A test fails or an outcome looks wrong | — | `debug-root-cause` |
| Before saying "done" | `/verify` | `verify-before-done` |
| Before the PR | `/review`, then `/learn <finding>` | `review-and-learn` |
| Behind on a milestone | `/catch-up NN` | — |
| Use-case work | — | {{FILL: your use-case skills, e.g. add-rule, add-tool, add-golden-case}} |

The procedures behind these are written out for people in `workflows/`. Third-party sources and licences are in `.claude/skills/THIRD_PARTY_NOTICES.md` (vendored) or the plugin's `THIRD_PARTY_NOTICES.md`.

## MCP servers and plugins

**Plugins:** {{FILL: either "the process skills and milestone commands are vendored in `.claude/`" or "install `spec-driven-build@fde-project-kit` (enabled in `.claude/settings.json`); its commands run as `/spec-driven-build:<name>`"}}.

**MCP servers you may use while building** (listed in `.mcp.json`; each needs approval the first time):

| Server | Use it for | Never use it for |
|---|---|---|
| {{FILL: e.g. github, or "none"}} | {{FILL: e.g. reading issues and PRs}} | {{FILL: e.g. pushing, merging, or anything outside this repo}} |

{{FILL: one line on runtime tools: the tools the *system's* agent calls at runtime are not these servers. Say where they live (e.g. "behind the tool gateway in `src/<pkg>/tools/`") and whether runtime MCP is in or out of scope.}}

Secrets for MCP servers come from environment variables (`${VAR}` in `.mcp.json`), never from the file itself.

## Style

{{FILL: language version, libraries (e.g. pydantic v2), typing, docstrings explain *why*, plain names. Tests are small, named for the behaviour, and cover both sides of every threshold.}}

## Clarifications (questions the spec left open, and the answer that stands)

Add one line when you ask something and get an answer: the question, the answer, and where it came from. Don't re-ask what's settled here.

<!-- - **<question, short>:** <answer>. (<who or what settled it>) -->

## Learnings from PRs (add to this list; it's how the next session learns)

One line per lesson learned in review: what went wrong, and the rule that prevents it.

<!-- - <what went wrong, concretely>. <The rule that prevents it.> -->
