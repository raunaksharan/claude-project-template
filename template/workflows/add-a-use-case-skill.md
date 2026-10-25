# Add a use-case skill

**When:** you've made the same kind of change twice (a new rule, a new tool, a new golden
case), or a review finding shows a procedure that people get wrong.

## Steps

1. Copy `.claude/skills/_use-case-skill-template/` to `.claude/skills/add-<thing>/`.
2. Fill in the `description` with the words a request would use; that's how Claude
   picks the skill.
3. Name exact files, the decision to ask about, every fault or edge case, the tests, the
   eval case and the doc row. Point to an existing example in the code.
4. Add it to the Skills and commands table in CLAUDE.md.
5. Try it: ask Claude for that change in a fresh session and check that it used the skill.

## Done when

A fresh session makes the change correctly using the skill, with `/verify` green.
