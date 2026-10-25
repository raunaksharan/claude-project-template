---
name: plan-project
description: Use when a user brings a new project objective (a feature list and/or a description) and wants it turned into an approved build plan. Interviews the user section by section until every plan-phase file of claude-project-template is filled, proposes skills, MCP servers and plugins, writes PLAN.md, and stops for the user's approval. Never writes code.
---

# Plan a project with the user, then stop for approval

The user knows what they want to build better than any file does, but they haven't yet
decided most of what Claude needs to build it without guessing. Your job is to find those
decisions with them, write each one into the right file, and stop when the plan is
complete. **You write no code and no tests in this skill.**

Inputs: the user's objective, as a bullet list of features and/or a text document (a path
or pasted text). Output: every plan-phase file filled in, `PLAN.md` written with
`Status: DRAFT`, `check_ready.py` passing, and a stop.

## 0. Set up

- If the project has no `CLAUDE.md` with `{{FILL` markers, it wasn't created from the
  template. Ask for the project name, package and CLI name, then run
  `python3 <template>/scripts/new_project.py` (ask where the template is if you don't
  know).
- Read the objective in full. Read `QUESTIONS.md`, `CATALOG.md` and `PATTERNS.md` next to this file.
- Run `python3 <template>/scripts/check_ready.py .` to see every open field.

## 1. Fill what the objective already answers

Before asking anything, write into the files everything the objective states, worded as
the user worded it. For example, features become FR rows, and "for X users" becomes a
user row. Never ask a question the objective already answers.

## 2. Interview, section by section, in this order

1. requirements;
2. invariants and decisions (ADRs);
3. failure modes;
4. architecture;
5. milestone map;
6. each milestone's SPEC;
7. CLAUDE.md: scope, commands, style;
8. tooling (skills, MCP servers, plugins).

`QUESTIONS.md` lists what to ask for each section.

- **Ask 1–4 related questions at a time** (with AskUserQuestion when you have it), each
  saying what the answer changes. Put your recommended option first.
- **After each answer,** write it into the file at once, then move on. Show the user the
  section you just filled in a few lines, so they can correct it early.
- **When the user doesn't know** ("not sure", "you decide", "whatever is standard"):
  offer 2–3 concrete options with the trade-off of each and your recommendation. Draw
  them from `PATTERNS.md` (next to this file) and `QUESTIONS.md`. Record the choice in
  PLAN.md › Decisions as "chosen from options". If it shapes the architecture, it also
  gets an ADR. Never fill a field silently with your own default.
- **When the user is away or says "fill the rest yourself":** fill each open field with
  your recommended option, and list every one under PLAN.md › Assumptions still open.
  Those are what the user must look at before approving.
- **Precision for specs** (PLAN-PHASE.md step 6) is where you add the most value. Ask
  about:
  - the order of checks;
  - `>` against `>=`, and units;
  - missing, empty and malformed input;
  - the exact messages;
  - id formats;
  - rounding;
  - the clock.

  Write acceptance criteria with concrete values, and read them back to the user.

## 3. Propose tooling

From `CATALOG.md`, propose what fits this project:

- the process-skill delivery (vendored or plugin);
- a use-case skill for each change the user expects to repeat;
- MCP servers for build time, each with a "use it for" and a "never use it for";
- any plugins.

Ask what they already use and include it. Write the choices into `CLAUDE.md` › Skills and
commands, › MCP servers and plugins, `.mcp.json` and `.claude/settings.json`. Create each
use-case skill from `_use-case-skill-template`.

## 4. Write PLAN.md and say so

When `check_ready.py` passes:

1. Fill `PLAN.md` from the files: goal, scope, milestones, decisions (with who chose),
   assumptions still open, how it will be built, and the gates. Keep the status `DRAFT`.
2. Say, in these words or close to them: **"Okay, I'm good. This is the plan."** Then give
   a short summary: the milestones, the decisions you want them to look at hardest, and
   the open assumptions.
3. Tell them how to change it: edit any file or ask you. Tell them how to approve it:
   type `! python3 scripts/approve_plan.py --by "<name>"` in Claude Code. Then **stop**.

## 5. While waiting

- If the user asks for changes, make them, re-run `check_ready.py`, update PLAN.md, and
  stop again.
- If the user says "approved" or "go ahead" in chat, remind them that approval is the
  `! python3 scripts/approve_plan.py` command, run by them. The hook checks that, not the
  chat.
- Don't start `/build-project` until `.claude/plan-approval.json` exists. The plan-gate
  hook blocks writes to `src/` and `tests/` before that anyway.

<rules>
- Never approve the plan yourself, never write `.claude/plan-approval.json`, and never run
  `approve_plan.py`.
- No code and no tests during planning; the hook will stop you if you try.
- Every decision has an owner: "user stated" or "user chose from options". A field you
  filled without asking is listed as an open assumption.
- Thresholds, expected outcomes and what counts as a failure come from the user, never
  from you.
</rules>
