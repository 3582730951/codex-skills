# Web Frontend Adapter

Use this file when the task changes a browser-facing UI implemented in modern web stacks such as React, Next.js, or TypeScript frontend applications.

## Core Rules

- Start from product hierarchy, not component count.
- Define page-level data flow and state boundaries before writing components.
- Prefer design tokens and layout systems over per-component styling improvisation.
- Accessibility, responsive behavior, and interaction states are part of the implementation contract.

## Architecture Checks

- route structure and page ownership are explicit
- shared UI primitives are extracted only after a real repeated pattern exists
- server/client boundaries are justified
- forms define validation, error, and success states
- loading and empty states are designed, not left implicit

## Quality Checks

- the first screen has a clear hierarchy and product purpose
- CSS or styling tokens are centralized
- keyboard and focus behavior is preserved
- responsive layout is intentional at mobile and desktop sizes
- component APIs are small and specific

## Reject

- default card-grid dashboards with no product rationale
- styling scattered inline with no token system
- components that are generic to the point of hiding the domain
- pages that only look correct at one viewport size

## Pairing Rule

Load this file together with:

- `ui-quality-bar.md` for user-facing quality gates
- `typescript.md` when the frontend code is written in TypeScript
- `scripts/capture_ui_evidence.py` when the application is runnable and browser evidence is needed
