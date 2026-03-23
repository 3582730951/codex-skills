# Plan Output Spec

Use this file when writing the actual plan artifact.

## Required Sections

Write these sections in order:

```text
Execution Mode:
Assurance Level:
Task Charter:
Agent Roster:
Delegation Map:
Architecture Contract Summary:
Parallel Tracks:
File Ownership:
Dependencies:
Model Routing:
Context Packages:
Quality Gates:
Assurance Scorecard:
Open Risks:
State Snapshot:
```

## Output Rules

- keep the main agent as PM
- distinguish real delegated workers from fallback checkpoints
- map every track to an owner
- show which files or modules are at risk of collision
- show which evidence will be required in execution

## Failure Conditions

Reject the plan if:

- the PM role is not the main agent
- `standard` or `heavy` claims real multi-agent planning without real workers
- the architecture summary is too vague to derive concrete engineering tracks
- quality gates are missing
