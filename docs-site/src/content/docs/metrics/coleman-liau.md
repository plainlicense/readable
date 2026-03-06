---
# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

title: Coleman-Liau Index
description: Estimates US grade level using letter count and sentence length. Designed in 1975 for optical scanners that could detect character boundaries without recognizing characters.
---

Meri Coleman and T.L. Liau published this formula in 1975 in the *Journal of Applied Psychology*.
They designed it for optical scanning devices that could count how many characters were in a word
without knowing which letters they were. That hardware constraint is long gone, but the formula
remains useful: it is fully deterministic, requires no phonological analysis, and scores
consistently across processing environments.

## At a Glance

| | |
|---|---|
| **Output** | US grade level |
| **Best for** | Educational content, curriculum materials, legal and health literacy analysis |
| **Method** | `r.coleman_liau()` |
| **What it counts** | Letters per word (no digits), sentences per 100 words |
| **Minimum text** | 100 words (default) |

## When to Use This Metric

- You are evaluating **educational or curriculum materials**. Coleman and Liau developed the
  formula specifically for assessing US public school textbooks. It is well calibrated for
  grade 4 through 12 content.
- You want **fully deterministic scores**. Coleman-Liau counts only letters and sentence
  boundaries. No syllable heuristics, no phoneme rules. Two tools always agree on the same text.
- You are running **readability checks at scale**. The formula is a single pass over the text
  with no dictionary lookups. For batch processing of large document collections, this matters.
- You want to **cross-check ARI**. The two formulas use similar approaches but handle numerals
  differently. Running both and comparing is a quick way to detect whether digit-heavy content
  is driving a score in either direction.

## How It Works

Coleman-Liau counts letters in each word and sentence boundaries across the text. It then
normalizes both counts to a per-100-words rate before applying the formula. This normalization
makes the score the same whether you analyze 200 words or 2,000.

```
score = 0.0588 × L - 0.296 × S - 15.8
```

Where:
- `L` = average letters per 100 words (letters only — digits do not count)
- `S` = average sentences per 100 words

A higher `L` means longer words on average, which raises the score. A higher `S` means more
(shorter) sentences per 100 words, which lowers the score. The constant -15.8 anchors the
output to US grade levels.

The result is rounded to the nearest integer for the grade level.

## Score Interpretation

| CLI Score | Grade Level | Reading Context |
|-----------|-------------|-----------------|
| 1–2 | Grades 1–2 | Early primary |
| 3–4 | Grades 3–4 | Primary school |
| 5–6 | Grades 5–6 | Late primary |
| 7–8 | Grades 7–8 | Middle school |
| 9–10 | Grades 9–10 | Early high school |
| 11–12 | Grades 11–12 | High school |
| 13+ | College+ | Post-secondary |

General-audience materials typically target grade 8 to 10. Patient-facing health materials
generally target grade 6 to 8. Legal documents often score at grade 12 to 15.

## Return Values

`r.coleman_liau()` returns a `ColemanLiauResult` object:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw CLI score before rounding |
| `grade_levels` | `list[str]` | Grade level as a single-element list, e.g. `["10"]` |
| `grade_level` | `str` | The first item in `grade_levels` (property on the result) |

Coleman-Liau has no additional fields. The result is a single grade level estimate with no
supplementary data.

## Minimum Requirements

The library defaults to a 100-word minimum. Passing fewer words raises a `ValueError`.

```python
# Fewer than 100 words raises ValueError by default
r = Readability(short_text)
r.coleman_liau()  # ValueError: 100 words required.

# Lower the threshold with min_words — but scores become less reliable below 100 words
r = Readability(short_text, min_words=50)
r.coleman_liau()
```

Coleman and Liau's original paper recommended samples of at least 300 words for reliable
results. The 100-word minimum is a practical floor, not a guarantee of accuracy.

:::caution[ARI and Coleman-Liau diverge on numeral-heavy text]
ARI counts letters and digits. Coleman-Liau counts letters only. On prose, the two formulas
produce similar scores. On text with many numerals — data tables, scientific measurements,
financial figures, code — they can diverge by a grade level or more.

If your content is digit-heavy, run both and check whether they agree. Agreement suggests
the score reflects prose complexity. Significant divergence suggests numerals are distorting
one or both scores. In that case, a syllable-based formula like
[Flesch-Kincaid](/readscore/metrics/flesch-kincaid/) may be more appropriate.
:::

## Limitations

- **Letters-only counting creates edge cases with alphanumeric content.** Coleman-Liau treats
  "H2O", "CO2", and "3D" differently from ARI because digits are excluded. Documents with
  chemical formulas, version numbers, or identifier codes will produce different character-to-word
  ratios than documents where the same concepts are written out in words.
- **Common long words score as hard.** Like ARI, Coleman-Liau cannot tell "interesting" from
  "exsanguination." Both count the same number of letters. The formula has no knowledge of word
  frequency or familiarity.
- **Prose only.** The formula assumes running sentences with clear sentence boundaries. Bullet
  lists, tables, code blocks, and structured forms produce unreliable scores because sentence
  detection fails on non-prose content.
- **English only.** The formula was developed and validated on English-language US school
  textbooks. Letter-length distributions differ across languages, and applying Coleman-Liau to
  non-English text is not appropriate.

## Example

```python
from readscore import Readability

text = """
The judicial opinion in this matter turns on two questions. First, whether the contract
language unambiguously establishes the parties' intent. Second, whether the subsequent
conduct of the parties confirms or contradicts that reading. The court finds that the
contract is ambiguous on its face. The term "reasonable notice" is not defined anywhere
in the agreement, and the parties' course of dealing does not resolve the ambiguity.
Accordingly, the matter is remanded for further factual findings on the parties' intent
at the time of contracting. Each party shall bear its own costs on this appeal.
"""

r = Readability(text)
result = r.coleman_liau()

print(f"Score: {result.score:.1f}")         # Score: ~13.4
print(f"Grade: {result.grade_levels}")      # ['13']
```

## See Also

- [ARI](/readscore/metrics/ari/) — same character-based approach, but counts digits too;
  includes a reader age range in the result
- [Flesch-Kincaid Grade Level](/readscore/metrics/flesch-kincaid/) — uses syllables instead
  of characters; better for content where word familiarity matters more than word length
- [Choosing a Metric](/readscore/choosing-a-metric/) — decision guide for all nine metrics
