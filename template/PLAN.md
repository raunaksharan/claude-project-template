# PLAN.md: {{PROJECT}}

**Status:** DRAFT
<!-- Claude writes this page at the end of /plan-project and sets nothing below.
     Approval is a human act: review this page and the files it links, change anything,
     then run in Claude Code:  ! python3 scripts/approve_plan.py --by "<your name>"
     Until then a hook blocks every write to the build paths (src/, tests/). -->

## Goal

{{FILL: one paragraph: what is being built, for whom, and what success looks like (from architecture/requirements.md)}}

## Scope

- **In:** {{FILL: the features, as the bullet list the plan settled on}}
- **Out:** {{FILL: what will not be built}}

## Milestones

| # | Milestone | Builds | Acceptance command |
|---|---|---|---|
| 01 | {{FILL}} | {{FILL}} | {{FILL}} |

## Decisions taken in planning

One line per decision, and who made it: the user stated it, or chose it from options.

| Decision | Chosen | Alternatives offered | Recorded in |
|---|---|---|---|
| {{FILL}} | {{FILL}} | {{FILL: or "user stated"}} | {{FILL: ADR, SPEC §, CLAUDE.md}} |

## Assumptions still open

{{FILL: anything the user deferred, with the default Claude will use. Or "none".}}

## How it will be built

- **Test mode:** {{FILL: Mode A (tests given) or Mode B (Claude writes tests first; you approve them)}}
- **Process skills and commands:** {{FILL: vendored, or the spec-driven-build plugin}}
- **Use-case skills:** {{FILL: names}}
- **MCP servers while building:** {{FILL: names and their limits, or "none"}}
- **Other plugins:** {{FILL: names, or "none"}}
- **Gates where Claude stops for you:** the plan (this page), each milestone's plan
  (G1), {{FILL: tests in Mode B (G2),}} review findings (G3), merge (G4).

## Files this plan fixes

`ARCHITECTURE.md`, `architecture/`, `CLAUDE.md`, `milestones/*/SPEC.md` and `PROMPTS.md`,
`.claude/`, `.mcp.json`. The approval records a hash of this page. If it changes, it
must be approved again.
