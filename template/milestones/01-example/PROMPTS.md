# Milestone {{FILL: NN}} prompt pack: build {{FILL: title}} with Claude Code

You build {{FILL: N}} modules from `SPEC.md`. {{FILL: what is given}}.

```bash
{{FILL: install}}
{{FILL: test}} --continue-on-collection-errors     # red: {{FILL: what is red and why}}
claude
```

```text
/start-milestone {{FILL: NN}}
```

## 1. Clarify and plan ({{FILL: min}})

```text
/plan-milestone {{FILL: NN}}
```

{{FILL: what a good plan for this milestone looks like, and the plan to reject (e.g. "starts with the loop before its validators").}}

## 2. Tests first (Mode B only)

```text
/write-tests {{FILL: NN}}
```

Check that every AC in SPEC.md has a test, and both sides of each threshold. Approve, or ask for changes, before any code is written.

## 3. Scaffold the interfaces (5 min)

Test files import names from several modules at the top. Until every name exists, each file errors at import. The scaffold makes each test fail on its own:

```text
<task>Scaffold the public API of milestone {{FILL: NN}}'s modules</task>
<spec>milestones/{{FILL: NN-slug}}/SPEC.md, every "Public API" list</spec>
<method>In each module, keep the module docstring and add every public name with its
exact signature and docstring, and a body of `raise NotImplementedError`. Constants get
their values; classes get their fields and method stubs; constructors (`__init__`) just
store their arguments.</method>
<tests>{{FILL: test}} --continue-on-collection-errors</tests>
<done_when>The tests fail one by one (NotImplementedError) rather than at import, and
lint is clean. No logic yet.</done_when>
```

## 4. {{FILL: first module}} ({{FILL: min}})

```text
<task>Build {{FILL: src/{{PACKAGE}}/x.py}}: {{FILL: the public names}}</task>
<spec>milestones/{{FILL: NN-slug}}/SPEC.md, section "{{FILL}}"</spec>
<tests>{{FILL: the narrowest test command, e.g. -k "name"}}</tests>
<constraints>{{FILL: the two or three rules most likely to be broken here}}</constraints>
<done_when>Those tests pass and lint is clean.</done_when>
```

{{FILL: one "ask Claude why…" prompt that makes the human check understanding.}}

## 5. {{FILL: next module}}

{{FILL: repeat the block; put modules in an order where each step's tests can pass without later steps' code. The last step runs the whole suite.}}

## 6. Verify, review, learn

```text
/verify
/review
/learn <anything worth keeping>
```

## Done when

- {{FILL: the acceptance command}} is green.
- {{FILL: the explanation the PR must contain, in the author's own words}}

## Don't delegate

{{FILL: the decisions the human owns in this milestone: thresholds, which steps escalate, golden answers.}}
