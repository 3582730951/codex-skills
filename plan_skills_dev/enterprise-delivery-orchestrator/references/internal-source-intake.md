# Internal Source Intake

Use this file when the team wants the skill to learn from existing internal source such as a proprietary protection engine, virtualization-based protection modules, internal runtime components, or previously shipped security products.

Treat internal source as task-local reference material, not as public skill content.

## Intake Rules

- Do not paste large proprietary code dumps into `SKILL.md` or public-facing reference files.
- Prefer a private local path or private repository checkout that the skill can read in the current workspace.
- Register the source root first with `scripts/register_internal_reference.py`.
- Load only the files relevant to the current task instead of bulk-loading the entire codebase into context.
- Derive summaries, boundaries, invariants, and compatibility notes before attempting edits.

## Required Metadata

For every internal source root, capture:

- product or module name
- owning team
- sensitivity level
- allowed use:
  - `reference-only`
  - `modify-in-place`
  - `port concepts with rewrite`
- license or IP basis
- supported platforms
- build system
- exported interfaces or major entrypoints
- known invariants
- known no-touch areas

## VMP / Protection Code Rule

When the internal source is a protection engine or a virtualization-based protection component:

- focus review on correctness, compatibility, observability, performance budget, and auditability
- preserve explicit ownership and provenance for reused ideas
- prefer controlled, explainable protection boundaries over opaque behavior
- do not introduce hidden persistence, anti-forensics, or undocumented cross-process control

## Recommended Workflow

1. Register the source root and generate a provenance register.
2. Build an `Engineering Baseline` from the actual internal codebase.
3. Summarize the modules, hooks, contracts, and tests relevant to the requested optimization.
4. Only then propose changes.
5. Record whether the result is a direct edit, a rewrite informed by internal patterns, or a new module with compatible contracts.

## Refusal Conditions

Stop and clarify if:

- ownership or allowed use is unclear
- third-party or partner code is mixed into the source without a clean basis
- the request asks for stealth, evasion, or non-auditable behavior under the label of "protection"
