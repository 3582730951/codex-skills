# Model Routing

Use this file when choosing models for subagents or when translating the skill to platforms with different model names.

## Stability Rule

Do not bind the workflow to a fixed generation of model names.

The stable contract is the capability tier:

- `tier-small`
- `tier-medium`
- `tier-strong`

Concrete model IDs are runtime bindings that may change over time.

## Capability Tiers

Treat model choice as a routing problem:

- `tier-small`: cheapest or fastest model that can reliably read, search, summarize, or classify
- `tier-medium`: balanced model for routine coding, scoped refactors, unit tests, and narrow reviews
- `tier-strong`: strongest model for architecture, ambiguity, security, conflict resolution, and final sign-off

## Resolution Order

Resolve concrete model names in this order:

1. user or repository policy, if it already defines tier aliases
2. platform-discovered currently available models
3. [model-policy-template.yaml](model-policy-template.yaml), adapted by the host environment
4. this file's fallback examples

If the platform exposes a model list or a recommended latest family for each tier, prefer that instead of freezing older names into the plan.

## Default OpenAI Mapping

Use this mapping as a fallback example, not as a permanent contract:

- `tier-small`: `gpt-5.4-nano` if the platform offers it; otherwise `gpt-5.4-mini`
- `tier-medium`: `gpt-5.4-mini`
- `tier-strong`: `gpt-5.4`

If OpenAI later introduces a better successor in the same cost and capability slot, the PM should swap to that newer model without rewriting the skill.

## Cross-Platform Rule

For Claude or other platforms, preserve the tier semantics and replace names with the closest small, medium, and strong options available in that environment.

Do not keep the literal model names if the platform does not provide them.
Do not force OpenAI names into a non-OpenAI environment.

## Routing Recommendations By Work Type

- retrieval, repo scan, grep analysis, issue triage, changelog extraction: `tier-small`
- simple code generation inside one clear boundary: `tier-medium`
- unit test authoring and routine bug fixing: `tier-medium`
- architecture, migration design, concurrency, debugging with unclear root cause: `tier-strong`
- security review, public API design, data model changes, acceptance arbitration: `tier-strong`

## Escalate To Tier-Strong When

- more than three modules interact
- the root cause is ambiguous
- the change touches persistence, auth, billing, or public contracts
- the tester finds failures that point to design issues rather than syntax issues
- two agents disagree on boundaries or implementation direction

## Downgrade To Smaller Tiers When

- the task is read-only or purely diagnostic
- the output is easy to verify mechanically
- the work is localized and the blast radius is small
- the agent is producing data for a stronger reviewing agent rather than final decisions

## PM Rule

Let the PM choose the cheapest model that can do the job without creating rework. Cheap first is good; cheap that causes retries is waste.

The PM must report routing like this:

```text
Model Routing:
- PM: tier-strong -> <resolved model or alias>
- Architect: tier-strong -> <resolved model or alias>
- Engineer A: tier-medium -> <resolved model or alias>
- Tester: tier-medium -> <resolved model or alias>
- Security Reviewer: tier-strong -> <resolved model or alias>
```

If the runtime cannot determine the concrete model names, keep the tier labels and state that the mapping must be resolved by the host environment.
