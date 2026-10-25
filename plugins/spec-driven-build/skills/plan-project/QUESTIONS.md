# The interview: what to ask, section by section

For each field: the question, and the options to offer when the user doesn't know. Skip
anything the objective already answers. Ask 1–4 at a time, and write each answer into its
file straight away.

## 1. Requirements → `architecture/requirements.md`

- What does the work look like today, step by step? Where does the time go, and where do
  errors come from?
- Who uses it, and what does each of them need from it?
- What counts as success, as a number? Options: time per case; error rate; throughput;
  cost per case.
- Non-functional targets: latency, availability, cost per unit, privacy, audit,
  residency. Don't know? Options: "offline prototype: no targets beyond determinism and
  audit" (recommended for a first build), or concrete numbers marked [A].

## 2. Invariants and decisions → `ARCHITECTURE.md` § 2, `architecture/adr/`

- Which steps must be exact and reproducible (code), and which need judgement or
  unstructured input (model)? (P1)
- Who makes the final decision: the model, rules, or a human? Options: the model proposes
  and rules decide (P2, recommended where a decision has consequences); the model
  decides and a human reviews; the model decides.
- What happens when data is missing or conflicting? Options: escalate to a human with a
  reason code (P3, recommended); reject; proceed with a flag.
- Which actions change another system (writes)? Do they need approval? Options:
  approval plus re-authorization (P8, recommended); approval only; automatic below a
  threshold.
- Is there anything the model must never touch? (e.g. control loops, money movement,
  thresholds)

## 3. Failure modes → `architecture/failure-modes.md`

For each external dependency and each AI component: what happens when it returns
nothing, returns garbage, or never returns? Propose the default response from the
patterns (typed status → escalate or degrade), and ask only where the business answer
isn't obvious (required or optional?).

## 4. Architecture → `ARCHITECTURE.md`

- The components, and the kind of each (confirm your proposal).
- The trust layers between the model and an action (propose P6, P7, P9, P10 as fits).
- Control flow: which steps escalate, which degrade, which fall back? (P12)
- Do runs need to survive restarts or wait for humans? Options: durable runs (P13); a
  single process, in memory (recommended for a first build).
- Evaluation: the golden cases (who writes the expected answers?), the invariants and the
  gates. (P15)
- Deployment view: in scope or not? Options: one process, everything in memory
  (recommended first); containers; the cloud.
- Out of scope: say it plainly. Offer the usual list (UI, auth, multi-region, billing,
  real providers) for the user to tick.

## 5. Milestone map → `milestones/README.md`

Propose 4–8 milestones, bottom-up (domain and deterministic core first, then AI pieces,
orchestration, evaluation and operations), each with its acceptance command. Ask the
user to reorder, merge or cut. Ask what is the seed (given) and what is built.

## 6. Each milestone's SPEC → `milestones/NN-*/SPEC.md`

For each module, propose the public API, then ask only where it changes behaviour:

- thresholds: the value, the unit, `>` or `>=`, and what a value exactly on the line does;
- the order of checks, when several can fire;
- missing, empty and malformed input: exactly what happens;
- the exact messages that tests, repair turns or humans read;
- id formats, key order, rounding, regexes, the clock and randomness.

Then write the acceptance criteria with concrete values, both sides of each threshold,
and read them back.

Test mode: Mode A (the tests are written now, in planning, and reviewed) or Mode B
(Claude writes them first, per milestone, and the user approves them). Recommend B for
speed, A for safety-relevant logic.

## 7. CLAUDE.md

Language and libraries, the commands (install, lint, test, run, eval), the style, and
what never to touch without being asked (thresholds, reference data, golden answers).

## 8. Tooling

See `CATALOG.md`.
