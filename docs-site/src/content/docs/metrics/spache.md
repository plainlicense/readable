---
# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

title: Spache Readability Formula
description: Estimates grade level for primary-grade text (grades 1–3) by checking words against a familiar-word list. Developed by George Spache in 1953. Not valid above grade 3.
---

George Spache developed this formula in 1953 specifically for primary-grade reading
materials, filling a gap in readability research: no existing formula was calibrated
for texts intended for beginning readers in grades 1–3.

## At a Glance

| | |
|---|---|
| **Output** | US grade level (grades 1–3 only) |
| **Best for** | Children's books, early reader texts, primary-grade instructional materials |
| **Method** | `r.spache()` |
| **What it counts** | Unique unfamiliar words (not on the word list), words per sentence |
| **Minimum text** | 100 words (default) |

:::caution[This formula is only valid for grades 1–3]
Spache was designed and calibrated on primary-grade texts. The formula will compute a score
for any text, but scores above grade 3 mean the text is outside the formula's valid range.
If `spache()` returns a grade above 3, the result is not a reliable estimate. Use
[Dale-Chall](/readscore/metrics/dale-chall/) for text above grade 3.
:::

## When to Use This Metric

- You are assessing **children's books, leveled readers, or early literacy materials**
  for grades 1–3. Spache is purpose-built for this range and more accurate here than any
  formula calibrated on older readers.
- You are evaluating **classroom reading materials** for kindergarten through grade 3, where
  matching text complexity to developing reader ability is a deliberate instructional goal.
- You want to check whether a **children's health or safety document** is appropriate for
  early readers.
- You are using Spache alongside [Dale-Chall](/readscore/metrics/dale-chall/) to assess
  text at the grade 4 boundary. At that level, running both gives you a fuller picture.

## How It Works

Spache checks each word against a list of words familiar to primary-grade readers. Words
not on the list count as "difficult" — but with one key difference from Dale-Chall: Spache
counts each unique unfamiliar word **once**, regardless of how many times it appears in the
text. The formula then combines the percentage of unique difficult words with average
sentence length.

```
grade_level = 0.141 × (words / sentences) + 0.086 × (unique_difficult_words / total_words × 100) + 0.839
```

These are the coefficients from Spache's 1953 original formula, which this library
implements.

### Unique-word counting

This counting method differs meaningfully from Dale-Chall. If a text uses the word
"photosynthesis" twenty times, Spache counts it as one difficult word. Dale-Chall would
count all twenty occurrences. Spache's approach is more forgiving of texts that use a
small set of unfamiliar words repeatedly — which is common in primary-grade instructional
materials where controlled vocabulary repetition is a deliberate teaching strategy.

:::note[This library implements the 1953 original formula]
Spache revised his formula in 1978, producing slightly lower grade estimates with
coefficients of `0.121 × ASL + 0.082 × PDW + 0.659`. The 1978 revision was recalibrated
against updated text samples. This library uses the 1953 original (`0.141`, `0.086`,
`0.839`), which is the most widely cited version in formal and academic contexts. Be aware
that tools using the 1978 revision will return somewhat different scores on the same text.
:::

### The word list

The Spache word list contains approximately 925 words familiar to primary-grade readers —
basic action verbs, common nouns for everyday objects, family members, animals, and
function words. Words on the list in their base form are also familiar in regular inflected
forms: `-ing`, `-ed`, `-es`, `-ly`, `-er`, `-est`. Irregular forms are treated as difficult
unless they independently appear on the list. First names are treated as familiar.

## Score Interpretation

Spache returns a grade level directly as a rounded number. The formula's reliable range
is grades 1 through 3. Scores above 3 are outside that range.

| Spache Score | Grade Level | What This Means |
|--------------|-------------|-----------------|
| ~1.0–1.9 | Grade 1 | Early first-grade readers |
| ~2.0–2.9 | Grade 2 | Second-grade readers |
| ~3.0–3.9 | Grade 3 | Third-grade readers |
| 4.0 and above | Outside valid range | Use Dale-Chall for this text |

If you receive a score of 4 or above, treat it as a signal that the text is too complex
for the formula's intended population — not as a meaningful grade estimate. Run
[Dale-Chall](/readscore/metrics/dale-chall/) instead.

## Return Values

`r.spache()` returns a `SpacheResult` object:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw Spache score (grade level as a float) |
| `grade_levels` | `list[str]` | Grade level rounded to nearest integer, e.g. `["2"]` |
| `grade_level` | `str` | First item in `grade_levels` |

## Minimum Requirements

The library defaults to a 100-word minimum. Passing fewer words raises a `ValueError`.
You can lower this threshold with `Readability(text, min_words=50)`, but scores from
short texts are less reliable — and this is especially true for Spache, where the
word list is small (~925 words) and a single unfamiliar word has more impact on
the score.

## Limitations

- **Only valid for grades 1–3.** This is the most important thing to understand about
  Spache. The formula will compute a number for any text, but that number is not a
  meaningful grade estimate outside the calibrated range. Applying Spache to adult text
  or middle-grade literature produces a technically computed result that is practically
  meaningless.

- **The word list reflects 1950s–1970s American children's vocabulary.** The list was
  constructed from primary-grade reading materials of that era. Contemporary words that
  children now recognize — "tablet," "video," "app," "emoji" — are absent. Words that
  were common then but are less familiar today — "harness," "sled," "rye" — remain on
  the list. Scores on texts that use contemporary children's vocabulary may be
  higher than the actual difficulty warrants.

- **Unique-word counting can underestimate density.** A text could use one specialized
  term dozens of times and Spache would count it as a single difficult word. This is
  appropriate for controlled-vocabulary instructional materials, but can mislead when
  applied to other text types.

- **Syntactic complexity is not captured.** The formula measures sentence length and
  word familiarity, not grammatical structure. A short sentence with a subordinate clause
  or pronoun reference may be harder to parse than its length suggests, and Spache will
  not detect this.

:::note[Porter stemming in this library]
The library uses Porter stemming to match words against the Spache list. This is an
engineering compromise, not a validated approach. Aggressive stemming can cause some
words to match list entries that a strict Spache implementation would count as difficult.
Scores may be slightly lower than a strict implementation would produce. This effect is
more pronounced on short texts, where each word carries more weight.
:::

## Example

```python
from readscore import Readability

text = """
Ben has a dog named Spot. Spot is brown and white. Ben and Spot play in the yard
every day after school. Ben throws a ball and Spot runs to get it. Spot brings the
ball back and drops it at Ben's feet. Then Ben throws it again. They play this game
for a long time. When they are tired, they sit under the big tree in the yard. Spot
puts his head on Ben's lap. Ben pets Spot softly. They are best friends. Ben's mom
calls them in for dinner. Spot wags his tail and runs to the door.
"""

r = Readability(text)
result = r.spache()

print(f"Score: {result.score:.2f}")         # Score: ~1.84
print(f"Grades: {result.grade_levels}")     # ['2']
print(f"Primary grade: {result.grade_level}")  # '2'
```

This text is within Spache's valid range. A score of ~1.84 rounds to grade 2, consistent
with a text for second-grade readers.

## See Also

- [Dale-Chall Readability Formula](/readscore/metrics/dale-chall/) — same word-list
  approach, designed for grade 4 and above
- [Choosing a Metric](/readscore/choosing-a-metric/) — decision guide for all nine metrics,
  including the Spache/Dale-Chall handoff at grade 4
