# The plan phase: what the architect fixes before Claude builds

> **Two ways through this page:** run `/plan-project <objective>` and Claude interviews
> you through these steps, writing each answer into its file; or fill the files by hand,
> step by step. Either way it ends the same. `check_ready.py` passes, Claude writes
> `PLAN.md`, and **nothing is built until you approve it** with
> `! python3 scripts/approve_plan.py --by "<name>"`, which a hook enforces.

Claude can build almost anything you can specify precisely. What it cannot do is read
your mind about decisions nobody wrote down. The plan phase writes those decisions down,
once, in files that every later session reads.

Work through the steps in order. Each produces a file in the new project. Claude is a
good sparring partner for every step: ask it to challenge the draft, list the failure
modes you missed, or point out where a spec is still ambiguous. Don't let it decide the
things marked **architect decides**.

Rough effort for a 4–6 milestone system: one to two days. In our trials it repaid itself
on the first milestone.

---

## Step 1. Requirements: the problem in the users' words

**File:** `architecture/requirements.md`

- [ ] The business problem in two or three sentences, with today's cost (time, errors,
      risk).
- [ ] The current workflow as observed, numbered. Mark where time goes and where errors
      come from.
- [ ] The users, and what each needs from the system.
- [ ] Functional requirements, numbered `FR-n`, each testable.
- [ ] Non-functional requirements with numbers: latency, availability, cost per unit of
      work, privacy, auditability, residency. Mark which are assumptions.
- [ ] What success looks like, as a measurable outcome.

**Architect decides:** the outcome and the non-negotiables. Claude can draft the rest
from interview notes.

## Step 2. Invariants and decisions

**Files:** `architecture/adr/NNNN-*.md`, and the invariants table in `ARCHITECTURE.md` § 2

An invariant is a rule the system must never break, whatever the model says. Every
agentic system needs at least these four decisions written down. The patterns that
answer them are in [PATTERNS.md](plugins/spec-driven-build/skills/plan-project/PATTERNS.md):

- [ ] **Where the model may act, and where it may not.** Which components are AI and
      which are deterministic, and why (pattern P1). For example: an LLM is never in a
      real-time control loop.
- [ ] **Who decides.** Does the model propose and code decide (P2)? Which actions need a
      human (P8)? Which writes need approval, and are they re-authorized at execution?
- [ ] **What happens when data is missing or conflicting.** Escalate, never guess (P3).
      Name the escalation outcome.
- [ ] **How failures are represented.** Typed results at every boundary, never `None` or
      a bare exception (P4).

For each invariant, fill in three columns: what enforces it in code, what checks it (a
test or an eval invariant), and which ADR explains it.

**Architect decides:** all of it. This is the core of the job.

## Step 3. Failure modes

**File:** `architecture/failure-modes.md`

For every component, ask: what does the system do when this returns nothing, returns
garbage, or never returns? If the answer is "it guesses", the design is wrong.

- [ ] One row per failure: where it happens, the impact if unhandled, the designed
      response (with the reason code or status), and how it is injected for testing.
- [ ] Every external dependency (model, tool, store) has at least a timeout, an error and
      a malformed-answer row.
- [ ] Every AI component has a "confidently wrong" row and a "provider down" row.
- [ ] Number them `F1…Fn`. Specs, plans and reviews cite these numbers.

## Step 4. Architecture

**File:** `ARCHITECTURE.md` (fill every section of the template)

- [ ] The system view: one diagram of the request path, plus a deployment view if it
      differs.
- [ ] The components table, with kind (AI / deterministic / tool / human), module and
      the reason for that kind.
- [ ] The trust model: the layers between model output and a consequential action.
- [ ] Boundaries and contracts: the type crossing each boundary and its failure shape.
- [ ] Dependency direction: which packages may import which.
- [ ] Control flow and resilience: per-step timeout, retries and what failure means
      (escalate / degrade / fall back).
- [ ] Sources of truth: who may change thresholds, reference data and expected outcomes.
- [ ] Evaluation and release gates: expectations, invariants, gates.
- [ ] Observability: what one trace of one unit of work contains, and what never goes in
      it (personal data).
- [ ] Out of scope, said plainly. Claude adds what isn't forbidden.

## Step 5. The milestone map

**File:** `milestones/README.md`

- [ ] Four to eight milestones, each shippable and testable on its own.
- [ ] Order them bottom-up: the domain types and the deterministic core first, then the
      AI pieces that lean on them, then orchestration, then evaluation and operations.
- [ ] For each milestone: its goal, the modules built, the failure modes it closes, and
      its acceptance command.
- [ ] Per milestone, the **seed** (given) versus the **build** (Claude writes). Typically
      the seed is the domain types, reference data, fixtures and wiring. The build is the
      logic.

## Step 6. One SPEC.md per milestone: the contract

**File:** `milestones/NN-*/SPEC.md` (template in `milestones/01-example/`)

This is where most of the precision goes. In our trials the specs that rebuilt cleanly
had every item below. The ones that didn't left 10–20 gaps per milestone, and each gap
turned into a guess.

- [ ] **Public API:** every public name, with its exact signature, field types and
      defaults. List the names other modules import from it, and name what it builds on.
- [ ] **Behaviour,** one bullet per rule, including:
  - [ ] the order of checks, when more than one can fire (and so which message comes first);
  - [ ] each threshold's comparison (`>` or `>=`), unit and tolerance; a value exactly at a
        tolerance passes or fails;
  - [ ] what happens on missing, empty and malformed input, never "handle gracefully";
  - [ ] rounding (where, how many places) and the number formatting in messages;
  - [ ] key order and id formats when a structure is serialised or shown to a model;
  - [ ] the regexes, when text is parsed;
  - [ ] the clock and randomness: always injected, never read directly.
- [ ] **Exact messages** wherever a test, a model's repair turn or a human reads them.
      Write them as format strings: `"figures.{name} = {value} but the fact is {actual}"`.
- [ ] **Acceptance criteria,** numbered `AC-NN.k`, in Given / When / Then form, with
      concrete values. One for each side of every threshold. Every AC becomes at least
      one test.
- [ ] **Changes to earlier modules,** or "None".
- [ ] **The acceptance command:** what must be green to call the milestone done.

**Tests: choose one per project** (record it in `CLAUDE.md` § Plan):

- **Mode A, tests given.** The architect, or Claude in a separate reviewed session,
  writes the acceptance tests in the plan phase. They ship with the milestone as the
  answer key. This is the most reliable; use it for safety-relevant logic.
- **Mode B, criteria given.** The SPEC's acceptance criteria are the contract. Claude
  writes the tests first (`/write-tests`), a human approves them (**gate**), then Claude
  writes the code. It's faster for the architect, but approving the tests is a real
  review, not a formality.

## Step 7. CLAUDE.md

**File:** `CLAUDE.md` (fill every `{{FILL}}`)

- [ ] **Context:** the business, the decisions already made (link the ADRs), the sources
      of truth, and where a milestone is specified.
- [ ] **Scope:** in scope, out of scope ("don't add them"), and "per milestone, only what
      SPEC.md lists".
- [ ] **Plan:** the build loop, and which test mode (A or B) this project uses.
- [ ] **Commands:** install, lint, test, run, eval. All offline, with no API key.
- [ ] **Rules:** the invariants from step 2, as numbered imperatives.
- [ ] **Don't touch without being asked:** tests (in Mode A), evals, thresholds,
      reference data, golden answers.
- [ ] **Code map** and **Skills and commands** tables.
- [ ] **Clarifications** and **Learnings from PRs:** start them empty, with the format
      line. They fill up during the build.

## Step 8. Prompts, skills and commands

- [ ] **`milestones/NN-*/PROMPTS.md`:** for each milestone, start with
      `/start-milestone` and `/plan-milestone`. Then a scaffold step, then one
      XML-tagged prompt per module (`<task> <spec> <tests> <constraints> <done_when>`),
      then `/verify`, `/review` and `/learn`. Put modules in an order where each step's
      tests can pass without later steps' code.
- [ ] **Use-case skills:** one for each change you expect to repeat (add a rule, add a
      tool, add a golden case, add a node). Copy
      `.claude/skills/_use-case-skill-template/`. Each names the files to touch, the
      decisions to ask about, the tests and the doc row.
- [ ] **Commands:** edit only `/verify`'s check list. Add a project command only for a
      prompt you'd otherwise retype (for example, explaining one decision from its audit
      trail).
- [ ] **Process skills:** keep them as they are. They are generic on purpose. Choose how
      they arrive (`new_project.py --kit`):
  - **vendored**, copied into `.claude/`, which works offline, in headless runs and in
    untrusted folders;
  - **plugin**, `spec-driven-build@fde-project-kit`, enabled in `.claude/settings.json`,
    so every project shares one maintained copy and its commands are namespaced
    `/spec-driven-build:<name>`.

## Step 8b. MCP servers and other plugins

**Files:** `.mcp.json`, `CLAUDE.md` § MCP servers and plugins

There are two different questions here, so keep them apart:

- **Build time: what may Claude Code reach while it builds?** List each MCP server in
  `.mcp.json` (start from `.mcp.example.json`). Pass secrets as `${VAR}`, never as
  literals. In `CLAUDE.md`, give one row per server: what to use it for, and what it must
  never be used for (e.g. GitHub: read issues and PRs; never push or merge). If you need
  none, leave `.mcp.json` empty and say "none". Project servers ask for approval the
  first time. `claude -p` runs load them without asking, so list only servers you trust
  unattended. Block a server everywhere with `disabledMcpjsonServers`.
- **Runtime: what tools does the system's own agent call?** They are part of the
  architecture, not of Claude Code's setup. Put them behind the system's tool boundary
  (pattern P10), with versioned contracts, scopes and audit, whether they are local
  functions or MCP servers. Say in `ARCHITECTURE.md` whether runtime MCP is in scope.
- [ ] **Other plugins:** list any team plugin the project relies on (e.g. a deploy or
      review plugin) in `.claude/settings.json` (`enabledPlugins`, plus
      `extraKnownMarketplaces` for a private marketplace), and say in `CLAUDE.md` what
      each is for.

## Step 9. Seed and readiness

- [ ] The seed is in place: package layout, `pyproject.toml`, domain types if they are
      architect-owned, fixtures and reference data, a mock for every external dependency
      (model, tools), and an offline test run that collects.
- [ ] `python3 scripts/check_ready.py <project>` passes. That means no `{{FILL}}` is left,
      every required section exists, and every milestone has a SPEC with a Public API
      and acceptance criteria.
- [ ] Optional dry run: ask a fresh Claude session to read everything and list the
      questions it would still need answered. Every question is a spec gap. Fix it, or
      answer it under Clarifications.

---

## Then the build phase: the human gates

| Gate | When | What the human checks |
|---|---|---|
| G1 Plan | After `/plan-milestone` | The order, the tests per step, the failure modes named, nothing from a later milestone |
| G2 Tests (Mode B only) | After `/write-tests` | Every AC has a test; both sides of each threshold; the messages match the SPEC |
| G3 Review | After `/review` | Which findings to accept. Each accepted, reusable finding becomes a line under Learnings via `/learn` |
| G4 Merge | `/verify` green | The PR explains the decisions in the author's own words |

Between gates, Claude works alone: build a module, run its tests, repeat. When the spec
is unclear it stops and asks (`clarify-before-building`). If nobody can answer, it
records an assumption in the plan.
