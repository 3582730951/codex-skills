---
name: enterprise-delivery-orchestrator
description: "Enterprise-grade delivery orchestration for turning a requirement into a real product with clarification, product definition, architecture, UI direction, API contracts, implementation tracks, testing evidence, and independent review. Use when the user wants end-to-end delivery, not just a plan: requirement analysis, product design, UI/UX polish, frontend, backend, API design, testing, security review, system design, kernel/runtime/FFI work, launch readiness, authorization audit, proprietary source governance, code protection boundaries, or high-quality code with low AI-smell. Also trigger for TypeScript, React, Next.js, web frontend, dashboard, landing page, internal source intake, regulated security products, and Chinese requests such as 需求分析, 产品设计, UI美化, 前后端联动, 完整交付, 代码规范, API定义, 函数定义, 漏洞分析, 系统架构, 内核开发, 运行时, 驱动, 授权审计, 内部源码, 代码保护, Rust/C++/Python/Java/C coding quality."
---

# Enterprise Delivery Orchestrator

Use this skill when the user wants a requirement turned into a real deliverable with enterprise-grade controls rather than a loose implementation.

The `main_agent` is always `PM / Delivery Lead`. Do not hide the PM behind roleplay. In non-trivial work, the PM orchestrates, clarifies, assigns, gates, and tells the truth about what is not yet proven.

## Trigger Policy

Auto-use this skill when the request involves one or more of:

- turning a requirement into a shipped feature or product
- building a project from zero / greenfield delivery
- requirement analysis, product definition, or UX/UI direction
- frontend plus backend coordination
- TypeScript, React, Next.js, or browser-facing frontend delivery
- API design, contract design, or function boundary design
- code quality rescue, anti-sloppiness controls, or "make Codex write high-quality code"
- testing evidence, release readiness, or security review
- system design, low-level design, runtime, kernel, FFI, driver, concurrency, memory, ABI, or platform work
- authorized defensive system protection tools such as integrity monitors, config auditors, process scanners, hardening agents, or observability daemons
- proprietary internal source intake, source provenance, submission traceability, authorization annotation, or company audit preparation
- internal code protection runtime work that must stay explainable, authorized, and auditable
- Chinese requests such as `把需求完整落地`, `做成成熟产品`, `高质量代码`, `前后端+测试+安全`, `系统层`, `内核层`, `架构层`

Do not auto-use this skill for:

- plan-only requests with no execution or delivery expectation
- lightweight local edits that do not change product behavior or architecture
- pure writing, summarization, or casual advice

If the user only wants a plan, prefer the repository's planning skills instead.

## Core Promise

This skill enforces the following sequence:

1. Discover the repository and current constraints before proposing implementation details.
2. If the project is greenfield, bootstrap the product baseline before architecture.
3. Run a clarification gate for high-impact ambiguity.
4. Produce product, architecture, API, and function-boundary artifacts before coding.
5. Load the right language adapters and system constraints before writing code.
6. Reject low-quality, copied, or AI-generic code through explicit gates.
7. Require testing evidence and independent review before claiming delivery.

If the session did not actually follow this sequence, do not claim enterprise-grade delivery assurance.

## Operating Model

Read [references/operating-model.md](references/operating-model.md) at the start of any real task.

Always produce or update these artifacts:

- `Task Charter`
- `Engineering Baseline`
- `Greenfield Bootstrap Plan` when no usable project baseline exists
- `Product/Experience Brief`
- `Architecture Contract`
- `ADR`
- `API Contract Table`
- `Function Boundary Table`
- `Execution Contract`
- `Capability Routing Table`
- `Delegation Template Table`
- `Spawn Agent Template Table`
- `Plan Coverage Matrix`
- `Execution Ledger`
- `Requirement-to-Change Map`
- `Test Matrix + Evidence Log`
- `Threat Review`
- `Authorization Manifest` for regulated internal security products
- `Audit Annotation Register` when privileged or submission-sensitive files exist
- `Source Provenance Register` when internal or proprietary source is used as reference or implementation input
- `Platform Submission Notes` when source packaging or external submission is in scope
- `Claim-to-Evidence Map`
- `Review Package`
- `Release Readiness Checklist`
- `Decision Log`
- `State Snapshot`

Missing artifacts are not "to be filled later". They are evidence that the work is not ready for approval.

## Clarification First

The default ambiguity policy for this skill is strict clarification.

Do not guess on high-impact unknowns such as:

- product scope or non-goals
- public API shape or compatibility
- data ownership or migration behavior
- auth, permission, secret, or trust-boundary assumptions
- platform or language choice when the repository does not establish one
- runtime, locking, memory, ABI, or failure-domain assumptions in system work

Low-impact uncertainty may be handled with explicit assumptions recorded in the `Decision Log`.

## Load References Intentionally

Read only the references needed for the task:

- [references/trigger-boundary.md](references/trigger-boundary.md): when this skill should win, lose, or downgrade
- [references/feasibility-envelope.md](references/feasibility-envelope.md): what this skill can honestly deliver as a "complete product"
- [references/greenfield-bootstrap.md](references/greenfield-bootstrap.md): how to start from zero or near-zero repositories
- [references/project-bootstrap-gates.md](references/project-bootstrap-gates.md): minimum quality gates for brand-new projects
- [references/repo-discovery-baseline.md](references/repo-discovery-baseline.md): how to build the `Engineering Baseline`
- [references/artifact-templates.md](references/artifact-templates.md): exact artifact templates and minimum fields
- [references/plan-completeness-bar.md](references/plan-completeness-bar.md): reject shallow plans before coding
- [references/execution-discipline.md](references/execution-discipline.md): how to keep implementation aligned to locked plan steps
- [references/replan-protocol.md](references/replan-protocol.md): when and how to stop and replan
- [references/capability-routing.md](references/capability-routing.md): which work must use strongest models and strongest reasoning
- [references/escalation-and-delegation.md](references/escalation-and-delegation.md): when to escalate and how to keep reusable spawn templates
- [references/runtime-spawn-integration.md](references/runtime-spawn-integration.md): how to generate actual runtime-facing `spawn_agent` templates
- [references/api-contract-bar.md](references/api-contract-bar.md): API and function-boundary rules
- [references/readability-rubric.md](references/readability-rubric.md): code-quality scoring and veto items
- [references/anti-laziness.md](references/anti-laziness.md): reject fake progress, hardcoding, and unverifiable claims
- [references/conflict-stopline.md](references/conflict-stopline.md): stop-line and merge-order rules
- [references/delivery-gates.md](references/delivery-gates.md): approval, downgrade, and release truthfulness rules
- [references/ui-quality-bar.md](references/ui-quality-bar.md): only when UI or user-facing UX changes
- [references/originality-and-sourcing.md](references/originality-and-sourcing.md): anti-copying, naming, and sourcing controls
- [references/system-architecture-bar.md](references/system-architecture-bar.md): only for runtime, kernel, system, driver, FFI, JNI, ABI, concurrency, or memory-sensitive work
- [references/linux-system.md](references/linux-system.md): Linux defensive tool guidance
- [references/windows-system.md](references/windows-system.md): Windows defensive tool guidance
- [references/macos-system.md](references/macos-system.md): macOS defensive tool guidance
- [references/authorization-audit-bar.md](references/authorization-audit-bar.md): authorization, audit tags, and submission-traceability rules
- [references/internal-source-intake.md](references/internal-source-intake.md): how to use internal proprietary source as a local reference corpus
- [references/code-protection-boundaries.md](references/code-protection-boundaries.md): safe boundaries for internal protection-runtime work

Use the scripts when execution needs repeatable structure:

- `scripts/bootstrap_project.py`: create bounded greenfield scaffolds for supported stacks
- `scripts/bootstrap_system_tool.py`: create bounded defensive system-tool scaffolds
- `scripts/generate_execution_control.py`: create the locked execution artifacts
- `scripts/generate_capability_routing.py`: create the capability-routing artifact
- `scripts/generate_delegation_templates.py`: create reusable role and spawn templates
- `scripts/generate_spawn_agent_templates.py`: create runtime-facing spawn-agent payload templates
- `scripts/validate_delivery.py`: validate that artifact bundles satisfy required gates
- `scripts/score_plan_quality.py`: score whether the plan is complete enough to start coding
- `scripts/check_capability_routing.py`: verify that critical work is not assigned to weak tiers
- `scripts/check_spawn_agent_templates.py`: verify that runtime-facing spawn-agent templates match routing and templates
- `scripts/check_execution_alignment.py`: verify that execution stayed aligned to the locked plan
- `scripts/build_review_package.py`: generate a standard review package markdown file
- `scripts/capture_ui_evidence.py`: capture desktop/tablet/mobile screenshots plus Lighthouse metrics
- `scripts/score_code_quality.py`: produce a heuristic code-quality scorecard before manual review
- `scripts/generate_review_prompts.py`: generate independent reviewer prompts from a review package
- `scripts/generate_verdict_template.py`: generate a standard verdict template for each reviewer
- `scripts/generate_threat_model.py`: generate a bounded threat review artifact
- `scripts/run_system_checks.py`: run static checks for defensive system-tool projects
- `scripts/bootstrap_audit_bundle.py`: create authorization, annotation, provenance, and submission templates
- `scripts/register_internal_reference.py`: create a tracked provenance register for local proprietary source
- `scripts/scan_audit_annotations.py`: verify audit tags in sensitive files

Then load the repository's detected language adapters:

- [references/language-adapters/c.md](references/language-adapters/c.md)
- [references/language-adapters/cpp.md](references/language-adapters/cpp.md)
- [references/language-adapters/rust.md](references/language-adapters/rust.md)
- [references/language-adapters/python.md](references/language-adapters/python.md)
- [references/language-adapters/java.md](references/language-adapters/java.md)
- [references/language-adapters/typescript.md](references/language-adapters/typescript.md)
- [references/language-adapters/web-frontend.md](references/language-adapters/web-frontend.md)

If multiple languages are present, load every adapter that touches changed surfaces.

## Coding Rules

Before coding, derive a task-specific `Engineering Baseline` from the repository:

1. local repository standards
2. language adapter rules
3. system-layer rules when applicable
4. generic fallback rules

Never let generic adapter advice override a stronger local rule.

If the repository contains internal proprietary source or company protection-runtime code:

- do not paste large sensitive code blocks into the skill itself
- register the source root first and record ownership, sensitivity, and allowed use
- load only task-relevant files into context
- annotate privileged or submission-sensitive code with visible audit tags
- keep authorization and provenance artifacts in sync with the changed surfaces

If the repository is empty or lacks usable product structure:

- do not improvise file trees ad hoc
- load the greenfield references
- create the bootstrap artifacts first
- define the stack, quality tools, delivery scope, and first release boundary before implementation

Do not start implementation until these are defined:

- owned files and tracks
- API contracts
- function boundaries
- locked plan steps and release slice
- validation location
- error semantics
- tests and review evidence

Before coding on non-trivial work:

1. create or update the `Execution Contract`
2. create the `Capability Routing Table`
3. create the `Delegation Template Table`
4. create the `Spawn Agent Template Table`
5. create the `Plan Coverage Matrix`
6. run `scripts/score_plan_quality.py`
7. run `scripts/check_capability_routing.py`
8. run `scripts/check_spawn_agent_templates.py`
9. do not code if any plan dimension is below `4` or critical work is routed to weak tiers

During implementation:

- update the `Execution Ledger`
- cite `plan_step_id` and `requirement_id` in progress reasoning
- escalate critical blockers to strongest model tier instead of looping on weak workers
- if work drifts outside the locked plan, stop and use [references/replan-protocol.md](references/replan-protocol.md)

## Approval Rules

Use one of these execution modes:

- `real-multi-agent`: real delegated workers and independent reviewers exist
- `constrained-single-agent`: delegation is unavailable; the work may proceed, but approval claims are downgraded

Do not claim `3-agent approved` unless there are three real independent reviewers and their outputs are independently attributable.

Reviewer matrix:

- user-facing product/UI work: `Architecture Reviewer`, `UI Reviewer`, `Security Reviewer`
- system/kernel/runtime work: `Architecture Reviewer`, `Systems Reviewer`, `Security Reviewer`

`Tester` is not a reviewer slot. `Tester` owns the test evidence package. If testing is self-reported by the implementer, mark it explicitly and downgrade confidence.

## Delivery Truthfulness

This skill does not allow false completion claims.

If the work lacks clarification, artifacts, evidence, or independent review, say so plainly and stop the approval claim at the correct gate.

If the skill did not auto-trigger but the user expects enterprise-grade controls, tell them to restart with the explicit bootstrap prompt from [references/trigger-boundary.md](references/trigger-boundary.md).

Do not promise that any arbitrary request can become a fully complete product in one pass. Instead, use [references/feasibility-envelope.md](references/feasibility-envelope.md) to decide whether the request is:

- small enough for direct delivery
- suitable for parallel multi-agent delivery
- too broad and must be de-scoped into a credible release slice first
