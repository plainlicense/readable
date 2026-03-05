# Documentation Framework: Readable Metrics

**Purpose**: This document defines how to write metric documentation for the Readable library. It is a working guide, not published documentation. Review and adjust this framework before writing the actual metric pages.

**Date**: 2026-03-05
**Status**: Draft for review

---

## 1. Documentation Audit

### What Exists

**`README.md`**
Good: Quick-start code example, installation, list of metrics, project background.
Missing: Any explanation of what metrics do, how to choose one, or how to interpret results. The code example prints values without explaining what those values mean.

**`docs/metrics.md`**
A list of nine metrics with one of them (ARI) linked. No content beyond bullet points.

**`docs/ari.md`**
One paragraph (copied verbatim from the archive RST), a code snippet, and a link to readabilityformulas.com. No score interpretation, no minimum requirements, no guidance on when to use it.

**`docs/extending.md`**
The best-written existing doc. Clear structure, working code examples, a table of available statistics. This is the reference standard for quality. Other metric docs should match this level of completeness.

**`archive/docs/source/*.rst`**
Nine RST files, each with one or two sentences of "about" text, a code snippet, and a reference link. This is the documentation floor, not the ceiling. Some notes worth preserving:
- Flesch RST mentions the US Department of Defense and Florida insurance use cases - useful context
- Flesch-Kincaid RST mentions US Army and Pennsylvania insurance use
- Dale-Chall RST explains why familiar words matter - this is good framing
- Spache RST has the most complete description: explains the word list origin, publication source, and best-use range (grades 1-3)
- Gunning Fog RST has the clearest one-sentence description of what the score means
- Coleman-Liau RST has one useful fact: it tends to give lower scores than Flesch, ARI, or Kincaid on technical documents

**Metric `about` properties**
Each metric class has an `about` property that returns one or two sentences. The content is thin. ARI says "designed to gauge the understandability of a text" - that describes every metric. None of them describe what is distinctive about the formula.

### What Is Missing

Everything that would help a developer make a decision:

1. What does each metric actually measure? (What inputs does it use? What does a high vs. low score mean?)
2. When should I use this metric vs. another?
3. What are the known weaknesses of this formula?
4. How do I interpret the score I got back?
5. What is the minimum text length, and what happens if my text is shorter?
6. What do "grade levels" mean for non-US audiences?
7. A comparison or selection guide across all nine metrics
8. How the `ease` field on Flesch works
9. How the `ages` field on ARI works
10. What the Gunning Fog "na" grade level means
11. The SMOG `ignore_length` and `all_sentences` parameters are completely undocumented

---

## 2. Template for Individual Metric Docs

Each metric gets its own file in `docs/metrics/`. The file name matches the method name: `flesch.md`, `ari.md`, `smog.md`, and so on.

Every file follows this structure. Sections marked [REQUIRED] must be present. Sections marked [IF APPLICABLE] are included only when they add value.

```
# [Metric Full Name]

> One sentence. What does this metric measure? Who designed it and when?

## At a Glance

[A two-row summary table]

## When to Use This Metric

[Two to four bullet points. Be concrete about use cases, not generic.]

## How It Works

[Two to four sentences. Describe the inputs, not the math. What does the formula pay attention to?]
[Include the formula if it helps understanding, but do not require readers to parse it.]

## Score Interpretation

[Interpretation table or mapped list. Required for every metric.]

## Return Values

[Field-by-field description of what the result object contains.]

## Minimum Requirements

[What text length is needed? What happens if the text is too short?]

## Limitations

[Two to four concrete weaknesses. Not disclaimers - actual gotchas a developer will encounter.]

## Example

[Working code snippet with realistic output shown in a comment.]

## See Also

[Links to related metrics, comparison guide, selection guide.]
```

### Filled-In Template: Flesch Reading Ease

The example below shows what every section should look like. This is not the final Flesch doc - it is a model for the other eight.

---

**`docs/metrics/flesch.md`**

```markdown
# Flesch Reading Ease

> Scores English text from 0 to 100. Higher scores mean easier reading.
> Rudolf Flesch developed this formula in 1948 based on sentence length and
> average syllables per word.

## At a Glance

| | |
|---|---|
| **Output range** | 0 to 100 (higher = easier) |
| **Best for** | General English prose, adult audiences |
| **Minimum text** | 100 words recommended |
| **What it counts** | Words per sentence, syllables per word |
| **Method** | `r.flesch()` |

## When to Use This Metric

- You want a single, widely recognized score that non-technical stakeholders can
  understand. Flesch is the most cited readability formula in the world.
- You are checking whether body text is appropriate for a general adult audience
  (a score of 60-70 is standard for that audience).
- You need to comply with legal requirements. Florida requires a score of 45 or
  higher on life insurance policies. The US Department of Defense uses this
  formula for its documents and forms.
- You want a quick check and do not need a precise grade level. Use
  Flesch-Kincaid if you need a grade level from the same formula.

## How It Works

Flesch counts two things: how many words are in each sentence on average, and
how many syllables are in each word on average. Text with short sentences and
simple words scores high. Text with long sentences and complex words scores low.

Formula: `206.835 - (1.015 × words/sentence) - (84.6 × syllables/word)`

The score runs backwards compared to most other metrics. A score of 30 is
harder to read than a score of 70. New users often get this backwards.

## Score Interpretation

| Score | Ease label | Grade level | Example |
|-------|-----------|-------------|---------|
| 90-100 | Very Easy | 5th grade | *The cat sat on the mat.* |
| 80-89 | Easy | 6th grade | Most children's books |
| 70-79 | Fairly Easy | 7th grade | Popular fiction |
| 60-69 | Standard | 8th-9th grade | Most news articles |
| 50-59 | Fairly Difficult | 10th-12th grade | Academic writing |
| 30-49 | Difficult | College level | Legal documents |
| 0-29 | Very Confusing | College graduate | Dense academic prose |

Note: The library returns the `ease` field as a snake_case string
(`"very_easy"`, `"fairly_difficult"`, etc.) rather than a number. This makes
it safe to use in display logic without needing a lookup table.

## Return Values

`r.flesch()` returns a `FleschResult` object with these fields:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw Flesch score, typically 0-100 |
| `ease` | `str` | Category label: `"very_easy"`, `"easy"`, `"fairly_easy"`, `"standard"`, `"fairly_difficult"`, `"difficult"`, `"very_confusing"` |
| `grade_levels` | `list[str]` | US grade levels for this score range, e.g. `["8", "9"]` or `["college"]` |
| `grade_level` | `str` (property) | First item in `grade_levels` |

## Minimum Requirements

The library defaults to 100 words. If you pass fewer, the `Readability`
constructor raises a warning. You can change the minimum by passing `min_words`
to `Readability()`, but scores from short texts are less reliable.

## Limitations

- **English only.** The syllable counting and formula constants are calibrated
  for English. Scores on other languages will not be meaningful.
- **Prose only.** The formula assumes connected sentences. Tables, code, bullet
  lists, and poetry all produce misleading scores because sentence boundaries
  are ambiguous.
- **Syllable counting is approximate.** The library uses an algorithmic
  syllable counter. Words with unusual pronunciation patterns (like technical
  jargon or proper nouns) may be miscounted.
- **High score does not mean appropriate.** A children's book scores high, but
  so does text that is repetitive, condescending, or lacks substance. This
  formula measures complexity, not quality.

## Example

```python
from readable import Readability

text = """
Plain language means writing that your audience can understand the first time
they read it. Short sentences help. Common words help more. You do not need to
simplify your ideas - just the way you express them.
"""

r = Readability(text)
result = r.flesch()

print(result.score)        # 72.4 (approximately - varies by exact text)
print(result.ease)         # "fairly_easy"
print(result.grade_levels) # ["7"]
```

## See Also

- **Flesch-Kincaid Grade Level** - Same inputs, different formula. Gives a US
  grade level directly instead of an ease score.
- **Gunning Fog** - Also measures sentence length and word complexity, but uses
  polysyllabic word counts rather than average syllables per word.
- [Choosing a Metric](../choosing-a-metric.md) - Decision guide for all nine metrics.
```

---

### Template Guidance Notes

These notes explain the decisions in the template above. Apply them when writing the other eight metric docs.

**The one-sentence opener**: It must answer two questions: what does the score tell you, and who created it? "Scores English text from 0 to 100" is concrete. "A readability formula for English text" is not.

**At a Glance table**: This table exists so a developer can scan four rows and decide whether to read further. Every row should be scannable in two seconds. Keep cell values short.

**When to Use**: This is the highest-value section for a developer choosing a metric. Be specific. "Widely used" is not useful. "Used by the US Army for technical manuals" is useful. Four bullets is the right length - fewer leaves the section too thin, more becomes a lecture.

**How It Works**: Describe the inputs in plain language before showing the formula. A developer who does not know what "polysyllabic" means needs the concept before the variable name. Show the formula only if it helps - it is not required.

**Score Interpretation**: Every metric needs this table or list. For metrics where the score is a grade level directly (Flesch-Kincaid, Coleman-Liau, Linsear Write, Spache), a table is still useful for showing the grade-to-reading-level mapping. Do not just say "grade 8 = grade 8." Give context.

**Return Values**: One row per field. Describe what the values look like in practice, not just the type. For `grade_levels`, show an example value. For `ease`, list all possible values.

**Minimum Requirements**: State the actual number. State what happens if you do not meet it (exception or warning). State the SMOG-specific case (30 sentences, not 100 words).

**Limitations**: These are not disclaimers. A disclaimer says "results may vary." A limitation says "this formula scores bullet lists as if they were sentences, which inflates the word count and produces unreliable results." Be concrete. Aim for three to four limitations per metric. If you cannot name three concrete limitations, you have not thought about the metric carefully enough.

**Example**: Use realistic text that would actually be run through a readability check. The Gunning Fog paragraph from the README (about the Gunning Fog index) is a good model - it is a real paragraph, not "The quick brown fox." Show actual output. If the exact score varies by version, note that with "approximately."

---

## 3. Score Interpretation Guide

This section defines how each metric's scoring works, so documentation writers apply it consistently.

### The Backwards Problem: Flesch Reading Ease

Flesch is the only metric where a higher score means easier text. Every other metric in this library works the other way: a higher score means harder text or a higher grade level.

This is genuinely confusing. Documentation should state this fact directly and early for Flesch, not bury it. The template above puts it in "How It Works" with a direct statement: "The score runs backwards compared to most other metrics."

Do not soften this. Do not say "note that higher scores indicate easier text." Say: "Higher scores mean easier text. This is the opposite of what you might expect."

### Grade Levels: US Context for International Users

All metrics except Flesch Reading Ease return grade levels. These map to the US school system:

| Grade level | Age range | Label |
|-------------|-----------|-------|
| K | 5-6 years | Kindergarten |
| 1 | 6-7 | First grade |
| 2 | 7-8 | Second grade |
| ... | | |
| 8 | 13-14 | Middle school |
| 12 | 17-18 | High school senior |
| college | 18-24 | Undergraduate |
| college_graduate | 24+ | Graduate/professional |

Documentation should note once (in the main comparison page) that grade levels are US-calibrated. Individual metric pages do not need to repeat this every time. ARI's `ages` field sidesteps this by providing age ranges directly.

### The "na" Grade Level in Gunning Fog

When Gunning Fog scores below 6, the library returns `["na"]`. This is not an error. It means the text is simple enough that grade level is not a meaningful measure. Document this as expected behavior, not an edge case to avoid.

### Score Ranges That Extend Outside Their Scale

Some metrics produce scores outside their documented range for unusual text:
- Flesch can go below 0 or above 100 for very dense or very simple text
- Negative Flesch-Kincaid scores are technically possible for very short sentences with monosyllabic words

Documentation should note this for Flesch explicitly ("the library does not clamp the score to 0-100, so dense technical text may return a negative score"). For other metrics, note it only if it is likely to cause confusion.

### How to Present Score Tables

Use consistent column order across all metric pages:

For grade-level metrics: Score | Grade levels | Reading level description | Example text type

For Flesch (the inverted one): Score | Ease label | Grade level | Example text type

Keep the "Example text type" column vague enough to be international (say "most news articles" not "USA Today"). Do not say "newspaper" - print media is less universal than it was.

---

## 4. Comparison and Selection Guide

This guide belongs in `docs/choosing-a-metric.md`. It is a standalone page linked from each individual metric page.

### Structure of the Choosing a Metric Page

**Section 1: Quick Selector**

A decision table. Short enough to scan. Links each situation to the right metric.

Example draft:

| My text is... | Use this metric |
|---------------|-----------------|
| For young readers (grades 1-3) | Spache |
| For children (grades 4+) | Dale-Chall |
| For adults, general audience | Flesch Reading Ease |
| For technical documentation | ARI or Coleman-Liau |
| For health literacy compliance | SMOG |
| For military or government documents | Linsear Write or ARI |
| I need a US grade level directly | Flesch-Kincaid |
| I want the most common single metric | Flesch Reading Ease |
| My text is fewer than 30 sentences | Avoid SMOG |
| I need syllable-free calculation | ARI or Coleman-Liau |

**Section 2: What Each Metric Counts**

A table showing inputs. Developers who know what their text contains can use this to pick a metric.

| Metric | Sentence length | Syllables per word | Character count | Word familiarity |
|--------|----------------|-------------------|-----------------|-----------------|
| Flesch Reading Ease | Yes | Yes | - | - |
| Flesch-Kincaid | Yes | Yes | - | - |
| Gunning Fog | Yes | (polysyllabic count) | - | - |
| SMOG | - | (polysyllabic count) | - | - |
| ARI | Yes | - | Yes | - |
| Coleman-Liau | Yes | - | Yes | - |
| Dale-Chall | Yes | - | - | Yes (familiar word list) |
| Spache | Yes | - | - | Yes (primary word list) |
| Linsear Write | Yes | (polysyllabic count) | - | - |

**Section 3: Score Type by Metric**

| Metric | Score type | Return fields |
|--------|------------|---------------|
| Flesch Reading Ease | 0-100 ease score | `score`, `ease`, `grade_levels` |
| Flesch-Kincaid | US grade level | `score`, `grade_levels` |
| SMOG | US grade level | `score`, `grade_levels` |
| ARI | US grade level + ages | `score`, `grade_levels`, `ages` |
| Coleman-Liau | US grade level | `score`, `grade_levels` |
| Gunning Fog | Years of education | `score`, `grade_levels` |
| Dale-Chall | Raw score (maps to grade bands) | `score`, `grade_levels` |
| Spache | US grade level | `score`, `grade_levels` |
| Linsear Write | US grade level | `score`, `grade_levels` |

**Section 4: Minimum Text Requirements**

| Metric | Minimum | What happens if you fall short |
|--------|---------|-------------------------------|
| Most metrics | 100 words (default) | `ValueError` on construction |
| SMOG | 30 sentences | `ValueError` by default; pass `ignore_length=True` for a warning instead |
| Spache | 100 words | `ValueError` |

Note: You can lower the 100-word default by passing `min_words` to `Readability()`, but results become less reliable below 100 words.

**Section 5: Same Text, Different Results**

Show all nine metrics run on one paragraph, with actual output. This helps developers calibrate their expectations.

The paragraph from the README (the Gunning Fog description text) is a good choice. It is a real paragraph at approximately 10th-grade reading level, which means most metrics will return scores spread across a meaningful range rather than all clustered at the same level.

Example format (values are illustrative - real values must come from running the code):

```python
text = """
In linguistics, the Gunning fog index is a readability test for English writing.
The index estimates the years of formal education a person needs to understand
the text on the first reading. For instance, a fog index of 12 requires the
reading level of a United States high school senior (around 18 years old).
The test was developed in 1952 by Robert Gunning, an American businessman
who had been involved in newspaper and textbook publishing.
"""

r = Readability(text)

# Results (run with readable 0.x.x):
# r.flesch().score       = 52.4  -> "fairly_difficult" -> grade 10-12
# r.flesch_kincaid().score = 11.8 -> grade 12
# r.gunning_fog().score  = 13.2  -> college
# r.smog()               # raises ValueError: need 30 sentences
# r.ari().score          = 11.9  -> grade 12 -> ages [17, 18]
# r.coleman_liau().score = 12.1  -> grade 12
# r.dale_chall().score   = 7.4   -> grade 9-10
# r.spache().score       = 4.1   -> grade 4  (not appropriate: Spache is for grades 1-3)
# r.linsear_write().score = 11.0 -> grade 11
```

The Spache result illustrates why the selection guide matters. Using the wrong metric gives a meaningless result.

**Section 6: Combining Multiple Metrics**

Some production systems run several metrics and average or compare them. This is a valid approach when:
- You want to reduce the impact of any one formula's quirks
- You want to flag text where metrics disagree significantly (which can indicate unusual text structure)

Example pattern:

```python
r = Readability(text)
grade_estimates = [
    r.flesch_kincaid().grade_level,
    r.ari().grade_level,
    r.coleman_liau().grade_level,
]
average_grade = sum(grade_estimates) / len(grade_estimates)
```

Note that you should not combine Flesch Reading Ease with grade-level metrics without converting first - the scales are completely different.

---

## 5. File Organization

### Current Structure

```
docs/
  ari.md         (exists, thin)
  extending.md   (exists, good)
  metrics.md     (exists, list only)
```

### Proposed Structure

```
docs/
  choosing-a-metric.md    (new - comparison and selection guide)
  metrics/
    ari.md                (rewrite)
    coleman-liau.md       (new)
    dale-chall.md         (new)
    flesch.md             (new)
    flesch-kincaid.md     (new)
    gunning-fog.md        (new)
    linsear-write.md      (new)
    smog.md               (new)
    spache.md             (new)
  extending.md            (keep, minimal revision needed)
  metrics.md              (update to link into docs/metrics/)
```

The existing `docs/ari.md` moves to `docs/metrics/ari.md` as a rewrite. Do not delete it from the top level until the new file is in place, to avoid breaking any existing links.

The `README.md` should link to `docs/choosing-a-metric.md` and `docs/metrics/` from its Supported Metrics section. The README itself stays concise - its job is quick-start, not complete reference.

### What Stays in README.md

- Installation command
- Quick-start example (the current one is fine)
- One-paragraph project background (keep as-is)
- Supported metrics list (update to link to `docs/metrics/` pages)
- Contributors section

The README does not need a score interpretation table or metric descriptions. Those belong in the docs.

---

## 6. The `about` Property

### Current State

Each metric class has an `about` property that returns a one- or two-sentence string. Example from `ari.py`:

```python
"The Automated Readability Index (ARI) is a readability test for English texts, "
"designed to gauge the understandability of a text."
```

This is not useful. "Designed to gauge the understandability of a text" describes every metric in the library.

### Proposed Role

The `about` property serves one specific purpose: returning a brief, machine-readable description for display in tool output, CLI interfaces, and logging. It is not documentation. It should not attempt to be.

Given that role, the right length is two to three sentences. The content should:

1. Say what is distinctive about this metric (what inputs does it use?)
2. Say when it is most accurate or appropriate
3. Optionally name the score range or scale

### Proposed `about` Content for Each Metric

These are proposed strings. Finalize after reviewing the metric docs themselves.

**ARI**:
"Uses character count and sentence length to estimate US grade level. Unlike syllable-based metrics, it works reliably on technical documents where syllable counting struggles with jargon. Returns grade level and a corresponding age range."

**Coleman-Liau**:
"Uses character count and sentence length to estimate US grade level. Like ARI, it avoids syllable counting. Tends to score technical documents lower than syllable-based formulas. Works well when machine processing makes syllable counting impractical."

**Dale-Chall**:
"Compares words against a list of 3,000 familiar English words, then weights sentence length. Most accurate for text aimed at grade 4 and above. Less reliable for text with many proper nouns or technical terms not on the familiar-word list."

**Flesch Reading Ease**:
"Scores text on a 0-100 scale using sentence length and syllables per word. Higher scores mean easier text. The most widely cited readability formula; used in US government and legal requirements. Produces a continuous ease score rather than a grade level."

**Flesch-Kincaid Grade Level**:
"Uses the same inputs as Flesch Reading Ease (sentence length and syllables per word) but outputs a US grade level directly. The US Army uses this metric for technical manuals. The score corresponds to the school grade needed to understand the text."

**Gunning Fog**:
"Estimates years of formal education needed to understand text on first reading. Weights sentence length and the percentage of words with three or more syllables. Best for general prose; not calibrated for text below 6th-grade level."

**Linsear Write**:
"Developed for the US Air Force to assess technical manual readability. Weights words by syllable count (easy = 1 syllable or 2, hard = 3 or more) over a 100-word sample. Returns a US grade level."

**SMOG**:
"Counts polysyllabic words across a 30-sentence sample to estimate the US grade level needed to understand health or educational materials. Requires at least 30 sentences; use `ignore_length=True` to get a best-effort score on shorter text. Widely used in health literacy assessment."

**Spache**:
"Compares words against a list of familiar primary-grade words, then weights sentence length. Designed specifically for grades 1-3. Results above grade 3 indicate the text is outside the formula's calibrated range and should be verified with Dale-Chall or another formula."

---

## 7. Writing Guidelines

These are the style rules for all metric documentation.

### Reading Level Target

Write at approximately 8th grade reading level. This is the target for most general-audience documents in the US. To achieve it:

- Aim for sentences under 20 words. Break longer sentences in two.
- Use common words. "Use" not "utilize." "Show" not "demonstrate." "Help" not "facilitate."
- One idea per sentence.
- Active voice. "Flesch counts syllables" not "syllables are counted by Flesch."

Run each finished doc page through `r.flesch_kincaid()` or `r.gunning_fog()` to check your own writing. Aim for Flesch-Kincaid grade level 7-9. If it comes back at 12, revise.

### Concrete Over Abstract

Bad: "The metric provides a score that indicates text complexity."
Good: "A score of 60 means most adults can read this text without difficulty."

Bad: "Best used for appropriate text types."
Good: "Best for prose. Tables, bullet lists, and code will produce unreliable scores."

Bad: "Note that scores may vary."
Good: "This formula can return scores above 100 or below 0 for very simple or very dense text. The library does not clamp the result."

### What to Call Things

Use these names consistently across all docs:

| Concept | Use this term |
|---------|--------------|
| The Python class | `Readability` |
| The result object | "result" |
| Grade levels | "US grade level" (first use on a page); "grade level" (after that) |
| The library | "Readable" |
| K-12 grade | Write it as "grade 8" not "8th grade" (avoids ordinal abbreviation questions) |

Do not use "aforementioned," "utilize," "leverage" (as a verb), "seamless," "robust," or "powerful" anywhere in the docs.

### Code Example Rules

- Every code example must be runnable as written.
- Show both the call and the output.
- Use realistic text in examples, not placeholder strings like `"Your text here"` or `"..."`.
- If exact output depends on a specific version of the library or NLTK, note that with a comment.
- Use f-strings for output, not `print(variable)` alone.

Example of bad practice (from current `ari.md`):
```python
text = "..."
r = Readability(text)
ari = r.ari()
```

This does not run and teaches nothing.

Example of good practice:
```python
from readable import Readability

text = """
The city council approved the new zoning plan after two hours of public comment.
Residents spoke about parking, traffic, and school capacity. The vote was 4-3.
"""

r = Readability(text)
result = r.ari()
print(f"Score: {result.score:.1f}")    # Score: 8.4
print(f"Grade: {result.grade_level}")  # Grade: 9
print(f"Ages: {result.ages}")           # Ages: [14, 15]
```

### How to Handle Warnings vs. Errors

Several metrics raise `ValueError` for inputs that are too short. SMOG has special parameters (`ignore_length`, `all_sentences`). Document these as behavior, not as errors to avoid.

Show both the error case and the workaround in the SMOG doc. For other metrics, note the minimum and show the constructor argument that controls it.

Do not tell readers to "ensure text meets minimum requirements" without also telling them what happens if they do not.

### International Context

Grade levels are US-specific. UK readers know "year" not "grade." International developers need calibration. The recommended approach:

1. Add one sentence to `docs/choosing-a-metric.md` that explains US grade levels and provides an approximate UK/European mapping.
2. Do not repeat this on every metric page.
3. Mention that `ages` on ARI sidesteps this entirely - age ranges are more universal than school grades.

### Tone

Direct, not apologetic. "This metric does not work well on text below grade 4" is direct. "It should be noted that this metric may not be suitable for all text types" is not.

Assume the reader is a developer who wants the information quickly. Long preambles, hedging, and "in order to" constructions all slow them down.

Short is better than long when both options contain the same information.

---

## 8. Metric-Specific Notes for Writers

These are issues the writer needs to know before drafting each doc. They are not in the template itself - they are background research.

### Flesch Reading Ease

- The inverted scale (higher = easier) needs upfront prominence. Every other metric in the library works the opposite way.
- The `ease` field values are snake_case strings. List all seven possible values in the Return Values table.
- Flesch can produce scores outside 0-100. The library does not clamp.
- Grade levels returned: 5, 6, 7, 8-9, 10-12, college, college_graduate. Note that "8-9" is returned as `["8", "9"]` and "10-12" as `["10", "11", "12"]`.
- Legal context (Florida insurance, US DoD) is worth including briefly - it helps readers understand why this formula is everywhere.

### Flesch-Kincaid Grade Level

- Most widely used in US government and education contexts.
- Uses the same inputs as Flesch Reading Ease but cannot be derived from the Flesch score by a simple formula - they are separate formulas.
- Returns a single grade level in a list: `["8"]`. Simpler than Flesch.
- Score is a float; `grade_levels` rounds it to the nearest integer.

### SMOG Index

- The only metric that requires sentences as input, not just statistics. The `Readability` class handles this internally.
- Requires 30 sentences. By default, it takes 10 from the beginning, 10 from the middle, and 10 from the end of the text.
- Two important parameters: `all_sentences=True` uses the full text instead of the 30-sentence sample; `ignore_length=True` bypasses the sentence-count check and emits a warning instead of raising an error.
- Widely used in health literacy work. This is a concrete use-case worth naming.
- The "SMOG" name is an acronym: Simple Measure of Gobbledygook.

### ARI (Automated Readability Index)

- Uses character count (letters) rather than syllable count. This makes it faster and more consistent on technical text where syllable counting is unreliable.
- Returns `ages` as a list of two integers: the lower and upper bound of the likely reader age range. Example: `[14, 15]` for grade 9.
- Kindergarten text returns grade level `["K"]` and ages `[5, 6]`.
- The `grade_level` property returns an integer, but `grade_levels` returns strings, including the string `"K"` for kindergarten.

### Coleman-Liau Index

- Like ARI, uses character count instead of syllables. The two formulas often produce similar results.
- The archive docs note that Coleman-Liau tends to score technical documents lower than syllable-based metrics. This is worth including.
- Returns a single grade level as a rounded integer.
- No special fields beyond `score` and `grade_levels`.

### Gunning Fog

- "Fog" is not an acronym - it describes the effect of hard-to-read text.
- The score is not a grade level directly: it represents years of formal education needed. At grade 12, the two scales converge, but at lower levels, education years and grade levels diverge slightly.
- Below score 6, returns `["na"]`. This is not an error. Short, simple text falls below what the formula was designed to measure.
- "Complex words" in Gunning Fog counts polysyllabic words with some exclusions. The Gunning Fog definition of complex differs slightly from SMOG's; both use 3+ syllables as the threshold but Gunning Fog may apply different exclusion rules (the `num_gunning_complex` statistic is distinct from `num_poly_syllable_words`).
- Aimed at general prose. Not appropriate for children's text (use Spache or Dale-Chall for that).

### Dale-Chall

- The word list approach makes this more stable than syllable-counting on technical jargon - technical terms that happen to be polysyllabic will still score as "complex" under Flesch, but Dale-Chall checks against actual familiarity.
- Designed for grade 4 and above. For grades 1-3, use Spache.
- The raw score (around 5-10) maps to grade bands, not individual grades. `score <= 4.9` maps to grades 1-4 as a range.
- If more than 5% of words are unfamiliar, the formula adds 3.6365 to the raw score as an adjustment. This jump is built into the formula and explains why the score can appear to jump discontinuously.
- The word list is based on American English as it was known by 3rd graders around 1948. Some common modern words may not be on it.

### Spache

- Designed for grades 1-3. This is a hard constraint, not a preference.
- Works the same way as Dale-Chall but uses a different, smaller word list calibrated for very young readers.
- If the result is above grade 3, the text is outside the formula's calibrated range. The doc should say this clearly and recommend Dale-Chall for higher levels.
- The formula has no lower floor either - it will return grade 1 or below for very simple text, which is the correct result for that use case.

### Linsear Write

- Least-known metric in the library. Developers may need more context about its origin.
- Developed for the US Air Force for technical manual assessment.
- Operates on a 100-word sample, not the full text. The current implementation applies the formula to the full word statistics, which is an approximation noted in the source code. Document this limitation.
- "Easy words" = 1-2 syllables; "hard words" = 3+ syllables. Hard words count 3x in the formula.
- Returns a grade level as a rounded float.

---

## Appendix: Files Referenced in This Document

Source files examined during audit:
- `/home/knitli/readable/README.md`
- `/home/knitli/readable/docs/metrics.md`
- `/home/knitli/readable/docs/ari.md`
- `/home/knitli/readable/docs/extending.md`
- `/home/knitli/readable/readable/readability.py`
- `/home/knitli/readable/readable/types/results.py`
- `/home/knitli/readable/readable/metrics/ari.py`
- `/home/knitli/readable/readable/metrics/coleman_liau.py`
- `/home/knitli/readable/readable/metrics/dale_chall.py`
- `/home/knitli/readable/readable/metrics/flesch.py`
- `/home/knitli/readable/readable/metrics/flesch_kincaid.py`
- `/home/knitli/readable/readable/metrics/gunning_fog.py`
- `/home/knitli/readable/readable/metrics/linsear_write.py`
- `/home/knitli/readable/readable/metrics/smog.py`
- `/home/knitli/readable/readable/metrics/spache.py`
- `/home/knitli/readable/archive/docs/source/ari.rst`
- `/home/knitli/readable/archive/docs/source/coleman_liau.rst`
- `/home/knitli/readable/archive/docs/source/dale_chall.rst`
- `/home/knitli/readable/archive/docs/source/flesch.rst`
- `/home/knitli/readable/archive/docs/source/flesch_kincaid.rst`
- `/home/knitli/readable/archive/docs/source/gunning_fog.rst`
- `/home/knitli/readable/archive/docs/source/linear_write.rst`
- `/home/knitli/readable/archive/docs/source/smog.rst`
- `/home/knitli/readable/archive/docs/source/spache.rst`
