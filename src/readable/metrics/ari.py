"""Automated Readability Index (ARI) implementation."""

import math

from dataclasses import dataclass

from readable.types._interfaces import BaseMeasure
from readable.types.results import ARIResult


@dataclass(frozen=True, slots=True)
class ARI(BaseMeasure):
    """Automated Readability Index (ARI)."""

    def __post_init__(self):
        """Post-initialization checks or setup."""
        if self._stats.num_words < self._min_words:
            raise ValueError(f"{self._min_words} words required.")

    @property
    def score(self) -> ARIResult:
        """Calculate and return the score."""
        score = self._score()
        return ARIResult(
            score=score,
            grade_levels=self._grade_levels(score),
            ages=self._ages(score),
        )

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        letters_per_word = stats.num_letters / stats.num_words
        words_per_sent = stats.num_words / stats.num_sentences
        return 4.71 * letters_per_word + 0.5 * words_per_sent - 21.43

    def _grade_levels(self, score: float) -> list[str]:
        """Internal method to calculate grade levels based on the score."""
        score_ceil = math.ceil(score)
        if score_ceil <= 1:
            return ["K"]
        if score_ceil <= 2:
            return ["1", "2"]
        if score_ceil <= 12:
            return [str(score_ceil)]
        if score_ceil <= 13:
            return ["college"]
        return ["college_graduate"]

    def _ages(self, score: float) -> list[int]:  # ruff: noqa: C901
        """Internal method to calculate ages based on the score."""
        score_ceil = math.ceil(score)
        if score_ceil <= 1:
            return [5, 6]
        if score_ceil <= 2:
            return [6, 7]
        if score_ceil <= 3:
            return [7, 9]
        if score_ceil <= 4:
            return [9, 10]
        if score_ceil <= 5:
            return [10, 11]
        if score_ceil <= 6:
            return [11, 12]
        if score_ceil <= 7:
            return [12, 13]
        if score_ceil <= 8:
            return [13, 14]
        if score_ceil <= 9:
            return [14, 15]
        if score_ceil <= 10:
            return [15, 16]
        if score_ceil <= 11:
            return [16, 17]
        if score_ceil <= 12:
            return [17, 18]
        if score_ceil <= 13:
            return [18, 24]
        return [24, 100]

    @property
    def grade_level(self) -> int:
        """Return the primary grade level as an integer."""
        score_ceil = math.ceil(self._score())
        if score_ceil <= 1:
            return 0
        if score_ceil <= 12:
            return score_ceil
        if score_ceil <= 13:
            return 13
        return 14

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return (
            "Uses character count and sentence length to estimate US grade level. "
            "Unlike syllable-based metrics, it handles technical jargon more reliably "
            "because character counting is exact where syllable counting is approximate. "
            "Returns grade level and a corresponding age range."
        )
