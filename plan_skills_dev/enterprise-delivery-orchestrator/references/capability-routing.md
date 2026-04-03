# Capability Routing

Use this file before delegation, coding, review, or heavy analysis. The goal is to stop critical work from being assigned to weak models or weak reasoning settings.

## Core Rule

Not all work should use the same capability tier.

- retrieval, inventory, smoke-test execution, and artifact packaging may use lighter models
- planning, architecture, code authoring, complex debugging, security review, systems review, and final approval must use the strongest available model tier with high or extra-high reasoning

If the runtime does not let you choose model or reasoning settings, keep critical reasoning local in the main agent instead of delegating it to a weaker worker.

## Capability Tiers

- `frontier`: strongest available model for the current runtime
- `standard`: capable but not the strongest
- `fast`: cheapest / fastest helper tier

## Required Artifact

Create a `Capability Routing Table` before non-trivial work starts.

It should name:

- work item
- work class
- owner role
- required model tier
- preferred model or family
- required reasoning effort
- whether downgrade is allowed
- execution preference
- stall attempt limit
- escalation target
- stall escalation trigger

## Work-Class Routing Rules

These work classes must use `frontier` tier:

- `pm_planning`
- `product_definition`
- `architecture`
- `core_coding`
- `bounded_coding`
- `complex_debugging`
- `migration_refactor`
- `test_design`
- `code_review`
- `ui_design_review`
- `security_review`
- `systems_review`
- `release_verdict`

Default reasoning:

- `xhigh` for `pm_planning`, `architecture`, `complex_debugging`, `security_review`, `systems_review`, `release_verdict`
- `high` or `xhigh` for `product_definition`, `core_coding`, `bounded_coding`, `migration_refactor`, `test_design`, `code_review`, `ui_design_review`

These work classes may use lighter tiers:

- `repo_retrieval`
- `doc_extraction`
- `artifact_packaging`
- `test_execution`
- `smoke_test`
- `screenshot_capture`

Default reasoning:

- `medium` for `repo_retrieval`, `doc_extraction`, `test_execution`
- `low` for `artifact_packaging`, `smoke_test`, `screenshot_capture`

## Current Runtime Mapping

When the runtime offers named models such as:

- `gpt-5.4`
- `gpt-5.3-codex`
- `gpt-5.2`
- `gpt-5.1-codex-mini`

Prefer this mapping:

- `frontier` planning/review/security/systems: `gpt-5.4` with `xhigh`
- `frontier` coding/debugging: `gpt-5.4` or the strongest coding-capable frontier model with `high` to `xhigh`
- `standard`: `gpt-5.2` or equivalent with `medium` to `high`
- `fast`: `gpt-5.1-codex-mini` or equivalent with `low` to `medium`

If the current runtime exposes a stronger model than the examples above, use the stronger one.

## Stall Escalation

Escalate immediately to `frontier` + `xhigh` when:

- a lower-tier worker repeats the same blocker twice
- the output stays shallow across two iterations
- the task touches security, systems, ABI, or architecture unexpectedly
- a code path cannot be explained cleanly
- the PM cannot map the work to a credible release slice

Do not let a weak worker keep "trying again" on critical work.

## Downgrade Rule

Downgrade is forbidden for:

- planning
- architecture
- coding
- security review
- systems review
- code review
- release verdict

Downgrade is acceptable only for explicitly light work classes and only when the result is still checked by a stronger tier before approval.

## Delegation Templates

Create a `Delegation Template Table` for reusable spawn settings.

At minimum define templates for:

- PM
- product
- architect
- coding
- security review
- systems review
- code review / UI review
- retrieval
- test execution
- packaging

Use `scripts/generate_delegation_templates.py` to create the table.
