# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Dale-Chall Readability Score implementation."""

from dataclasses import dataclass

from readable.constants.about_metric import DALE_CHALL as _DALE_CHALL_ABOUT
from readable.types._interfaces import BaseMeasure
from readable.types.results import DaleChallResult


# (upper_bound_exclusive, grade_strings, integer_grade)
_DALE_CHALL_RANGES: tuple[tuple[float, tuple[str, ...], int], ...] = (
    (5.0, ("1", "2", "3", "4"), 4),
    (6.0, ("5", "6"), 6),
    (7.0, ("7", "8"), 8),
    (8.0, ("9", "10"), 10),
    (9.0, ("11", "12"), 12),
    (10.0, ("college",), 13),
)
_DALE_CHALL_DEFAULT: tuple[tuple[str, ...], int] = (("college_graduate",), 14)


@dataclass(frozen=True, slots=True)
class DaleChall(BaseMeasure):
    """Dale-Chall Readability Score."""

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
        grades, _ = next(
            (
                (grade, grade_level)
                for threshold, grade, grade_level in _DALE_CHALL_RANGES
                if score < threshold
            ),
            _DALE_CHALL_DEFAULT,
        )
        return list(grades)

    @property
    def grade_level(self) -> int:
        """Return the primary grade level as an integer."""
        score = self._score()
        _, grade_level = next(
            (
                (grade, grade_level)
                for threshold, grade, grade_level in _DALE_CHALL_RANGES
                if score < threshold
            ),
            _DALE_CHALL_DEFAULT,
        )
        return grade_level

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return _DALE_CHALL_ABOUT


__all__ = ("DaleChall",)
