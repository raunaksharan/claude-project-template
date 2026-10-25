# Worked example: agentic-credit-underwriter

The template was abstracted from this project (private repo
`raunaksharan/agentic-credit-underwriter`). It's an FDE Academy course: an agentic credit
underwriting platform for a fictional lender, built over six "lessons" (milestones). The
lessons were rebuilt by headless Claude Code from the plan-phase files alone (lessons
1–6, all tests green, eval 32/32).

The course uses "lesson" where the template says "milestone", and `course/kit/` where
the template says `kit/`.

| Template file | Filled version in the underwriter | Notes |
|---|---|---|
| `ARCHITECTURE.md` | `ARCHITECTURE.md` | The 14 sections, filled |
| `architecture/requirements.md` | `architecture/requirements.md` | Observed workflow, users, NFRs |
| `architecture/failure-modes.md` | `architecture/failure-modes.md` | F1–F17, each with an injected test |
| `architecture/adr/0000-template.md` | `architecture/adr/0001…0003` | Hybrid AI; agent proposes, engine decides; escalate, never guess |
| `CLAUDE.md` | `CLAUDE.md` | 7 rules, 7 clarifications, 6 learnings from PRs |
| `milestones/README.md` | `lessons/README.md` | The course map and starter table |
| `milestones/NN/SPEC.md` | `lessons/0N-*/SPEC.md` | Narrative behaviour, exact messages, generated Public API. Written in **Mode A**, so tests ship with the lesson and there's no AC table: the tests are the ACs |
| `milestones/NN/PROMPTS.md` | `lessons/0N-*/PROMPTS.md` | Clarify and plan, scaffold, one XML prompt per module, verify, review, learn |
| `.claude/skills/` process skills | `.claude/skills/{clarify-before-building,write-plan,tdd-module,debug-root-cause,verify-before-done,review-and-learn,karpathy-guidelines}` | The same skills, with lending-specific examples |
| `_use-case-skill-template` | `add-policy-rule`, `add-tool-check`, `add-golden-case`, `add-sample-application`, `add-regulatory-document`, `add-retrieval-case`, `new-prompt-version`, `add-workflow-node`, `investigate-decision` | Nine use-case skills |
| `.claude/commands/` | `start-lesson`, `plan-lesson`, `build-module`, `clarify`, `verify`, `review`, `learn`, `catch-up`, plus `explain-decision`, `trace`, `eval-report` | Three project-specific commands |
| `workflows/` | `course/workflows/` | Plus course-only ones: mini track, slides |
| `kit/` | `course/kit/` (`lessons.json`, `make_kit.py`, `steps.json`, `check_steps.py`) | Starter branches `lesson-0N-start` |

## What the trials taught (now built into the template)

- **Spec gaps cluster in the same places.** Two rounds of rebuild trials found 33 gaps in
  lessons 1 and 3 alone. Nearly all were one of these:
  - the order of checks;
  - `>` against `>=`;
  - missing-input behaviour;
  - the exact wording of a message;
  - key order and id formats;
  - regexes;
  - the clock;
  - rounding.

  These are now the checklist in PLAN-PHASE.md step 6.
- **Scaffold before building.** Test files import names from several modules, so until
  every name exists each file errors at import. A scaffold step (stubs that raise
  `NotImplementedError`; constructors store their arguments) makes each test fail on its
  own.
- **Generated Public API.** Exact signatures generated from code (`make_kit.py spec`)
  removed a whole class of name and signature mismatches.
- **Unattended runs need a fallback for questions.** `/plan-lesson` was changed so that,
  with nobody to ask, it writes assumptions into the plan instead of stalling.
