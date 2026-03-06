"""Linsear Write Formula implementation."""

from dataclasses import dataclass

from readable.constants.about_metric import LINSEAR_WRITE
from readable.types._interfaces import BaseMeasure
from readable.types.results import LinsearWriteResult


@dataclass(frozen=True, slots=True)
class LinsearWrite(BaseMeasure):
    """Linsear Write Formula."""

    def __post_init__(self):
        """Post-initialization checks or setup."""
        if self._stats.num_words < self._min_words:
            raise ValueError(f"{self._min_words} words required.")

    @property
    def score(self) -> LinsearWriteResult:
        """Calculate and return the score."""
        score = self._score()
        return LinsearWriteResult(score=score, grade_levels=self._grade_levels(score))

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        num_easy_words = stats.num_words - stats.num_poly_syllable_words
        num_hard_words = stats.num_poly_syllable_words
        # Note: This is an approximation based on the original library's implementation
        inter_score = (num_easy_words + (num_hard_words * 3)) / stats.num_sentences
        if inter_score > 20:
            return inter_score / 2
        return (inter_score - 2) / 2

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
        return LINSEAR_WRITE
