# ARCHITECTURE.md: {{PROJECT}}

The one-page architecture of {{PROJECT}}. Read it after `CLAUDE.md`. The detail lives in
[`architecture/`](architecture/): requirements, ADRs and failure modes. This page ties
them together and links to them rather than repeating them.

<!-- How to fill this in: PLAN-PHASE.md steps 2–4 in claude-project-template.
     Worked example: agentic-credit-underwriter/ARCHITECTURE.md.
     Patterns to pick from: patterns/agentic-patterns.md (P1–P19). -->

## 1. Problem and outcome

{{FILL: two or three sentences on the business problem and today's cost. Then the outcome, in one sentence a stakeholder would sign. Link architecture/requirements.md.}}

| Who | What they need from the system |
|---|---|
| {{FILL: user or stakeholder}} | {{FILL: need}} |

## 2. Non-negotiables (the invariants)

Each invariant is enforced in code and checked by a test or an eval invariant, never left
to the prompt. They are the Rules in `CLAUDE.md`.

| # | Invariant | Enforced by | Checked by | ADR / pattern |
|---|---|---|---|---|
| I1 | {{FILL: e.g. the model proposes; code decides}} | {{FILL: module}} | {{FILL: test or eval invariant}} | {{FILL: ADR-0001 / P2}} |

## 3. System view

```mermaid
flowchart LR
    {{FILL: the request path, one node per component, labelled AI / deterministic / tool / human}}
```

{{FILL: one paragraph saying which module implements the flow and which owns the components.}}

**Deployment view** (only if it differs from the code view): {{FILL: or "Same process; out of scope."}}

## 4. Components: where AI earns its place

| Component | Kind | Module | Why this kind |
|---|---|---|---|
| {{FILL}} | {{FILL: AI / deterministic / tool / human}} | {{FILL: path}} | {{FILL: reason}} |

## 5. The trust model

The layers between model output and a consequential action:

1. **Input:** {{FILL: what the model may and may not see; ids it must cite (P6)}}
2. **Output:** {{FILL: schema plus semantic checks, repair once, fallback (P7)}}
3. **Action:** {{FILL: allow-list, gateway, budgets (P9, P10)}}
4. **Decision:** {{FILL: who decides; when a human must approve (P2, P8)}}

## 6. Boundaries and contracts

| Boundary | Contract (type) | Failure shape |
|---|---|---|
| {{FILL}} | {{FILL}} | {{FILL: status values or exception, never None}} |

**Dependency direction** (imports point down only):

```text
{{FILL: package layering, e.g.
cli, evaluation
  └── runtime
        └── agents ── llm
        └── tools, rules
              └── domain}}
```

## 7. Control flow and resilience

| Step | Timeout | Attempts | On failure | Why |
|---|---|---|---|---|
| {{FILL}} | {{FILL}} | {{FILL}} | {{FILL: escalate / degrade / fallback}} | {{FILL}} |

{{FILL: what is retried (only transient), how a run pauses for a human and resumes, where state is checkpointed.}}

## 8. Failure model

Failure modes F1–Fn, each with a designed response and an injected test:
[failure-modes.md](architecture/failure-modes.md). Faults are injected with
{{FILL: the CLI flags or env vars}} and refused when `APP_ENV=production`.

## 9. Data and sources of truth

| Truth | Where | Who may change it |
|---|---|---|
| {{FILL: thresholds / reference data / expected outcomes}} | {{FILL: path}} | {{FILL: owner; never tuning}} |

## 10. Evaluation and release gates

- **Expectations** per golden case: {{FILL: outcome, reason codes, trajectory}}
- **Invariants** on every case: {{FILL}}
- **Gates** on the run: {{FILL: pass rate, zero unsafe outcomes, p95 latency, tokens, baseline}}

A change ships only when {{FILL: the /verify checks}} are green.

## 11. Observability

{{FILL: one trace per unit of work: the span tree, the attributes, what is redacted, where it goes in production.}}

## 12. Out of scope

{{FILL: say it plainly. Claude adds whatever isn't forbidden. E.g. UI, multi-region, billing.}}

## 13. Decisions

| ADR | Decision |
|---|---|
| [0001](architecture/adr/0001-{{FILL: slug}}.md) | {{FILL}} |

## 14. How this repo is built

Spec-driven, milestone by milestone, with Claude Code ([claude-project-template](https://github.com/)):

| File | Role |
|---|---|
| `CLAUDE.md` | Context, scope, plan, rules, clarifications, learnings from PRs |
| `ARCHITECTURE.md` + `architecture/` | This page, requirements, ADRs, failure modes |
| `milestones/NN-*/SPEC.md` | What to build: public API, behaviour, exact messages, acceptance criteria |
| `milestones/NN-*/PROMPTS.md` | How to build it with Claude, one module per step |
| `.claude/` | Process skills, use-case skills, commands, the lint hook |
| `workflows/` | The same procedures written for people |
