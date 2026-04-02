# UI Quality Bar

Use this file only when the task changes user-facing UI or UX.

## Applicability

- user-facing pages, screens, flows, dashboards, settings, and major components
- marketing, editorial, or product surfaces

Mark UI review as `N/A` only when no user-facing surface changed.

## Gate 1: Design Direction Review

Required artifact:

```text
Design Direction Review:
- Target user:
- Task goal:
- Visual thesis:
- Content hierarchy:
- Interaction thesis:
- Existing design system or new token system:
- Type scale:
- Spacing scale:
- Component states:
- Inspiration log:
- Explicit don't-do list:
```

Do not start UI implementation before this gate passes.

## Gate 2: Implementation QA

Required evidence:

- desktop screenshots
- tablet screenshots
- mobile screenshots
- key interaction recording or precise reproduction steps
- token list for typography, color, spacing, radius, and motion
- keyboard / focus / contrast results
- responsive behavior summary
- performance / layout-stability summary

If a specific item truly does not apply, mark it `N/A` and explain why.

Use `scripts/capture_ui_evidence.py` when the site is runnable and you want repeatable screenshot and Lighthouse evidence.

## Scoring

Score each dimension from `0` to `5`.

- Typography and hierarchy
- First-screen composition
- Color and token coherence
- Motion purpose
- Responsive execution
- Accessibility
- Brand / content clarity
- Performance stability

### Score Meaning

- `0`: broken or absent
- `3`: serviceable but generic
- `4`: strong and deliberate
- `5`: unusually polished and distinctive

Pass rule:

- every applicable dimension must be `>= 4`
- no veto item may appear

## Veto Items

- unreadable text or weak contrast
- broken mobile layout
- no visible focus states
- key interaction does not work
- default-looking UI with no system reason
- copied layout or visual identity from a third party
- asset license is unknown

## Design-System Branching

If the product already has a design system:

- follow it
- improve within its token and component boundaries
- do not invent a parallel visual system for novelty

If the product has no design system:

- define tokens, type scale, and spacing scale first
- then implement
