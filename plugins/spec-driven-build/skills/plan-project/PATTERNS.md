# Agentic system patterns: a catalogue to choose from

These are the patterns behind `agentic-credit-underwriter`, plus the ones a production
agent platform needs (from an Agent Factory platform design). In the plan phase, pick the
ones that fit your project. Name them in `ARCHITECTURE.md` and the ADRs, and turn each
one you adopt into an invariant with a test.

Each entry gives the problem, the pattern, how to test it, when not to use it, and where
the worked example uses it (`underwriter:` paths are in agentic-credit-underwriter).

| # | Pattern | Use it when |
|---|---|---|
| P1 | AI only where it earns its place | Always |
| P2 | The model proposes; code decides | Any consequential decision |
| P3 | Escalate, never guess | Data can be missing or conflicting |
| P4 | Typed results at every boundary | Any external call |
| P5 | Provider port plus a deterministic mock with faults | Any LLM use |
| P6 | Minimised, citable context | A model sees facts about people or systems |
| P7 | Validate, repair once, fail safe | A model's output is used by code |
| P8 | Human approval, re-authorized at execution | Writes or irreversible actions |
| P9 | Bounded agent loop | The model chooses tools |
| P10 | Tool gateway and versioned tool contracts | More than a handful of tools, or any write tool |
| P11 | Fault injection as a feature | Always |
| P12 | Per-step failure policy | A multi-step workflow |
| P13 | Durable execution | Runs outlive a process, or wait for humans |
| P14 | Append-only audit | Regulated or safety-relevant domains |
| P15 | Three-layer evals, plus trajectory | Always, before the first release |
| P16 | Immutable versions, an eval gate and a canary | More than one version will ever run |
| P17 | One trace per unit of work | Always |
| P18 | Hybrid retrieval with citations | The model needs long reference text |
| P19 | Tenant in every key | More than one customer |

---

### P1. AI only where it earns its place

- **Problem:** Models are flexible and occasionally confidently wrong. Arithmetic,
  thresholds and lookups have exact answers.
- **Pattern:** Classify each component as AI, deterministic, tool or human, and write
  down why. Use a model only for unstructured input, or for judgement and explanation.
- **Test:** The components table in `ARCHITECTURE.md`. No arithmetic sits in a prompt.
- **Not when:** Never skip it.
- **Example:** underwriter ADR-0001; `risk/calculations.py` is code, and the agent
  explains.

### P2. The model proposes; code decides

- **Problem:** Prompt quality shouldn't decide compliance.
- **Pattern:** The model writes a typed proposal. A deterministic engine applies the
  rules and produces the decision. The model may escalate; it may never relax a rule.
  Record every override (`overridden_by_policy`); a rising override rate is drift.
- **Test:** Write an override matrix (rule outcome × model outcome → final). Add eval
  invariants such as `UNSAFE_APPROVAL` and `UNFAIR_DECLINE`.
- **Not when:** Low-stakes, reversible output (drafting text a human edits anyway).
- **Example:** underwriter ADR-0002, `decision/engine.py`.

### P3. Escalate, never guess

- **Problem:** A missing value silently defaulted to 0 becomes a wrong decision.
- **Pattern:** Missing or conflicting data becomes a reason code and the escalation
  outcome (MANUAL_REVIEW, NEEDS_REVIEW). No defaults for facts. Every decision cites at
  least one reason code.
- **Test:** One case per missing input; the eval invariant "decision has reason codes".
- **Example:** underwriter ADR-0003; APP-003 (no bureau record), APP-007 (no payslip).

### P4. Typed results at every boundary

- **Problem:** `None` and bare exceptions get interpreted differently by every caller.
- **Pattern:** Every external call returns a result with a status (`OK`, `UNAVAILABLE`,
  `INVALID`), a reason and data. A malformed answer is `INVALID`, never `OK`. Callers
  branch on status, not on whether the data happens to be there.
- **Test:** For each tool and each fault kind, the expected status.
- **Example:** underwriter `CheckResult`, `tools/checks.py`.

### P5. Provider port plus a deterministic mock with faults

- **Problem:** Tests that need an API key don't run in CI, and real models aren't
  repeatable.
- **Pattern:** An `LLMClient` port. Nothing outside `llm/` imports a model SDK. A mock
  model reads only the structured block of the prompt and answers deterministically. It
  takes named faults (`malformed`, `wrong_number`, `bad_citation`, `unavailable`, `loop`,
  `disallowed_tool`, each with an `_always` variant).
- **Test:** The whole suite runs offline.
- **Example:** underwriter `llm/client.py`, `llm/mock.py`.

### P6. Minimised, citable context

- **Problem:** Personal data leaks to vendors, and the model cites things that don't
  exist.
- **Pattern:** Build the context in code. Leave out personal data. Give every fact an id
  (`signal:CODE`, `metric:name`, `doc:path`, `policy#chunk`) and an allowed-ids map.
  Under a budget, cut the least important content first (reference excerpts), never the
  facts.
- **Test:** A PII scan over every sample's prompt; budget tests.
- **Example:** underwriter `agents/context.py`.

### P7. Validate, repair once, fail safe

- **Problem:** Output that parses can still be wrong.
- **Pattern:**
  1. Check the schema (`extra="forbid"`).
  2. Run semantic checks: cited ids exist, numbers match the facts within a stated
     tolerance, recommendation and evidence are consistent.
  3. Send the exact errors back in one repair turn.
  4. If it's still invalid, fall back to the escalation outcome with
     `INVALID_MODEL_OUTPUT`.

  Don't retry a provider outage.
- **Test:** One fault per check, and the repaired path.
- **Example:** underwriter `agents/validation.py`, `agents/underwriting.py`.

### P8. Human approval, re-authorized at execution

- **Problem:** An agent acting on a write, or permissions changing between proposal and
  approval.
- **Pattern:** Classify each tool as READ or WRITE. A WRITE parks the run (`interrupt()`,
  or the `WAITING_APPROVAL` status) without holding a worker. On approval, check the
  approver's permission again, then execute with an idempotency key. Validate the human
  decision (reviewer, decision, note) and append it to the audit.
- **Test:** An approve path, a reject path, and permission revoked between proposal and
  approval.
- **Example:** underwriter `workflow/graph.py` `human_review`; Agent Factory approvals.

### P9. Bounded agent loop

- **Problem:** Loops, runaway cost, calls to tools the agent shouldn't have.
- **Pattern:**
  - an allow-list of tools, where a refused call becomes a tool result, not an exception;
  - a cap on tool calls, a token budget, and a deadline read from an injected clock;
  - detection of repeated identical calls.

  Hitting any limit gives the escalation outcome with `AGENT_LIMIT_REACHED`. Default to a
  fixed workflow, and add a loop only where the task really branches.
- **Test:** The `loop` and `disallowed_tool` faults; a fake clock for the deadline.
- **Example:** underwriter `agents/tool_agent.py`, `agents/tools.py`.

### P10. Tool gateway and versioned tool contracts

- **Problem:** With many tools, each one becomes its own security and reliability
  surface.
- **Pattern:** A tool is a versioned contract: input and output schemas, side-effect
  class, required scopes, timeout, rate limit, owner. Agent versions pin
  `tool@version`. One gateway is the only path to a tool. It:
  - validates arguments against the schema (and rejects them, never fixes them);
  - checks that the tenant enabled the tool and the user's scopes cover it;
  - calls the tool on behalf of the user, with no god-mode account;
  - removes fields the user may not see;
  - rate-limits per tenant;
  - writes the audit record.

  Treat tool output as untrusted data.
- **Test:** One test per rejection reason; a test that a scope can't widen from model
  output.
- **Example:** the pilot `adas-agent-factory`, milestone 2.

### P11. Fault injection as a feature

- **Problem:** Failure handling that has never run doesn't work.
- **Pattern:** Every external dependency, and every workflow step, takes named faults
  (`timeout`, `rate_limit`, `server_error`, `malformed`, `latency:<ms>`; `error`,
  `transient`, `hang`) from a CLI flag or an environment variable. Faults are refused
  when `APP_ENV=production`.
- **Test:** Each failure mode in `failure-modes.md` has an injected test or golden case.
- **Example:** underwriter `tools/faults.py`, `workflow/resilience.py`.

### P12. Per-step failure policy

- **Problem:** "Retry everything" hides bugs, and "fail everything" wastes good work.
- **Pattern:** Each step has a timeout, a number of attempts, and a meaning for failure:
  - **escalate:** the step is required, so a human decides;
  - **degrade:** carry on without it, and record that;
  - **fallback:** use a safe default proposal.

  Retry only timeouts and transient errors. A bug fails on its first attempt.
- **Test:** One injected fault per policy kind.
- **Example:** underwriter `NODE_POLICIES` in `workflow/graph.py`.

### P13. Durable execution

- **Problem:** Runs that outlive a process: pod restarts, deploys, approvals that take
  days.
- **Pattern:**
  - a checkpoint after every step, keyed `(run_id, step_no)`;
  - a worker that holds a lease with a heartbeat, so an expired lease means another
    worker resumes from the last checkpoint;
  - at-least-once steps, so every side effect carries the idempotency key
    `run_id:step_no` and the downstream side honours it;
  - a cancel flag checked between steps;
  - in-flight runs pinned to the version they started on.
- **Test:** A crash between steps resumes without repeating a write; an expired lease is
  taken over; a cancel stops the run.
- **Example:** the pilot, milestone 3. The underwriter uses LangGraph's checkpointer for
  human review.

### P14. Append-only audit

- **Problem:** Nobody can reproduce why something was decided.
- **Pattern:** Every step that runs, retries, degrades or fails appends an event:
  `(step, actor, summary, data)`. Nodes return only their new events, and state merges
  the lists rather than replacing them.
- **Test:** Each trail starts at intake; a degraded step leaves a failure event.
- **Example:** underwriter `AuditEvent`, `operator.add` on graph state.

### P15. Three-layer evals, plus trajectory

- **Problem:** Unit tests pass while overall quality drifts.
- **Pattern:**
  - **expectations** per golden case: the outcome, the reason codes, and for agents the
    expected **trajectory** (the tools, their arguments, their order);
  - **invariants** on every case;
  - **gates** on the run: the pass rate, zero unsafe outcomes, p95 latency, mean tokens,
    and growth against a baseline.

  Golden answers come from the rules, never from running the system.
- **Test:** A mutation drill: change one threshold and watch the eval fail.
- **Example:** underwriter `evaluation/harness.py`, `evals/`.

### P16. Immutable versions, an eval gate and a canary

- **Problem:** Shipping a prompt or a model change blind.
- **Pattern:**
  1. An agent version (prompt, model policy, tool pins, budgets) is immutable.
  2. It must pass the eval gate before it can deploy.
  3. A canary routes a cohort to it and compares task success, escalation rate, tool
     error rate, latency and cost against the stable version.
  4. Rollback is a pointer flip.
- **Test:** A regression blocks promotion; a canary breach rolls back; in-flight runs stay
  on their version.
- **Example:** the pilot, milestone 4.

### P17. One trace per unit of work

- **Problem:** Nobody can say why a run was slow or expensive.
- **Pattern:** One root span per run, with child spans for steps, model calls and tool
  calls. Spans carry GenAI token attributes, cost and retries. Free text is redacted.
  Use-metering goes on every result. In production, send the spans into the observability
  platform that already exists.
- **Test:** A span tree test, and a PII test over every span.
- **Example:** underwriter `observability/`, `llm/instrumented.py`.

### P18. Hybrid retrieval with citations

- **Problem:** Long reference text, and answers that need sources.
- **Pattern:** Parse, chunk on structure, then retrieve with BM25 plus vectors, fused
  with RRF. Apply filters (tenant, ACL, in-force date) before ranking. Return citations,
  or abstain. Give retrieval its own eval.
- **Example:** underwriter `rag/`.

### P19. Tenant in every key

- **Problem:** Cross-tenant leaks and noisy neighbours.
- **Pattern:** Put `tenant_id` on every request, row, cache key, queue partition and span.
  Rate-limit and fair-queue per tenant. Use per-tenant encryption keys for stored state.
- **Test:** A cross-tenant read is refused; one tenant's burst doesn't starve another.
