# Anti-Laziness Controls

Use this file to detect fake progress and lazy implementation patterns.

## Always Require

- `Requirement-to-Change Map`
- `Claim-to-Evidence Map`
- executed tests or explicit execution gaps
- review package built from primary artifacts

## Lazy Patterns To Reject

- "done" with no changed-surface explanation
- "tested" with no command, environment, or output summary
- hardcoded constants copied from expected outputs
- validation removed or weakened to make tests pass
- reviewers asked to trust an implementer summary instead of artifacts
- architecture described only after code already drifted into shape
- generic abstractions added to look sophisticated
- UI made from the same default SaaS pattern regardless of product
- internal source copied or referenced with no provenance trail
- privileged or submission-sensitive code changed with no authorization or audit-note update

## Map Rules

`Requirement-to-Change Map` must let a reviewer trace each requirement to code and verification.

`Claim-to-Evidence Map` must let a reviewer challenge every completion claim.

If either map is shallow, stale, or generic, reject the approval claim.

## Self-Reported Evidence

Mark evidence as `self-reported` when the implementer is also the executor of the tests or checks.

Self-reported evidence:

- is acceptable for local progress tracking
- is not enough for independent approval on non-trivial work
- must be clearly separated from reviewer verdicts

## Truth Rule

When evidence is incomplete, say the work is not yet proven. Do not upgrade confidence through optimism.
