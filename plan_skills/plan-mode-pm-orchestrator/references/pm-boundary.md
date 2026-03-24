# PM Boundary

Use this file when the main agent is PM and the plan risks collapsing into PM-led coding.

## Core Rule

In `standard` and `heavy` planning, PM coordinates and approves the plan. PM does not quietly absorb the engineer track.

## Required Check

The plan must say:

- who the PM is
- who the implementation owner will be
- whether PM takeover is forbidden, allowed only in fallback, or already required

## Failure Rule

Reject the plan if PM is still labeled PM but is also the undisclosed implementation owner.
