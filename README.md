# codex-skills

Reusable Codex skills organized by category.

## Repository Layout

```text
plan_skills/
  multi-agent-plan-orchestrator/
  plan-mode-pm-orchestrator/
  scripts/
    install_plan_skills.py
plan_skills_dev/
  enterprise-delivery-orchestrator/
scripts/
  install_repo_skills.py
```

Each installable skill is a directory that contains `SKILL.md`.

## Install One Skill From GitHub

Use Codex's GitHub skill installer against a single path inside this repo:

```text
install-skill-from-github.py --repo 3582730951/codex-skills --path plan_skills/plan-mode-pm-orchestrator
install-skill-from-github.py --repo 3582730951/codex-skills --path plan_skills/multi-agent-plan-orchestrator
install-skill-from-github.py --repo 3582730951/codex-skills --path plan_skills_dev/enterprise-delivery-orchestrator
```

Equivalent URL form:

```text
install-skill-from-github.py --url https://github.com/3582730951/codex-skills/tree/main/plan_skills/plan-mode-pm-orchestrator
```

After installation, restart Codex.

## Install The Whole Repository

Clone the repo and install every discovered skill:

```powershell
git clone https://github.com/3582730951/codex-skills.git
cd codex-skills
python .\scripts\install_repo_skills.py
```

Install only one group:

```powershell
python .\scripts\install_repo_skills.py --group plan_skills
python .\scripts\install_repo_skills.py --group plan_skills_dev
```

Install only selected skills:

```powershell
python .\scripts\install_repo_skills.py --skill plan-mode-pm-orchestrator --skill multi-agent-plan-orchestrator
python .\scripts\install_repo_skills.py --skill enterprise-delivery-orchestrator
```

List discovered skills without copying anything:

```powershell
python .\scripts\install_repo_skills.py --list
```

Default install destination:

- `$CODEX_HOME/skills`
- if `CODEX_HOME` is unset: `~/.codex/skills`

After installation, restart Codex.

## Install Only `plan_skills`

If users only want the planning skills, they do not need the rest of the repository.

Use Git sparse checkout:

```powershell
git clone --filter=blob:none --no-checkout https://github.com/3582730951/codex-skills.git
cd codex-skills
git sparse-checkout init --cone
git sparse-checkout set plan_skills
git checkout main
python .\plan_skills\scripts\install_plan_skills.py
```

Install only one planning skill after sparse checkout:

```powershell
python .\plan_skills\scripts\install_plan_skills.py --skill plan-mode-pm-orchestrator
```

Users can also download only the `plan_skills` directory contents, then run:

```powershell
python .\plan_skills\scripts\install_plan_skills.py
```

After installation, restart Codex.

## Install Only `plan_skills_dev`

If users only want the delivery orchestration skill:

```powershell
git clone --filter=blob:none --no-checkout https://github.com/3582730951/codex-skills.git
cd codex-skills
git sparse-checkout init --cone
git sparse-checkout set plan_skills_dev
git checkout main
python .\scripts\install_repo_skills.py --group plan_skills_dev
```

After installation, restart Codex.

## Configure Codex

Codex discovers local skills from:

- `$CODEX_HOME/skills`
- if `CODEX_HOME` is unset: `~/.codex/skills`

Recommended options:

```powershell
# Option 1: install planning skills only
python .\plan_skills\scripts\install_plan_skills.py

# Option 2: install delivery skills only
python .\scripts\install_repo_skills.py --group plan_skills_dev

# Option 3: set a custom Codex home first
$env:CODEX_HOME = 'D:\CodexHome'
python .\scripts\install_repo_skills.py --group plan_skills_dev
```

Expected installed paths:

```text
%USERPROFILE%\.codex\skills\plan-mode-pm-orchestrator
%USERPROFILE%\.codex\skills\multi-agent-plan-orchestrator
%USERPROFILE%\.codex\skills\enterprise-delivery-orchestrator
```

After copying or installing skills:

1. Restart Codex.
2. Start a new session if needed.
3. Use natural planning prompts or explicit skill invocation.

Examples:

```text
/plan Build an implementation plan for this feature
Help me write a technical plan for this refactor
帮我写一个实现计划
Use $plan-mode-pm-orchestrator to decompose this task
Use $multi-agent-plan-orchestrator to run PM-led planning and execution
Use $enterprise-delivery-orchestrator to take this requirement from clarification to release with high-quality code and independent review
用 $enterprise-delivery-orchestrator 按企业级流程把这个需求从澄清到交付完整落地
```

## Planning Skills

`plan_skills/plan-mode-pm-orchestrator`

- plan-only skill for `write plan`, `/plan`, Plan mode, task breakdown, and re-planning
- keeps `main_agent` as PM
- requires real delegated subagents when the runtime supports them

`plan_skills/multi-agent-plan-orchestrator`

- broader PM-led planning and execution orchestration
- adds architecture, testing, review, security, context integrity, and anti-fake-multi-agent controls

## Delivery Skills

`plan_skills_dev/enterprise-delivery-orchestrator`

- enterprise-grade requirement-to-product orchestration
- adds clarification, product definition, API/function contract design, testing evidence, system and UI quality gates, originality checks, and release truthfulness
- includes repository-aware language adapters for C, C++, Rust, Python, Java, TypeScript, and web frontend work, plus extra controls for kernel/runtime/system-layer work
- includes runnable helper scripts for greenfield scaffolding, UI evidence capture, code-quality scoring, reviewer package generation, and regulated internal security-product audit/provenance workflows
- includes locked-plan execution controls to reduce shallow plans and implementation drift
- includes capability-routing controls to keep critical work on stronger models and stronger reasoning

## Notes

- Skill auto-triggering depends on each user's local Codex discovering the skill in their own `~/.codex/skills` or `$CODEX_HOME/skills`.
- Repository availability alone is not enough. Each user must install the skill locally, then restart Codex.
