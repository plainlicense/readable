---
# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

title: Flesch-Kincaid Grade Level
description: Outputs a US grade level directly using sentence length and syllables per word. Developed for the US Navy in 1975 — it targets 75% comprehension, not full comprehension, and will score 2–4 grade levels lower than SMOG on the same text.
---

Kincaid, Fishburne, Rogers, and Chissom developed this formula in 1975 under a US Navy contract. It uses the same two inputs as Flesch Reading Ease — words per sentence and syllables per word — but outputs a US grade level directly instead of a 0–100 score.

## At a Glance

| | |
|---|---|
| **Output** | US grade level (higher = harder) |
| **Best for** | General prose, government documents, compliance checking |
| **Method** | `r.flesch_kincaid()` |
| **What it counts** | Words per sentence, syllables per word |
| **Minimum text** | 100 words (default) |

:::caution[Flesch-Kincaid scores lower than SMOG — this is expected]
Flesch-Kincaid targets **75% comprehension**. SMOG targets **100% comprehension**. On the same text, SMOG will typically score 2–4 grade levels **higher** than Flesch-Kincaid. This is not an error in either formula. A text scoring grade 7 on Flesch-Kincaid may score grade 10–11 on SMOG. Do not compare the two scores as if they measure the same thing.
:::

## When to Use This Metric

- You need a grade level output that non-technical stakeholders can act on immediately. "Grade 8" is more actionable than a 0–100 score. This was the main reason the Navy commissioned the formula — Flesch Reading Ease required a lookup table, and the Navy wanted a number that was directly interpretable.
- You must meet a compliance requirement. The US Army adopted Flesch-Kincaid for technical publications in 1978. The IRS, Social Security Administration, and many state insurance codes specify Flesch-Kincaid grade level limits.
- You are screening general-purpose prose — news articles, government web content, business writing — for gross readability problems.
- You want a grade level from the same inputs as Flesch Reading Ease. Use [Flesch Reading Ease](/readable/metrics/flesch/) if you want a 0–100 ease score from the same formula.

## How It Works

Flesch-Kincaid counts the average number of words per sentence and the average number of syllables per word. Text with short sentences and simple words scores low. Text with long sentences and complex words scores high.

```
grade level = (0.38 × words per sentence) + (11.8 × syllables per word) − 15.59
```

The syllable coefficient (11.8) is about 31 times larger than the sentence-length coefficient (0.38). This means word complexity drives the score far more than sentence length does. Shortening sentences while keeping complex vocabulary will barely move the result. Replacing polysyllabic words with simpler ones will.

The output is a continuous float. `grade_levels` rounds it to the nearest integer. A score of 8.4 becomes `["8"]`.

## Score Interpretation

| Grade Level | Reading Context | What this looks like |
|-------------|-----------------|----------------------|
| 1–4 | Elementary school | Early readers, children's books |
| 5–6 | Late elementary | Children's magazines, simple stories |
| 7–8 | Middle school | Most news articles, general web content |
| 9–10 | Early high school | Business writing, quality newspapers |
| 11–12 | Late high school | Academic writing, professional journals |
| 13+ | College | Legal documents, dense academic prose |

A grade level below 0 is mathematically possible for very short, simple sentences with monosyllabic words. The library does not clamp the result.

:::note[Grade levels are US-calibrated]
These grade levels reflect US schooling conventions. Grade 8 corresponds to approximately age 13–14. Grade 12 is the final year of secondary school, roughly age 17–18. The formula was normed in 1975 against 531 US Navy enlisted personnel reading Navy technical manuals — a narrow population.
:::

## Return Values

`r.flesch_kincaid()` returns a `FleschKincaidResult` object:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw grade level as a float, e.g. `8.4` |
| `grade_levels` | `list[str]` | Grade level rounded to nearest integer, e.g. `["8"]` |
| `grade_level` | `str` | The primary grade level (first item in `grade_levels`) |

## Minimum Requirements

The library defaults to a 100-word minimum. Passing fewer words raises a `ValueError`. You can lower the threshold with `Readability(text, min_words=50)`, but scores from short texts are less stable.

```python
# Fewer than 100 words — raises ValueError by default
r = Readability(short_text)
r.flesch_kincaid()  # ValueError: 100 words required.

# Lower the minimum if needed
r = Readability(short_text, min_words=50)
r.flesch_kincaid()  # Runs, but with reduced reliability
```

## Limitations

- **The formula was normed on a narrow population.** The 531 Navy enlisted personnel in the 1975 study were predominantly young, American, male, and reading Navy technical manuals. The formula generalizes well to general prose, but it was not calibrated for diverse audiences or modern document types.
- **Short medical and technical jargon is invisible.** A sentence like "The patient presented with acute MI and low EF" scores as relatively accessible because those terms are short. The formula cannot tell the difference between a short familiar word and a short specialist term.
- **Flesch-Kincaid and SMOG are not comparable.** Because they target different comprehension thresholds (75% vs. 100%), a text scoring grade 7 on Flesch-Kincaid may still be difficult for many readers. Healthcare organizations including the Centers for Medicare & Medicaid Services have explicitly warned that Flesch-Kincaid underestimates reading difficulty in health materials.
- **The formula does not measure comprehension directly.** Two sentences of the same length — one clear, one tortured with embedded clauses — score identically. The formula responds only to word count per sentence and average syllable count.

## Example

```python
from readable import Readability

text = """
Government agencies use readability scores to check that public communications
are accessible to most citizens. A document written at grade 8 or below should
be readable by most adults in the United States. Grade levels above 12 signal
that the text may be too complex for a general audience, even if the subject
matter itself is not inherently difficult. The goal is not to remove precision —
it is to express ideas in the clearest possible language for the intended reader.
Writers who work on public-facing documents often run readability checks as part
of their editing process, tracking changes in score across successive drafts.
"""

r = Readability(text)
result = r.flesch_kincaid()

print(f"Score: {result.score:.1f}")        # Score: ~10.2
print(f"Grade: {result.grade_levels}")    # ['10']
```

## See Also

- [Flesch Reading Ease](/readable/metrics/flesch/) — same inputs, outputs a 0–100 ease score instead of a grade level
- [SMOG Index](/readable/metrics/smog/) — targets 100% comprehension; scores 2–4 grade levels higher than Flesch-Kincaid on the same text
- [Choosing a Metric](/readable/choosing-a-metric/) — decision guide for all nine metrics
