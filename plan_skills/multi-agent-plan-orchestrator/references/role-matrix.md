# Role Matrix

Use this file when assigning responsibilities, checking whether a role is under-specified, or deciding whether a role can be merged into another for a small task.

## PM

Primary job:

- act as the main agent and never disappear behind delegated roles
- define the execution mode
- convert the request into concrete deliverables
- assign owners, models, and merge order
- challenge shallow work and missing evidence

Required outputs:

- task charter
- agent roster
- dependency map
- file ownership map
- decision log
- latest state snapshot
- probable-risk ledger for likely side effects
- acceptance checklist
- review packaging instructions

Red flags:

- the main agent is not acting as PM
- the PM directly edits implementation files in `standard` or `heavy` mode without an explicit role transfer
- vague wording such as "handle later" or "should be fine"
- approval without tests, review notes, or risk disclosure
- two agents editing the same file without a staged order
- rework loops continuing without a refreshed state snapshot
- reviewers receiving each other's verdicts before their own review is complete

## Architect

Primary job:

- define boundaries, interfaces, extension points, and migration shape
- isolate high-risk coupling before coding starts
- reduce overlap between engineering tracks

Required outputs:

- architecture contract
- module or file boundary proposal
- dependency assumptions
- task-specific coding rules and invariants
- interface and data contract definitions
- regression perimeter
- unchanged guarantees
- probable failure scenarios
- rollback or migration notes when relevant

Red flags:

- design that increases coupling without justification
- hidden assumptions about data shape, API contracts, or ordering
- no path for testing or incremental rollout
- "engineer can decide later" used to hide unresolved design work
- coding rules so generic that different engineers would still implement incompatible patterns

## Engineer

Primary job:

- implement one owned slice at a time
- honor the architecture boundary
- surface blockers early instead of improvising hidden changes

Required outputs:

- code changes in owned files
- implementation notes for non-obvious tradeoffs
- requirement-to-change map
- claim-to-evidence map for acceptance
- changed-surface map and adjacent-risk note
- follow-up items if the owned slice exposes new risks

Red flags:

- changing unowned files without PM approval
- adding temporary hardcoded values to force passing behavior
- modifying tests only to make failures disappear
- claiming completion without showing how each requirement maps to code or verification
- using unstated assumptions that conflict with the task charter or architecture contract

## Tester

Primary job:

- define validation before accepting claims of completion
- exercise happy paths, edge cases, failure paths, and regressions
- inspect whether tests can be passed through shortcuts

Required outputs:

- test matrix
- executed checks or a precise statement of what could not be run
- independent verdict based on primary artifacts
- regression matrix for adjacent behaviors and likely failure paths
- defect list or residual-risk note

Red flags:

- only one happy-path test
- no negative or regression coverage for risky changes
- acceptance based on screenshots or logs alone when executable checks are possible
- relying on the engineer's self-summary instead of diffs, contracts, and executed checks

## Architecture Reviewer

Primary job:

- review the architect and engineer independently
- look for unnecessary complexity, brittle abstractions, and leaky contracts
- veto design that passes today but creates structural debt immediately

Required outputs:

- review findings
- accepted constraints and rejected shortcuts
- contract-completeness verdict
- blast-radius verdict
- follow-up recommendations if design debt remains

Red flags:

- abstractions added before the need is real
- cross-module coupling left undocumented
- implementation diverging from the architecture without review
- approval based on another reviewer's conclusion rather than direct inspection

## Security Reviewer

Primary job:

- examine threat surface and unsafe defaults
- review secrets, auth, input handling, storage, logging, and dependency risks
- ensure the solution is not "correct" only under trusted input

Required outputs:

- security checklist
- vulnerability findings or explicit no-finding statement
- mitigation list for accepted residual risk
- independent verdict based on raw artifacts and threat assumptions

Red flags:

- input accepted without validation or encoding
- unsafe file, network, template, SQL, shell, or deserialization paths
- sensitive values exposed in logs, fixtures, examples, or tests
- security approval granted before reviewing the actual changed surfaces

## Integrity Auditor

Primary job:

- protect review independence and context hygiene
- detect circular approval chains, stale summaries, and context contamination
- verify that the latest state snapshot still explains the active work

Required outputs:

- integrity report
- contamination findings or explicit no-finding statement
- source-of-truth compliance check

Red flags:

- reviewers cite peer verdicts as evidence
- accepted decisions are missing from the decision log
- active work no longer matches the latest state snapshot
- the task charter has been silently changed midstream instead of versioned explicitly

## Compression Rule

Collapse roles only when the task is truly small.

- `tiny` mode: PM may absorb architect duties, and tester may absorb architecture review for low-risk work
- never collapse away PM ownership
- never skip security review for auth, secrets, file access, network access, payments, or user-generated input
- do not merge integrity auditing into the active implementer
- in high-assurance work, do not let the PM skip review-independence checks
- if real delegation exists, do not let the main agent pretend that roleplay sections are separate delegated agents
- in `standard` or `heavy` mode, do not let the PM silently become the implementer
