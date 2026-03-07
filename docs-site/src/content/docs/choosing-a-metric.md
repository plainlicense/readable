---
# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

title: Choosing a Metric
description: Not all readability metrics measure the same thing. This guide helps you pick the right one for your text and audience.
---

readscore supports nine readability metrics. They are not interchangeable. Each formula
was built for a specific context, makes different assumptions, and targets a different
kind of reader. Picking the wrong metric gives you a number that means nothing.

This guide helps you choose.

## Quick Selector

Find your situation in the left column. The right column tells you which metric to start with.

| My text is... | Use this metric |
|---------------|-----------------|
| For young readers (grades 1–3) | [Spache](/metrics/spache/) |
| For children (grades 4+) | [Dale-Chall](/metrics/dale-chall/) |
| For a general adult audience | [Flesch Reading Ease](/metrics/flesch/) |
| For health communications or patient materials | [SMOG](/metrics/smog/) |
| For technical documentation or manuals | [ARI](/metrics/ari/) |
| For military or government documents | [ARI](/metrics/ari/) or [Linsear Write](/metrics/linsear-write/) |
| I need a US grade level number directly | [Flesch-Kincaid](/metrics/flesch-kincaid/) |
| I need the most widely recognized single metric | [Flesch Reading Ease](/metrics/flesch/) |
| My text has fewer than 30 sentences | Anything except [SMOG](/metrics/smog/) |
| I want to avoid syllable counting | [ARI](/metrics/ari/) or [Coleman-Liau](/metrics/coleman-liau/) |

## SMOG and Flesch-Kincaid Are Not Comparable

:::danger[Do not mix SMOG and Flesch-Kincaid scores in the same analysis]
SMOG and Flesch-Kincaid target different comprehension thresholds:

- **SMOG** was designed for **100% comprehension** — the grade level at which virtually
  all readers can understand the text.
- **Flesch-Kincaid** was designed for **75% comprehension** — the grade level at which
  most readers can follow it.

On the same text, SMOG consistently scores **2–4 grade levels higher** than
Flesch-Kincaid. If your text scores grade 8 on FK and grade 11 on SMOG, both scores
are correct. They just answer different questions.

If you report one to stakeholders, use only that metric. If you report both, explain
what each measures.
:::

## What Each Metric Counts

The inputs a metric uses tell you a lot about what it can and cannot detect.

| Metric | Sentence length | Syllables per word | Character count | Word list |
|--------|:-:|:-:|:-:|:-:|
| [Flesch Reading Ease](/metrics/flesch/) | Yes | Average | — | — |
| [Flesch-Kincaid](/metrics/flesch-kincaid/) | Yes | Average | — | — |
| [Gunning Fog](/metrics/gunning-fog/) | Yes | Count (3+) | — | — |
| [SMOG](/metrics/smog/) | — | Count (3+) | — | — |
| [ARI](/metrics/ari/) | Yes | — | Letters + digits | — |
| [Coleman-Liau](/metrics/coleman-liau/) | Yes | — | Letters only | — |
| [Dale-Chall](/metrics/dale-chall/) | Yes | — | — | 3,000 familiar words |
| [Spache](/metrics/spache/) | Yes | — | — | Primary-grade word list |
| [Linsear Write](/metrics/linsear-write/) | Yes | Weighted | — | — |

**Character-based metrics (ARI, Coleman-Liau)** count letters instead of syllables.
This makes them fully deterministic — two systems always agree — and better at handling
technical jargon where syllable counting is unreliable.

**Word-list metrics (Dale-Chall, Spache)** check each word against a list of familiar
words. This captures vocabulary difficulty more directly but requires the word list to
match your audience and era. Both lists were built in the mid-20th century, which
affects modern vocabulary coverage.

**Syllable-based metrics (Flesch, Flesch-Kincaid, Gunning Fog, SMOG)** treat longer
words as harder. This holds up well across general prose but breaks down for text
with many short technical terms or long common words.

## Score Types

All metrics except Flesch return a US grade level or education level. Flesch returns
an ease score that runs from 0 to 100.

| Metric | Score type | Extra fields |
|--------|------------|--------------|
| Flesch Reading Ease | 0–100 ease score (higher = easier) | `ease` (text label) |
| Flesch-Kincaid | US grade level | — |
| SMOG | US grade level | — |
| ARI | US grade level | `ages` (age range) |
| Coleman-Liau | US grade level | — |
| Gunning Fog | Years of formal education needed | — |
| Dale-Chall | Raw score mapped to grade bands | — |
| Spache | US grade level | — |
| Linsear Write | US grade level | — |

:::note[Grade levels are US-specific]
All grade levels in this library are calibrated for the US school system. Grade 8 means
the reading level of a US 8th grader (age 13–14). International users can use ARI's
`ages` field as a more portable alternative — age ranges translate across educational
systems better than grade names do.

Approximate mapping: grades 1–5 = primary school, grades 6–8 = middle school,
grades 9–12 = secondary/high school, college = undergraduate.
:::

## Minimum Text Requirements

| Metric | Minimum | What happens if too short |
|--------|---------|--------------------------|
| Most metrics | 100 words (default) | `ValueError` on construction |
| SMOG | 30 sentences | `ValueError` by default; pass `ignore_length=True` for a warning |

You can lower the 100-word default with `Readability(text, min_words=N)`, but scores
from short texts are less reliable.

## Same Text, Different Results

Running all nine metrics on the same paragraph shows how much the scores can vary.
The paragraph below is from this library's README — a description of the Gunning Fog
index, written at roughly a 10th–12th grade level.

```python
from readscore import Readability

text = """
In linguistics, the Gunning fog index is a readability test for English writing.
The index estimates the years of formal education a person needs to understand
the text on the first reading. For instance, a fog index of 12 requires the
reading level of a United States high school senior (around 18 years old).
The test was developed in 1952 by Robert Gunning, an American businessman
who had been involved in newspaper and textbook publishing.
"""

r = Readability(text)

print(r.flesch().score)          # ~52.4  → "fairly_difficult" → grades 10–12
print(r.flesch_kincaid().score)  # ~11.8  → grade 12
print(r.ari().score)             # ~11.9  → grade 12, ages [17, 18]
print(r.coleman_liau().score)    # ~12.1  → grade 12
print(r.gunning_fog().score)     # ~13.2  → college level
print(r.dale_chall().score)      # ~7.4   → grades 9–10
print(r.linsear_write().score)   # ~11.0  → grade 11

# SMOG raises ValueError — this paragraph has fewer than 30 sentences
# r.smog()  →  ValueError: SMOG requires at least 30 sentences. 6 found.

# Spache runs but is outside its valid range — designed for grades 1–3
print(r.spache().score)          # ~4.1   → grade 4 (not meaningful for adult text)
```

The Spache result illustrates why metric selection matters. Spache was designed for
primary school text. Applying it to adult prose produces a score that is technically
computed but practically meaningless.

## Combining Multiple Metrics

Running several metrics and comparing the results is a valid approach when:

- You want to reduce the effect of any single formula's quirks on your assessment
- You want to flag text where metrics disagree significantly, which can indicate unusual
  sentence structure, heavy jargon, or formatting that confuses the parsers

```python
r = Readability(text)

grade_estimates = [
    r.flesch_kincaid().grade_level,
    r.ari().grade_level,
    r.coleman_liau().grade_level,
]
average = sum(grade_estimates) / len(grade_estimates)
spread = max(grade_estimates) - min(grade_estimates)

print(f"Average grade estimate: {average:.1f}")
print(f"Spread across metrics: {spread} grades")
```

A large spread (4+ grade levels) between metrics on the same text is a signal to look
more closely. It often means the text has features that one formula handles differently —
heavy technical terms, very short sentences with long words, or non-prose formatting.

:::caution[Do not mix Flesch ease scores with grade-level metrics]
Flesch Reading Ease produces a score from 0 to 100 on an inverted scale (higher = easier).
It cannot be averaged with grade-level metrics without conversion. Keep Flesch scores
separate or use Flesch-Kincaid for any analysis that combines metrics.
:::

## Metric Strengths at a Glance

| Metric | Particularly strong when... |
|--------|----------------------------|
| Flesch Reading Ease | Communicating ease to non-technical audiences; legal compliance |
| Flesch-Kincaid | Reporting US grade level; government and education contexts |
| SMOG | Health communications; when 100% comprehension matters |
| ARI | Technical manuals; avoiding syllable-counting errors on jargon |
| Coleman-Liau | Batch processing; deterministic results at scale |
| Gunning Fog | Business and journalism contexts; identifying "foggy" prose |
| Dale-Chall | Educational materials; validating vocabulary for grade 4+ audiences |
| Spache | Primary school materials; grades 1–3 only |
| Linsear Write | Military and government technical documents |
