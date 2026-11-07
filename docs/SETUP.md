# Installation and local setup

This document is for a **generic example workstation**. It intentionally contains no personal account data or real notebook identifiers.

## 1. Prerequisites

- macOS or Linux
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) on the PATH
- Access to Google Colab and NotebookLM, and optionally Codex and Antigravity
- Permission to use each service and sufficient account-specific quota

Verify the installed versions and help before using copy-pasted commands.

## 2. Install command-line tools

~~~bash
uv tool install google-colab-cli
uv tool install "notebooklm-py[browser]"
uv tool update-shell
~~~

Open a new terminal if your installed executables are not on PATH.

~~~bash
command -v colab
command -v notebooklm
colab --help
notebooklm --help
~~~

`google-colab-cli` is an official Google Colab tool. `notebooklm-py` is an **unofficial, community-maintained** project whose behavior can change when the service changes.

## 3. Authenticate locally

~~~bash
colab usage
notebooklm login
~~~

Follow the tools' instructions in your own browser or terminal. Do not paste one-time codes, cookies, or OAuth URLs containing state parameters into issues or conversations.

Some `notebooklm-py` installations offer browser-cookie extraction with an optional dependency:

~~~bash
uv tool install --force "notebooklm-py[browser,cookies]"
notebooklm login --browser-cookies brave
~~~

This **reads existing browser cookies**, which are powerful credentials. It is not required for ordinary browser sign-in; use it only when you understand the trust boundary. Do not run it inside an untrusted agent sandbox. Ensure the authorization complies with the service terms and your environment's policies.

Read-only connectivity checks:

~~~bash
colab usage
colab sessions
notebooklm list --json
~~~

The output may reveal private notebook titles or billing data; do not copy the raw output into a public issue.

## 4. Install/identify Skills

Codex looks for project Skills under `.agents/skills/<name>/SKILL.md` and personal Skills under `$HOME/.agents/skills/<name>/SKILL.md`.

This repository includes:
- `.agents/skills/literature-audit/SKILL.md`
- `.agents/skills/colab-safety/SKILL.md`

For NotebookLM's own bundled skill:

~~~bash
notebooklm skill install --scope user --target agents
notebooklm skill status --scope user --target agents
~~~

Antigravity also recognizes workspace Skills under `.agents/skills/`. Exact global paths differ by Antigravity product/version; consult [official skills documentation](https://antigravity.google/docs/skills) before installation. Use Antigravity independently from Codex. This guide does not reuse credentials between the two agents.

For Colab's upstream skill, use the version-matched `colab skill --help` and preserve pre-existing local files.

## 5. Safe starter harness

No dependency installation is needed for the local Python wrapper.

~~~bash
python3 -m harness.cli doctor
python3 -m harness.cli doctor --online
python3 -m harness.cli notebook-sources --notebook YOUR_NOTEBOOK_ID
python3 -m unittest discover -s tests -v
~~~

`doctor` defaults to offline PATH checks. `--online` performs read-only CLI checks and prints **only success/failure**, not the CLI's raw account data. The notebook ID is supplied at runtime and must not be saved into this public repository.

## 6. NotebookLM discovery (manual CLI example)

After creating or choosing your own notebook:

~~~bash
notebooklm source add-research "K3 surfaces and the Hodge conjecture" \
  --mode fast -n YOUR_NOTEBOOK_ID --json
~~~

This action starts remote research. To preview a research command first, use:

~~~bash
python3 -m harness.cli research --notebook YOUR_NOTEBOOK_ID \
  --mode fast --query "K3 surfaces and the Hodge conjecture"
~~~

The example wrapper requires interactive approval before execution and never automatically imports found sources. To review sources, use the version-matched `research status` and `source list` commands.

## 7. Colab computation

~~~bash
colab usage
colab sessions
colab run --gpu T4 experiment.py
~~~

**The final line is billable remote execution** and is only an example; do not run it without an approved script, suitable input data, and a clear cost estimate. GPU allocation is not guaranteed and the project harness does not impose a hard CU cap. Check `colab sessions` afterward.

## 8. Troubleshooting

| Symptom | Check |
|---|---|
| `command not found` | `uv tool update-shell`, reopen terminal, check `PATH` |
| NotebookLM authentication fails | Use local interactive login; do not disclose cookies |
| Notebook ID not found | Verify which account and notebook are selected |
| CLI flags are rejected | Compare with installed `--help` |
| Agent cannot call CLI | Check local sandbox/permission policy; do not silently relax it |
| GPU unavailable | Provider availability, account quota, permissions |

For any authentication incident, assume copied cookies/tokens are compromised and follow the provider's revocation procedures.
