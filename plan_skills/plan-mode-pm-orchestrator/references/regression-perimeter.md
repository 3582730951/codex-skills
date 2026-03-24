# Regression Perimeter

Use this file when the plan fixes a bug or changes behavior.

## Required Questions

The plan must answer:

- what path is changing
- what nearby paths may be affected
- what must stay unchanged
- what is most likely to break next
- what tests or checks will catch those breakages

## Required Headings

```text
Root Cause:
Changed Path:
Adjacent Paths:
Unchanged Guarantees:
Second-Order Risks:
Regression Matrix:
```

## Failure Rule

Reject the plan if it only proves that the original bug no longer reproduces.
