---
# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

title: Dale-Chall Readability Formula
description: Checks words against a 3,000-word familiar-word list to estimate grade level for text aimed at grade 4 and above. Developed by Edgar Dale and Jeanne Chall in 1948.
---

Edgar Dale and Jeanne Chall developed this formula in 1948 to measure reading difficulty
by checking whether words are familiar to a typical 4th-grade reader, rather than counting
syllables or characters.

## At a Glance

| | |
|---|---|
| **Output** | Raw score (4–10+) that maps to grade bands |
| **Best for** | Educational materials, patient health content, general adult audiences |
| **Method** | `r.dale_chall()` |
| **What it counts** | Unfamiliar words (not on the 3,000-word list), words per sentence |
| **Minimum text** | 100 words (default) |

## When to Use This Metric

- You are writing for a **general adult audience** and vocabulary familiarity is the
  primary concern. Dale-Chall has more validation research for educational and patient
  materials than any other formula in this library.
- You are checking **patient education materials**, health pamphlets, or consumer health
  information. Multiple systematic reviews name Dale-Chall as the highest-validity formula
  for these use cases.
- You are assessing **government documents or public information** materials intended for
  general adult comprehension.
- You need to check text aimed at **grade 4 and above**. For younger readers (grades 1–3),
  use [Spache](/metrics/spache/) instead.

## How It Works

Dale-Chall checks each word in the text against a list of approximately 3,000 words that
80% of American 4th-grade students recognized during data collection. Words not on the
list are counted as "difficult." The formula then combines the percentage of difficult words
with average sentence length.

```
raw_score = 0.1579 × (difficult_words / total_words × 100) + 0.0496 × (total_words / sentences)
```

If more than 5% of words are difficult, the formula adds a fixed adjustment:

```
adjusted_score = raw_score + 3.6365
```

:::caution[The score can appear to jump discontinuously]
When the percentage of difficult words crosses the 5% threshold, the formula adds 3.6365
to the raw score. This is built into the formula, not an error. A text with 4.9% difficult
words will score noticeably lower than a nearly identical text with 5.1% difficult words.
The adjustment reflects the non-linear reality that frequent unfamiliar words disrupt
reading fluency in ways a linear formula cannot capture.
:::

### The word list

The library implements the "New Dale-Chall" — the 1948 formula coefficients combined with
the revised 1995 word list (Chall & Dale, *Readability Revisited*). The 1995 revision
expanded the list from about 769 words to approximately 3,000.

Words on the list in their base form are also familiar in these inflected forms:
regular plurals (`-s`, `-es`), past tense (`-ed`), progressive (`-ing`), comparative
(`-er`), and superlative (`-est`). Derivational suffixes that create new words are not
covered. For example, `complete` is on the list, but `completion` is counted as difficult.

Proper nouns (names of people and places) are treated as familiar regardless of whether
they appear on the list.

## Score Interpretation

Dale-Chall scores do not map to individual grade levels. They map to **grade bands**. The
formula cannot distinguish between grade 1 and grade 4 text; both fall in the same band.

| Raw Score | Grade Band | Reading Level |
|-----------|------------|---------------|
| 4.9 and below | Grades 1–4 | Elementary school |
| 5.0–5.9 | Grades 5–6 | Upper elementary |
| 6.0–6.9 | Grades 7–8 | Middle school |
| 7.0–7.9 | Grades 9–10 | Early high school |
| 8.0–8.9 | Grades 11–12 | Late high school |
| 9.0–9.9 | College | Undergraduate |
| 10.0 and above | College graduate | Graduate/professional |

A score of 7.5, for example, places a text at approximately grades 9–10. The `grade_levels`
field returns this band as a list: `["9", "10"]`.

## Return Values

`r.dale_chall()` returns a `DaleChallResult` object:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw Dale-Chall score, typically 4–10 |
| `grade_levels` | `list[str]` | Grade band for this score, e.g. `["9", "10"]` or `["college"]` |
| `grade_level` | `str` | First item in `grade_levels` (the lower bound of the band) |

## Minimum Requirements

The library defaults to a 100-word minimum. Passing fewer words raises a `ValueError`.
You can lower this threshold with `Readability(text, min_words=50)`, but scores from
short texts are less reliable.

## Limitations

- **Does not work well for technical or software documentation.** Words like "cookie,"
  "stream," "execute," "crash," and "enter" appear on the familiar-word list in their
  everyday English senses. A page about browser cookies or command-line syntax will score
  as easier than it actually is for readers without that domain knowledge.

:::caution[The polysemy problem]
The Dale-Chall word list contains words, not word senses. "Cookie" (the baked good) and
"cookie" (the browser storage mechanism) receive the same score. A text heavy with
technical terminology that happens to share names with everyday words will score
misleadingly easy. This is a concrete limitation for software documentation, user
interfaces, and technical writing aimed at non-specialist audiences.
:::

- **Not appropriate for grades 1–3.** The formula's lowest score band covers grades 1–4
  as a single undifferentiated range. It cannot distinguish between a text appropriate for
  grade 1 and one appropriate for grade 4. Use [Spache](/metrics/spache/) for
  primary-grade text.

- **The word list reflects 1984 American English.** The 1995 revision was calibrated on
  word familiarity data from approximately 1984. Words common in contemporary life but
  absent from that era — "app," "email," "wifi," "streaming" — are not on the list and
  will be counted as difficult. Agricultural vocabulary from mid-20th-century American
  life, such as "haystack" and "bushel," appears on the list even though many contemporary
  readers may not recognize these words.

- **Derivational suffixes count as difficult.** A text using abstract nouns ending in
  `-tion`, `-ment`, or `-ation` will score harder than a text using the same root words
  in base form, because the suffixes create "new words" not covered by the list.
  `Complete` is familiar; `completion` is difficult.

:::note[Porter stemming in this library]
The library uses Porter stemming to match words against the Dale-Chall list. This is an
engineering compromise, not a validated approach. Porter stemming aggressively reduces
words to root forms, which can cause some derivational forms to match list entries when
the original Dale-Chall rules would mark them as difficult. For example, `completion`
might stem to `complet`, which matches `complete` on the list. Scores may be slightly
lower than a strict Dale-Chall implementation would produce.
:::

## Example

```python
from readscore import Readability

text = """
Before you take this medicine, tell your doctor about all other medicines you take,
including vitamins and supplements. Some medicines can interact with each other and
cause problems. Your doctor needs this information to keep you safe. Store this
medicine at room temperature, away from heat and direct light. Keep it out of
reach of children. Do not use it after the expiration date on the package. If you
miss a dose, take it as soon as you remember. If it is almost time for your next
dose, skip the missed dose. Do not take two doses at the same time to make up for
a missed one. Contact your doctor or pharmacist if you have questions.
"""

r = Readability(text)
result = r.dale_chall()

print(f"Score: {result.score:.2f}")         # Score: ~5.12
print(f"Grades: {result.grade_levels}")     # ['5', '6']
print(f"Primary grade: {result.grade_level}")  # '5'
```

## See Also

- [Spache Readability Formula](/metrics/spache/) — same word-list approach,
  designed for grades 1–3
- [Choosing a Metric](/choosing-a-metric/) — decision guide for all nine metrics,
  including when to choose Dale-Chall over syllable-counting formulas
