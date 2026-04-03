# plan_skills_dev

Delivery-focused Codex skills.

## Skills

`enterprise-delivery-orchestrator`

- enterprise-grade requirement-to-product orchestration
- covers greenfield bootstrap, clarification, product definition, architecture, API/function contracts, implementation tracks, testing evidence, UI/system quality, security review, and release gates
- adds repository-aware code quality controls for C, C++, Rust, Python, Java, TypeScript, and web frontend projects
- includes runnable helper scripts for project bootstrap, UI evidence capture, code-quality scoring, and reviewer package generation
- includes platform guidance and tooling for authorized defensive system tools on Linux, Windows, and macOS
- includes audit, authorization, provenance, and internal-source workflows for regulated security products and proprietary protection code
- includes locked-plan controls so agents have to prove plan completeness and execution alignment
- includes capability-routing controls so planning, coding, and security review stay on strongest models and strongest reasoning

## Helper Scripts

Inside `enterprise-delivery-orchestrator/scripts/`:

- `bootstrap_project.py`
- `bootstrap_system_tool.py`
- `generate_execution_control.py`
- `generate_capability_routing.py`
- `validate_delivery.py`
- `score_plan_quality.py`
- `check_capability_routing.py`
- `check_execution_alignment.py`
- `build_review_package.py`
- `capture_ui_evidence.py`
- `score_code_quality.py`
- `generate_review_prompts.py`
- `generate_verdict_template.py`
- `generate_threat_model.py`
- `run_system_checks.py`
- `bootstrap_audit_bundle.py`
- `register_internal_reference.py`
- `scan_audit_annotations.py`

## Install From GitHub

Single skill:

```text
install-skill-from-github.py --repo 3582730951/codex-skills --path plan_skills_dev/enterprise-delivery-orchestrator
```

Clone-and-install this group:

```powershell
git clone https://github.com/3582730951/codex-skills.git
cd codex-skills
python .\scripts\install_repo_skills.py --group plan_skills_dev
```

Restart Codex after installation.

## Configure Codex

Codex reads local skills from:

- `$CODEX_HOME/skills`
- if `CODEX_HOME` is unset: `~/.codex/skills`

Examples:

```text
Use $enterprise-delivery-orchestrator to take this requirement from clarification to release with high-quality code and independent review
用 $enterprise-delivery-orchestrator 按企业级流程把这个需求从澄清到交付完整落地
```
