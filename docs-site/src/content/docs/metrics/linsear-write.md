---
# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

title: Linsear Write Formula
description: Estimates US grade level by weighting easy and hard words over full-text statistics. Developed in 1966 by John O'Hayre for the US Bureau of Land Management as a plain-language writing tool.
---

John O'Hayre developed Linsear Write in 1966 for the US Bureau of Land Management as a tool
to help government writers produce plainer prose. It classifies every word as easy or hard based
on syllable count, then calculates a grade level from the ratio of hard words to sentence length.

## At a Glance

| | |
|---|---|
| **Output** | US grade level |
| **Best for** | Technical and government documents, polysyllabic jargon assessment |
| **Method** | `r.linsear_write()` |
| **What it counts** | Easy words (1–2 syllables) and hard words (3+ syllables) per sentence |
| **Minimum text** | 100 words (default) |

## When to Use This Metric

- You are assessing technical or government documents where sentence complexity and
  polysyllabic word density are the main concerns. Linsear Write was designed for exactly
  this context — bureaucratic writing that uses long, technical words when shorter ones
  would work.
- You want a fast check on jargon density without needing a word-familiarity list. Unlike
  [Dale-Chall](/metrics/dale-chall/) and [Spache](/metrics/spache/), Linsear
  Write uses no word list. It treats all 3+ syllable words as hard, regardless of domain.
- You are comparing two drafts of a technical document against each other. Linsear Write
  is consistent within a domain, which makes it useful for relative comparisons
  even when the absolute grade level is approximate.
- You want a secondary check to validate results from another metric. Use it alongside
  [ARI](/metrics/ari/) or [Flesch-Kincaid](/metrics/flesch-kincaid/) rather
  than as the sole measure for important decisions.

## How It Works

Linsear Write labels every word as easy (1–2 syllables) or hard (3+ syllables). Easy words
contribute 1 point each; hard words contribute 3 points each. The formula sums those points,
divides by the number of sentences, then converts the result to a grade level.

```
intermediate = (easy_words × 1 + hard_words × 3) / sentences

if intermediate > 20:  grade level = intermediate / 2
if intermediate ≤ 20:  grade level = (intermediate − 2) / 2
```

The two-branch conversion was added to the original formula at some point after O'Hayre
published it. The reasoning behind the split at 20 is not documented.

O'Hayre's original 1966 formula was actually a writing-quality scale — he called it a measure
of "writeability," not readability. A score of 70–80 on his scale meant the prose was
appropriate for a general adult reader; 80 was ideal. The plain-language context matters: his
goal was to move government writers away from passive voice and bureaucratic phrasing by
rewarding monosyllabic words. The Air Force later adopted the formula for its own technical
writing programs, which is why many sources attribute it to the Air Force. O'Hayre and the
Bureau of Land Management are the documented origin.

:::note[This library uses full-text statistics, not a 100-word sample]
The Linsear Write formula was designed to operate on a 100-word sample from the text.
This library applies it to the entire text instead. For long documents, this reduces variance
and produces more stable scores. It also means the result may differ from a hand-calculated
score that follows the original 100-word sampling procedure.
:::

## Score Interpretation

Linsear Write returns a grade level directly. The table below gives context for what each
level represents in practice.

| Score | Grade Level | Reading Context |
|-------|-------------|-----------------|
| 5–6 | Grades 5–6 | Elementary school |
| 7–8 | Grades 7–8 | Middle school |
| 9–10 | Grades 9–10 | Early high school |
| 11–12 | Grades 11–12 | Late high school |
| 13+ | College+ | Post-secondary |

Government plain-language guidelines generally recommend grade 8 or lower for public-facing
documents. A Linsear Write score above 12 on a technical document suggests a high density of
polysyllabic terms that may slow non-specialist readers.

:::caution[The grade-level conversion is not well validated]
The formula that converts the intermediate score to a grade level has unknown authorship.
Testing has shown it can be off by up to two grade levels compared to other well-validated
formulas. For any decision where the grade level matters — legal compliance, accessibility
requirements, health literacy standards — verify Linsear Write results against at least one
other metric.
:::

## Return Values

`r.linsear_write()` returns a `LinsearWriteResult` object:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw Linsear Write score (grade level as a float) |
| `grade_levels` | `list[str]` | Grade level rounded to nearest integer, e.g. `["10"]` |
| `grade_level` | `str` | The primary grade level (first item in `grade_levels`) |

## Minimum Requirements

The library defaults to a 100-word minimum. Passing fewer words raises a `ValueError`.
You can lower this threshold with `Readability(text, min_words=50)`, but scores from
short texts are even less reliable for Linsear Write than for other metrics. The original
formula requires a 100-word sample to operate as designed.

## Limitations

- **The grade-level conversion has unknown authorship and limited validation.** The formula
  that maps the intermediate score to a grade level was added after O'Hayre's original work.
  Who created it and how it was validated against actual reading comprehension is not
  documented. Independent testing has found it can be off by up to two grade levels.
- **Full-text statistics replace the 100-word sample.** O'Hayre's formula operates on a
  100-word passage. This library computes the same calculation across the entire text. This
  is a practical approximation that reduces variance but deviates from the original
  specification. Long texts will produce more stable scores; short texts near the 100-word
  minimum will behave closest to the original design.
- **Syllable count treats all polysyllabic words the same.** "Beautiful" (three syllables)
  and "perpendicular" (five syllables) both count as hard words, even though most readers
  find "beautiful" easy. Linsear Write cannot distinguish between common long words and
  rare technical terms. [Dale-Chall](/metrics/dale-chall/) handles this better for
  general-audience texts.
- **Not designed as a comprehension predictor.** O'Hayre built this formula to change writer
  behavior, not to measure reader comprehension. Using it to guarantee that readers of a
  specific grade level will understand the text goes beyond what the formula was designed to
  do. SMOG and Flesch-Kincaid have substantially more comprehension validation research.

## Example

```python
from readscore import Readability

text = """
Federal land managers must weigh the environmental consequences of proposed
actions before approving new permits. The review process requires coordination
between multiple agencies and public comment periods that can extend for months.
Applicants should submit documentation demonstrating compliance with applicable
regulations and environmental standards.

When an application involves activities with significant potential impacts, an
Environmental Impact Statement may be required. This document must analyze
alternatives, assess cumulative effects, and identify mitigation measures.
The review process is structured to ensure transparency and public participation
at each stage. Agencies must respond to substantive comments and explain how
those comments influenced the final decision.
"""

r = Readability(text)
result = r.linsear_write()

print(f"Score: {result.score:.1f}")        # Score: ~11.2
print(f"Grade: {result.grade_levels}")    # ['11']
print(f"Grade level: {result.grade_level}")  # 11
```

The text above contains many polysyllabic words common to government documents:
"environmental," "consequences," "coordination," "documentation," "compliance." These push
the score into the high school range, which matches what a plain-language review would flag
for revision.

## See Also

- [ARI](/metrics/ari/) — also developed for technical government documents; uses
  character count instead of syllable count and is better validated for grade-level prediction
- [Choosing a Metric](/choosing-a-metric/) — decision guide for all nine metrics,
  including when to combine Linsear Write with other formulas
