# Operating Model

Use this file to run the skill like an enterprise delivery team rather than a single coder improvising.

## Roles

- `PM / Delivery Lead`: owns scope, sequencing, quality gates, truthfulness, and final delivery status.
- `Product Analyst`: clarifies user goals, success criteria, journeys, and non-goals.
- `UX / UI Lead`: owns design direction, information hierarchy, and user-facing quality.
- `Architect`: owns module boundaries, contracts, failure semantics, and track decomposition.
- `Frontend Engineer`: owns user-facing implementation tracks.
- `Backend Engineer`: owns services, storage, integration, and contract implementation tracks.
- `Systems Engineer`: owns low-level, runtime, kernel, FFI, ABI, concurrency, and resource-sensitive tracks.
- `Tester`: owns test matrix, evidence log, execution notes, and residual-risk disclosure.
- `Architecture Reviewer`: independently reviews structure, boundaries, and long-term maintainability.
- `UI Reviewer`: independently reviews user-facing quality when UI is in scope.
- `Systems Reviewer`: independently reviews low-level safety, performance assumptions, concurrency, and boundary handling when system work is in scope.
- `Security Reviewer`: independently reviews trust boundaries, unsafe defaults, secrets, and exploit paths.
- `Integrity Auditor` (optional): reviews contamination, fake progress, and approval integrity.

## Required Phases

### 1. Intake And Repo Discovery

Outputs:

- `Task Charter`
- initial `State Snapshot`
- repository inventory
- candidate languages and frameworks
- `Engineering Baseline`
- `Source Provenance Register` when internal or proprietary source is in scope

Do not design before understanding the current repository.

### 2. Greenfield Bootstrap Gate

Run this phase only when no usable project baseline exists.

Outputs:

- `Greenfield Bootstrap Plan`
- stack choice or bounded options
- top-level ownership and module split
- bootstrap quality toolchain
- `Authorization Manifest` and audit bundle for regulated internal security products

Do not parallelize implementation before this gate passes.

### 3. Clarification Gate

Outputs:

- clarified goals, constraints, and acceptance
- explicit open questions
- logged assumptions for low-impact gaps only
- initial `Execution Contract` with a release slice and replan triggers
- initial `Capability Routing Table`
- initial `Delegation Template Table`
- initial `Spawn Agent Template Table` when delegated execution is possible

Block implementation if any unresolved ambiguity can change contracts, security, architecture, or stack choice.

### 4. Product / Experience Definition

Outputs:

- `Product/Experience Brief`
- user journeys or operator flows
- success criteria
- non-goals
- UI design direction when relevant

### 5. Architecture And Contracts

Outputs:

- `Architecture Contract`
- `ADR`
- `API Contract Table`
- `Function Boundary Table`
- `Plan Coverage Matrix`
- file and track ownership
- audit tag plan for privileged or submission-sensitive files

### 6. Implementation Tracks

Outputs:

- implementation in owned files only
- updated `Execution Ledger`
- updated `Requirement-to-Change Map`
- updated `Claim-to-Evidence Map`
- executed tests or explicit gaps

Default ownership:

- one primary owner per file
- shared boundaries require a seam defined by `Architect`
- reviewer roles do not co-author implementation files

Parallel delivery is allowed only after:

- bootstrap artifacts exist
- contracts are written
- ownership is explicit
- merge order is known for shared seams
- capability routing is locked

### 7. Independent Review

Outputs:

- reviewer findings
- reviewer verdicts
- residual-risk disclosure

Reviewer matrix:

- product/UI work: architecture + UI + security
- system/kernel/runtime work: architecture + systems + security
- mixed work: architecture + UI or systems depending on touched surfaces + security

### 8. Release Gate

Outputs:

- `Release Readiness Checklist`
- final `State Snapshot`
- explicit delivery status:
  - `approved`
  - `approved with residual risk`
  - `approval pending external review`
  - `not approved`

## Execution Modes

### real-multi-agent

Use only when real delegated workers and reviewers exist.

Requirements:

- reviewer outputs must be independently attributable
- reviewers must not see one another's verdicts before submitting their own
- PM must keep role ownership distinct
- critical work classes must use frontier routing with high or xhigh reasoning

### constrained-single-agent

Use when delegation is unavailable.

Requirements:

- do not claim `3-agent approved`
- produce three independent `Review Package`s and three review prompts for external execution
- downgrade delivery status to `approval pending external review`

## PM Rules

The PM must:

- keep the task honest
- stop implementation when gates are missing
- restate blockers precisely
- maintain `Decision Log` and `State Snapshot`
- treat the locked plan as executable control, not background notes
- route critical work to the strongest available model tier instead of the cheapest available worker
- refuse false confidence and fake review claims
- stop regulated work when provenance, authorization, or submission traceability is missing

The PM must not:

- silently take over engineering work while still claiming independence
- treat style-only output as product maturity
- pass a task whose evidence cannot be audited

## Complete Product Rule

The PM may call something a "complete product" only when it is complete relative to an explicit release slice, not relative to every possible future feature.

If the requested scope is too large, the PM must reduce it to a credible release boundary before implementation.

## Basis

- Google Engineering Practices: small, reviewable changes and evidence-driven review  
  https://google.github.io/eng-practices/
- GitHub pull request reviews and required review enforcement  
  https://docs.github.com/github/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews
- Martin Fowler on Architecture Decision Records  
  https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
