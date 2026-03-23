# Coordination And Quality Gates

Use this file when agents overlap, when acceptance criteria look weak, or when the PM needs concrete rejection rules.

## Canonical Artifacts

Require these artifacts before trusting progress on non-trivial work:

- `Task Charter`
- `Architecture Contract` for non-`tiny` work
- `Decision Log`
- latest `State Snapshot`

If any of these are missing, stale, or contradictory, downgrade all completion claims until the PM repairs the record.

## File Ownership Policy

Default to one primary owner per file.

If real delegated agents are available, require real ownership by delegated workers for `standard` and `heavy` plans. A single main-agent roleplay does not satisfy the ownership rule.

Before implementation, require:

- a file or module owner list
- a merge order for shared boundaries
- a note on which tracks are truly parallel and which are only apparently parallel

If two agents need the same file:

1. pause concurrent editing
2. ask the architect for a seam or extraction plan
3. assign one primary owner
4. have other agents contribute via proposed diffs, tests, review comments, or interface requests
5. merge sequentially and re-run impacted checks

Reviewers should not become co-authors of the implementation file unless the PM explicitly converts them into implementers and restages ownership.

## Anti-Laziness Checks

Reject work that shows any of these patterns:

- broad claims with no artifact, diff, or executed validation
- placeholder architecture disguised as a plan
- "temporary" hardcoding used to satisfy acceptance
- test edits that remove coverage instead of fixing behavior
- unresolved blocker hidden behind optimistic wording
- security-sensitive code shipped with no threat review
- missing requirement-to-change or claim-to-evidence mapping
- architecture contract missing task-specific coding rules
- progress summaries that cannot be traced back to the latest state snapshot

## Hardcoding Detection

Inspect for:

- constants copied from expected test outputs
- mocks or fixtures that bypass real behavior without saying so
- environment checks that silently short-circuit the failing path
- suppressed exceptions or weakened assertions added near the bug fix
- feature flags permanently left in bypass mode
- contract checks or validators stubbed out only for the changed path
- planner logic with special cases for demo data while claiming general correctness

## Blind Review Protocol

Enforce reviewer independence like this:

1. package the review input from primary artifacts only
2. provide the task charter, architecture contract, diff, test evidence, and relevant source files
3. withhold other reviewers' verdicts until the current reviewer finishes
4. collect findings independently
5. compare the findings after submission and resolve conflicts from raw evidence

Reject reviews that rely on social proof such as "the other reviewer already approved it."

If the runtime supports real delegation, reviewers should be distinct delegated agents rather than sections in the implementer's own answer.

## Context Packaging Rules

Each role should receive only:

- the task charter
- the relevant slice of the architecture contract
- the latest state snapshot
- the owned files or raw evidence needed for that role

Avoid passing:

- long conversational history when a state snapshot is enough
- another agent's conclusion when the raw artifact is available
- stale plans that predate the latest accepted decision log entry

## Rework Reset Protocol

Trigger a reset when:

- the same bug or review finding reappears twice
- two accepted decisions now conflict
- active edits exceed the planned ownership boundary
- no one can explain the current diff from the task charter and architecture contract
- three iterations pass without a stable acceptance decision

Reset procedure:

1. freeze edits
2. publish a fresh state snapshot
3. mark invalidated assumptions in the decision log
4. update the architecture contract if design assumptions changed
5. restart only the affected tracks with a new context package

## Acceptance Gates

Call the task complete only after:

- the PM confirms all critical deliverables are met
- the tester confirms intended behavior and regression coverage
- the architecture reviewer signs off on boundary soundness
- the security reviewer signs off on risky surfaces or explicitly documents residual risk
- the implementer's claims are matched to evidence
- review independence is preserved

If any gate cannot run, state that clearly and downgrade the completion claim.

If real delegation was available but not used, downgrade the plan to `constrained-single-agent` and lower the assurance claim accordingly.

## Dispute Resolution

When agents disagree:

1. let the PM summarize the actual conflict
2. ask the architect to restate the intended boundary or invariant
3. ask the tester what is observable and verifiable
4. ask the security reviewer whether either option creates new exposure
5. pick the option with the lower long-term risk and clearer validation path

Never resolve a dispute by averaging two incompatible designs.
