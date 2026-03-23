# Delegation Audit

Use this file to verify whether the planning workflow is genuinely multi-agent.

## Real Delegation Test

Count a role as truly delegated only if:

- it maps to a real worker identity
- it owns a distinct planning artifact or track
- it receives a bounded context package

Sections inside one main-agent answer do not count.

## Required Critical Roles

When real delegation is available, require distinct workers for:

- architect
- engineer-planner
- tester-planner
- at least one reviewer

The main agent remains PM.

## Verdicts

- `pass-real-delegation`
- `pass-constrained-fallback`
- `fail-fake-multi-agent`
- `fail-unverifiable`
