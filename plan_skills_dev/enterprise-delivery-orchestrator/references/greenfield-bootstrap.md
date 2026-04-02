# Greenfield Bootstrap

Use this file when the repository is empty, nearly empty, or lacks a usable product baseline.

## Greenfield Detection

Treat the project as greenfield if one or more are true:

- there is no meaningful source tree yet
- only docs or placeholders exist
- there is no established app/service/runtime structure
- there is no build, lint, test, or packaging baseline

## Goal

Do not jump from an empty folder straight into feature coding.

First create the minimum product baseline that lets later implementation stay coherent:

- chosen stack
- repository layout
- quality toolchain
- architecture seams
- API / module contracts
- first release slice

## Required Bootstrap Artifact

```text
Greenfield Bootstrap Plan:
- Product type:
- Chosen stack:
- Why this stack:
- Top-level modules / apps:
- Build / run toolchain:
- Lint / format / type / test baseline:
- Environment / config strategy:
- API and data boundaries:
- UI or operator surface strategy:
- Initial release slice:
- Out-of-scope features:
- First milestone sequence:
```

## Bootstrap Sequence

1. clarify product class and target user
2. choose stack or present candidate stacks
3. define top-level module/app split
4. define quality toolchain
5. define API / function boundaries
6. define release-1 scope
7. only then scaffold and implement

When the stack matches a supported scaffold profile, prefer using `scripts/bootstrap_project.py` instead of rewriting the same starter files manually.

## Do Not

- generate a random boilerplate tree without explaining why
- install extra frameworks "just in case"
- start with infrastructure before product seams are defined
- create more packages/modules than the first release needs

## Parallel Greenfield Rule

Parallel work starts only after bootstrap artifacts exist.

Before that, the PM and Architect should converge on:

- top-level structure
- contracts
- ownership
- first milestone boundaries

Otherwise multiple agents will scaffold incompatible foundations.
