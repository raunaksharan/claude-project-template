# claude-project-template

A reusable kit for building an agentic AI system with Claude Code, spec first.

The architect fixes a small set of files in a **plan phase**:

- the architecture;
- `CLAUDE.md`;
- the milestone specs and prompts;
- any project-specific skills or commands.

From then on Claude builds milestone by milestone. A human reviews the plan, the tests
and the PR at fixed gates.

The method comes from [`agentic-credit-underwriter`](examples/credit-underwriter.md).
There, headless Claude Code rebuilt six milestones from these files alone, with every
test green and 32/32 on the eval.

## How a project goes

| # | Step | Who | What happens |
|---|---|---|---|
| 1 | **Objective** | User | The user brings the feature list and a short description of what they want to build and show |
| 2 | **Interview** | Claude, with the user | `/plan-project <objective>`: Claude fills what the objective already answers, then asks questions section by section (meta-prompting) until every template field is filled. It writes each answer into its file as it goes |
| 3 | **Unknowns** | Claude, with the user | For a field the user can't answer, Claude offers 2–3 concrete options with a recommendation and records the choice ("chosen from options") |
| 4 | **Tooling** | Claude, with the user | Claude proposes process skills, use-case skills, MCP servers and plugins that fit, and adds any the user names |
| 5 | **"Okay, I'm good. This is the plan."** | Claude | `check_ready.py` passes; Claude writes `PLAN.md` (status DRAFT), summarises it, lists the open assumptions, and **stops** |
| 6 | **Approval, then build** | User, then Claude | The user edits anything, then approves by typing `! python3 scripts/approve_plan.py --by "<name>"`. Until then a hook blocks every write to `src/` and `tests/`. After approval, `/build-project` builds milestone by milestone, with human gates at each plan, the tests (Mode B), the review and the merge |

After the build, the learning loop continues:

- accepted review findings become lines in `CLAUDE.md` › Learnings;
- answered questions become Clarifications;
- repeated procedures become use-case skills.

An architect who prefers to fill the files by hand can follow
[PLAN-PHASE.md](PLAN-PHASE.md) instead of step 2. Steps 5 and 6 are the same either way.

## Start a project

```bash
python3 scripts/new_project.py --name adas-copilot --package adas_copilot \
        --cli adas --dest ../adas-copilot
python3 scripts/check_ready.py ../adas-copilot     # lists every {{FILL: …}} still open
```

To use the process skills as a shared plugin instead of copies, add `--kit plugin`, or
install it by hand in any project:

```text
/plugin install spec-driven-build --marketplace raunaksharan/claude-project-template
```

`new_project.py` copies `template/` and fills in the project name, the package and the
CLI name. Everything else is a `{{FILL: what to write}}` marker for the architect.
`check_ready.py` fails until none are left and the required sections exist. That is the
definition of ready for handing the project to Claude.

## What's in here

| Path | What it is | Change per project? |
|---|---|---|
| [PLAN-PHASE.md](PLAN-PHASE.md) | The architect's checklist: what to fix, in what order, and why. `/plan-project` follows the same order | No, follow it |
| `template/PLAN.md` | The one-page plan the user approves | Written by `/plan-project` |
| `template/scripts/approve_plan.py`, `template/.claude/hooks/plan_gate.py` | The approval (run by the user with `!`) and the hook that blocks `src/` and `tests/` until it exists and matches `PLAN.md` | No |
| [PATTERNS.md](plugins/spec-driven-build/skills/plan-project/PATTERNS.md) | Architecture patterns to choose from (trust layers, typed results, fault injection, node failure policies, eval layers, and more) | No, pick from it |
| `template/ARCHITECTURE.md` | The one-page architecture, in 14 sections | **Yes**, fully |
| `template/architecture/` | Requirements, failure modes, ADR template | **Yes** |
| `template/CLAUDE.md` | Context, Scope, Plan, Commands, Rules, How to work, Don't touch, Code map, Skills, Clarifications, Learnings | **Yes**, all except How to work |
| `template/milestones/` | The milestone map, plus `SPEC.md` and an XML-tagged `PROMPTS.md` per milestone | **Yes** |
| [`plugins/spec-driven-build/`](plugins/spec-driven-build/README.md) | **A Claude Code plugin**: `plan-project` (the interview, with its question bank, tooling catalogue and pattern catalogue), the process skills (`karpathy-guidelines`, plus six adapted from obra/superpowers) and the commands (`/plan-project`, `/build-project`, `/start-milestone`, `/plan-milestone`, `/clarify`, `/write-tests`, `/build-module`, `/review`, `/learn`, `/catch-up`). `new_project.py --kit vendored` copies them in; `--kit plugin` enables the plugin instead | No |
| [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) | Makes this repo a plugin marketplace, `fde-project-kit` | No |
| `template/.claude/` | `settings.json`, the lint hook, `commands/verify.md` (the project's check list), `skills/_use-case-skill-template` | `verify.md`, plus your use-case skills |
| `template/.mcp.json`, `.mcp.example.json` | The MCP servers Claude Code may use while building (empty by default) | **Yes**, decided in the plan phase (step 8b) |
| `template/workflows/` | The same procedures written for people | Rarely |
| `template/kit/` | Optional, copied only with `new_project.py --with-kit`. Generates each milestone's Public API section from code, makes starter branches, and proves the step order | Config only (`kit/milestones.json`) |
| [examples/credit-underwriter.md](examples/credit-underwriter.md) | Every template file mapped to its filled version in the worked example | No |

## Why this works

- **Claude can't guess what the architect decided.** The files hold those decisions:
  invariants, boundaries, exact names, exact messages, and what is out of scope.
- **The tests are the contract.** A spec without executable acceptance tests left
  10–20 gaps per milestone in our trials. With tests, plus a Public API section, the
  builds went green.
- **The process skills stop the usual failure modes.** Clarify instead of guessing.
  Plan before code. Watch the test fail before writing code. Find the root cause
  instead of patching the symptom. Show evidence before saying "done". Review, then
  record what was learned.
- **The files improve over time.** Every review finding becomes a line in `CLAUDE.md`,
  so the next session doesn't repeat it.

## License

This repository is released under the [MIT License](LICENSE).

`karpathy-guidelines` is MIT (forrestchang/andrej-karpathy-skills). The six process skills
are adapted from obra/superpowers (MIT, © 2025 Jesse Vincent). See
[`plugins/spec-driven-build/THIRD_PARTY_NOTICES.md`](plugins/spec-driven-build/THIRD_PARTY_NOTICES.md).
