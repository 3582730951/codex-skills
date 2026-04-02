#!/usr/bin/env python3
"""Bootstrap audit and submission artifacts for regulated internal projects."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent


FILES = {
    "docs/authorization-manifest.md": dedent(
        """\
        Authorization Manifest:
        - Product / component:
        - Business owner:
        - Engineering owner:
        - Authorized environments:
        - Allowed privilege level:
        - Allowed persistence model:
        - Allowed data access:
        - Disallowed behaviors:
        - Approval chain:
        """
    ),
    "docs/audit-annotation-register.md": dedent(
        """\
        Audit Annotation Register:
        - File / symbol:
        - Required tags:
        - Owner:
        - Last reviewed:
        - Related artifact or evidence:
        """
    ),
    "docs/source-provenance-register.md": dedent(
        """\
        Source Provenance Register:
        - Source root or package:
        - Owner / team:
        - Sensitivity:
        - Allowed use:
        - License / IP basis:
        - Modification policy:
        - Submission status:
        """
    ),
    "docs/platform-submission-notes.md": dedent(
        """\
        Platform Submission Notes:
        - Submission target:
        - Included source roots:
        - Omitted or redacted items:
        - Build instructions:
        - Reviewer:
        - Traceability links:
        """
    ),
}


def write_files(root: Path, overwrite: bool) -> None:
    for relative_path, content in FILES.items():
        file_path = root / relative_path
        if file_path.exists() and not overwrite:
            raise FileExistsError(f"{relative_path} already exists")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap audit and submission artifacts.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    write_files(root, overwrite=args.overwrite)

    print(f"Bootstrapped audit bundle at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
