# Runtime Spawn Integration

Use this file when the runtime supports real subagents and you need artifacts that can be turned directly into `spawn_agent` calls.

## Core Rule

Do not stop at abstract routing.

For delegated work, produce a `Spawn Agent Template Table` that includes:

- the work item
- the routing template id
- the actual `spawn_agent` core parameters
- the fallback policy if the runtime cannot honor the requested model or reasoning
- a reusable message template

## Actual `spawn_agent` Fields

The runtime-facing template should at least specify:

- `agent_type`
- `model`
- `reasoning_effort`
- `fork_context`

Critical work should either:

- stay on the main agent, or
- have a frontier spawn template ready

## Fallback Rule

If the runtime cannot honor the template:

- `keep_local_if_runtime_cannot_honor` means do not delegate downward
- `block_or_reassign` means stop and choose a stronger valid template

## Validation

Use:

- `scripts/generate_spawn_agent_templates.py`
- `scripts/check_spawn_agent_templates.py`

to make runtime handoff concrete instead of implicit.
