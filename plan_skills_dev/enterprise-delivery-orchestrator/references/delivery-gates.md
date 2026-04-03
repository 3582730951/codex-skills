# Delivery Gates

Use this file to decide what can honestly be claimed about the current state of the work.

## Gate Order

1. `Clarification Gate`
2. `Greenfield Bootstrap Gate` when applicable
3. `Architecture Gate`
4. `Implementation Gate`
5. `Evidence Gate`
6. `Independent Review Gate`
7. `Release Gate`

## Automatic Failure Conditions

Fail immediately if any of these are true:

- missing `Task Charter`
- missing `Engineering Baseline`
- missing `Greenfield Bootstrap Plan` for new projects
- missing `Architecture Contract` for non-trivial work
- missing `API Contract Table` or `Function Boundary Table` when boundaries changed
- missing `Execution Contract`
- missing `Capability Routing Table`
- missing `Delegation Template Table`
- missing `Spawn Agent Template Table`
- missing `Plan Coverage Matrix`
- missing `Execution Ledger`
- missing `Test Matrix + Evidence Log`
- implementer is the sole approver
- reviewer relies on another reviewer verdict or implementer summary as primary evidence
- public or system-sensitive code ignores applicable language adapters or system rules
- readability rubric has any dimension below `4`
- UI gate required but not completed
- system gate required but not completed
- security-sensitive work lacks a `Threat Review`
- defensive system-tool work lacks a permission model or bounded capability declaration
- regulated internal security-product work lacks an `Authorization Manifest`
- internal source reuse lacks a `Source Provenance Register`
- sensitive files required for audit lack visible annotations or an `Audit Annotation Register`
- plan-quality score has any dimension below `4`
- capability-routing check fails
- execution-alignment check fails
- implementation touches surfaces that cannot be mapped to a locked `plan_step_id`
- critical work is assigned below frontier tier or below high reasoning
- task claims `3-agent approved` without real independent reviewer evidence

## Reviewer Matrix

### Product / UI Work

- `Architecture Reviewer`
- `UI Reviewer`
- `Security Reviewer`

### System / Kernel / Runtime Work

- `Architecture Reviewer`
- `Systems Reviewer`
- `Security Reviewer`

### Mixed Work

- `Architecture Reviewer`
- `UI Reviewer` or `Systems Reviewer` depending on touched surfaces
- `Security Reviewer`

## Evidence Minimum

Approval requires:

- traceable maps from requirements to code and evidence
- executed commands or equivalent validation method
- output summaries that a reviewer can inspect
- residual risks and execution gaps stated plainly
- for defensive system tools: a threat model and permission model
- for regulated internal security products: authorization, provenance, and audit annotation evidence
- a locked plan and execution log that can be audited
- capability routing that matches the criticality of the work
- runtime-facing spawn templates for delegated work

## Complete Product Gate

Before using product-complete language, verify:

- release-1 scope is explicit
- core end-to-end journeys for that scope are implemented
- omitted features are listed as non-goals or later milestones
- the delivery claim matches the implemented release slice rather than the user's broadest dream wording

## Delivery Status Vocabulary

Use only one of these statuses:

- `approved`
- `approved with residual risk`
- `approval pending external review`
- `not approved`

## Truthfulness Rule

In `constrained-single-agent` mode:

- do not claim `3-agent approved`
- do produce review packages and explicit external review prompts

Use:

- `scripts/build_review_package.py` to standardize the package
- `scripts/generate_execution_control.py` to create the execution lock artifacts
- `scripts/generate_capability_routing.py` to create the capability-routing artifact
- `scripts/generate_delegation_templates.py` to create reusable spawn templates
- `scripts/generate_spawn_agent_templates.py` to create runtime-facing spawn-agent payload templates
- `scripts/generate_review_prompts.py` to create independent reviewer asks
- `scripts/generate_verdict_template.py` to normalize reviewer outputs
- `scripts/generate_threat_model.py` to create a first-pass threat review
- `scripts/run_system_checks.py` to scan for dangerous patterns and missing system-tool docs
- `scripts/bootstrap_audit_bundle.py` to create the audit and submission artifact set
- `scripts/register_internal_reference.py` to register proprietary local source as a tracked reference
- `scripts/scan_audit_annotations.py` to verify required comment tags in sensitive files
- `scripts/score_plan_quality.py` to reject shallow plans before coding
- `scripts/check_capability_routing.py` to reject weak routing on critical work
- `scripts/check_spawn_agent_templates.py` to validate runtime-facing spawn-agent templates
- `scripts/check_execution_alignment.py` to detect drift from the locked plan

## Rework Protocol

If a gate fails:

1. log the failing gate
2. summarize the blocking reasons
3. update artifacts, not just code
4. rerun only the affected gate after fixes

Two failed attempts on the same gate trigger the stop-line protocol.

Use `scripts/validate_delivery.py` when the artifacts live in a directory bundle and you need a quick mechanical gate check before manual review.
