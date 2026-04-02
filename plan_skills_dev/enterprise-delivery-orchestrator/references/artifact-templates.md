# Artifact Templates

Use these templates as the minimum fields for each artifact.

## Task Charter

```text
Task Charter:
- Objective:
- Deliverables:
- In Scope:
- Out of Scope:
- User / operator:
- Constraints:
- Acceptance criteria:
- Quality bar:
- Reviewer matrix:
- Forbidden shortcuts:
```

## Product / Experience Brief

```text
Product/Experience Brief:
- Problem:
- Target user:
- Primary journeys:
- Success metrics:
- Failure cost:
- UX / UI expectations:
- Non-goals:
```

## Architecture Contract

```text
Architecture Contract:
- Objective:
- Boundaries:
- Owned modules / files:
- APIs / contracts:
- Function boundaries:
- Data flow:
- Validation points:
- Error model:
- Concurrency / resource rules:
- Compatibility / migration:
- Observability:
- Regression perimeter:
- Open questions:
```

## ADR

```text
ADR:
- Decision:
- Context:
- Options considered:
- Chosen option:
- Consequences:
- Follow-ups:
```

## API Contract Table

```text
API Contract Table:
- Boundary name:
- Caller(s):
- Input schema:
- Output schema:
- Error model:
- Auth / trust boundary:
- Idempotency / side effects:
- Compatibility / versioning:
- Observability:
```

## Function Boundary Table

```text
Function Boundary Table:
- Symbol:
- Responsibility:
- Inputs:
- Returns:
- Error / failure semantics:
- Side effects:
- Caller(s):
- Tests covering it:
```

## Requirement-to-Change Map

```text
Requirement-to-Change Map:
- requirement_id:
  source:
  acceptance:
  owner_track:
  touched_files_or_symbols:
  validation:
  status:
  residual_risk:
```

## Test Matrix + Evidence Log

```text
Test Matrix + Evidence Log:
- test_id:
  requirement_ids:
  level:
  scenario:
  command_or_method:
  environment:
  result:
  key_output_summary:
  gaps_or_followups:
```

## Threat Review

```text
Threat Review:
- Assets:
- Trust boundaries:
- Attacker capabilities:
- Sensitive paths:
- Key risks:
- Mitigations:
- Residual risks:
```

## Authorization Manifest

```text
Authorization Manifest:
- Product / component:
- Business owner:
- Engineering owner:
- Authorized environments:
- Allowed privilege level:
- Allowed persistence model:
- Allowed data access:
- Disallowed behaviors:
- Approval chain:
```

## Audit Annotation Register

```text
Audit Annotation Register:
- File / symbol:
- Required tags:
- Owner:
- Last reviewed:
- Related artifact or evidence:
```

## Source Provenance Register

```text
Source Provenance Register:
- Source root or package:
- Owner / team:
- Sensitivity:
- Allowed use:
- License / IP basis:
- Modification policy:
- Submission status:
```

## Platform Submission Notes

```text
Platform Submission Notes:
- Submission target:
- Included source roots:
- Omitted or redacted items:
- Build instructions:
- Reviewer:
- Traceability links:
```

## Claim-to-Evidence Map

```text
Claim-to-Evidence Map:
- claim_id:
  related_requirements:
  changed_files_or_symbols:
  command_or_check:
  output_summary:
  reviewer_or_owner:
  evidence_gap:
```

## Review Package

```text
Review Package:
- Scope summary:
- Changed files:
- Relevant artifacts:
- Diff / patch reference:
- Executed commands:
- Evidence summary:
- Screenshots_or_recordings:
- Residual risks:
- Reviewer instructions:
```

## Release Readiness Checklist

```text
Release Readiness Checklist:
- Scope met:
- Tests executed:
- Reviewers complete:
- Security reviewed:
- Docs / config updated:
- Migration / rollout ready:
- Residual risks accepted:
- Delivery status:
```

## Decision Log / State Snapshot

```text
Decision Log:
- decision_id:
  date:
  decision:
  rationale:
  owner:

State Snapshot:
- Current phase:
- Completed artifacts:
- Active owners:
- Open blockers:
- Next actions:
```
