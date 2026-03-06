<!--
SPDX-FileCopyrightText: 2026 PlainLicense

SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT
-->

# API Reference Documentation Assessment

**Date**: 2026-03-05
**Question**: Should API reference docs for readscore be auto-generated using Griffe, or written manually?

---

## 1. Docstring Quality Verdict

**The existing docstrings are not good enough to auto-generate useful reference docs. The output would be thin and largely redundant with what a user could learn by reading the source.**

Evidence from the codebase:

- `Readability.__init__`: Two-line docstring. Describes the parameters accurately, but says nothing about what initialization does (analyzes text, initializes a tokenizer, warns on short text).
- `Readability.ari()`: One line — "Calculate Automated Readability Index (ARI)." The return type annotation tells you the same thing. Zero added value.
- `Readability.smog()`: The only method with parameter docs, because SMOG is the only method with non-obvious parameters. This is the exception, not the rule.
- `Readability.statistics()`: One line. No description of what the keys are, what the units mean, or why you would call this vs. reading from `stats` directly.
- `StatSummary`: No docstring beyond "Concrete statistics type for readability measures." All field documentation is inherited from `BaseStatSummary`, which also has no field-level docstrings.
- `BaseStatSummary`: Declares ten fields. No field has a docstring.
- `BaseResult`, `GradeResult`, `ARIResult`, `FleschResult`: One-line class docstrings. No field docstrings. The `grade_level` property on `GradeResult` has one line that essentially restates its signature.
- `ReadabilityMetric`: Reasonably well-structured enum, but the docstrings on methods like `_names` and `_all_names` describe mechanisms, not intent.

The `about` property on each metric class is the best source of human-readscore description in the codebase, but it lives inside the metric implementation classes (`ARI`, `Flesch`, etc.), which are not part of the public API. Users never instantiate them directly.

**If Griffe ran on this codebase today, the output would be a formatted echo of method signatures and one-sentence docstrings.** It would not answer: what does `grade_levels` contain? What is the difference between `grade_level` (property) and `grade_levels` (field)? When does `smog()` raise vs. warn? What do the `ages` values mean? None of that is in the docstrings.

---

## 2. Public API Scope

The public surface is small. A user only needs to know:

**`Readability` class** (the only public entry point)
- `__init__(text, min_words)` — 1 constructor
- `stats` — 1 property returning `StatSummary`
- `ari()`, `coleman_liau()`, `dale_chall()`, `flesch()`, `flesch_kincaid()`, `gunning_fog()`, `linsear_write()`, `smog()`, `spache()` — 9 metric methods
- `statistics()` — 1 utility method returning a plain dict

**Result types** (returned by the methods above, not instantiated by users)
- `GradeResult` — base for 7 metrics: `score`, `grade_levels`, `grade_level`
- `FleschResult` — extends with `ease`
- `ARIResult` — extends with `ages`
- `ScoreResult` — not currently returned by any public method (appears unused in public API)

**`StatSummary`** (accessible via `Readability.stats`)
- 10 fields: `num_letters`, `num_words`, `num_sentences`, `num_syllables`, `num_poly_syllable_words`, `avg_words_per_sentence`, `avg_syllables_per_word`, `num_gunning_complex`, `num_dale_chall_complex`, `num_spache_complex`

**`ReadabilityMetric` enum** (secondary API for programmatic access)
- 9 enum values
- `measure_class` property
- `metrics()` classmethod

Total documented items if written manually: roughly 25-30 entries. This is a small API.

---

## 3. Griffe Integration Options for Starlight

Griffe's primary ecosystem is MkDocs/mkdocstrings. Its relationship with Starlight is:

**There is no native Starlight plugin for Griffe.** Searching the Starlight plugin directory and npm confirms this gap. The Starlight ecosystem has plugins for OpenAPI (starlight-openapi) and TypeDoc (starlight-typedoc), but nothing targeting Python source.

**The realistic options are:**

**Option A: griffe2md (the Python package)**
`griffe2md` is the mkdocstrings project's own tool for rendering Griffe-extracted data to Markdown using Jinja templates. It produces `.md` files that could theoretically be dropped into Starlight's content directory.

Problems with this approach:
- `griffe2md` is an early-stage, experimental tool. It was created to demonstrate the concept, not for production use. Its README describes it as "a proof of concept."
- The output format is designed for MkDocs, not Starlight. Frontmatter and directory structure would need post-processing.
- Generated files would need to be either committed to the repo or regenerated at build time. Astro's build pipeline is Node.js; running a Python subprocess during `astro build` is non-standard and requires additional tooling.
- You would need a build script (likely in `package.json`) to run `griffe2md` before Astro builds. This adds a Python runtime dependency to the docs build environment.

**Option B: Griffe as a Python script, output committed to repo**
Write a small Python script that calls the Griffe API directly, renders custom output for each class and method, and writes `.md` files into the Starlight content directory. Run this manually when the API changes.

Problems: Still requires Jinja templating work, still produces output that needs manual review before commit, and the "run manually when API changes" step is easy to forget.

**Option C: Custom Astro integration using Griffe JSON output**
Griffe can serialize its extracted data to JSON via `griffe dump readscore`. An Astro integration could read this JSON at build time and generate pages. This is architecturally sound but requires building the integration from scratch — substantial work for a small library with no existing Python/Astro integration community.

**None of these options are off-the-shelf.** All require custom work to bridge Python source extraction and Starlight's Node.js build process.

---

## 4. Recommendation

**Write the API reference manually.**

The reasons are:

1. **The docstrings are not good enough to generate useful output.** To get value from Griffe, the docstrings would need to be substantially rewritten first — at which point the manual writing work is already done.

2. **The public API is small.** A library with one public class, 9 metric methods, and 3 result types is not a candidate for auto-generated reference docs. Auto-generation adds overhead when the surface area is small enough to cover in a few hundred lines of Markdown.

3. **There is no supported Griffe-Starlight path.** Building a working integration requires custom tooling. The maintenance burden (keeping a build-time Python dependency working in a Node.js build environment across versions) is not justified for this library's scale.

4. **The existing `doc-framework.md` already defines exactly what the reference page should cover.** The metric-specific notes, field descriptions, and return value tables in that document are more complete than anything Griffe would extract from the current codebase. The work is mostly done in plan form.

5. **Manual docs can cover what code cannot.** The most useful things to document about this API — when does `smog()` raise vs. warn, what `grade_levels` values look like in practice, why `statistics()` exists alongside `stats`, the difference between `num_poly_syllable_words` and `num_gunning_complex` — are behavioral and contextual. Griffe extracts signatures and docstrings; it does not extract wisdom.

The one advantage of auto-generation — keeping docs in sync with code automatically — is less important here because the API has been stable since the refactor and is intentionally small.

---

## 5. Manual Reference Page Structure

Given the recommendation to write manually, here is what the API reference should cover and how to structure it.

The reference belongs in `docs-site/src/content/docs/reference/`. A single file is likely sufficient: `api.md` or `readability.md`. If the content grows unwieldy, split into `readability.md` and `types.md`.

### Proposed Structure

```
# API Reference

Brief orientation paragraph: what's here, what's not (metric docs are in /metrics/).

## Readability

### Constructor

Readability(text, min_words)
- text parameter
- min_words parameter, default, warning behavior
- What initialization does (analyzes text, computes stats eagerly)

### Properties

stats -> StatSummary
- When to use this vs. statistics()
- All fields listed (link to StatSummary section)

### Metric Methods

Pattern for all 9 methods: signature, return type, link to metric doc page, note on ValueError.

ari() -> ARIResult
coleman_liau() -> ColemanLiauResult
dale_chall() -> DaleChallResult
flesch() -> FleschResult
flesch_kincaid() -> FleschKincaidResult
gunning_fog() -> GunningFogResult
linsear_write() -> LinsearWriteResult
smog(all_sentences, ignore_length) -> SmogResult    [SMOG gets expanded treatment for its params]
spache() -> SpacheResult

### Utility Methods

statistics() -> dict
- All keys listed (num_letters, num_words, num_sentences,
  num_polysyllabic_words, avg_words_per_sentence, avg_syllables_per_word)
- Note: subset of what stats provides; explain why this exists

## Result Types

### GradeResult (base for most metrics)

Fields:
- score: float — the raw formula output
- grade_levels: list[str] — one or more US grade level strings
  (possible values: "K", "1"..."12", "college", "college_graduate", "na")
- grade_level (property): str — first item in grade_levels

### FleschResult

Inherits GradeResult. Adds:
- ease: str — one of seven snake_case labels (list all 7 with score ranges)

### ARIResult

Inherits GradeResult. Adds:
- ages: list[int] — two-element list [lower, upper] for typical reader age range

## StatSummary

All 10 fields with types and descriptions:
- num_letters: int — total character count (excluding spaces and punctuation)
- num_words: int
- num_sentences: int
- num_syllables: int
- num_poly_syllable_words: int — words with 3 or more syllables
- avg_words_per_sentence: float
- avg_syllables_per_word: float
- num_gunning_complex: int — polysyllabic words excluding proper nouns and
  hyphenated compounds (Gunning Fog definition)
- num_dale_chall_complex: int — words not on the Dale-Chall familiar word list
- num_spache_complex: int — words not on the Spache familiar word list

Note: StatSummary is a frozen dataclass. All fields are read-only.

## ReadabilityMetric Enum

ReadabilityMetric.ARI ... ReadabilityMetric.SPACHE

Methods:
- ReadabilityMetric.metrics() -> list[str] — sorted list of all metric names
- ReadabilityMetric.measure_class — returns the internal measure class
  (advanced use: instantiating metrics directly with a StatSummary)

Note on when to use: primarily useful for programmatic iteration over all metrics.

## Exceptions

ValueError: raised when word count (or sentence count for SMOG) is below minimum.
UserWarning: raised when min_words < 100 at construction, or when SMOG is called
             with ignore_length=True on fewer than 30 sentences.
```

### What to Exclude

Do not document `BaseMeasure`, `BaseResult`, `BaseStatSummary` in the user reference. They are for library extension (covered in the Extending guide). Do not document `TextAnalyzer`, `Tokenizer`, `ResourceLoader`, or the individual metric classes (`ARI`, `Flesch`, etc.) — these are internal.

---

## 6. If Griffe Is Reconsidered Later

If the docstrings are substantially improved in a future pass, the path with the least integration cost would be:

1. Install `griffe` and `griffe2md` as dev dependencies in `pyproject.toml`
2. Write a Python build script that runs `griffe2md readscore --output docs-site/src/content/docs/reference/` with a custom template
3. Add `uv run python scripts/generate-api-docs.py` as a pre-build step in `docs-site/package.json`
4. Commit the generated files (do not gitignore them — Starlight needs them at build time, and a CI-only Python dep adds complexity)

The minimum docstring quality needed to make this worthwhile: all public parameters documented with types and descriptions, all return value fields described with example values, all exceptions documented. The current codebase does not meet that bar.

---

## Summary

| Question | Answer |
|----------|--------|
| Are docstrings good enough for auto-gen? | No. They are thin and would produce near-useless output. |
| Is the API large enough to justify tooling? | No. ~25 public items is manageable manually. |
| Is there a native Starlight-Griffe plugin? | No. No such plugin exists. |
| What is the cheapest working path? | Manual reference doc in `docs-site/src/content/docs/reference/`. |
| When would Griffe be worth revisiting? | If docstrings are substantially rewritten AND the API grows significantly. |
