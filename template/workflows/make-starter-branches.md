# Make the starter branches (optional)

**When:** you want people to rebuild a finished milestone themselves, for teaching,
onboarding or a re-implementation trial. The kit turns each milestone's reference code
into a starting point with its modules reduced to their docstrings.

## Steps

1. List each milestone's built modules and its reference commit in `kit/milestones.json`.
2. Refresh the generated Public API section of each SPEC.md: `python3 kit/make_kit.py spec all`.
3. Prove the PROMPTS.md step order works (every step's tests pass with only the earlier
   steps' code): list the steps in `kit/steps.json`, then run `python3 kit/check_steps.py all`.
4. Build the branches: `python3 kit/make_kit.py build all` creates `milestone-NN-start`.
5. Check one: on `milestone-NN-start` the tests are red only in the built modules;
   restoring them from the `milestone-NN` tag turns everything green.
6. Push with `--force` (the branches are regenerated).

## Done when

Every starter branch is rebuilt and `check_steps.py all` reports ok for every step.
