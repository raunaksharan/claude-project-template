---
name: tdd-module
description: Use when implementing a module, function or behaviour. Red, green, refactor against the milestone's tests; in Mode B, write the failing tests first from the SPEC's acceptance criteria. Adapted from obra/superpowers test-driven-development (MIT).
---

# Test-driven, one module at a time

If you didn't watch the test fail, you don't know whether it tests the right thing.
(Adapted from obra/superpowers `test-driven-development`; see THIRD_PARTY_NOTICES.md.)

## Where the failing tests come from

- **Mode A** (CLAUDE.md › Plan says the tests ship with the milestone): they already
  exist and they are the answer key. Never edit them.
- **Mode B** (acceptance criteria given): write them first. For each `AC-NN.k`, write at
  least one test named for the behaviour, with the AC id in its docstring. Use the exact
  values and messages from the SPEC. For each threshold, cover just inside, exactly on,
  just outside, and the input missing. Show the tests and stop for approval before
  writing the code.

## The loop

1. **Red.** Run the module's tests (the narrowest command: one file, or `-k`). Read why
   they fail. An import error means the name isn't there yet; that's a valid red. A test
   that already passes is testing nothing new: say so.
2. **Green.** Write the smallest code that makes those tests pass, with the names and
   signatures from SPEC.md. No extra options, layers or features.
3. **Whole suite.** Run every test in the project, not just your file. Fix what you
   broke now.
4. **Refactor** only while green, and only your own code.
5. **Repeat** for the next function or module in the plan.

<rules>
- Never weaken a test to make it pass. If a test looks wrong, stop and say why, with the
  line and the SPEC text it contradicts.
- Exact arithmetic and rules are code, never a model's estimate.
- The clock and randomness are injected, never read directly, so tests are repeatable.
- If you wrote code before its test, delete it and start the loop again.
</rules>
