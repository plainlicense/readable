---
title: SMOG Index
description: Estimates US grade level by counting polysyllabic words across 30 sentences. Designed for 100% comprehension — it scores higher than Flesch-Kincaid on the same text by design.
---

G. Harry McLaughlin developed SMOG (Simple Measure of Gobbledygook) in 1969 as a faster,
more reliable alternative to the Flesch-Kincaid formula for health and educational
materials. It counts words with three or more syllables across a 30-sentence sample and
returns a US grade level.

## At a Glance

| | |
|---|---|
| **Output** | US grade level |
| **Best for** | Health communications, patient materials, public health documents |
| **Method** | `r.smog()` |
| **What it counts** | Polysyllabic words (3+ syllables) in a 30-sentence sample |
| **Minimum text** | 30 sentences (hard requirement) |

:::caution[SMOG and Flesch-Kincaid are not comparable]
SMOG and Flesch-Kincaid target different comprehension thresholds. SMOG was designed for
**100% comprehension** — the grade level at which virtually all readers understand the
text. Flesch-Kincaid targets **75% comprehension**. On the same text, SMOG will typically
score 2–4 grade levels **higher** than Flesch-Kincaid. This is not an error. Do not
compare SMOG and FK scores as if they measure the same thing.
:::

## When to Use This Metric

- You are writing or reviewing **health communications**: patient instructions, consent
  forms, public health campaigns, or cancer screening materials. The National Cancer
  Institute and Harvard T.H. Chan School of Public Health both recommend SMOG for
  assessing health literacy materials.
- You need to ensure that text is accessible to the **lowest-literacy readers** in your
  audience, not just most readers. SMOG's 100% comprehension target makes it
  conservative — a good property when the stakes are high.
- You are working with documents that have clear sentence structure and at least 30
  sentences. SMOG is reliable only within that range.
- You want a formula that is **robust to sentence length manipulation**. Because SMOG
  counts polysyllabic words rather than averaging syllables, it is harder to game with
  sentence-length tricks than Flesch or Flesch-Kincaid.

## How It Works

SMOG selects 30 sentences from the text: the first 10, 10 from the middle, and the last
10. It then counts every word with three or more syllables in that sample and applies:

```
score = 1.0430 × √(30 × polysyllabic words / sentences) + 3.1291
```

The result is a grade level. A score of 9 means the text requires a 9th-grade reading
level for full comprehension.

McLaughlin's key insight was that counting polysyllabic words in a fixed sentence sample
captures the combined effect of word complexity and sentence length without needing
multiplication. The formula is simple to apply by hand — which was important for its
original use in clinical and public health settings before computers were widespread.

## Score Interpretation

SMOG returns a grade level directly. Grade 12 means high school level; grade 9 means
middle-high school level.

| SMOG Score | Grade Level | Reading Context |
|------------|-------------|-----------------|
| 5–6 | Grades 5–6 | Elementary school |
| 7–8 | Grades 7–8 | Middle school |
| 9–10 | Grades 9–10 | Early high school |
| 11–12 | Grades 11–12 | Late high school |
| 13+ | College+ | Post-secondary |

Health literacy guidelines generally recommend a target of grade 6–8 for patient-facing
materials. If SMOG returns grade 10 or higher, the text is likely too complex for a
general patient population.

## Return Values

`r.smog()` returns a `SmogResult` object:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw SMOG score (grade level as a float) |
| `grade_levels` | `list[str]` | Grade level rounded to nearest integer, e.g. `["9"]` |
| `grade_level` | `str` | The primary grade level (first item in `grade_levels`) |

## Minimum Requirements

SMOG requires **at least 30 sentences**. By default, passing fewer raises a `ValueError`.

```python
# Fewer than 30 sentences — raises ValueError by default
r = Readability(short_text)
r.smog()  # ValueError: SMOG requires at least 30 sentences. 12 found.

# Use ignore_length=True to get a best-effort score with a warning instead
r.smog(ignore_length=True)  # UserWarning + score computed on available sentences

# Use all_sentences=True to score the full text instead of the 30-sentence sample
r.smog(all_sentences=True)
```

:::note[When to use ignore_length]
`ignore_length=True` is appropriate for exploratory analysis or when you understand the
limitations. It is not appropriate when you need to meet a health literacy standard —
SMOG scores on fewer than 30 sentences are statistically unreliable.
:::

## Limitations

- **30-sentence minimum is a hard constraint for reliable results.** Short documents,
  executive summaries, and web copy rarely have 30 sentences. For shorter texts, use
  [Flesch-Kincaid](/readable/metrics/flesch-kincaid/) or [ARI](/readable/metrics/ari/).
- **SMOG scores higher than other metrics by design — this surprises users.** A text
  that scores grade 8 on Flesch-Kincaid may score grade 11–12 on SMOG. Neither score
  is wrong; they measure different things (75% vs. 100% comprehension).
- **Polysyllabic word counting can be fooled.** Proper nouns ("Philadelphia",
  "Connecticut"), technical abbreviations read aloud ("API" → "A-P-I"), and common
  long words ("beautiful", "interesting") all count as polysyllabic even when readers
  find them perfectly easy.
- **Prose only.** Like all formula-based metrics, SMOG assumes running sentences. It
  is not valid for tables, lists, or structured forms.

## Example

```python
from readable import Readability

# This text is long enough to meet the 30-sentence minimum
text = """
Adults with low health literacy are more likely to be hospitalized and less likely to
follow treatment plans. Plain language can help. When patients understand their
instructions, they take their medication correctly. They keep their follow-up
appointments. They recognize warning signs earlier.

Writing at a lower reading level does not mean writing less information. It means
organizing information clearly and using words that most people know. Short sentences
help, but they are not enough on their own. Choosing common words matters more.

A patient who reads at grade 6 can still understand complex ideas. What they need is
for those ideas to be expressed in words they recognize. The goal is not to simplify
the concept — it is to make the language match the reader.

Health writers often underestimate how hard their text is to read. They are experts
in their field, and expert language feels natural to them. Running a SMOG check is
a simple way to find out whether the text works for the intended audience. A target
of grade 6 to 8 is appropriate for most patient-facing health materials. Materials
above grade 10 should be revised before distribution to a general patient population.
Consent forms, discharge instructions, and medication guides are all high-stakes
documents where readability directly affects patient safety.
"""

r = Readability(text)
result = r.smog()

print(f"Score: {result.score:.1f}")       # Score: ~9.2
print(f"Grade: {result.grade_levels}")   # ['9']
```

## See Also

- [Flesch-Kincaid Grade Level](/readable/metrics/flesch-kincaid/) — targets 75%
  comprehension; scores lower than SMOG on the same text
- [Gunning Fog](/readable/metrics/gunning-fog/) — also counts polysyllabic words but
  uses a different sample and weighting scheme
- [Choosing a Metric](/readable/choosing-a-metric/) — includes an explanation of why
  SMOG and Flesch-Kincaid scores are not directly comparable
