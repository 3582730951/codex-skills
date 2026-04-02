# Readability Rubric

Use this rubric before approving code. The goal is not style purity. The goal is code that another strong engineer can trust quickly.

## Scoring

Score each required dimension from `0` to `5`.

- `0`: missing or dangerously unclear
- `1`: mostly unusable or misleading
- `2`: partial but risky
- `3`: workable with notable debt
- `4`: strong and trustworthy
- `5`: strong, crisp, and obviously maintainable

## Required Dimensions

- Naming quality
- Function responsibility
- Module / package boundary clarity
- API predictability
- Error-handling consistency
- Resource / lifetime safety
- Concurrency safety when relevant
- Testability
- Observability
- Auditability for privileged code
- Abstraction restraint
- Repository consistency
- Low AI-smell

## Low AI-Smell Criteria

Score low if the code shows:

- template-like naming with little domain vocabulary
- unnecessary wrappers or layered abstractions
- comments that narrate obvious code instead of explaining intent
- generic CRUD or card-grid structures copied from common AI patterns
- interfaces shaped by convenience rather than product semantics

Score high if the code shows:

- task-specific vocabulary
- boundaries aligned to actual domain responsibilities
- local consistency with the repository
- clear intent with restrained abstraction

## Veto Items

Reject immediately if any of these appear:

- generic placeholder naming in public or central code paths
- public interfaces with no explicit contract
- unsafe or resource-sensitive code with no ownership explanation
- privileged or submission-sensitive code with no visible AUTHORIZATION / AUDIT / PROVENANCE trail
- test changes that only hide failures
- hardcoded pass conditions
- architecture or module boundaries that the reviewer cannot explain

## Gate Rule

Every required dimension must score `>= 4` before approval.

Use `scripts/score_code_quality.py` for a heuristic first pass before human review. Treat it as a gate aid, not a replacement for reviewer judgment.

## Basis

- Google reviewer guidance on readability, naming, tests, and maintainability  
  https://google.github.io/eng-practices/review/reviewer/looking-for.html
