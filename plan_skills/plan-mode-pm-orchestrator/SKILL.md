---
name: plan-mode-pm-orchestrator
description: "Plan-only PM-led orchestration for Codex planning workflows. Use when writing a new plan, implementation plan, execution plan, task breakdown, technical design, replan-from-scratch, roadmap, or entering `/plan` or Plan mode. Also trigger for Chinese planning requests such as \u5199\u8BA1\u5212, \u505A\u65B9\u6848, \u4EFB\u52A1\u62C6\u89E3, \u6280\u672F\u65B9\u6848, \u5B9E\u65BD\u8BA1\u5212, \u6267\u884C\u8BA1\u5212, \u8DEF\u7EBF\u56FE, and \u91CD\u65B0\u89C4\u5212. Do not use for simple update_plan bookkeeping, status-only updates, or direct implementation after a plan already exists. Keep the main agent as PM, require real delegated subagents when the runtime supports them, and output task charter, delegation map, architecture contract summary, file ownership, quality gates, and an assurance scorecard."
---

# Plan Mode PM Orchestrator

## Overview

Use this skill only for planning. The job is to produce a trustworthy execution plan before coding, not to perform the implementation itself.

The `main_agent` always serves as `PM`. Do not delegate PM ownership away from the main agent.

## Trigger Policy

Auto-use this skill for:

- new plan drafting
- implementation plan writing
- execution plan writing
- technical design and task breakdown
- replanning after a reset
- `/plan` or Plan mode

Do not use this skill for:

- simple `update_plan` maintenance
- progress-only updates
- execution after an approved plan already exists

## Execution Mode

Require one of these modes:

- `real-multi-agent`: the runtime supports real delegated workers, and the main agent assigns actual subagents to critical planning roles
- `constrained-single-agent`: the runtime cannot delegate or policy forbids it, so the main agent simulates the checkpoints sequentially

If real delegation is available, `standard` and `heavy` planning must use real delegated workers for at least architect, engineer-planner, tester-planner, and one reviewer.

## PM Rule

The main agent, acting as PM, must:

- publish the `Task Charter`
- choose the assurance level
- assign the planning roster
- publish the delegation map
- require an architecture contract summary before finalizing the plan
- publish an assurance scorecard
- refuse fake multi-agent roleplay when real delegation exists

## Required Plan Outputs

Always produce these sections:

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

Treat any missing section as a degraded plan.

## Delegation And Independence Rules

Do not accept a plan as high-assurance unless:

- the main agent stays PM
- delegated roles map to real workers when the runtime supports them
- reviewers are independent from implementers
- the plan states clearly when it is falling back to `constrained-single-agent`

Load [references/delegation-audit.md](references/delegation-audit.md) when checking whether the claimed roster is real.

## Scoring Rule

Score the plan before approving it.

Required dimensions:

- architecture completeness
- evidence coverage
- review independence
- context integrity
- delegation integrity when real delegation is available

Load [references/plan-scorecard.md](references/plan-scorecard.md) for the thresholds.

## References

Read only what you need:

- [references/plan-output-spec.md](references/plan-output-spec.md): required sections and output expectations
- [references/delegation-audit.md](references/delegation-audit.md): how to detect fake multi-agent planning
- [references/plan-scorecard.md](references/plan-scorecard.md): plan-only scoring thresholds
- [references/zh-plan-template.md](references/zh-plan-template.md): Chinese plan template for `/plan` mode

## Output Style

Produce an operational plan, not a motivational summary.

Always show:

- that `main_agent` is PM
- whether delegation is real or constrained
- who owns each track
- what evidence will be required later
- whether the plan passed the assurance gate
