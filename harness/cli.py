"""Safety-first, standard-library CLI for Colab and NotebookLM.

Read-only checks never print the underlying tool output. Research starts only
after explicit interactive approval. No session creation, source imports,
secret file access, cloud GPU allocations, or authentication automation.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections.abc import Sequence


def _invoke(args: Sequence[str], timeout: int = 45) -> bool:
    """Run a fixed argument array, suppressing potentially sensitive output."""
    try:
        completed = subprocess.run(
            list(args),
            capture_output=True,
            text=True,
            check=False,
            shell=False,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False

    if completed.returncode != 0:
        return False

    # Some CLIs return a structured error envelope even with exit status 0.
    try:
        response = json.loads(completed.stdout)
    except (json.JSONDecodeError, TypeError, ValueError):
        return True

    if isinstance(response, dict):
        if response.get("error") is True:
            return False
        if str(response.get("status", "")).lower() == "error":
            return False
    return True


def _result(label: str, success: bool) -> int:
    print(f"{label}: {'OK' if success else 'FAILED'}")
    return 0 if success else 1


def _doctor(online: bool) -> int:
    available = {name: bool(shutil.which(name)) for name in ("colab", "notebooklm")}
    for name, found in available.items():
        print(f"{name} executable: {'FOUND' if found else 'MISSING'}")

    if not all(available.values()):
        return 1

    if not online:
        print("Offline check only; no account operations were performed.")
        return 0

    checks = (
        ("Colab usage query", ["colab", "usage"]),
        ("Colab session query", ["colab", "sessions"]),
        ("NotebookLM list query", ["notebooklm", "list", "--json"]),
    )
    ok = True
    for label, command in checks:
        passed = _invoke(command)
        _result(label, passed)
        ok = ok and passed
    print("Upstream output suppressed: no account balances or titles were printed.")
    return 0 if ok else 1


def _research(notebook: str, query: str, mode: str, execute: bool) -> int:
    # Never use --import-all, and never print the notebook ID or research query.
    command = [
        "notebooklm",
        "source",
        "add-research",
        query,
        "-n",
        notebook,
        "--mode",
        mode,
        "--no-wait",
        "--json",
    ]
    if not execute:
        print(
            f"DRY RUN: NotebookLM {mode} research would start. "
            "No remote request sent; notebook ID and query withheld."
        )
        return 0

    if not sys.stdin.isatty():
        print(
            "Execution refused: interactive terminal approval is required.",
            file=sys.stderr,
        )
        return 2

    print(
        "This sends the research query to NotebookLM and starts a remote task. "
        "Only submit public or authorized content."
    )
    try:
        answer = input("Type START NOTEBOOKLM RESEARCH to continue: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("Cancelled.")
        return 2

    if answer != "START NOTEBOOKLM RESEARCH":
        print("Cancelled; no remote request sent.")
        return 2

    return _result("Research start request", _invoke(command, timeout=90))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="research-harness",
        description="Privacy-first status checks and approved NotebookLM discovery.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Check installed tools.")
    doctor.add_argument(
        "--online", action="store_true", help="Make read-only remote checks."
    )

    sources = subparsers.add_parser(
        "notebook-sources", help="Check an existing notebook's source list."
    )
    sources.add_argument("--notebook", required=True)

    research_status = subparsers.add_parser(
        "research-status", help="Read research status without modifying sources."
    )
    research_status.add_argument("--notebook", required=True)

    research = subparsers.add_parser(
        "research", help="Preview or explicitly approve a research task."
    )
    research.add_argument("--notebook", required=True)
    research.add_argument("--query", required=True)
    research.add_argument("--mode", choices=("fast", "deep"), default="fast")
    research.add_argument(
        "--execute",
        action="store_true",
        help="Start research only after explicit interactive approval.",
    )

    args = parser.parse_args(argv)

    if args.command == "doctor":
        return _doctor(args.online)
    if args.command == "notebook-sources":
        return _result(
            "Source-list query",
            _invoke(["notebooklm", "source", "list", "-n", args.notebook, "--json"]),
        )
    if args.command == "research-status":
        return _result(
            "Research-status query",
            _invoke(["notebooklm", "research", "status", "-n", args.notebook, "--json"]),
        )
    if args.command == "research":
        return _research(args.notebook, args.query, args.mode, args.execute)

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
