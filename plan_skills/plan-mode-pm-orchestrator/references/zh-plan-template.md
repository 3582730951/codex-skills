# Chinese Plan Template

Use this template when the user wants the plan in Chinese or when `/plan` output should be concise and operational.

```text
Execution Mode:
- real-multi-agent | constrained-single-agent

Assurance Level:
- tiny | standard | heavy

Task Charter:
- Objective:
- Scope:
- Non-Goals:
- Acceptance Criteria:
- Constraints:
- Forbidden Shortcuts:
- Sources Of Truth:

Main PM:
- main_agent

Agent Roster:
- PM:
- Architect:
- Engineer-Planner:
- Tester-Planner:
- Reviewer:
- Security Reviewer:

Delegation Map:
- real delegated workers
- constrained fallback checkpoints

Architecture Contract Summary:
- boundaries
- interfaces
- invariants
- task-specific coding rules

Regression Perimeter:
- changed path
- adjacent paths
- unchanged guarantees
- second-order risks

Parallel Tracks:
- track / owner / dependencies / outputs

File Ownership:
- file or module -> owner

Model Routing:
- role -> tier -> resolved model or alias -> reason

Context Packages:
- what each role can rely on
- what each role must not rely on

Quality Gates:
- plan quality gate
- independence gate
- delegation gate

Assurance Scorecard:
- architecture completeness
- evidence coverage
- blast radius coverage
- review independence
- context integrity
- delegation integrity
- gate result

Open Risks:
- risk / owner / mitigation

State Snapshot:
- current truth
- accepted decisions
- blockers
- next actions
```
