# Failure modes

<!-- PLAN-PHASE.md step 3. For every component ask: what happens when it returns nothing,
     returns garbage, or never returns? If the answer is "it guesses", the design is wrong.
     Every external dependency gets timeout, error and malformed rows. Every AI component
     gets "confidently wrong" and "provider down" rows. -->

| # | Failure | Where | Impact if unhandled | Designed response | Injected by / test | Milestone |
|---|---|---|---|---|---|---|
| F1 | {{FILL}} | {{FILL}} | {{FILL}} | {{FILL: status or reason code, then outcome}} | {{FILL: fault flag or test name}} | {{FILL}} |
