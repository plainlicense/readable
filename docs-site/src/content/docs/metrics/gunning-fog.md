---
# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

title: Gunning Fog Index
description: Estimates years of formal education needed to understand text on first reading. Robert Gunning introduced it in 1952 for journalists and business writers. Scores below 6 return "na" — this is expected, not an error.
---

Robert Gunning developed this formula in 1952 as a practical tool for journalists and business writers. It estimates the **years of formal education** a reader needs to understand the text on first reading. "Fog" is not an acronym — it describes what hard-to-read text does to a reader.

## At a Glance

| | |
|---|---|
| **Output** | Years of formal education needed (roughly equivalent to US grade level above grade 6) |
| **Best for** | Business writing, journalism, corporate communications |
| **Method** | `r.gunning_fog()` |
| **What it counts** | Words per sentence, percentage of words with 3+ syllables |
| **Minimum text** | 100 words (default) |

:::note[The score means years of education, not strictly grade level]
A Gunning Fog score of 12 means a reader needs roughly 12 years of formal education — approximately a high school senior — to understand the text on first reading. The scale tracks US grade levels closely above grade 6, but the formula's intent is "education years needed," not a strict curriculum grade placement.
:::

## When to Use This Metric

- You are assessing **business writing, corporate reports, or journalism**. Gunning spent years as a readability consultant to over 60 large-city daily newspapers. The formula was validated on exactly this type of content.
- You want to give writers concrete feedback on **two specific things to fix**: sentence length and complex word percentage. Unlike formulas that report a single average syllable count, Gunning Fog reports both inputs through a transparent formula that writers can act on directly.
- You are researching whether a document is **deliberately complex**. A substantial body of financial research uses Gunning Fog as a proxy for obfuscation in SEC 10-K annual reports. Companies with worse financial results tend to produce more opaque filings (Li, 2008). If you are processing financial disclosures at scale, Fog has documented empirical value for this use case.
- You want a widely understood metric. Fog is taught alongside Flesch-Kincaid in most readability curricula and is available in many writing assistance tools.

## How It Works

Gunning Fog measures two things: how long sentences are on average, and what percentage of words have three or more syllables. Those polysyllabic words are what Gunning called "complex words."

```
score = 0.4 × (words per sentence + 100 × complex words / words)
```

Not every polysyllabic word counts as "complex." Gunning's original definition excludes:
- Proper nouns (names like "Philadelphia" or "Microsoft")
- Familiar compound words (like "butterfly" or "bookkeeper")
- Words made three syllables only by the suffixes **-ed** or **-es** (like "created" or "trespasses")

The library uses the `num_gunning_complex` count, which applies these exclusion rules. This count is different from the general polysyllabic word count used by SMOG. Two tools that apply the exclusions differently will produce different scores on the same text — especially for proper-noun-heavy documents like news articles.

The 0.4 coefficient was chosen empirically to make the output land on the same scale as US grade levels above grade 6.

## Score Interpretation

| Score | Education Level | Example publications |
|-------|-----------------|----------------------|
| below 6 | n/a | Below formula range — see note below |
| 6 | Grade 6 | Comics, very simple prose |
| 7–8 | Grades 7–8 | Reader's Digest, popular magazines |
| 9–10 | Grades 9–10 | Time magazine, news articles |
| 11–12 | Grades 11–12 | Atlantic Monthly, high school senior level |
| 13–16 | College | College-level texts, professional journals |
| 17+ | Post-graduate | Graduate academic writing |

Gunning's own benchmarks: the Bible and Mark Twain score approximately 6. Time magazine averages about 11. A score above 17 indicates post-graduate level material.

### What "na" means

When the Gunning Fog score rounds below 6, the library returns `["na"]` for `grade_levels`. This is not an error. It means the text is simple enough that the formula's education-level scale does not apply. Very short sentences with mostly monosyllabic words produce scores in this range.

```python
# Simple text with short sentences and common words
r = Readability("The dog ran. The cat sat. The bird flew.")
# This would return grade_level "na" if it met the word minimum
```

If you receive `["na"]`, the text is below the formula's calibrated range. It does not mean something went wrong.

## Return Values

`r.gunning_fog()` returns a `GunningFogResult` object:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw Gunning Fog score as a float, e.g. `11.3` |
| `grade_levels` | `list[str]` | One of: `["na"]`, a grade string like `["11"]`, `["college"]`, or `["college_graduate"]` |
| `grade_level` | `str` | The primary grade level (first item in `grade_levels`) |

The full set of possible `grade_levels` values:

| `grade_levels` value | When it appears |
|----------------------|-----------------|
| `["na"]` | Score rounds below 6 |
| `["6"]` through `["12"]` | Score rounds to 6–12 |
| `["college"]` | Score rounds to 13–16 |
| `["college_graduate"]` | Score rounds to 17 or above |

## Minimum Requirements

The library defaults to a 100-word minimum. Passing fewer words raises a `ValueError`.

```python
# Fewer than 100 words — raises ValueError by default
r = Readability(short_text)
r.gunning_fog()  # ValueError: 100 words required.

# Lower the minimum if needed
r = Readability(short_text, min_words=50)
r.gunning_fog()  # Runs, but with reduced reliability
```

## Limitations

- **Common long words count as "complex."** Words like "interesting," "important," "beautiful," "understand," and "government" all have three syllables and count as complex words. These are not difficult vocabulary for most adult readers, but they increase the score regardless.
- **Short specialist terms are invisible.** Medical, technical, and legal jargon often uses short words — "stat," "null," "flux," "cyst," "prion." These score as simple even when completely opaque to a lay reader. For health and medical materials, SMOG is a better choice.
- **Implementation variance on exclusions.** Fog scores from different tools may not agree on proper-noun-heavy text. A news article about "Mayor Alejandra Gutierrez" will score differently in tools that apply Gunning's proper noun exclusion versus tools that count all polysyllabic words. If you need to compare Fog scores across tools, check how each handles exclusions.
- **Scores below 6 are outside the formula's range.** The formula was designed for adult prose at sixth-grade level and above. Using it to assess simple text for children is not appropriate — use [Spache](/readscore/metrics/spache/) for grades 1–3 or [Dale-Chall](/readscore/metrics/dale-chall/) for grades 4 and above.

## Example

```python
from readscore import Readability

text = """
Annual reports for large public companies often run to hundreds of pages, covering
financial results, risk factors, legal proceedings, and management discussion.
Critics of corporate disclosure argue that complex language in these filings can
obscure performance problems from investors. Research by Frank Li at the University
of Michigan found that companies with worse earnings used more complex language in
their annual reports. The Gunning Fog Index has been used as a proxy for this
kind of deliberate opacity in financial communications research.

Plain language advocates argue that even technical financial information can be
expressed clearly. The goal is not to remove precision from a document — it is
to eliminate unnecessary complexity that serves no reader except the writer.
Short sentences and common words are compatible with accurate financial disclosure.
Writers who understand readability metrics can use them as a check on their own
habits, not as a target to optimize for mechanically.
"""

r = Readability(text)
result = r.gunning_fog()

print(f"Score: {result.score:.1f}")        # Score: ~13.1
print(f"Grade: {result.grade_levels}")    # ['college']
```

## See Also

- [Flesch Reading Ease](/readscore/metrics/flesch/) — also uses sentence length and syllables per word, but averages syllables rather than counting complex words
- [SMOG Index](/readscore/metrics/smog/) — also counts polysyllabic words, but uses a fixed 30-sentence sample and targets 100% comprehension; preferred for health materials
- [Flesch-Kincaid Grade Level](/readscore/metrics/flesch-kincaid/) — grade level output using average syllables per word rather than a polysyllabic word threshold
- [Choosing a Metric](/readscore/choosing-a-metric/) — decision guide for all nine metrics
