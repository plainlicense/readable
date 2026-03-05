"""Flesch Reading Ease implementation."""

from dataclasses import dataclass

from readable.types._interfaces import BaseMeasure
from readable.types.results import FleschResult


@dataclass(frozen=True, slots=True)
class Flesch(BaseMeasure):
    """Flesch Reading Ease."""

    def __post_init__(self):
        """Post-initialization checks or setup."""
        if self._stats.num_words < self._min_words:
            raise ValueError(f"{self._min_words} words required.")

    @property
    def score(self) -> FleschResult:
        """Calculate and return the score."""
        score = self._score()
        return FleschResult(
            score=score,
            ease=self._ease(score),
            grade_levels=self._grade_levels(score),
        )

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        words_per_sent = stats.num_words / stats.num_sentences
        syllables_per_word = stats.num_syllables / stats.num_words
        return 206.835 - (1.015 * words_per_sent) - (84.6 * syllables_per_word)

    def _ease(self, score: float) -> str:
        """Internal method to calculate reading ease description based on the score."""
        if score >= 90:
            return "very_easy"
        if 80 <= score < 90:
            return "easy"
        if 70 <= score < 80:
            return "fairly_easy"
        if 60 <= score < 70:
            return "standard"
        if 50 <= score < 60:
            return "fairly_difficult"
        if 30 <= score < 50:
            return "difficult"
        return "very_confusing"

    def _grade_levels(self, score: float) -> list[str]:
        """Internal method to calculate grade levels based on the score."""
        if score >= 90:
            return ["5"]
        if 80 <= score < 90:
            return ["6"]
        if 70 <= score < 80:
            return ["7"]
        if 60 <= score < 70:
            return ["8", "9"]
        if 50 <= score < 60:
            return ["10", "11", "12"]
        if 30 <= score < 50:
            return ["college"]
        return ["college_graduate"]

    @property
    def grade_level(self) -> int:
        """Return the primary grade level as an integer."""
        score = self._score()
        if score >= 90:
            return 5
        if 80 <= score < 90:
            return 6
        if 70 <= score < 80:
            return 7
        if 60 <= score < 70:
            return 9
        if 50 <= score < 60:
            return 12
        if 30 <= score < 50:
            return 13
        return 14

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return (
            "Scores text on a 0-100 scale using sentence length and syllables per word — "
            "higher scores mean easier text. The most widely cited readability formula; "
            "used in US government and legal requirements. Note: the scale runs backwards "
            "compared to every other metric in this library."
        )
