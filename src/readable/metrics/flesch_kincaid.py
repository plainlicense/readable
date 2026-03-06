"""Flesch-Kincaid Grade Level implementation."""

from dataclasses import dataclass

from readable.constants.about_metric import FLESCH_KINCAID
from readable.types._interfaces import BaseMeasure
from readable.types.results import FleschKincaidResult


@dataclass(frozen=True, slots=True)
class FleschKincaid(BaseMeasure):
    """Flesch-Kincaid Grade Level."""

    def __post_init__(self):
        """Post-initialization checks or setup."""
        if self._stats.num_words < self._min_words:
            raise ValueError(f"{self._min_words} words required.")

    @property
    def score(self) -> FleschKincaidResult:
        """Calculate and return the score."""
        score = self._score()
        return FleschKincaidResult(score=score, grade_levels=self._grade_levels(score))

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        return (0.38 * stats.avg_words_per_sentence) + (11.8 * stats.avg_syllables_per_word) - 15.59

    def _grade_levels(self, score: float) -> list[str]:
        """Internal method to calculate grade levels based on the score."""
        return [str(round(score))]

    @property
    def grade_level(self) -> int:
        """Return the primary grade level as an integer."""
        return round(self._score())

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return FLESCH_KINCAID
