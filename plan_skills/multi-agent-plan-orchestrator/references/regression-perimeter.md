# Regression Perimeter

Use this file when a bug fix or behavior change risks breaking nearby paths.

## Core Rule

Do not ask only "Does the reported bug still happen?"

Also ask:

- what else uses the same path
- what must remain unchanged
- what is most likely to break next
- what evidence would catch that breakage

## Required Sections

Write the perimeter with these headings:

```text
Root Cause:
Changed Path:
Adjacent Paths:
Shared Helpers Or Contracts:
Unchanged Guarantees:
Probable Failure Scenarios:
Regression Matrix:
Observability Or Rollback Signals:
```

## Rejection Rule

Reject the bug-fix plan if:

- the perimeter stops at the reproduced bug
- unchanged guarantees are missing
- probable failure scenarios are vague or unranked
- the regression matrix tests only the happy path
