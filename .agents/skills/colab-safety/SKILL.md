---
name: colab-safety
description: Use before Google Colab CLI GPU/TPU tasks to inspect available resources, estimate spending, approve cloud computation, and verify session cleanup. Do not silently allocate or retain billable sessions.
---

# Colab Cost and Session Safety

Use the **official** `colab` CLI. Check the installed CLI's help and account-specific availability.

## Before execution

1. Ask whether a cloud run is actually necessary; local CPU/GPU or a read-only analysis may suffice.
2. Check the current plan, compute balance, and active assignments:
   ~~~bash
   colab usage
   colab sessions
   ~~~
3. Estimate expected duration and cost with a **measured or documented CU/hour rate**. If the rate is unknown, do not invent it; present an unknown-cost risk.
4. Confirm the input files are approved for upload and contain no secrets or proprietary material unless an appropriate agreement exists.
5. Present the exact command, hardware request, expected outputs, maximum intended duration, and cleanup steps. Ask for explicit approval.
6. Never grant new sandbox permissions or extract tokens to make an agent run unattended.

## Execution (only after explicit approval)

A typical one-shot job is:

~~~bash
colab run --gpu T4 experiment.py
~~~

No GPU type is guaranteed. Avoid `--keep` unless the user explicitly requests a persistent session. `colab run` normally releases its own transient VM at completion, but do not assume cleanup on every failure or interruption.

Afterward:
- Verify results were saved and independently sanity-checked.
- Run `colab sessions` to inspect whether any session remains.
- Stop only the specific session authorized by the user, using the version-matched `colab stop --help` syntax.
- Record the actual consumed CU if available.

## Limitations

The example harness in this repository does not enforce hard CU spending caps and does not allocate GPUs. A forecast or approval prompt is not a provider-enforced budget limit. Do not claim numerical results establish a mathematical theorem.
