# Code Protection Boundaries

Use this file when working on authorized code-protection, anti-tamper, integrity, or protection-runtime components inside the company's own product line.

This file exists to keep protection work reviewable and auditable. It does not authorize malware-like behavior or functionality that a reviewer cannot safely explain.

## Allowed Focus Areas

- integrity verification of owned binaries or assets
- tamper-evident checks with explicit rollback behavior
- signed configuration, update, or policy validation
- controlled hardening of owned execution paths
- compatibility and performance improvements in owned protection runtimes
- observability for protection failures and operator diagnosis

## Mandatory Design Notes

Before implementing, write down:

- protected asset or boundary
- expected attacker pressure or misuse case
- false-positive tolerance
- compatibility targets
- performance budget
- rollback or disable path
- operator-visible failure behavior

## Disallowed Directions

- hidden persistence outside the owned product boundary
- undocumented injection into unrelated processes
- anti-forensics or audit suppression
- unbounded anti-debugging changes that break legitimate support workflows
- data collection beyond the declared product boundary

## Review Expectations

Reviewers should verify:

- the protection logic is scoped to owned assets
- the failure mode is observable and reversible
- performance impact is measured or bounded
- audit tags and provenance notes exist for sensitive components
- no change relies on "security through obscurity" as the only control
