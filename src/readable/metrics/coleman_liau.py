"""Coleman-Liau Index implementation."""

from dataclasses import dataclass

from readable.constants.about_metric import COLEMAN_LIAU
from readable.types._interfaces import BaseMeasure
from readable.types.results import ColemanLiauResult


@dataclass(frozen=True, slots=True)
class ColemanLiau(BaseMeasure):
    """Coleman-Liau Index."""

    def __post_init__(self):
        """Post-initialization checks or setup."""
        if self._stats.num_words < self._min_words:
            raise ValueError(f"{self._min_words} words required.")

    @property
    def score(self) -> ColemanLiauResult:
        """Calculate and return the score."""
        score = self._score()
        return ColemanLiauResult(score=score, grade_levels=self._grade_levels(score))

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        # l is the average number of letters per 100 words
        letters_per_100 = (stats.num_letters / stats.num_words) * 100
        # s is the average number of sentences per 100 words
        sentences_per_100 = (stats.num_sentences / stats.num_words) * 100
        return 0.0588 * letters_per_100 - 0.296 * sentences_per_100 - 15.8

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
        return COLEMAN_LIAU
