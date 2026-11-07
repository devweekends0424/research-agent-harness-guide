# Source-grounded research workflow

This workflow is designed for literature-heavy research, including mathematics, but can be adapted to other disciplines.

## Provenance and evidence

A research statement can originate from distinct layers:

1. **Original source**: paper, official correction, primary data, or authoritative code.
2. **Source excerpt/user-supplied text**: faithfully attributed and within copyright limits.
3. **NotebookLM synthesis**: a helpful, potentially incomplete or incorrect interpretation.
4. **Other agent analysis**: a secondary inference, not a primary source.
5. **New analysis**: clearly labeled as unverified until independently checked.

Do not promote layer 3, 4, or 5 into layer 1 by rewriting it as a source fact.

## Recommended source manifest

Store only **non-sensitive metadata** in a public repository. A private research workspace may retain more detailed records.

| Field | Example/meaning |
|---|---|
| `source_key` | Public identifier you define |
| `title`, `authors` | Original bibliographic metadata |
| `doi`, `arxiv_id` | Identifier as verified against original source |
| `version`, `date_checked` | Exact version and most recent verification date |
| `primary_url` | DOI resolver, publisher, or arXiv landing page |
| `checksum_sha256` | Integrity hash of a locally archived copy |
| `notebook_source_id` | **Private-local only**: do not publish real IDs |
| `claim` | Exact statement the project needs |
| `assumptions` | All hypotheses and quantifiers |
| `location` | Section, theorem, page, or precise citation |
| `status` | Verified / conditional / numerical / speculative / unknown |
| `next_check` | Smallest unresolved validation step |

## Worked example: a K3 surface product

Research question: *Under which hypotheses does a published theorem establish algebraicity of specified Hodge classes on a product of K3 surfaces?*

The agent must first identify the **precise theorem**. It may depend on the Picard rank, geometric specializations, field of definition, or properties of the transcendental lattice. Before reusing it, check whether the target surface satisfies every hypothesis.

A finding for one special K3 surface (or a bounded computation) is not evidence of a proof for **all** K3 surfaces unless a valid general reduction is supplied. Quantifier order matters.

Workflow:

1. Discover original papers via NotebookLM Fast/Deep Research and independent literature search.
2. Verify authors, publication/withdrawal status, exact PDF version, and errata.
3. Quote or paraphrase the original theorem accurately with a page/theorem reference.
4. Encode assumptions explicitly; check necessity, sufficiency, degeneracies, and proof dependencies.
5. Seek a minimal counterexample to any overgeneralization.
6. If using Lean, check theorem statements, dependencies, imported axioms, `sorry`, and kernel results.
7. Record what remains conditional or unknown. A successful search is not proof; a missing hit does not prove no paper exists.

## Source lifecycle

Discovery → identity check → duplicate check → original version audit → user-approved import → cited analysis → periodic recheck → archival.

Treat deletions, replacements, and private uploads as explicit user-authorized changes. Use exact identifiers and perform a read-back after any mutation. Keep local backups independently of NotebookLM.

## Acceptance criteria

An auditable literature claim should have: a resolvable primary source, exact version, quoted theorem location, reproduced assumptions, a clear applicability analysis, and an uncertainty label if any dependency remains unverified.
