# Plan Scorecard

Use this file before approving the plan.

## Dimensions

Score each from `0` to `5`:

- architecture completeness
- evidence coverage
- blast radius coverage
- PM boundary integrity
- review independence
- context integrity
- delegation integrity when applicable

## Thresholds

- `tiny`: optional
- `standard`: every required dimension must be `>= 4`
- `heavy`: every required dimension must be `>= 4`, and the average must be `>= 4.5`

## Automatic Failures

Fail immediately if:

- the main agent is not PM
- the plan claims real multi-agent work without real delegated workers
- reviewers are not independent
- the plan has no task charter
- the architecture summary is missing for non-`tiny` work
- a bug fix has no regression perimeter or unchanged guarantees
- the PM is acting as the hidden implementer in `standard` or `heavy`
