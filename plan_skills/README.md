# plan_skills

Planning-focused Codex skills.

## Skills

`plan-mode-pm-orchestrator`

- plan-only PM-led orchestration for `write plan`, `/plan`, Plan mode, task breakdown, and replanning

`multi-agent-plan-orchestrator`

- broader PM-led planning and execution orchestration with architecture, testing, review, security, and context-integrity controls

## Install From GitHub

Single skill:

```text
install-skill-from-github.py --repo 3582730951/codex-skills --path plan_skills/plan-mode-pm-orchestrator
install-skill-from-github.py --repo 3582730951/codex-skills --path plan_skills/multi-agent-plan-orchestrator
```

Clone-and-install all planning skills:

```powershell
git clone https://github.com/3582730951/codex-skills.git
cd codex-skills
python .\plan_skills\scripts\install_plan_skills.py
```

Restart Codex after installation.

## Sparse Checkout Only `plan_skills`

If users only want this folder:

```powershell
git clone --filter=blob:none --no-checkout https://github.com/3582730951/codex-skills.git
cd codex-skills
git sparse-checkout init --cone
git sparse-checkout set plan_skills
git checkout main
python .\plan_skills\scripts\install_plan_skills.py
```

Install only one skill:

```powershell
python .\plan_skills\scripts\install_plan_skills.py --skill plan-mode-pm-orchestrator
```

## Configure Codex

Codex reads local skills from:

- `$CODEX_HOME/skills`
- if `CODEX_HOME` is unset: `~/.codex/skills`

Default install:

```powershell
python .\plan_skills\scripts\install_plan_skills.py
```

Custom Codex home:

```powershell
$env:CODEX_HOME = 'D:\CodexHome'
python .\plan_skills\scripts\install_plan_skills.py
```

Manual destination override:

```powershell
python .\plan_skills\scripts\install_plan_skills.py --dest 'D:\CodexHome\skills'
```

After installation:

1. Restart Codex.
2. Open a new session.
3. Trigger the skills with planning prompts or explicit skill names.

Examples:

```text
/plan Create an execution plan for this task
Write a technical plan for this migration
帮我做任务拆解
Use $plan-mode-pm-orchestrator to write a plan
Use $multi-agent-plan-orchestrator to coordinate PM-led execution
```
