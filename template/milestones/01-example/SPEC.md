# Milestone {{FILL: NN}} spec: {{FILL: title}}

<!-- PLAN-PHASE.md step 6. Precision is the point: every item below that is missing
     becomes a guess. Copy this folder to milestones/NN-<slug>/ for each milestone. -->

**You build:** {{FILL: the modules, one per line, with their paths}}

**Given (the seed):** {{FILL: what already exists: types, data, mocks, wiring, and (Mode A) tests}}

**Acceptance command:** `{{FILL: e.g. uv run pytest tests/test_x.py && uv run {{CLI}} eval}}`

**Failure modes closed:** {{FILL: F-numbers from architecture/failure-modes.md}}

## `{{FILL: src/{{PACKAGE}}/module.py}}`: {{FILL: what it is for, one line}}

**Constants:** {{FILL: name = value, with the unit and why}}

**Public API:**

- `{{FILL: ClassName}}` (pydantic / dataclass, frozen?):
  - `{{FILL: field}}: {{FILL: type}} = {{FILL: default}}`
- `{{FILL: function(arg: Type, ...) -> Return}}`: {{FILL: one line}}

Imported elsewhere (keep these names exactly): {{FILL}}. Builds on: {{FILL}}.

**Behaviour** (one bullet per rule, in the order the checks run):

- {{FILL: rule. Comparison (> or >=), unit, tolerance, and what a value exactly on the line does.}}
- {{FILL: missing, empty or malformed input → exactly what happens (status, reason code, message). Never "handle gracefully".}}
- {{FILL: rounding, ordering, id formats, regexes, the clock (injected), randomness (seeded).}}

**Exact messages** (format strings; tests and repair turns read them):

| When | Message |
|---|---|
| {{FILL}} | `"{{FILL: text with {placeholders}}}"` |

**Acceptance criteria** (each becomes at least one test; cover both sides of every threshold):

| # | Given | When | Then |
|---|---|---|---|
| AC-{{FILL: NN}}.1 | {{FILL: concrete values}} | {{FILL: call}} | {{FILL: exact result}} |

## Changes to earlier modules

{{FILL: or "None." For each change, name any earlier SPEC rule or acceptance criterion it alters (e.g. "milestone 03 said the runner reads the clock only at start; it now also reads it at each checkpoint"), so earlier tests are updated on purpose, not broken by surprise.}}
