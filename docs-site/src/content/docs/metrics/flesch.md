---
# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

title: Flesch Reading Ease
description: Scores English text from 0 to 100. Higher scores mean easier reading. Learn how the formula works, when to use it, and where it falls short.
---

Rudolf Flesch developed this formula in 1948 to measure reading ease using sentence
length and syllables per word. It outputs a score from 0 to 100, where **higher scores
mean easier text**.

## At a Glance

| | |
|---|---|
| **Output** | 0–100 ease score (higher = easier) |
| **Best for** | General English prose, adult audiences |
| **Method** | `r.flesch()` |
| **What it counts** | Words per sentence, syllables per word |
| **Minimum text** | 100 words (default) |

:::caution[The score runs backwards]
Flesch is the only metric in this library where a **higher score means easier text**.
Every other metric works the opposite way: higher scores mean harder text or a higher
grade level. New users get this backwards almost every time.
:::

## When to Use This Metric

- You need a widely recognized score that non-technical stakeholders can understand.
  Flesch is the most cited readability formula in the world, built into Microsoft Word
  since the early 1990s and referenced in legal requirements across multiple US states.
- You are checking whether body text is appropriate for a general adult audience. A score
  between 60 and 70 is standard for most adult readers.
- You must meet a legal threshold. Florida requires a score of 45 or higher on life
  insurance policies. The US Department of Defense uses Flesch scores for its documents
  and forms.
- You want a quick reading ease check without needing a precise grade level. Use
  [Flesch-Kincaid](/readable/metrics/flesch-kincaid/) if you need a US grade level
  from the same formula.

## How It Works

Flesch counts two things: the average number of words per sentence, and the average
number of syllables per word. Text with short sentences and simple words scores high.
Text with long sentences and complex words scores low.

```
score = 206.835 − (1.015 × words per sentence) − (84.6 × syllables per word)
```

The syllable coefficient (84.6) is **83 times larger** than the sentence-length
coefficient (1.015). In practice, Flesch is almost entirely a measure of word complexity,
not sentence length. Cutting sentence length has a small effect on the score. Using
simpler words has a large one.

## Score Interpretation

| Score | Ease | Grade level | What this looks like |
|-------|------|-------------|----------------------|
| 90–100 | Very Easy | Grade 5 | Children's picture books |
| 80–89 | Easy | Grade 6 | Most children's books |
| 70–79 | Fairly Easy | Grade 7 | Popular fiction |
| 60–69 | Standard | Grades 8–9 | Most news articles |
| 50–59 | Fairly Difficult | Grades 10–12 | Academic writing |
| 30–49 | Difficult | College | Legal documents |
| 0–29 | Very Confusing | College graduate | Dense academic prose |

Scores outside 0–100 are possible. Dense technical text can score negative. Very simple
text can score above 100. The library does not clamp these values.

## Return Values

`r.flesch()` returns a `FleschResult` object:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw Flesch score, typically 0–100 |
| `ease` | `str` | One of: `"very_easy"`, `"easy"`, `"fairly_easy"`, `"standard"`, `"fairly_difficult"`, `"difficult"`, `"very_confusing"` |
| `grade_levels` | `list[str]` | US grade levels for this score range, e.g. `["8", "9"]` or `["college"]` |
| `grade_level` | `str` | The primary grade level (first item in `grade_levels`) |

## Minimum Requirements

The library defaults to a 100-word minimum. Passing fewer words raises a `ValueError`.
You can lower this threshold with `Readability(text, min_words=50)`, but scores from
short texts are less reliable.

## Limitations

- **Flesch is primarily a vocabulary measure, not a sentence measure.** The formula
  weights syllable count 83× more than sentence length. Simplifying sentence structure
  while keeping complex vocabulary will barely move the score.
- **High scores do not mean clear or appropriate writing.** Repetitive text, missing
  context, or condescending tone can all score high. The formula measures linguistic
  complexity, not whether readers actually understand the content.
- **Prose only.** The formula assumes connected sentences. Tables, bullet lists, code
  blocks, and forms produce unreliable scores because sentence boundaries are ambiguous.
- **English only.** The formula's constants and syllable-counting rules are calibrated
  for English. Scores on other languages are not meaningful.
- **Syllable counting is approximate.** The library uses an algorithmic counter. Technical
  terms, proper nouns, and words with irregular pronunciation may be miscounted.

## Example

```python
from readable import Readability

text = """
Plain language means writing that your audience can understand the first time they
read it. Short sentences help. Common words help more. You do not need to simplify
your ideas — just the way you express them. Jargon and long sentences slow people
down and make them feel excluded. Simple writing is not dumbed-down writing. It is
respectful writing.
"""

r = Readability(text)
result = r.flesch()

print(f"Score: {result.score:.1f}")        # Score: ~74.3
print(f"Ease: {result.ease}")              # fairly_easy
print(f"Grades: {result.grade_levels}")   # ['7']
```

## See Also

- [Flesch-Kincaid Grade Level](/readable/metrics/flesch-kincaid/) — same inputs, outputs
  a US grade level directly instead of an ease score
- [Gunning Fog](/readable/metrics/gunning-fog/) — also uses sentence length and word
  complexity, but counts polysyllabic words rather than average syllables per word
- [Choosing a Metric](/readable/choosing-a-metric/) — decision guide for all nine metrics
