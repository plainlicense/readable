"""Dale-Chall Readability Score implementation."""

from dataclasses import dataclass

from readable.constants.about_metric import DALE_CHALL
from readable.types._interfaces import BaseMeasure
from readable.types.results import DaleChallResult


@dataclass(frozen=True, slots=True)
class DaleChall(BaseMeasure):
    """Dale-Chall Readability Score."""

    def __post_init__(self):
        """Post-initialization checks or setup."""
        if self._stats.num_words < self._min_words:
            raise ValueError(f"{self._min_words} words required.")

    @property
    def score(self) -> DaleChallResult:
        """Calculate and return the score."""
        score = self._score()
        return DaleChallResult(score=score, grade_levels=self._grade_levels(score))

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        words_per_sent = stats.num_words / stats.num_sentences
        percent_difficult_words = stats.num_dale_chall_complex / stats.num_words * 100
        raw_score = 0.1579 * percent_difficult_words + 0.0496 * words_per_sent
        return raw_score + 3.6365 if percent_difficult_words > 5 else raw_score

    def _grade_levels(self, score: float) -> list[str]:
        """Internal method to calculate grade levels based on the score."""
        if score <= 4.9:
            return ["1", "2", "3", "4"]
        if 5 <= score < 6:
            return ["5", "6"]
        if 6 <= score < 7:
            return ["7", "8"]
        if 7 <= score < 8:
            return ["9", "10"]
        if 8 <= score < 9:
            return ["11", "12"]
        if 9 <= score < 10:
            return ["college"]
        return ["college_graduate"]

    @property
    def grade_level(self) -> int:
        """Return the primary grade level as an integer."""
        score = self._score()
        if score <= 4.9:
            return 4
        if 5 <= score < 6:
            return 6
        if 6 <= score < 7:
            return 8
        if 7 <= score < 8:
            return 10
        if 8 <= score < 9:
            return 12
        if 9 <= score < 10:
            return 13
        return 14

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return DALE_CHALL
