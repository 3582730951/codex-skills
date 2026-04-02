# Authorization And Audit Bar

Use this file when the task involves:

- a regulated internal codebase
- a system-level security product
- privileged defensive tooling
- source packages that must be prepared for external platform submission
- proprietary protection code that needs traceable authorization and audit evidence

This file does not authorize stealth, anti-forensics, hidden persistence, or behavior that cannot be explained to an internal auditor.

## Required Extra Artifacts

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

Audit Annotation Register:
- File / symbol:
- Required tags:
- Owner:
- Last reviewed:
- Related artifact or evidence:

Source Provenance Register:
- Source root or package:
- Owner / team:
- Sensitivity:
- Allowed use:
- License / IP basis:
- Modification policy:
- Submission status:

Platform Submission Notes:
- Submission target:
- Included source roots:
- Omitted or redacted items:
- Build instructions:
- Reviewer:
- Traceability links:
```

## Mandatory Annotation Tags

Sensitive or privileged files must carry comment annotations near the file header or the relevant symbol boundary.

Required tags:

- `AUTHORIZATION:` why this capability exists and who authorized it
- `SECURITY-BOUNDARY:` what the code can touch and what it must not touch
- `AUDIT:` where the related manifest or evidence lives
- `PROVENANCE:` whether the code is internal original work, internal reference-derived, or third-party with approved basis

Optional tag:

- `SUBMISSION:` external platform packaging or submission note reference

## Rules

- No privileged or security-sensitive code path should exist without a visible authorization note.
- No imported internal source should be used without provenance and allowed-use tracking.
- If a code path changes privilege level, persistence, or data-access scope, update the authorization manifest before approval.
- If submission packaging is in scope, keep submission notes in sync with the actual source roots and build steps.
- If provenance is mixed or unclear, stop implementation until ownership and allowed use are resolved.

## Reviewer Focus

Reviewers should challenge:

- undocumented privilege assumptions
- file or symbol surfaces with no audit tags
- internal source reuse with unclear ownership or allowed use
- source packages that cannot be reconstructed from the submission notes
- comments that sound official but do not identify a real artifact

## Basis

- least-privilege design
- auditable change control
- traceable provenance for proprietary code
