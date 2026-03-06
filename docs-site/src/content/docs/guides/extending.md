---
# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

title: Extending readscore
description: Learn how to implement your own custom readability metrics.
---

One of the primary goals of the `readscore` library is to make it easy to implement and use custom readability metrics.

## How to Implement a Custom Metric

To implement a new readability metric, you need to:

1.  **Define a Result Type**: Create a dataclass that inherits from `BaseResult` or `GradeResult`.
2.  **Define a Measure Class**: Create a dataclass that inherits from `BaseMeasure`.

### 1. Define a Result Type

Result types use Python dataclasses for clean, typed data structures.

```python
from dataclasses import dataclass
from readscore.types.results import GradeResult

@dataclass(frozen=True, slots=True)
class MyCustomResult(GradeResult):
    """Result for my custom readability metric."""
    # You can add additional fields here if needed
```

### 2. Define a Measure Class

The measure class performs the actual calculation using the text statistics.

```python
from dataclasses import dataclass
from readscore.types._interfaces import BaseMeasure

@dataclass(frozen=True, slots=True)
class MyCustomMetric(BaseMeasure):
    """Implementation of my custom readability metric."""

    def __post_init__(self):
        """Perform initialization checks (like word counts)."""
        if self._stats.num_words < self._min_words:
            raise ValueError(f"{self._min_words} words required.")

    @property
    def score(self) -> MyCustomResult:
        """Calculate and return the result object."""
        score = self._score()
        return MyCustomResult(
            score=score,
            grade_levels=self._grade_levels(score)
        )

    def _score(self) -> float:
        """Internal calculation method."""
        stats = self._stats
        # Your formula here
        return stats.avg_words_per_sentence * 0.5

    def _grade_levels(self, score: float) -> list[str]:
        """Convert the score to grade levels."""
        return [str(round(score))]

    @property
    def grade_level(self) -> int:
        """Return the primary grade level as an integer."""
        return round(self._score())

    @property
    def about(self) -> str:
        """Return a description of the metric."""
        return "Measures readability using average sentence length."
```

The `about` property returns a short description of the metric. It is used when the metric is introspected, displayed in CLI output, or written to logs.

## Using Your Custom Metric

Pass the `stats` object from a `Readability` instance to your metric. The `_stats` parameter accepts any `BaseStatSummary`, and `_min_words` sets the minimum word count required before the metric will calculate.

```python
from readscore import Readability

text = """
Plain language means writing that your audience can understand the first time they
read it. Short sentences help. Common words help more. You do not need to simplify
your ideas — just the way you express them. Jargon and long sentences slow people
down and make them feel excluded. Simple writing is not dumbed-down writing. It is
respectful writing.
"""

readability = Readability(text)

# Use your custom metric with the pre-calculated statistics
result = MyCustomMetric(_stats=readability.stats).score

print(f"Score: {result.score}")
print(f"Grade: {result.grade_level}")
```

### Setting a minimum word count

`_min_words` defaults to `100`, which matches the built-in metrics. You can lower or raise it for your formula:

```python
# Accept texts as short as 30 words
result = MyCustomMetric(_stats=readability.stats, _min_words=30).score

# Require at least 200 words for a reliable score
result = MyCustomMetric(_stats=readability.stats, _min_words=200).score
```

If `_stats.num_words` is less than `_min_words`, the `__post_init__` check in the example above raises a `ValueError`. If you do not add that check in your subclass, no minimum is enforced regardless of the `_min_words` value.

## Available Statistics

`readability.stats` returns a `StatSummary` object. All fields below are available to your metric via `self._stats`. Every field is defined on `BaseStatSummary`, so they are guaranteed to be present for any stats implementation.

| Field | Type | Description |
|---|---|---|
| `num_letters` | `int` | Total character count, excluding whitespace and punctuation |
| `num_words` | `int` | Total word count |
| `num_sentences` | `int` | Total sentence count |
| `num_syllables` | `int` | Total syllable count across all words |
| `num_poly_syllable_words` | `int` | Words with three or more syllables |
| `avg_words_per_sentence` | `float` | Average number of words per sentence |
| `avg_syllables_per_word` | `float` | Average number of syllables per word |
| `num_gunning_complex` | `int` | Words counted as complex under Gunning Fog rules |
| `num_dale_chall_complex` | `int` | Words not on the Dale-Chall familiar-word list |
| `num_spache_complex` | `int` | Words not on the Spache familiar-word list |

## Programmatic Access via `ReadabilityMetric`

The `ReadabilityMetric` enum maps each built-in metric name to its measure class. Use it when you need to select or iterate over metrics by name at runtime.

```python
from readscore import Readability
from readscore.types.enums import ReadabilityMetric

text = """
Plain language means writing that your audience can understand the first time they
read it. Short sentences help. Common words help more. You do not need to simplify
your ideas — just the way you express them.
"""

readability = Readability(text)
stats = readability.stats

# Access a metric class by enum value
flesch_class = ReadabilityMetric.FLESCH.measure_class
result = flesch_class(_stats=stats).score

# Iterate over all built-in metrics
for metric in ReadabilityMetric:
    cls = metric.measure_class
    result = cls(_stats=stats).score
    print(f"{metric}: {result.score:.1f}")
```

`ReadabilityMetric` uses lazy imports inside `measure_class` to avoid circular dependencies, so importing the enum does not load all metric modules upfront.
