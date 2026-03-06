"""Spache Readability Formula implementation."""

from dataclasses import dataclass

from readable.constants.about_metric import SPACHE
from readable.types._interfaces import BaseMeasure
from readable.types.results import SpacheResult


@dataclass(frozen=True, slots=True)
class Spache(BaseMeasure):
    """Spache Readability Formula."""

    def __post_init__(self):
        """Post-initialization checks or setup."""
        if self._stats.num_words < self._min_words:
            raise ValueError(f"{self._min_words} words required.")

    @property
    def score(self) -> SpacheResult:
        """Calculate and return the score."""
        score = self._score()
        return SpacheResult(score=score, grade_levels=self._grade_levels(score))

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        avg_sentence_len = stats.num_words / stats.num_sentences
        percent_difficult_words = (stats.num_spache_complex / stats.num_words) * 100
        return (0.141 * avg_sentence_len) + (0.086 * percent_difficult_words) + 0.839

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
        return SPACHE
