# Context Integrity

Use this file when the task is long, multi-agent, ambiguous, or already showing signs of drift.

## Source-Of-Truth Hierarchy

Trust artifacts in this order:

1. `Task Charter`
2. accepted entries in the `Decision Log`
3. latest `State Snapshot`
4. raw source artifacts such as code, diffs, tests, logs, and API contracts
5. conversational summaries

If a lower-priority source conflicts with a higher-priority one, discard the lower-priority assumption.

## Task Charter

The PM should publish a task charter with:

- objective
- scope
- non-goals
- acceptance criteria
- constraints
- forbidden shortcuts
- source-of-truth artifacts

Change the task charter only by versioning it explicitly in the decision log.

## Decision Log

The decision log is append-only.

For each entry, record:

- decision
- status: accepted, rejected, superseded
- rationale
- owner
- affected files or modules

Do not silently rewrite history.

## State Snapshot

Publish a fresh state snapshot whenever a major decision changes or a rework loop resets.

Use this format:

```text
State Snapshot:
- Objective:
- Current Truth:
- Accepted Decisions:
- Rejected Paths:
- Active Ownership:
- Blockers:
- Evidence Collected:
- Next Actions:
```

The snapshot must be short enough to re-seed a fresh agent context.

## Bounded Context Packages

Package context by role:

- architect: task charter, relevant source artifacts, current boundaries, prior accepted decisions
- engineer: task charter, architecture contract, owned files, relevant tests, latest state snapshot
- tester: task charter, architecture contract, diffs, executable checks, latest state snapshot
- reviewers: task charter, architecture contract, diffs, tests, raw evidence, but not peer verdicts

Do not pass the whole chat history unless it contains unique primary evidence not captured elsewhere.

## Contamination Signals

Assume context contamination when:

- different reviewers repeat the same phrasing or unsupported conclusion
- the current diff cannot be explained from the latest snapshot
- agents cite stale plans that were superseded
- reviewers quote another review instead of raw evidence
- task scope grows without a corresponding decision log entry

## Recovery Protocol

When contamination is suspected:

1. stop adding new implementation changes
2. rebuild a fresh state snapshot from the task charter, decision log, code, and test artifacts
3. invalidate stale assumptions explicitly
4. reissue bounded context packages
5. rerun the affected review or implementation track
