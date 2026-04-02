# Trigger Boundary

Use this file to decide when this skill should run and how to recover when it did not trigger.

## Prefer This Skill When

- the user wants a requirement turned into a mature feature or product
- the user wants to start a project from zero
- the request spans product thinking, UI, backend, testing, or security
- the user asks for "high-quality code", "no AI smell", "enterprise-grade", or similar quality guarantees
- the work touches public APIs, function contracts, migrations, launch readiness, or system architecture
- the work touches low-level surfaces such as FFI, JNI, runtime, kernel, driver, allocator, concurrency, or ABI

## Prefer Planning Skills Instead When

- the user explicitly wants only a plan
- the user wants decomposition or technical design without execution
- the task is clearly a light local change with no delivery orchestration need

## Startup Truthfulness

If the session did not begin with this skill but the user expects enterprise-grade delivery controls, say so.

Use this bootstrap prompt:

```text
Use $enterprise-delivery-orchestrator to take this requirement from clarification to architecture, implementation, testing, and release with repository-aware code quality, API/function contracts, originality checks, and independent review.
```

Chinese bootstrap prompt:

```text
用 $enterprise-delivery-orchestrator 按企业级流程把这个需求从澄清、产品定义、架构、编码、测试到交付完整落地，要求遵循仓库语言规范、定义 API 与函数边界、拒绝抄袭和 AI 味、并走独立审查。
```

## Conflict With Other Skills

When multiple skills could trigger:

1. this skill owns end-to-end delivery orchestration
2. specialized implementation skills may still be loaded during implementation
3. final acceptance still belongs to this skill's delivery gates

Examples:

- UI implementation may load `frontend-design` or `frontend-skill`
- system work may load platform-specific skills if available
- plan-only tasks should be routed away from this skill
