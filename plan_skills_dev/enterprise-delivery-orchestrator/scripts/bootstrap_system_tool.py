#!/usr/bin/env python3
"""Bootstrap an authorized defensive system tool scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent


PYTHON_AGENT_FILES = {
    ".gitignore": dedent(
        """\
        .venv/
        __pycache__/
        *.pyc
        .pytest_cache/
        """
    ),
    "pyproject.toml": dedent(
        """\
        [build-system]
        requires = ["setuptools>=68"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "defensive-system-agent"
        version = "0.1.0"
        description = "Authorized defensive system inspection agent scaffold"
        requires-python = ">=3.11"

        [tool.pytest.ini_options]
        testpaths = ["tests"]
        """
    ),
    "README.md": dedent(
        """\
        # Defensive System Agent

        Authorized, read-first system inspection scaffold.

        ## Principles

        - Explicit permissions
        - Observable actions
        - Reversible changes
        - No stealth behavior
        """
    ),
    "run.py": dedent(
        """\
        # AUTHORIZATION: Authorized defensive local entrypoint for declared scan roots only.
        # SECURITY-BOUNDARY: Starts the owned inspection agent with no hidden persistence behavior.
        # AUDIT: Keep docs/authorization-manifest.md and docs/audit-annotation-register.md in sync.
        # PROVENANCE: Company-owned scaffold; replace ownership details before release.

        from agent.main import main


        if __name__ == "__main__":
            raise SystemExit(main())
        """
    ),
    "agent/__init__.py": "",
    "agent/config.py": dedent(
        """\
        from dataclasses import dataclass


        @dataclass(frozen=True)
        class AgentConfig:
            scan_root: str = "/etc"
            require_root: bool = False
            log_path: str = "./agent.log"
        """
    ),
    "agent/checks.py": dedent(
        """\
        from pathlib import Path


        def collect_permission_findings(scan_root: str) -> list[str]:
            root = Path(scan_root)
            findings: list[str] = []
            if not root.exists():
                findings.append(f"Scan root does not exist: {scan_root}")
                return findings
            for path in sorted(root.iterdir())[:25]:
                if path.is_file() and path.stat().st_mode & 0o002:
                    findings.append(f"World-writable file detected: {path}")
            return findings
        """
    ),
    "agent/main.py": dedent(
        """\
        # AUTHORIZATION: Authorized defensive inspection of declared local paths only.
        # SECURITY-BOUNDARY: Reads configured paths and prints findings; no stealth or privilege escalation.
        # AUDIT: Review with docs/authorization-manifest.md and docs/audit-annotation-register.md.
        # PROVENANCE: Company-owned scaffold to be adapted for a specific product boundary.

        from .checks import collect_permission_findings
        from .config import AgentConfig


        def main() -> int:
            config = AgentConfig()
            findings = collect_permission_findings(config.scan_root)
            print("Authorized defensive scan summary:")
            if findings:
                for finding in findings:
                    print(f"- {finding}")
            else:
                print("- no findings in sampled paths")
            return 0
        """
    ),
    "docs/permission-model.md": dedent(
        """\
        Permission Model:
        - Intended platform:
        - Read paths:
        - Write paths:
        - Requires elevation:
        - Reduced-privilege mode:
        - Rollback / uninstall:
        """
    ),
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
    "docs/threat-model.md": dedent(
        """\
        Threat Model:
        - Assets:
        - Trust boundaries:
        - Allowed capabilities:
        - Abuse cases:
        - Mitigations:
        - Residual risks:
        """
    ),
    "tests/test_checks.py": dedent(
        """\
        import tempfile
        import unittest
        from pathlib import Path

        from agent.checks import collect_permission_findings


        class ChecksTestCase(unittest.TestCase):
            def test_missing_root_reports_finding(self) -> None:
                findings = collect_permission_findings("/path/does/not/exist")
                self.assertTrue(findings)


        if __name__ == "__main__":
            unittest.main()
        """
    ),
}


RUST_CLI_FILES = {
    ".gitignore": "target/\n",
    "Cargo.toml": dedent(
        """\
        [package]
        name = "defensive-system-cli"
        version = "0.1.0"
        edition = "2021"

        [dependencies]
        anyhow = "1"
        clap = { version = "4", features = ["derive"] }
        """
    ),
    "README.md": dedent(
        """\
        # Defensive System CLI

        Authorized system inspection CLI scaffold.
        """
    ),
    "src/main.rs": dedent(
        """\
        // AUTHORIZATION: Authorized defensive inspection CLI for declared local paths only.
        // SECURITY-BOUNDARY: Reads operator-provided paths; no hidden persistence or privilege escalation.
        // AUDIT: Keep docs/authorization-manifest.md and docs/audit-annotation-register.md in sync.
        // PROVENANCE: Company-owned scaffold; replace ownership details before release.

        use anyhow::Result;
        use clap::Parser;

        #[derive(Parser, Debug)]
        struct Args {
            #[arg(long, default_value = "/etc")]
            scan_root: String,
        }

        fn main() -> Result<()> {
            let args = Args::parse();
            println!("Authorized defensive inspection for {}", args.scan_root);
            Ok(())
        }
        """
    ),
    "docs/permission-model.md": dedent(
        """\
        Permission Model:
        - Intended platform:
        - Read paths:
        - Write paths:
        - Requires elevation:
        - Reduced-privilege mode:
        """
    ),
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
    "docs/threat-model.md": dedent(
        """\
        Threat Model:
        - Assets:
        - Trust boundaries:
        - Allowed capabilities:
        - Abuse cases:
        - Mitigations:
        - Residual risks:
        """
    ),
}


STACK_MAP = {
    "python-system-agent": PYTHON_AGENT_FILES,
    "rust-system-cli": RUST_CLI_FILES,
}


def write_files(root: Path, files: dict[str, str], overwrite: bool) -> None:
    for relative_path, content in files.items():
        file_path = root / relative_path
        if file_path.exists() and not overwrite:
            raise FileExistsError(f"{relative_path} already exists")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a defensive system tool scaffold.")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--stack", required=True, choices=sorted(STACK_MAP))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    write_files(root, STACK_MAP[args.stack], overwrite=args.overwrite)

    print(f"Bootstrapped {args.stack} at {root}")
    print("Next step: fill the authorization, provenance, threat-model, and system-architecture artifacts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
