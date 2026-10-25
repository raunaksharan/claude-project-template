# Release a milestone

**When:** a milestone's code, spec and prompts are finished and reviewed.

## Steps

1. **Verify:** `/verify`. All green, with the numbers written down in the PR.
2. **Close the loop on the spec:** for every assumption in the plan and every accepted
   review finding that was really a spec gap, update SPEC.md, CLAUDE.md › Clarifications
   or Learnings. The next milestone starts from better files.
3. **Commit and tag:** `git tag milestone-NN`.
4. **Refresh generated sections** (optional, if you use the kit): `python3
   kit/make_kit.py spec NN` writes the Public API section from the code, so later
   milestones see the exact contract.
5. **Push:** `git push origin main --tags`.

## Done when

The tag is pushed, and every assumption from the build is either in a SPEC or under
Clarifications.
