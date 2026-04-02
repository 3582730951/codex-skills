# Repo Discovery Baseline

Use this file before architecture or coding. The goal is to teach the agent what "good" means in this repository before it writes anything.

## Required Discovery Pass

Inspect, at minimum:

- root manifests: `package.json`, `pyproject.toml`, `requirements*.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `CMakeLists.txt`, `Makefile`, `meson.build`
- lint, format, and type config
- test runners and existing test layout
- existing API and module structure
- logging, error, and configuration patterns
- CI or workflow files if they encode quality gates

## Engineering Baseline Output

Write a compact artifact with these sections:

```text
Engineering Baseline:
- Languages / frameworks:
- Source-of-truth configs:
- Existing architectural seams:
- Naming conventions:
- Module / package layout:
- API style:
- Function / method style:
- Error handling semantics:
- Validation location:
- Logging / observability conventions:
- Test conventions:
- Performance / concurrency constraints:
- Forbidden shortcuts:
- Applicable language adapters:
- Applicable system-layer rules:
```

## Priority Order

Resolve quality rules in this order:

1. repository conventions and explicit configs
2. task-specific architecture contract
3. language adapter rules
4. system-layer rules when relevant
5. fallback readability rubric

Never apply a generic preference that conflicts with a stronger repository rule.

## Stack Choice Rule

If the repository does not establish a stack:

- do not jump straight to implementation
- produce 2-3 candidate stacks with tradeoffs
- ask the user to choose if the decision materially affects delivery

## Failure Rule

If the agent cannot explain the repository's quality baseline, it is not ready to code.
