#!/usr/bin/env python3
"""Unified control entrypoint for enterprise delivery orchestration."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
PYTHON = sys.executable


def run_python(script_name: str, args: list[str]) -> None:
    command = [PYTHON, str(SCRIPT_DIR / script_name), *args]
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_template_ids(capability_routing_path: Path) -> list[str]:
    text = read_text(capability_routing_path)
    seen: set[str] = set()
    ordered: list[str] = []
    for match in re.finditer(r"(?m)^\s+delegation_template_id:\s*(\S+)\s*$", text):
        template_id = match.group(1)
        if template_id not in seen:
            seen.add(template_id)
            ordered.append(template_id)
    return ordered


def run_bootstrap_project(args: argparse.Namespace) -> None:
    forward = [
        "--project-root",
        args.target_dir,
        "--stack",
        args.stack,
    ]
    if args.overwrite:
        forward.append("--overwrite")
    run_python("bootstrap_project.py", forward)


def run_plan_runtime(args: argparse.Namespace) -> None:
    artifact_dir = Path(args.artifact_dir).resolve()
    artifact_dir.mkdir(parents=True, exist_ok=True)

    execution_output = artifact_dir / args.execution_output_name
    capability_output = artifact_dir / args.capability_output_name

    execution_args = [
        "--artifact-dir",
        str(artifact_dir),
        "--release-slice",
        args.release_slice,
        "--current-gate",
        args.current_gate,
        "--plan-lock-version",
        args.plan_lock_version,
        "--output-name",
        args.execution_output_name,
    ]
    for step in args.step:
        execution_args.extend(["--step", step])
    for track in args.track:
        execution_args.extend(["--track", track])
    if args.overwrite:
        execution_args.append("--overwrite")
    run_python("generate_execution_control.py", execution_args)

    capability_args = [
        "--artifact-dir",
        str(artifact_dir),
        "--output-name",
        args.capability_output_name,
    ]
    for item in args.item:
        capability_args.extend(["--item", item])
    if args.overwrite:
        capability_args.append("--overwrite")
    run_python("generate_capability_routing.py", capability_args)

    template_ids = args.template_id or extract_template_ids(capability_output)
    if not template_ids:
        raise SystemExit("No delegation templates were found or specified.")

    delegation_args = [
        "--artifact-dir",
        str(artifact_dir),
        "--output-name",
        args.delegation_output_name,
    ]
    for template_id in template_ids:
        delegation_args.extend(["--template-id", template_id])
    if args.overwrite:
        delegation_args.append("--overwrite")
    run_python("generate_delegation_templates.py", delegation_args)

    spawn_args = [
        "--artifact-dir",
        str(artifact_dir),
        "--output-name",
        args.spawn_output_name,
    ]
    if args.overwrite:
        spawn_args.append("--overwrite")
    run_python("generate_spawn_agent_templates.py", spawn_args)

    if args.run_checks:
        run_python("score_plan_quality.py", ["--artifact-dir", str(artifact_dir)])
        run_python("check_capability_routing.py", ["--artifact-dir", str(artifact_dir)])
        run_python("check_spawn_agent_templates.py", ["--artifact-dir", str(artifact_dir)])
        validate_args = ["--artifact-dir", str(artifact_dir)]
        if args.require_greenfield:
            validate_args.append("--require-greenfield")
        if args.require_ui:
            validate_args.append("--require-ui")
        if args.require_system:
            validate_args.append("--require-system")
        run_python("validate_delivery.py", validate_args)

    print(f"Runtime control artifacts ready in {artifact_dir}")
    print(f"- execution: {execution_output.name}")
    print(f"- capability routing: {capability_output.name}")
    print(f"- delegation templates: {args.delegation_output_name}")
    print(f"- spawn templates: {args.spawn_output_name}")


def run_review_bundle(args: argparse.Namespace) -> None:
    output_dir = Path(args.output_dir).resolve()
    prompts_dir = output_dir / "review-prompts"
    verdicts_dir = output_dir / "review-verdicts"
    review_package = output_dir / args.review_package_name
    output_dir.mkdir(parents=True, exist_ok=True)

    package_args = [
        "--output",
        str(review_package),
        "--scope-summary",
        args.scope_summary,
    ]
    for artifact in args.artifact:
        package_args.extend(["--artifact", artifact])
    for changed_file in args.changed_file:
        package_args.extend(["--changed-file", changed_file])
    for command in args.command:
        package_args.extend(["--command", command])
    for evidence in args.evidence:
        package_args.extend(["--evidence", evidence])
    for screenshot in args.screenshot:
        package_args.extend(["--screenshot", screenshot])
    for residual_risk in args.residual_risk:
        package_args.extend(["--residual-risk", residual_risk])
    for reviewer_instruction in args.reviewer_instruction:
        package_args.extend(["--reviewer-instruction", reviewer_instruction])
    run_python("build_review_package.py", package_args)

    prompt_args = [
        "--output-dir",
        str(prompts_dir),
        "--scope-summary",
        args.scope_summary,
        "--review-package",
        str(review_package),
        "--work-type",
        args.work_type,
    ]
    run_python("generate_review_prompts.py", prompt_args)

    for prompt_path in sorted(prompts_dir.glob("*.txt")):
        role = prompt_path.stem
        run_python(
            "generate_verdict_template.py",
            [
                "--role",
                role,
                "--output",
                str(verdicts_dir / f"{role}.md"),
            ],
        )

    print(f"Review bundle ready in {output_dir}")
    print(f"- review package: {review_package.name}")
    print(f"- prompts: {prompts_dir}")
    print(f"- verdict templates: {verdicts_dir}")


def run_capture_ui(args: argparse.Namespace) -> None:
    forward = [
        "--url",
        args.url,
        "--output-dir",
        args.output_dir,
        "--wait-timeout-ms",
        str(args.wait_timeout_ms),
    ]
    if args.wait_selector:
        forward.extend(["--wait-selector", args.wait_selector])
    if args.skip_lighthouse:
        forward.append("--skip-lighthouse")
    run_python("capture_ui_evidence.py", forward)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Unified control entrypoint for enterprise delivery orchestration."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    bootstrap = subparsers.add_parser("bootstrap-project", help="Bootstrap a bounded greenfield project.")
    bootstrap.add_argument("--target-dir", required=True)
    bootstrap.add_argument("--stack", required=True)
    bootstrap.add_argument("--overwrite", action="store_true")
    bootstrap.set_defaults(handler=run_bootstrap_project)

    plan = subparsers.add_parser("plan-runtime", help="Generate runtime delivery control artifacts.")
    plan.add_argument("--artifact-dir", required=True)
    plan.add_argument("--release-slice", required=True)
    plan.add_argument("--current-gate", default="Clarification Gate")
    plan.add_argument("--plan-lock-version", default="v1")
    plan.add_argument("--step", action="append", default=[], help="STEP_ID:summary")
    plan.add_argument("--track", action="append", default=[], help="TRACK:owner")
    plan.add_argument("--item", action="append", default=[], help="WORK_ID:WORK_CLASS:OWNER_ROLE")
    plan.add_argument("--template-id", action="append", default=[], help="Optional delegation template override")
    plan.add_argument("--execution-output-name", default="execution-control.md")
    plan.add_argument("--capability-output-name", default="capability-routing.md")
    plan.add_argument("--delegation-output-name", default="delegation-templates.md")
    plan.add_argument("--spawn-output-name", default="spawn-agent-templates.md")
    plan.add_argument("--overwrite", action="store_true")
    plan.add_argument("--run-checks", action="store_true")
    plan.add_argument("--require-greenfield", action="store_true")
    plan.add_argument("--require-ui", action="store_true")
    plan.add_argument("--require-system", action="store_true")
    plan.set_defaults(handler=run_plan_runtime)

    review = subparsers.add_parser("review-bundle", help="Generate review package, prompts, and verdict templates.")
    review.add_argument("--output-dir", required=True)
    review.add_argument("--scope-summary", required=True)
    review.add_argument("--work-type", required=True)
    review.add_argument("--review-package-name", default="review-package.md")
    review.add_argument("--artifact", action="append", default=[])
    review.add_argument("--changed-file", action="append", default=[])
    review.add_argument("--command", action="append", default=[])
    review.add_argument("--evidence", action="append", default=[])
    review.add_argument("--screenshot", action="append", default=[])
    review.add_argument("--residual-risk", action="append", default=[])
    review.add_argument("--reviewer-instruction", action="append", default=[])
    review.set_defaults(handler=run_review_bundle)

    capture = subparsers.add_parser("capture-ui", help="Capture UI evidence through the unified entrypoint.")
    capture.add_argument("--url", required=True)
    capture.add_argument("--output-dir", required=True)
    capture.add_argument("--wait-selector")
    capture.add_argument("--wait-timeout-ms", type=int, default=1500)
    capture.add_argument("--skip-lighthouse", action="store_true")
    capture.set_defaults(handler=run_capture_ui)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.handler(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
