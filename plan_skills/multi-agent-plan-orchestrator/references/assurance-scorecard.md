# Assurance Scorecard

Use this file when deciding whether a plan is detailed enough, independent enough, and stable enough to execute.

## Scoring Rule

Score each dimension from `0` to `5`.

- `0`: absent or unusable
- `1`: mostly rhetorical, unsafe to execute
- `2`: partial, major blind spots remain
- `3`: workable but still risky
- `4`: strong and materially trustworthy
- `5`: strong, explicit, and backed by direct evidence

## Dimensions

### Architecture Completeness

Check whether the architecture contract defines:

- boundaries
- interfaces and data contracts
- invariants
- task-specific coding rules
- validation and rollback shape

### Evidence Coverage

Check whether requirements map to:

- owned files or modules
- concrete implementation tasks
- tests or review evidence

### Blast Radius Coverage

Check whether the plan identifies:

- the directly changed path
- neighboring paths that may be affected
- unchanged guarantees
- probable failure scenarios
- regression checks beyond the reproduced bug

### PM Boundary Integrity

Check whether:

- the main agent stays in the PM role
- implementation ownership belongs to engineers or other delegated workers
- any PM takeover is explicit, justified, and independently reviewed

### Review Independence

Check whether reviewers are blind to peer verdicts and rely on primary artifacts rather than social proof.

### Context Integrity

Check whether the task charter, decision log, and latest state snapshot are present, fresh, and consistent.

### Task Continuity

Check whether the current plan and current diff can still be explained from the canonical artifacts after rework.

### Security Coverage

Use this only when the task touches risky surfaces such as auth, secrets, networking, file access, persistence, or public APIs.

### Delegation Integrity

Check whether the claimed multi-agent plan uses real delegated agents when the runtime supports them.

- `5`: real delegated agents own distinct tracks with bounded context packages
- `4`: real delegated agents are used for the critical tracks
- `3`: constrained single-agent fallback is clearly disclosed because delegation is unavailable
- `1-2`: roleplay is used even though delegation likely exists
- `0`: the plan falsely claims real multi-agent execution with no actual delegation

## Gate Thresholds

- `tiny`: scorecard optional
- `standard`: each required dimension must be `>= 4`
- `heavy` or high-assurance: each required dimension must be `>= 4`, and the average must be `>= 4.5`

Required dimensions:

- always: architecture completeness, evidence coverage, review independence, context integrity, task continuity
- add blast radius coverage when fixing a bug or changing behavior
- add PM boundary integrity in `standard` and `heavy` modes
- add security coverage when relevant
- add delegation integrity when the runtime supports real delegation

## Automatic Failure Conditions

Fail the plan immediately if any of these are true:

- no task charter
- no architecture contract for `standard` or `heavy`
- reviewers see peer verdicts before finishing their own review
- hardcoded pass conditions or weakened tests are part of the plan
- the same agent implements and solely approves
- the plan claims real multi-agent execution without real delegation
- a bug fix has no written regression perimeter or unchanged guarantees
- the PM is acting as the active implementer in `standard` or `heavy` mode without an explicit role transfer

## Reporting Format

Use this structure:

```text
Assurance Scorecard:
- Architecture Completeness: 4.5
- Evidence Coverage: 4.0
- Blast Radius Coverage: 4.5
- PM Boundary Integrity: 5.0
- Review Independence: 4.5
- Context Integrity: 4.0
- Task Continuity: 4.0
- Security Coverage: N/A
- Delegation Integrity: 5.0
- Gate Result: pass | fail
- Reasons:
```
