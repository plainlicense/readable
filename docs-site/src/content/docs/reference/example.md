---
title: API Reference
description: Complete reference for the Readable public API.
---

This page covers everything you call directly: the `Readability` class, the result types it
returns, the `StatSummary` object, and the `ReadabilityMetric` enum. Detailed explanations of
what each metric measures and when to use it live in the [metrics section](/readable/metrics/).

---

## `Readability`

The single entry point for the library. Pass text to the constructor, then call metric methods
on the resulting object.

### Constructor

```python
Readability(text: str, min_words: int = 100)
```

**Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | — | The text to analyze. Plain prose works best. Accepts any Unicode string. |
| `min_words` | `int` | `100` | Minimum word count required before calling metric methods. |

Text analysis runs at construction time. By the time `__init__` returns, the full `StatSummary`
is available via `r.stats`.

:::note[When `min_words` matters]
Setting `min_words` below 100 triggers a `UserWarning` at construction. The warning does not
prevent construction — it signals that scores on short texts are less reliable. Individual
metric methods raise `ValueError` if the text's actual word count is below `min_words`.
SMOG uses sentence count rather than word count and raises `ValueError` when the text has
fewer than 30 sentences (unless you pass `ignore_length=True`).
:::

### `stats` property

```python
r.stats -> StatSummary
```

Returns the `StatSummary` computed at construction. All 10 statistical fields are available
immediately after creating a `Readability` instance. Use `stats` when you want direct access
to the underlying counts. See the [StatSummary section](#statsummary) for all fields.

### Metric methods

All nine metric methods take no required parameters and return a frozen result dataclass.
Each raises `ValueError` if the text is shorter than `min_words`.

#### `ari()`

```python
r.ari() -> ARIResult
```

Calculates the [Automated Readability Index](/readable/metrics/ari/). Returns a grade level
and a corresponding reader age range. Uses character count and sentence length — no syllable
counting.

#### `coleman_liau()`

```python
r.coleman_liau() -> ColemanLiauResult
```

Calculates the [Coleman-Liau Index](/readable/metrics/coleman-liau/). Uses letters per word
and sentences per 100 words. Character-based, like ARI.

#### `dale_chall()`

```python
r.dale_chall() -> DaleChallResult
```

Calculates the [Dale-Chall Readability Score](/readable/metrics/dale-chall/). Compares words
against a list of 3,000 familiar words to count unfamiliar vocabulary.

#### `flesch()`

```python
r.flesch() -> FleschResult
```

Calculates the [Flesch Reading Ease](/readable/metrics/flesch/) score. Returns a 0–100 score
where higher means easier, plus an ease label and grade levels. This is the only metric in the
library where a higher score means simpler text.

#### `flesch_kincaid()`

```python
r.flesch_kincaid() -> FleschKincaidResult
```

Calculates the [Flesch-Kincaid Grade Level](/readable/metrics/flesch-kincaid/). Uses the same
inputs as Flesch but outputs a US grade level rather than an ease score.

#### `gunning_fog()`

```python
r.gunning_fog() -> GunningFogResult
```

Calculates the [Gunning Fog Index](/readable/metrics/gunning-fog/). Counts polysyllabic words,
excluding proper nouns and hyphenated compounds.

#### `linsear_write()`

```python
r.linsear_write() -> LinsearWriteResult
```

Calculates the [Linsear Write Formula](/readable/metrics/linsear-write/). Designed for
technical writing. Counts words with two or fewer syllables against words with three or more.

#### `smog()`

```python
r.smog(all_sentences: bool = False, ignore_length: bool = False) -> SmogResult
```

Calculates the [SMOG Index](/readable/metrics/smog/). Requires at least 30 sentences by
default.

**Parameters**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `all_sentences` | `bool` | `False` | When `False` (default), SMOG samples 10 sentences from the beginning, middle, and end of the text. When `True`, uses all sentences. |
| `ignore_length` | `bool` | `False` | When `False` (default), raises `ValueError` if the text has fewer than 30 sentences. When `True`, issues a `UserWarning` instead and computes a score anyway. |

:::note[SMOG sentence requirements]
SMOG is designed for texts with at least 30 sentences. The standard procedure draws a
30-sentence sample from three equally spaced positions. Passing `ignore_length=True`
on a short text produces a score, but that score does not follow the standard method
and should be treated as approximate.
:::

#### `spache()`

```python
r.spache() -> SpacheResult
```

Calculates the [Spache Readability Formula](/readable/metrics/spache/). Designed for primary
school texts (grades 1–3). Compares vocabulary against a word list calibrated for young readers.

### `statistics()`

```python
r.statistics() -> dict
```

Returns a plain dictionary with six of the most commonly needed statistics:

| Key | Type | Description |
|-----|------|-------------|
| `"num_letters"` | `int` | Total letter count (excludes spaces and punctuation) |
| `"num_words"` | `int` | Total word count |
| `"num_sentences"` | `int` | Total sentence count |
| `"num_polysyllabic_words"` | `int` | Words with three or more syllables |
| `"avg_words_per_sentence"` | `float` | Average words per sentence |

:::note[Key name differs from `r.stats`]
`statistics()` uses `"num_polysyllabic_words"` for this field. The equivalent attribute
on `r.stats` is `num_poly_syllable_words` (with `_syllable_` in the middle). Both return
the same value; only the name differs.
:::
| `"avg_syllables_per_word"` | `float` | Average syllables per word |

This is a convenience method for quick inspection or serialization. It is a subset of what
`r.stats` provides. Use `r.stats` when you need word-list-based counts (`num_gunning_complex`,
`num_dale_chall_complex`, `num_spache_complex`) or direct attribute access.

```python
from readable import Readability

r = Readability("The cat sat on the mat. Simple words make simple text." * 5)
stats = r.statistics()
print(stats["num_words"])               # 55
print(stats["avg_syllables_per_word"])  # 1.18
```

---

## Result types

Metric methods return frozen dataclasses. You cannot modify them after construction. All result
types are comparable and orderable by `score`.

### Common fields

Seven of the nine metrics return a `GradeResult` or a subclass. These fields are present on
every result except `FleschResult` and `ARIResult` (which add extra fields):

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw formula output |
| `grade_levels` | `list[str]` | One or more US grade level strings |
| `grade_level` | `str` (property) | The first item in `grade_levels`; `"na"` if the list is empty |

**`grade_levels` values.** The list contains strings from this set: `"K"`, `"1"` through
`"12"`, `"college"`, `"college_graduate"`. Some formulas return a range (e.g., `["8", "9"]`
for a Flesch score of 60–69) and some return a single value. The `grade_level` property
always returns the first item.

```python
result = r.flesch_kincaid()
print(result.score)         # 8.4
print(result.grade_levels)  # ['8']
print(result.grade_level)   # '8'
```

### `FleschResult`

Returned by `r.flesch()`. Adds one field to `GradeResult`:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Flesch ease score, typically 0–100 (can exceed range) |
| `ease` | `str` | Reading ease label (see table below) |
| `grade_levels` | `list[str]` | US grade level(s) for this score range |
| `grade_level` | `str` (property) | Primary grade level |

**`ease` values by score range:**

| Score range | `ease` value |
|-------------|--------------|
| 90 and above | `"very_easy"` |
| 80–89 | `"easy"` |
| 70–79 | `"fairly_easy"` |
| 60–69 | `"standard"` |
| 50–59 | `"fairly_difficult"` |
| 30–49 | `"difficult"` |
| Below 30 | `"very_confusing"` |

```python
result = r.flesch()
print(result.score)   # 74.3
print(result.ease)    # 'fairly_easy'
```

### `ARIResult`

Returned by `r.ari()`. Adds one field to `GradeResult`:

| Field | Type | Description |
|-------|------|-------------|
| `score` | `float` | Raw ARI score |
| `ages` | `list[int]` | Two-element list `[lower, upper]` for typical reader age range |
| `grade_levels` | `list[str]` | US grade level(s) for this score |
| `grade_level` | `str` (property) | Primary grade level |

The `ages` list always has exactly two elements. For example, an ARI score in the grade 8 range
returns `[13, 14]`. College-level scores return `[18, 24]` and graduate-level scores return
`[24, 100]`.

```python
result = r.ari()
print(result.score)         # 9.1
print(result.grade_levels)  # ['10']
print(result.ages)          # [15, 16]
```

### Metric-specific result types

The remaining seven metrics each have a named result type that inherits directly from
`GradeResult` without adding fields. They exist as distinct types for clarity in type
annotations and `isinstance` checks.

| Method | Result type |
|--------|-------------|
| `coleman_liau()` | `ColemanLiauResult` |
| `dale_chall()` | `DaleChallResult` |
| `flesch_kincaid()` | `FleschKincaidResult` |
| `gunning_fog()` | `GunningFogResult` |
| `linsear_write()` | `LinsearWriteResult` |
| `smog()` | `SmogResult` |
| `spache()` | `SpacheResult` |

---

## `StatSummary`

A frozen dataclass with all statistical counts computed from the text. Access it via `r.stats`.

All fields are read-only. The object is computed once at construction and shared across all
metric calls.

| Field | Type | Description |
|-------|------|-------------|
| `num_letters` | `int` | Total letter count, excluding spaces and punctuation |
| `num_words` | `int` | Total word count |
| `num_sentences` | `int` | Total sentence count |
| `num_syllables` | `int` | Total syllable count across all words |
| `num_poly_syllable_words` | `int` | Words with three or more syllables |
| `avg_words_per_sentence` | `float` | Average words per sentence |
| `avg_syllables_per_word` | `float` | Average syllables per word |
| `num_gunning_complex` | `int` | Polysyllabic words excluding proper nouns and hyphenated compounds (Gunning Fog definition) |
| `num_dale_chall_complex` | `int` | Words not found on the Dale-Chall familiar word list |
| `num_spache_complex` | `int` | Words not found on the Spache familiar word list |

The difference between `num_poly_syllable_words` and `num_gunning_complex`: both count
words with three or more syllables, but `num_gunning_complex` applies Gunning Fog's
exclusion rules (proper nouns and compound words do not count as complex, even if
polysyllabic).

```python
r = Readability(text)
s = r.stats

print(s.num_words)               # 312
print(s.num_poly_syllable_words) # 47
print(s.num_gunning_complex)     # 39
print(s.num_dale_chall_complex)  # 28
```

---

## `ReadabilityMetric` enum

Provides programmatic access to all nine metrics by name. Useful for iterating over metrics,
building dynamic reporting, or resolving a metric by string name.

**Members**

| Member | String representation |
|--------|-----------------------|
| `ReadabilityMetric.ARI` | `"ARI"` |
| `ReadabilityMetric.COLEMAN_LIAU` | `"Coleman-Liau"` |
| `ReadabilityMetric.DALE_CHALL` | `"Dale-Chall"` |
| `ReadabilityMetric.FLESCH` | `"Flesch"` |
| `ReadabilityMetric.FLESCH_KINCAID` | `"Flesch-Kincaid"` |
| `ReadabilityMetric.GUNNING_FOG` | `"Gunning Fog"` |
| `ReadabilityMetric.LINSEAR_WRITE` | `"Linsear Write"` |
| `ReadabilityMetric.SMOG` | `"SMOG"` |
| `ReadabilityMetric.SPACHE` | `"Spache"` |

**`metrics()` classmethod**

```python
ReadabilityMetric.metrics() -> list[str]
```

Returns a sorted list of all enum member names as strings (the Python attribute names, not
the short display names):

```python
from readable.types.enums import ReadabilityMetric

print(ReadabilityMetric.metrics())
# ['ARI', 'COLEMAN_LIAU', 'DALE_CHALL', 'FLESCH', 'FLESCH_KINCAID',
#  'GUNNING_FOG', 'LINSEAR_WRITE', 'SMOG', 'SPACHE']
```

**`measure_class` property**

Returns the internal measure class for a given enum member. This is an advanced use case for
callers who want to instantiate a metric directly using a `StatSummary` rather than going
through `Readability`:

```python
from readable.types.enums import ReadabilityMetric

metric = ReadabilityMetric.FLESCH
cls = metric.measure_class  # <class 'readable.metrics.flesch.Flesch'>
```

**Iterating over all metrics**

```python
from readable import Readability
from readable.types.enums import ReadabilityMetric

r = Readability(text)

for member in ReadabilityMetric:
    method_name = member._names.var        # e.g. "flesch_kincaid"
    method = getattr(r, method_name, None)
    if method:
        result = method()
        print(f"{member}: {result.score:.1f}")
```

---

## Exceptions and warnings

| Signal | Type | When raised |
|--------|------|-------------|
| `UserWarning` | warning | `Readability(text, min_words=N)` where `N < 100` |
| `ValueError` | exception | Any metric method when `r.stats.num_words < min_words` |
| `ValueError` | exception | `r.smog()` when sentence count is below 30 and `ignore_length=False` |
| `UserWarning` | warning | `r.smog(ignore_length=True)` when sentence count is below 30 |

Lowering `min_words` at construction only suppresses the constructor warning. It also lowers
the threshold that metric methods check against. Setting `min_words=50` means metric methods
will accept texts with as few as 50 words without raising `ValueError`.
