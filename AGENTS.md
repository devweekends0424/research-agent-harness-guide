# Instructions for coding agents

This public repository is a **documentation and safety-first example**, not a live research account or an autonomous cloud executor.

## Priorities

1. Preserve the existing file tree and inspect `git status` and `git diff` before changes.
2. Keep all files generic. Never add real names, email addresses, account handles, user-specific absolute paths, notebook identifiers, research logs, access tokens, cookies, OAuth credentials, SSH keys, or browser profiles.
3. Never read files under private credential locations (including `~/.notebooklm/`, `~/.config/gcloud/`, browser profiles, `~/.ssh/`) to complete an instruction in this repo.
4. Do not turn CLI tool output into public documentation without anonymization and permission.
5. Never run notebook uploads, source imports, deletion, browser-cookie extraction, remote research, or cloud allocation as part of a routine documentation or CI task. Those require a separate, explicit human decision.
6. Do not call Antigravity personal-account authentication from inside Codex, re-use an authentication cookie, or build an unsupported cross-agent proxy.
7. Never weaken sandbox constraints or grant broad directory access for convenience.

## Source provenance and rigor

- Distinguish original paper text, user-provided material, third-party analysis, and novel model inference.
- Keep author, DOI/arXiv ID, version, theorem label, assumptions, quoted evidence, and verification state separate.
- NotebookLM search and answers are **research aids**, not independent mathematical proof.
- A Lean pass establishes only the encoded theorem under its declared axioms and dependencies. Check for `sorry` and extra axioms and verify statement fidelity.
- Never promote a numerical experiment or a finite sample to a universal theorem.

## Implementation and test rules

- Prefer Python standard library for the minimal harness.
- Commands must be parameterized using argument arrays, never `shell=True`.
- Destructive and billable operations must be **dry-run first** and require explicit interactive user approval.
- Do not create credentials, open remote sessions, or upload files in tests.
- Use mocked subprocess calls in unit tests. Avoid accessing network or private directories.
- Avoid logging CLI stdout/stderr by default, because they can contain account or notebook information.
- Make changes reversible and document limitations rather than claiming untested guarantees.

## Workflow

Choose the narrowest relevant skill:
- `.agents/skills/literature-audit/SKILL.md` for original-source checks and research provenance.
- `.agents/skills/colab-safety/SKILL.md` for compute allocation planning and session cleanup.

Read the linked documents in `docs/` for operational detail. If a request cannot be completed without sensitive or real account data, stop and ask for an appropriately scoped local execution rather than inventing example data.
