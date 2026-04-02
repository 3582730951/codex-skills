# Python Adapter

Use this file when changed surfaces are written in Python.

## Core Rules

- Add type hints to public and cross-module boundaries.
- Keep modules focused and side effects minimal.
- Validate external inputs at the boundary.
- Use exceptions that communicate the real failure mode.
- Prefer explicit data models over ad hoc dictionaries for important contracts.

## Quality Checks

- public functions and methods have meaningful names and annotations
- exception handling is specific, not blanket
- serialization boundaries are explicit
- tests cover normal and failing behavior

## Reject

- broad `except Exception` without re-raising or translation
- mutable default arguments
- modules that do heavy work at import time
- generic helper names with weak domain meaning

## Basis

- PEP 8: https://peps.python.org/pep-0008/
- PEP 257: https://peps.python.org/pep-0257/
- PEP 484: https://peps.python.org/pep-0484/
