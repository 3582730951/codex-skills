# Platform Adapter

Use this file when the same orchestration policy must work across Codex, Claude, or another agent runtime.

## Core Rule

Keep the workflow constant even when the platform changes:

- main agent serves as PM and leads
- architect defines boundaries
- engineers implement owned slices
- tester validates behavior
- architecture reviewer audits structure
- security reviewer audits threats

Only the execution mechanism changes.

## Codex-Style Runtime

If the runtime supports skills and subagents:

- invoke `$multi-agent-plan-orchestrator`
- keep the main agent as PM
- spawn real parallel agents when the task is not tiny
- let the PM assign models and coordinate merge order

For `standard` or `heavy` work, do not treat single-thread roleplay as equivalent to real multi-agent execution.

If the runtime supports skills but not real subagents:

- still invoke the skill
- simulate each role in explicit sections
- keep the same file ownership and gate rules

## Claude-Style Runtime

If the runtime does not support Codex skill discovery, paste the essential contract into the working prompt:

```text
Use a PM-led multi-agent workflow.
Create roles for PM, architect, engineer, tester, architecture reviewer, and security reviewer.
Assign one owner per file.
Plan parallel tracks before coding.
Reject shallow planning, hardcoded pass conditions, fake completion, and unreviewed risky changes.
Route small tasks to small models, routine coding to medium models, and architecture/security/final review to the strongest model.
Show execution mode, agent roster, file ownership, model routing, quality gates, merge order, and open risks.
```

Then execute the work either with real subagents, if the platform has them, or by simulating the roles sequentially.

## Portability Rule

Do not hard-code platform-specific tool names into the workflow itself.

Describe the workflow in terms of:

- roles
- ownership
- checkpoints
- escalation
- acceptance evidence

Translate only the mechanics:

- skill invocation
- subagent spawning
- model names
- review tooling

Translate model names last. Keep the tier contract first.
Prefer a repository-level model policy derived from [model-policy-template.yaml](model-policy-template.yaml) so new model generations do not require rewriting the workflow.
