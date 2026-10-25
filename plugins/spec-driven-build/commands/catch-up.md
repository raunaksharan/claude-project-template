---
description: Bring a milestone's reference modules in when you're behind, so the next milestone can start
argument-hint: "<milestone number to catch up on, e.g. 02>"
---
<task>Catch me up on milestone $ARGUMENTS with the reference code.</task>

<steps>
1. Check that the tag `milestone-$ARGUMENTS` exists (`git tag -l milestone-$ARGUMENTS`). If
   it doesn't, say there is no reference for it and stop.
2. Read kit/milestones.json if it exists, or the "You build" list in
   milestones/$ARGUMENTS-*/SPEC.md, for that milestone's modules.
3. Show me which of my files would be replaced, and wait for my yes.
4. Run `git checkout milestone-$ARGUMENTS -- <those files>`, then /verify.
</steps>

<note>Suggest I commit my own attempt on its own branch first, so I can compare with
`git diff milestone-$ARGUMENTS -- <file>`.</note>
