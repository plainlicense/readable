# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Example of implementing a custom readability metric."""

from dataclasses import dataclass

from readable import Readability
from readable.types._interfaces import BaseMeasure
from readable.types.results import GradeResult


@dataclass(frozen=True, slots=True)
class SimpleReadingIndexResult(GradeResult):
    """Result for our custom Simple Reading Index."""


@dataclass(frozen=True, slots=True)
class SimpleReadingIndex(BaseMeasure):
    """
    A simple custom reading index.

    Formula: (avg_words_per_sentence + avg_syllables_per_word * 10) / 2.
    """

    def __post_init__(self):
        """Custom check if needed."""
        if self._stats.num_words < self._min_words:
            raise ValueError(f"At least {self._min_words} words are required.")

    @property
    def score(self) -> SimpleReadingIndexResult:
        """Calculate and return the result."""
        score = self._score()
        return SimpleReadingIndexResult(score=score, grade_levels=self._grade_levels(score))

    def _score(self) -> float:
        """Internal calculation."""
        # Simple custom formula
        stats = self._stats
        return (stats.avg_words_per_sentence + (stats.num_syllables / stats.num_words) * 10) / 2

    def _grade_levels(self, score: float) -> list[str]:
        """Convert score to grade level."""
        return [str(round(score))]

    @property
    def grade_level(self) -> int:
        """Primary grade level."""
        return round(self._score())

    @property
    def about(self) -> str:
        """Description."""
        return "A simple custom readability index for demonstration purposes."


def main() -> None:
    """Main function to demonstrate custom metric usage."""
    text = """
    Readability scoring can be complex, but it's essential for
    ensuring that your writing reaches your intended audience.
    By analyzing syllable counts, word lengths, and sentence structures,
    we can provide scientific estimates of how difficult a text is
    to understand. This library makes it easy to add your own custom
    metrics if the standard ones don't meet your needs.
    """

    # Analyze the text
    readability = Readability(text, min_words=20)  # Lower min words for example

    # Use our custom metric with the stats from the readability object
    custom_metric = SimpleReadingIndex(_stats=readability.stats, _min_words=20)
    result = custom_metric.score

    print(f"Custom Score: {result.score:.2f}")
    print(f"Custom Grade Level: {result.grade_level}")
    print(f"About: {custom_metric.about}")


if __name__ == "__main__":
    main()
