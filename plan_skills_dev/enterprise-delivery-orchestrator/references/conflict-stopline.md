# Conflict Stop-Line

Use this file when multiple tracks collide or the current diff can no longer be explained cleanly.

## Trigger Conditions

Trigger a stop-line if any of these occur:

- two owners need the same file at the same time
- the same review finding appears twice
- the diff exceeds the current `Task Charter` or `Architecture Contract`
- accepted decisions now conflict
- system-layer assumptions changed after coding began
- nobody can explain the current diff from the latest `State Snapshot`

## Required Stop-Line Steps

1. freeze editing on the conflicting area
2. publish a `Conflict Snapshot`
3. ask `Architect` to produce a `Seam Proposal`
4. let `PM` assign one primary owner and a merge order
5. rerun affected validation
6. if the diff is still incoherent, reset to the latest trusted snapshot and restart the affected track

## Conflict Snapshot

```text
Conflict Snapshot:
- Trigger:
- Conflicting files / symbols:
- Current owners:
- Broken assumption:
- Risk if merged now:
- Required decision:
```

## Seam Proposal

```text
Seam Proposal:
- Primary owner:
- Extracted boundary:
- Secondary contribution path:
- Merge order:
- Required retests:
```

## Reviewer Rule

Reviewers do not fix ownership conflicts by casually editing implementation files. The PM must formally reassign ownership first.
