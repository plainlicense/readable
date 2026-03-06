---
# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

title: Automated Readability Index (ARI)
description: Estimates US grade level and reader age range using character count and sentence length. Developed for military technical documentation in 1967, recalibrated in 1975.
---

E.A. Smith and R.J. Senter developed the Automated Readability Index in 1967 at Wright-Patterson
Air Force Base. It estimates US grade level using character count and sentence length instead of
syllables. The formula was recalibrated in 1975 by Kincaid et al. using comprehension test results
from 531 Navy enlisted personnel.

## At a Glance

| | |
|---|---|
| **Output** | US grade level + reader age range |
| **Best for** | Technical documentation, military manuals, adult-level prose |
| **Method** | `r.ari()` |
| **What it counts** | Letters and digits per word, words per sentence |
| **Minimum text** | 100 words (default) |

## When to Use This Metric

- You are assessing **technical or military documentation**. ARI was validated on Air Force and
  Navy technical manuals. It is more defensible for this domain than formulas derived from general
  prose or children's readers.
- Your text has **specialized terminology, abbreviations, or acronyms** that confuse syllable
  counters. Character counting is exact; syllable counting is not. "API" has one syllable for
  algorithmic counters, three for a human reader — ARI sidesteps this entirely.
- You need **consistent results across processing environments**. Two systems running ARI on
  the same text always agree. Syllable-counting formulas can disagree by a grade level or more
  depending on their heuristics.
- You want a score that **includes a reader age range**. ARI is the only metric in this library
  that returns ages alongside grade levels, which helps when your audience is international.

## How It Works

ARI counts two things: the average number of characters per word, and the average number of
words per sentence. Characters here means letters and digits — not spaces or punctuation.

The formula was designed to run on a mechanical counter attached to an IBM Selectric typewriter.
Each keypress is one character. That is why characters were chosen over syllables: a keypress is
countable by a simple machine; a syllable requires linguistic knowledge.

```
score = 4.71 × (characters / words) + 0.5 × (words / sentences) - 21.43
```

The character coefficient (4.71) is nearly ten times larger than the sentence length coefficient
(0.5). Word complexity drives the score far more than sentence length does.

The constant -21.43 anchors the output to US grade levels. This version of the constant comes from
the 1975 Kincaid recalibration. The original 1967 Smith/Senter formula used -21.34 — a small
difference, but worth knowing if you compare scores from different tools.

## Score Interpretation

ARI rounds fractional scores up to the nearest whole number before mapping to grade levels.

| ARI Score | Grade Level | Ages | Reading Context |
|-----------|-------------|------|-----------------|
| 1 or below | K | 5–6 | Kindergarten |
| 2 | 1–2 | 6–7 | Early primary |
| 3 | 3 | 7–9 | Primary school |
| 4 | 4 | 9–10 | Upper primary |
| 5 | 5 | 10–11 | Late primary |
| 6 | 6 | 11–12 | Middle school |
| 7 | 7 | 12–13 | Middle school |
| 8 | 8 | 13–14 | Middle school |
| 9 | 9 | 14–15 | Early high school |
| 10 | 10 | 15–16 | High school |
| 11 | 11 | 16–17 | High school |
| 12 | 12 | 17–18 | High school senior |
| 13 | college | 18–24 | Undergraduate |
| 14+ | college_graduate | 24+ | Graduate level |

## Return Values

`r.ari()` returns an `ARIResult` object:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw ARI score before rounding |
| `grade_levels` | `list[str]` | Grade level for this score, e.g. `["9"]`, `["K"]`, `["college"]` |
| `grade_level` | `str` | The first item in `grade_levels` (property on the result) |
| `ages` | `list[int]` | Two-element list with lower and upper reader age bounds, e.g. `[14, 15]` |

:::note[The ages field]
`ages` is unique to ARI. US grade labels like "grade 9" or "college" do not translate directly
to educational systems in other countries. Age ranges do. If your audience is international,
`ages` is the more portable field to display or check against.
:::

## Minimum Requirements

The library defaults to a 100-word minimum. Passing fewer words raises a `ValueError`.

```python
# Fewer than 100 words raises ValueError by default
r = Readability(short_text)
r.ari()  # ValueError: 100 words required.

# Lower the threshold with min_words — but scores from short texts are less reliable
r = Readability(short_text, min_words=50)
r.ari()
```

## Limitations

- **Abbreviations and short codes score as easy.** The formula sees "mm", "Hz", "SQL", and "API"
  as very short words. A document dense with technical notation will score easier than its actual
  difficulty warrants. Expanding abbreviations raises the ARI score but may also genuinely help
  readers.
- **Common long words score as hard.** "Interesting," "information," "important," and
  "beautiful" each have nine or more characters. They push the score up even though most adult
  readers know them instantly. ARI cannot distinguish a long common word from a long rare word.
- **Prose only.** The formula assumes running sentences. Bullet lists, code blocks, tables, and
  numbered steps create artificial sentence boundaries. Scores on non-prose formats are not
  reliable.
- **English only.** The formula's coefficients were derived from English text. Character-length
  distributions differ across languages. Applying ARI to non-English text is not appropriate.

## Example

```python
from readscore import Readability

text = """
Technical manuals often fail not because the concepts are too hard, but because
the writing is too complex. Engineers writing for technicians assume shared knowledge
that novice readers do not have. An ARI check identifies passages that exceed
the target grade level before the document is distributed. This allows writers to
revise specific sections rather than rewriting from scratch. The goal is a score
that matches the reading level of the intended audience — typically grade 10 to 12
for detailed technical procedures and grade 8 to 10 for general maintenance guides.
"""

r = Readability(text)
result = r.ari()

print(f"Score: {result.score:.1f}")         # Score: ~11.2
print(f"Grade: {result.grade_levels}")      # ['12']
print(f"Ages: {result.ages}")               # [17, 18]
```

## See Also

- [Coleman-Liau Index](/readscore/metrics/coleman-liau/) — same character-based approach,
  but counts letters only (no digits)
- [Flesch-Kincaid Grade Level](/readscore/metrics/flesch-kincaid/) — uses syllables instead
  of characters; more sensitive to spoken-language complexity
- [Choosing a Metric](/readscore/choosing-a-metric/) — decision guide for all nine metrics
