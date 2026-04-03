#!/usr/bin/env python3
"""Generate execution-control artifacts for locked-plan delivery."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent


def parse_named_pairs(items: list[str]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in items:
        if ":" not in item:
            raise ValueError(f"Expected NAME:VALUE format, got: {item}")
        left, right = item.split(":", 1)
        pairs.append((left.strip(), right.strip()))
    return pairs


def render(root: Path, release_slice: str, gate: str, version: str, steps: list[tuple[str, str]], tracks: list[tuple[str, str]]) -> str:
    step_lines = []
    for step_id, summary in steps:
        step_lines.extend(
            [
                f"- step_id: {step_id}",
                f"  summary: {summary}",
                "  entry_gate:",
                "  exit_evidence:",
            ]
        )
    if not step_lines:
        step_lines = [
            "- step_id:",
            "  summary:",
            "  entry_gate:",
            "  exit_evidence:",
        ]

    track_lines = []
    for track_name, owner in tracks:
        track_lines.append(f"- {track_name}: {owner}")
    if not track_lines:
        track_lines = ["- "]

    return dedent(
        f"""\
        Execution Contract:
        - release_slice: {release_slice}
        - current_gate: {gate}
        - plan_lock_version: {version}
        - parallel_tracks:
        {chr(10).join(track_lines)}
        - track_owners:
        {chr(10).join(track_lines)}
        - ordered_steps:
        {chr(10).join(step_lines)}
        - allowed_out_of_plan_work: none
        - replan_triggers:
          - contract gap
          - new trust boundary
          - out-of-plan file touch
          - missing evidence for a completed requirement
        - blocked_by:

        Plan Coverage Matrix:
        - requirement_id:
          user_value:
          plan_step_ids:
          owner_track:
          implementation_targets:
          validation_ids:
          status:

        Execution Ledger:
        - event_id:
          plan_step_id:
          requirement_ids:
          owner:
          changed_files_or_symbols:
          validation_or_reason:
          result:
          drift_status:
        """
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate execution-control artifacts.")
    parser.add_argument("--artifact-dir", required=True)
    parser.add_argument("--release-slice", required=True)
    parser.add_argument("--current-gate", default="Clarification Gate")
    parser.add_argument("--plan-lock-version", default="v1")
    parser.add_argument("--step", action="append", default=[], help="STEP_ID:summary")
    parser.add_argument("--track", action="append", default=[], help="TRACK:owner")
    parser.add_argument("--output-name", default="execution-control.md")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    root = Path(args.artifact_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    output = root / args.output_name
    if output.exists() and not args.overwrite:
        raise FileExistsError(f"{output} already exists")

    steps = parse_named_pairs(args.step)
    tracks = parse_named_pairs(args.track)
    output.write_text(
        render(root, args.release_slice, args.current_gate, args.plan_lock_version, steps, tracks),
        encoding="utf-8",
    )
    print(f"Execution control written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
