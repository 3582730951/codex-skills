# PM Boundary

Use this file when the main agent is PM and there is a risk that PM work drifts into implementation.

## Core Rule

In `standard` and `heavy` modes, PM is a coordination role, not the default coder.

The PM may own:

- task charter
- delegation map
- decision log
- state snapshot
- assurance scorecard
- acceptance notes

The PM may not quietly own:

- implementation files
- regression tests for the implementation track
- migrations
- production config changes
- final approval of PM-authored code

## Allowed Exceptions

The PM may take over execution only if one of these is true:

- the runtime cannot delegate and the plan is explicitly `constrained-single-agent`
- a delegated worker failed or is unavailable and the PM logs a `Role Transfer`
- the task is `tiny` and the plan says the PM is absorbing smaller roles

## Role Transfer Protocol

If PM must take over implementation:

1. publish a decision-log entry named `Role Transfer`
2. state the reason for takeover
3. restate which files or tracks changed ownership
4. downgrade the assurance claim if needed
5. assign an independent reviewer for the PM-authored work

## Failure Conditions

Fail the plan if:

- PM authors implementation code in `standard` or `heavy` mode without role transfer
- PM is both implementer and sole approver
- PM takeover happens repeatedly instead of fixing delegation problems
