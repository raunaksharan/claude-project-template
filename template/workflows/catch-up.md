# Catch up on a milestone

**When:** you're behind and the next milestone needs this one's code.

## Steps

1. Commit your own attempt on its own branch, so you can compare later.
2. `/catch-up NN` (or by hand: `git checkout milestone-NN -- <the milestone's modules>`).
3. `/verify`.
4. Later: `git diff milestone-NN -- <file>` to see how the reference differs from your attempt.

## Done when

`/verify` is green and the next milestone's `/start-milestone` shows only its own modules red.
