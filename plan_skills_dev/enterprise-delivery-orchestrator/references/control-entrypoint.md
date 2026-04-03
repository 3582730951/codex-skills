# Unified Control Entrypoint

Use `scripts/run_delivery_control.py` when the task needs one stable command surface instead of several manual script calls.

Use it for four common paths:

- `bootstrap-project`: create a bounded greenfield scaffold through `bootstrap_project.py`
- `plan-runtime`: generate `Execution Contract`, `Capability Routing Table`, `Delegation Template Table`, and `Spawn Agent Template Table`
- `review-bundle`: generate `Review Package`, reviewer prompts, and reviewer verdict templates
- `capture-ui`: capture screenshot and Lighthouse evidence through the same entrypoint

Rules:

- Prefer this entrypoint when the task is on the critical path and you want fewer manual steps.
- Do not reimplement the logic from the underlying scripts inside the main agent. Call the entrypoint or the underlying scripts.
- `plan-runtime` should usually run with `--run-checks` so routing, spawn templates, plan quality, and delivery gates are validated immediately.
- If a delegated work item has no `delegation_template_id`, stop and fix routing rather than inventing runtime parameters ad hoc.
- Keep this file short. Detailed policy still lives in the original references and scripts.
