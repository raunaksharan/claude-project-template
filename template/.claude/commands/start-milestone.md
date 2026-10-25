---
description: Start a milestone: what to build, what's red, where to begin
argument-hint: "<milestone number, e.g. 03>"
---
<task>Get me started on milestone $ARGUMENTS.</task>

<check_branch>If this is a git repo, run `git status` and `git log --oneline -1` and tell
me the branch. Suggest `git switch -c milestone-$ARGUMENTS` if I'm on main with no branch
for this work. Without git, skip this.</check_branch>

<steps>
1. Read milestones/$ARGUMENTS-*/SPEC.md and PROMPTS.md, and CLAUDE.md › Plan (which test
   mode this project uses).
2. Install, then run the tests with collection errors allowed (see CLAUDE.md › Commands).
   Summarize what's red and why (missing modules, NotImplementedError, import errors).
3. List the modules I'll build, in the order PROMPTS.md gives, with the ACs and the test
   file for each.
</steps>

<next>Suggest `/plan-milestone $ARGUMENTS`. Don't write code.</next>
