# Execution Discipline

Use this file to keep implementation aligned to the approved plan.

## Core Rule

Do not treat the plan as background prose. Treat it as a lock:

- work must cite the relevant `plan_step_id`
- work must cite the relevant `requirement_id`
- out-of-plan edits must stop and go through replan

## Required Artifacts

- `Execution Contract`
- `Capability Routing Table`
- `Delegation Template Table`
- `Plan Coverage Matrix`
- `Execution Ledger`

## Rules

- No coding before the `Execution Contract` exists.
- Every implementation step should map to one or more locked plan steps.
- Every changed surface should map back to a requirement entry.
- Every claim of progress should update the `Execution Ledger`.
- If an edit cannot be justified by the locked plan, mark it `out_of_plan` and stop normal implementation.
- Parallel tracks are allowed only for explicitly declared plan steps.
- Critical work classes must stay on the routing tier declared in the `Capability Routing Table`.
- If a low-tier worker stalls on a critical surface, stop and escalate instead of iterating blindly.

## Commentary And Status Discipline

When reporting progress, the PM or implementer should name:

- current gate
- active `plan_step_id`
- affected `requirement_id`
- whether the step is `in_plan`, `replanned`, or blocked

Generic updates like "working on the backend" are not enough.

## Validation

Use `scripts/check_execution_alignment.py` to verify that:

- requirements have coverage
- executed work matches locked steps
- evidence exists for completed requirements
