# Project Bootstrap Gates

Use this file for brand-new projects to ensure the first scaffold is not low-quality by default.

## Required Bootstrap Gates

### Scope Gate

Must exist:

- product type
- target user
- release-1 scope
- explicit non-goals

### Stack Gate

Must exist:

- chosen stack or shortlisted options
- reason for the choice
- package/build strategy
- environment strategy

### Quality Tooling Gate

Must exist:

- formatter
- linter
- tests
- type or compile checks appropriate to the language

### Architecture Gate

Must exist:

- top-level module or app split
- public boundary list
- file ownership plan
- error and validation strategy

### Product Gate

Must exist for user-facing products:

- UI direction or operator workflow
- navigation or entry path
- core user flow list

## Automatic Bootstrap Failures

Fail bootstrap if:

- the stack is chosen by habit with no product reason
- boilerplate is generated with no release-1 boundary
- no lint/test/tooling baseline exists
- no contract exists between major modules
- more modules are created than the first release needs

## Bootstrap Completion Rule

Greenfield implementation may start only after all required bootstrap gates pass.
