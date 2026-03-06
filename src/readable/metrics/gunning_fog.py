"""Gunning Fog Index implementation."""

from dataclasses import dataclass

from readable.constants.about_metric import GUNNING_FOG
from readable.types._interfaces import BaseMeasure
from readable.types.results import GunningFogResult


@dataclass(frozen=True, slots=True)
class GunningFog(BaseMeasure):
    """Gunning Fog Index."""

    def __post_init__(self):
        """Post-initialization checks or setup."""
        if self._stats.num_words < self._min_words:
            raise ValueError(f"{self._min_words} words required.")

    @property
    def score(self) -> GunningFogResult:
        """Calculate and return the score."""
        score = self._score()
        return GunningFogResult(score=score, grade_levels=self._grade_levels(score))

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        words_per_sent = stats.num_words / stats.num_sentences
        percent_complex_words = (stats.num_gunning_complex / stats.num_words) * 100
        return 0.4 * (words_per_sent + percent_complex_words)

    def _grade_levels(self, score: float) -> list[str]:
        """Internal method to calculate grade levels based on the score."""
        rounded = round(score)
        if rounded < 6:
            return ["na"]
        if 6 <= rounded <= 12:
            return [str(rounded)]
        if 13 <= rounded <= 16:
            return ["college"]
        return ["college_graduate"]

    @property
    def grade_level(self) -> int:
        """Return the primary grade level as an integer."""
        rounded = round(self._score())
        if rounded < 6:
            return 0
        if 6 <= rounded <= 12:
            return rounded
        if 13 <= rounded <= 16:
            return 13
        return 14

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return GUNNING_FOG
