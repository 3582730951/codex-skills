# Delegation Audit

Use this file when a plan claims to be multi-agent and you need to verify whether the delegation is real.

## Core Rule

A plan is only `real-multi-agent` if the runtime actually created distinct delegated workers with distinct ownership boundaries.

Role labels inside one main-agent response do not count as real delegation.

## Audit Procedure

Check the delegation claim in this order:

1. identify whether the runtime supports real delegation
2. list every claimed role in the roster
3. map each claimed role to a concrete worker identity, thread, or agent handle
4. verify each worker has a bounded context package and an owned output
5. verify reviewers are not the same worker as the implementer
6. verify the PM is still the main agent and is coordinating rather than impersonating all roles
7. verify the PM is not also the hidden owner of the engineer track

## Required Evidence For Real Delegation

Require evidence such as:

- delegated worker identifiers
- distinct owned tracks
- distinct write scopes or review scopes
- bounded context packages per worker
- independent reviewer outputs

If those artifacts do not exist, do not claim `real-multi-agent`.

## Failure Patterns

Mark delegation as failed if any of these happen:

- one main agent writes "Architect:", "Engineer:", and "Tester:" sections without real workers
- the plan uses plural role names but provides no worker identities
- the implementer and reviewer are the same worker
- reviewers rely on the implementer's own summary instead of primary artifacts
- the plan claims parallelism but all work is still serialized inside one thread even though real delegation is available
- the PM remains labeled PM but is also the undisclosed code author

## Verdicts

Use one of these verdicts:

- `pass-real-delegation`: real delegated workers exist for the critical tracks
- `pass-constrained-fallback`: the runtime cannot delegate, and the plan states `constrained-single-agent` honestly
- `fail-fake-multi-agent`: the runtime could delegate, but the plan only roleplays multiple agents
- `fail-unverifiable`: the plan claims delegation but provides no evidence

## Reporting Format

```text
Delegation Audit:
- Runtime Supports Real Delegation: yes | no | unknown
- Claimed Execution Mode: real-multi-agent | constrained-single-agent
- PM Identity: <main agent>
- Architect Worker: <worker id or none>
- Engineer Worker(s): <worker id(s) or none>
- Tester Worker: <worker id or none>
- Reviewer Worker(s): <worker id(s) or none>
- Distinct Ownership Verified: yes | no
- Independent Review Verified: yes | no
- Verdict: pass-real-delegation | pass-constrained-fallback | fail-fake-multi-agent | fail-unverifiable
- Notes:
```
