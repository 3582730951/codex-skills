# Replan Protocol

Use this file when implementation drifts, the original plan proves shallow, or a new fact invalidates the locked path.

## Replan Triggers

Replan immediately if any of these happen:

- a required contract was missing from the original plan
- a change touches files not covered by the current plan
- acceptance criteria changed materially
- a blocked dependency changes the release slice
- the plan-quality gate drops below `4`
- the execution-alignment check fails
- capability routing is missing or assigns critical work to a weak tier
- a low-tier worker loops on a critical blocker

## Required Steps

1. Freeze normal implementation.
2. Log the trigger in the `Decision Log`.
3. Update the `State Snapshot`.
4. Revise the `Execution Contract`.
5. Revise the `Plan Coverage Matrix`.
6. Resume only after the updated plan passes quality and alignment checks.

## Allowed Fast Path

Minor replans are allowed only when:

- the release slice stays the same
- no new trust boundary appears
- no new shared ownership is introduced
- no hidden out-of-plan work is being retroactively justified

Even in the fast path, the plan lock version must change.

## Forbidden Behavior

- quietly continuing with a broken plan
- pretending out-of-plan work was always part of the plan
- backfilling artifacts only after code is already merged
