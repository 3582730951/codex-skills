---
name: multi-agent-plan-orchestrator
description: "PM-led high-assurance multi-agent planning and execution orchestration. Use when Codex, Claude, or another coding agent is writing a new plan, implementation plan, execution plan, task breakdown, technical design, roadmap, replan-from-scratch, or entering `/plan` or Plan mode. Also trigger for Chinese planning requests such as \u5199\u8BA1\u5212, \u505A\u65B9\u6848, \u4EFB\u52A1\u62C6\u89E3, \u6280\u672F\u65B9\u6848, \u5B9E\u65BD\u8BA1\u5212, \u6267\u884C\u8BA1\u5212, \u8DEF\u7EBF\u56FE, and \u91CD\u65B0\u89C4\u5212. Do not use for lightweight status-only plan updates or simple update_plan bookkeeping unless the task is being re-planned. Coordinate PM, architect, engineer, tester, architecture reviewer, security reviewer, and optional integrity auditor; preserve context integrity through task charters, architecture contracts, decision logs, and state snapshots; prevent shallow planning, fake progress, hardcoded pass conditions, or weak acceptance; and route models by capability tier."
---

# Multi-Agent Plan Orchestrator

## Overview

Start with a multi-agent plan by default for any non-trivial request. Put a PM role in charge first, then define parallel workstreams, file ownership, model tiers, and quality gates before implementation.

If the platform supports real subagents, spawn them in parallel. If it does not, simulate the same roles explicitly in one response and keep the same deliverables, review gates, and escalation rules.

The `main_agent` always serves as `PM`. Do not delegate PM ownership away from the main agent.

## Trigger Policy

Auto-use this skill when the agent is creating a new plan or entering a planning workflow.

Treat these as positive triggers:

- writing a new plan
- writing an implementation plan, execution plan, or technical design
- decomposing work before coding
- replanning from scratch after a reset
- entering `/plan` or Plan mode
- responding to common planning requests in another language, including Chinese planning prompts covered by the frontmatter description

Treat these as non-triggers unless the task is being re-planned:

- lightweight status-only plan updates
- simple `update_plan` bookkeeping with no new decomposition
- minor progress notes that do not redesign the work

## Choose The Operating Mode

Use one of these modes:

- `tiny`: Keep PM, engineer, and tester explicit. Treat architect and security as checkpoints instead of full-time agents.
- `standard`: Use PM, architect, engineer, tester, architecture reviewer, and security reviewer.
- `heavy`: Use the full roster, allow multiple engineers or testers, require blind review, and make file ownership and merge order explicit before edits.

Pick `tiny` only for low-risk, low-ambiguity work such as a small localized change. Pick `standard` or `heavy` for cross-file work, ambiguous requirements, architecture decisions, risky migrations, public APIs, authentication, payments, concurrency, data model changes, or production-impacting tasks.

Add high-assurance controls whenever the task is safety-critical, security-sensitive, contract-sensitive, audit-sensitive, or already showing context drift. High-assurance controls include blind review, immutable task artifacts, stop-the-line reset rules, and an optional integrity auditor.

If real subagents are available and permitted:

- `tiny`: the main agent may stay PM and absorb the smaller roles
- `standard` or `heavy`: the main agent must assign real subagents for at least architect, engineer, tester, and one reviewer

If real subagents are available but the plan still keeps all roles inside one main-agent roleplay, mark that as a process failure, not a valid multi-agent plan.

## Appoint The PM

Make the PM the mandatory orchestrator.

The `main_agent` is always the PM.

The PM must:

- restate the task in precise deliverables
- publish the initial `Task Charter`
- create the agent roster and assign owners
- assign model tiers based on task difficulty
- maintain the `Decision Log` and the latest `State Snapshot`
- block lazy plans, vague promises, and acceptance by hardcoding
- detect overlapping file ownership before coding starts
- resolve agent conflicts and sequencing when two agents want the same file
- require evidence for completion: tests, review notes, security checks, and known risks

Reject outputs that sound finished but do not show concrete artifacts, verification, or file ownership.

## Build The Agent Roster

Create the roster in this order:

1. `PM`: orchestration, acceptance, dependency tracking, anti-shortcut enforcement.
2. `Architect`: design boundaries, interfaces, decomposition, migration shape.
3. `Engineer`: implement one owned slice at a time.
4. `Tester`: define cases, run validation, challenge assumptions, look for false positives.
5. `Architecture Reviewer`: audit the architect and engineer for unnecessary complexity, coupling, and brittle interfaces.
6. `Security Reviewer`: audit threat surface, unsafe defaults, secret handling, and exploit paths.
7. `Integrity Auditor` (optional but recommended in `heavy` or high-assurance work): audit context hygiene, blind-review independence, and approval integrity.

Load [references/role-matrix.md](references/role-matrix.md) when assigning detailed responsibilities.

## Enforce Real Delegation When Available

Do not confuse role labels with real delegation.

If the runtime supports subagents or parallel delegated workers, a `standard` or `heavy` plan must assign real agents. The main agent may coordinate them, but should not pretend to be all of them in one thread.

Require the plan to state one of these execution modes:

- `real-multi-agent`: real delegated agents exist and own distinct tracks
- `constrained-single-agent`: the runtime cannot delegate or policy forbids delegation, so the main agent simulates the checkpoints sequentially

Do not claim `real-multi-agent` unless the roster maps to actual delegated workers.
Do not claim full multi-agent assurance from a `constrained-single-agent` fallback.

Load [references/delegation-audit.md](references/delegation-audit.md) when verifying whether the claimed roster maps to real delegated workers.

## Create Canonical Artifacts First

Before coding begins, create these canonical artifacts:

- `Task Charter`: the immutable statement of objective, scope, non-goals, constraints, acceptance criteria, forbidden shortcuts, and source-of-truth artifacts
- `Architecture Contract`: the architect's binding design and coding-rules package for non-`tiny` work
- `Decision Log`: append-only record of accepted and rejected decisions, with rationale
- `State Snapshot`: the latest compact summary of current truth, blockers, owned work, and next actions

Treat these artifacts as the only durable memory of the task.

If the chat history, an agent summary, or an older plan conflicts with the latest `State Snapshot`, prefer the `Task Charter`, then the `Decision Log`, then the latest `State Snapshot`.

Load [references/architecture-contract.md](references/architecture-contract.md) when drafting or reviewing the design.
Load [references/context-integrity.md](references/context-integrity.md) when packaging context, running rework loops, or recovering from drift.

## Plan Parallel Workstreams

Create a plan artifact with these headings:

```text
Execution Mode:
Assurance Level:
Task Summary:
Task Charter:
Agent Roster:
Delegation Map:
Canonical Artifacts:
Parallel Tracks:
File Ownership:
Dependencies:
Regression Perimeter:
Unchanged Guarantees:
Second-Order Risks:
Model Routing:
Context Packages:
Quality Gates:
Assurance Scorecard:
Merge Order:
Open Risks:
State Snapshot:
```

Make every parallel track concrete:

- assign one clear owner
- list owned files, modules, or decision surfaces
- state the output artifact expected from that role
- state what blocks the role and what can proceed independently
- state which canonical artifacts the role is allowed to rely on
- state which files or evidence the role must not edit directly
- state whether the role is a real delegated agent or a constrained single-agent checkpoint

Do not leave critical files without an owner. Do not let multiple agents edit the same file at the same time unless the PM has already staged a merge order.
Do not let reviewers approve work using the engineer's own conclusions as their primary evidence.

## Enforce File Ownership And Conflict Rules

Use a single writer per file by default.

When overlap appears:

1. make the PM pause the conflicting tracks
2. ask the architect to define a seam, interface, or extraction boundary
3. reassign one primary file owner
4. let secondary agents propose diffs, tests, or interface changes instead of direct concurrent edits
5. merge sequentially and re-run affected validation

Prefer splitting a large file into smaller owned units instead of letting multiple agents fight over one file.

Load [references/coordination-gates.md](references/coordination-gates.md) for conflict handling and acceptance gates.

## Map The Regression Perimeter Before Fixing Bugs

Do not treat the reproduced bug as the whole problem.

For any bug fix or behavior change, require a `Regression Perimeter` before implementation. The perimeter must identify:

- directly changed logic and data paths
- adjacent callers, callees, and shared helpers
- unchanged guarantees that must still hold
- probable failure scenarios and second-order side effects
- regression checks for the reproduced case and nearby cases

If the plan only proves that the original bug no longer reproduces, the plan is incomplete.

Load [references/regression-perimeter.md](references/regression-perimeter.md) when mapping likely collateral damage, unchanged guarantees, and probability-ranked risks.

## Require Detailed Design Before Coding

For any `standard` or `heavy` task, the architect must produce an `Architecture Contract` before the engineer writes code.

The contract must define:

- scope, non-goals, and invariants
- interfaces, data contracts, and failure handling
- file ownership boundaries and extension seams
- task-specific coding rules, not just generic style advice
- regression perimeter, unchanged guarantees, and probable failure scenarios
- validation hooks, test strategy, and rollback or migration notes
- explicit open questions and who owns each answer

If the design is too vague to derive concrete task cards for engineers and testers, stop and refine it. Do not let engineers "figure it out while coding" on medium or large tasks.

Load [references/architecture-contract.md](references/architecture-contract.md) for the full checklist and template.

## Run Blind Review And Anti-Collusion Controls

Require independent review for all non-`tiny` work.

Blind review means:

- reviewers see the `Task Charter`, relevant source artifacts, diffs, tests, and the `Architecture Contract`
- reviewers do not see another reviewer's verdict before submitting their own
- reviewers do not use the engineer's self-assessment as their main evidence
- the PM compares independent findings and resolves disagreement from raw artifacts

Never allow the same agent to both implement a change and be the sole approver of that same change.
Never accept "looks good" without artifact-based reasoning.

For `heavy` or high-assurance tasks, add the optional `Integrity Auditor` or make the PM explicitly perform the same checks.

Load [references/assurance-scorecard.md](references/assurance-scorecard.md) when quantifying whether the plan is truly detailed, independent, and stable enough to trust.

## Route Models By Difficulty

Route models by capability tier, not by habit.

- use the smallest fast model for retrieval, indexing, grep-style search, log triage, and mechanical summarization
- use a mid-tier model for focused implementation, unit tests, refactors with limited blast radius, and routine review
- use the strongest model for architecture, ambiguous debugging, cross-module refactors, security review, conflict resolution, and final acceptance

Treat concrete model names as replaceable examples, not hard requirements.

Resolve models in this order:

1. project or user-provided aliases such as `tier-small`, `tier-medium`, and `tier-strong`
2. the platform's currently available models, mapped by capability tier
3. an explicit policy file such as [references/model-policy-template.yaml](references/model-policy-template.yaml), adapted by the host environment
4. the default fallback examples in [references/model-routing.md](references/model-routing.md)

When the runtime can inspect or list available models, do that first and prefer the newest suitable model in the same tier.

When using OpenAI-family models and no explicit mapping is provided, prefer this fallback example unless the environment lacks one tier:

- retrieval and scan: `gpt-5.4-nano` if available, otherwise `gpt-5.4-mini`
- simple coding and test scaffolding: `gpt-5.4-mini`
- complex coding, architecture, final review, and security: `gpt-5.4`

When using a non-OpenAI platform such as Claude, keep the same small, medium, and strong tier semantics even if model names differ.

Always record both the abstract tier and the resolved concrete model name in the plan artifact when a concrete model has been chosen.

Load [references/model-routing.md](references/model-routing.md) when choosing tiers or escalation rules.
Load [references/model-policy-template.yaml](references/model-policy-template.yaml) when creating a portable model policy for a repository or team.

## Score The Plan Before Execution

For `standard` and `heavy` tasks, publish an `Assurance Scorecard` before implementation begins.

Score the plan on these dimensions:

- architecture completeness
- evidence coverage
- blast radius coverage
- review independence
- context integrity
- task continuity
- security coverage when the task touches risky surfaces
- delegation integrity when the runtime supports real subagents

Do not begin execution if the scorecard shows a plan that is vague, self-approving, context-polluted, or pretending to be multi-agent without real delegation.

Load [references/assurance-scorecard.md](references/assurance-scorecard.md) for the scoring rubric and failure thresholds.

## Manage Context Integrity And Rework

Package context intentionally instead of letting it accumulate indefinitely.

- give each role only the source artifacts, owned files, and checks needed for that role
- prefer raw artifacts over peer summaries
- expire stale assumptions when a new `State Snapshot` is published
- rebuild from canonical artifacts after repeated rework instead of relying on long chat history

Trigger a stop-the-line reset when any of these happen:

- the same defect or review finding is reopened twice
- two accepted decisions now conflict
- the file ownership map no longer matches the actual change surface
- three iterations pass without stable acceptance
- agents can no longer explain the current diff from the `Task Charter` and `Architecture Contract`

When a reset triggers:

1. freeze implementation
2. publish a fresh `State Snapshot`
3. update the `Decision Log` with what was learned and what was invalidated
4. ask the architect whether the `Architecture Contract` must change
5. restart only the affected workstreams with the refreshed context package

## Enforce Quality Gates

Require these gates before calling the task done:

- architect output reviewed by the architecture reviewer
- implementation validated by the tester
- security-sensitive surfaces reviewed by the security reviewer
- review independence verified by the PM or integrity auditor
- likely adjacent regressions reviewed, tested, or explicitly accepted as residual risk
- PM confirmation that the result solves the stated requirement without hidden shortcuts

Treat these as automatic rejection signals:

- hardcoded values only added to satisfy tests or demos
- disabled checks or weakened assertions to make the task appear complete
- no ownership for changed files
- no regression coverage for risky changes
- bug fixes that validate only the reproduced path and ignore adjacent paths
- architecture that ignores obvious coupling or migration fallout
- security-sensitive changes shipped without explicit review
- reviewers approving from summaries instead of primary evidence
- repeated rework with no refreshed `State Snapshot`
- `standard` or `heavy` plans that roleplay multiple agents even though real delegation is available

## Use The References

Read only the reference file needed for the current step:

- [references/role-matrix.md](references/role-matrix.md): detailed responsibilities, outputs, and red flags for each role
- [references/model-routing.md](references/model-routing.md): model tier mapping, escalation triggers, and downgrade rules
- [references/model-policy-template.yaml](references/model-policy-template.yaml): portable alias template for future model updates
- [references/assurance-scorecard.md](references/assurance-scorecard.md): quantitative gating for architecture quality, review independence, context integrity, and delegation integrity
- [references/regression-perimeter.md](references/regression-perimeter.md): blast-radius mapping, unchanged-guarantee checks, and probability-ranked failure scenarios
- [references/delegation-audit.md](references/delegation-audit.md): concrete audit steps for detecting fake multi-agent roleplay and verifying real delegated ownership
- [references/coordination-gates.md](references/coordination-gates.md): file ownership policy, anti-hardcoding checks, acceptance criteria, and conflict resolution workflow
- [references/architecture-contract.md](references/architecture-contract.md): required design sections, coding-rule expectations, and contract completeness checks
- [references/context-integrity.md](references/context-integrity.md): source-of-truth hierarchy, context packaging, blind review, and reset protocol
- [references/zh-plan-template.md](references/zh-plan-template.md): Chinese execution template for Codex planning and `/plan` mode
- [references/platform-adapter.md](references/platform-adapter.md): portable usage pattern for Codex, Claude, and other agents

## Output Style

Produce plans that are operational, not rhetorical.

Always show:

- the current `Task Charter` and `State Snapshot`
- who owns what
- what can run in parallel
- which files or modules are at risk of collision
- which model tier each role gets
- what evidence is required for acceptance

If real subagents are unavailable, still present the plan as if those roles exist, then execute the work sequentially while preserving the same checkpoints.
