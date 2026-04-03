# Escalation And Delegation

Use this file to stop low-tier agents from grinding on critical blockers.

## Core Rule

For critical work, the runtime should either:

- keep the work on the main agent, or
- delegate it to a frontier worker with high or extra-high reasoning

Do not let a fast worker keep iterating on planning, architecture, coding, security review, systems review, or release truthfulness.

## Required Artifacts

- `Capability Routing Table`
- `Delegation Template Table`
- `Spawn Agent Template Table`
- `Execution Ledger`

## Stall Policy

For critical work classes:

- `stall_attempt_limit` must be `2`
- after the same blocker appears twice, escalate to `frontier`
- escalation reasoning must be `xhigh` for planning, architecture, security, systems, and release verdict
- escalation reasoning must be `high` or `xhigh` for critical coding and review

For light work classes:

- a fast worker may be used first
- if the output is incomplete, ambiguous, or repeated, escalate at least to `standard`
- the stronger tier must validate the result before approval

## Delegation Template Rule

When the runtime supports subagents, keep a small set of reusable templates:

- PM frontier xhigh
- product frontier high
- architect frontier xhigh
- coding frontier high/xhigh
- security frontier xhigh
- systems frontier xhigh
- review frontier high/xhigh
- retrieval fast medium
- test execution fast medium
- packaging fast low

If the runtime does not support the required model or reasoning override, keep critical work local instead of delegating downward.

Use `scripts/generate_delegation_templates.py` to generate these templates and keep them versioned in the artifact bundle.

## Forbidden Behavior

- retrying the same weak worker on the same blocker more than twice
- assigning release verdict to anything below frontier + xhigh
- assigning security or systems review to low reasoning
- pretending a low-tier result was independently verified when it was not
