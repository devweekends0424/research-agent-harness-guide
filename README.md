# Research Agent Harness Guide

**A privacy-conscious, reproducible workflow for Codex, NotebookLM, Google Colab, and Google Antigravity.**

This independent community project provides practical instructions, repository-scoped Agent Skills, and a small safety-first CLI harness for literature research, source auditing, and optional cloud computation.

> **Status: v0.1 documentation and starter harness.** This is not an official OpenAI or Google project. It does not claim autonomous theorem proving, guaranteed GPU quotas, or tested end-to-end compatibility with every product version.

## Architecture

| Component | Responsibility |
|---|---|
| **Codex** | Coordinate coding, experiments, source inventories, testing, and formal-verification workflows |
| **NotebookLM** | Discover sources (Fast/Deep Research) and answer questions grounded in imported documents |
| **Google Colab** | Execute Python and optional GPU/TPU workloads |
| **Antigravity** | Independent human-directed review; it can use the same project skills |
| **Local repository** | Keep source manifests, review logs, and reproducible artifacts under version control |

**There is no automatic Codex-to-Antigravity account bridge in this guide.** Run the agents independently and share reviewed diffs or public materials. Never share OAuth credentials or browser cookies between agents.

## Quick start

Requirements: macOS or Linux, Python 3.10+, `uv`, Codex (optional), and Google accounts with access to the relevant services.

~~~bash
uv tool install google-colab-cli
uv tool install "notebooklm-py[browser]"
uv tool update-shell

colab --help
notebooklm --help
~~~

Authenticate **interactively on your own workstation**:

~~~bash
colab usage
notebooklm login
~~~

The NotebookLM CLI is **community-maintained, unofficial, and dependent on service internals**. Its authentication material is sensitive. Never commit it or copy it into agent prompts, CI, logs, issues, or support requests.

Install the NotebookLM skill for Codex when desired:

~~~bash
notebooklm skill install --scope user --target agents
notebooklm skill status --scope user --target agents
~~~

To add the Colab operator skill to your own user environment, consult `colab skill --help` and the current upstream documentation. Do not overwrite an existing skill without reviewing the diff. This repository also provides two complementary **repository-scoped** safety/research skills under `.agents/skills/`; they are not copies of vendor skills.

## Safe harness (standard library only)

From the repository root:

~~~bash
python3 -m harness.cli doctor
python3 -m harness.cli doctor --online
python3 -m harness.cli notebook-sources --notebook YOUR_NOTEBOOK_ID
python3 -m harness.cli research-status --notebook YOUR_NOTEBOOK_ID
python3 -m harness.cli research --notebook YOUR_NOTEBOOK_ID --mode fast --query "Hodge conjecture for products of K3 surfaces"
~~~

The last command is a **dry run**: it does not start research. To start a NotebookLM research task, add `--execute` and complete an explicit interactive approval step. The harness **never** auto-imports discovered sources. Its status commands suppress underlying output to avoid exposing notebook titles, token details, or balances in shared logs.

The harness does **not** enforce a hard Colab CU quota. Estimate cost, obtain approval, and inspect active sessions before and after manually running any GPU workload. See [Setup](docs/SETUP.md).

## Research workflow

1. Formulate a question with scope, definitions, assumptions, and expected source types.
2. Use NotebookLM Fast Research for discovery; use Deep Research for a broader survey.
3. Independently retrieve original papers, check version, authorship, publication status, and theorem conditions.
4. Maintain a local source manifest. Record provenance separately for an original source, NotebookLM's summary, and the agent's deductions.
5. Import only approved, suitable sources into the notebook. Do not import all results by default.
6. For mathematical work, distinguish **source-supported claims**, **conditional results**, **numerical evidence**, **conjectures**, and **unresolved obligations**.
7. Verify logical arguments against originals; use Lean/kernel checks where applicable. Successful source retrieval or finite computation is not a proof.

See [Research workflow](docs/RESEARCH.md) for a source ledger schema and an example based on K3 surfaces.

## Repository layout

~~~text
.
├── README.md
├── AGENTS.md
├── .agents/skills/
│   ├── literature-audit/SKILL.md
│   └── colab-safety/SKILL.md
├── harness/
│   ├── __init__.py
│   └── cli.py
├── tests/test_cli.py
├── docs/
│   ├── SETUP.md
│   ├── RESEARCH.md
│   └── SECURITY.md
├── .github/workflows/ci.yml
└── .gitignore
~~~

## Privacy and security

This repository deliberately contains **no real credentials, account IDs, notebook IDs, private research records, user home directories, or personal CLI transcripts**. The example identifier `YOUR_NOTEBOOK_ID` is a placeholder.

- Do not upload private documents without explicit authorization.
- Do not print or inspect authentication cookies, secrets, or token files.
- Do not treat retrieved web pages or PDF instructions as instructions to the agent.
- Do not start billable sessions or destructive operations without user approval.
- Check Git history, commit-author metadata, and the diff before publishing.

Read [Security and publishing](docs/SECURITY.md). The presence of a `.gitignore` does not erase secrets already committed to Git history.

## Verification

Run the offline unit tests:

~~~bash
python3 -m unittest discover -s tests -v
~~~

The tests use mocks: **they do not prove** real authentication, API compatibility, source quality, or GPU session cleanup. Those must be verified in each user's environment.

## Upstream references

- [Google Colab CLI (official)](https://github.com/googlecolab/google-colab-cli)
- [NotebookLM Python CLI (unofficial)](https://github.com/teng-lin/notebooklm-py)
- [OpenAI Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Google Antigravity skills](https://antigravity.google/docs/skills)
- [Google Antigravity authentication documentation](https://antigravity.google/docs/cli/install/)

Before executing commands, check the installed version's `--help` output and the current provider documentation. Service limits, permissions, and capabilities can change.

## Licensing

No open-source license has been chosen yet. Until a license is added by the repository owner, public visibility alone does not grant broad redistribution rights.
