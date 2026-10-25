# spec-driven-build

The generic half of `claude-project-template`, packaged as a Claude Code plugin: the
process skills and the milestone commands. Install it once and every spec-driven project
gets the same loop, without copying folders.

```text
/plugin marketplace add raunaksharan/claude-project-template
/plugin install spec-driven-build@fde-project-kit
```

Or, in one step (Claude Code 2.1.275 or later):

```text
/plugin install spec-driven-build --marketplace raunaksharan/claude-project-template
```

Plugin components are namespaced, so the commands run as `/spec-driven-build:plan-milestone`,
`/spec-driven-build:write-tests` and so on.

| Skills | Commands |
|---|---|
| `karpathy-guidelines` (vendored, MIT) | `start-milestone`, `plan-milestone`, `clarify` |
| `clarify-before-building`, `write-plan`, `tdd-module`, `debug-root-cause`, `verify-before-done`, `review-and-learn` (adapted from obra/superpowers, MIT) | `write-tests`, `build-module`, `review`, `learn`, `catch-up` |

What stays in each project, because it is project-specific:

- `CLAUDE.md`;
- `.claude/commands/verify.md`, which holds the project's check list;
- the lint hook;
- use-case skills;
- `.mcp.json`.

See `THIRD_PARTY_NOTICES.md` for sources and licences.
