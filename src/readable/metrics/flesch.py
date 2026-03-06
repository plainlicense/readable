# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Flesch Reading Ease implementation."""

from dataclasses import dataclass

from readable.constants.about_metric import FLESCH as _FLESCH_ABOUT
from readable.types._interfaces import BaseMeasure
from readable.types.results import FleschResult


# (lower_bound_inclusive, ease_str, grade_strings, integer_grade) — sorted descending
_FLESCH_RANGES: tuple[tuple[float, str, tuple[str, ...], int], ...] = (
    (90.0, "very_easy", ("5",), 5),
    (80.0, "easy", ("6",), 6),
    (70.0, "fairly_easy", ("7",), 7),
    (60.0, "standard", ("8", "9"), 9),
    (50.0, "fairly_difficult", ("10", "11", "12"), 12),
    (30.0, "difficult", ("college",), 13),
)
_FLESCH_DEFAULT: tuple[str, tuple[str, ...], int] = ("very_confusing", ("college_graduate",), 14)


@dataclass(frozen=True, slots=True)
class Flesch(BaseMeasure):
    """Flesch Reading Ease."""

    @property
    def score(self) -> FleschResult:
        """Calculate and return the score."""
        score = self._score()
        return FleschResult(
            score=score, ease=self._ease(score), grade_levels=self._grade_levels(score)
        )

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        words_per_sent = stats.num_words / stats.num_sentences
        syllables_per_word = stats.num_syllables / stats.num_words
        return 206.835 - (1.015 * words_per_sent) - (84.6 * syllables_per_word)

    def _ease(self, score: float) -> str:
        """Internal method to calculate reading ease description based on the score."""
        ease, _, _ = next(
            (
                (ease, grade, grade_level)
                for threshold, ease, grade, grade_level in _FLESCH_RANGES
                if score >= threshold
            ),
            _FLESCH_DEFAULT,
        )
        return ease

    def _grade_levels(self, score: float) -> list[str]:
        """Internal method to calculate grade levels based on the score."""
        _, grades, _ = next(
            (
                (ease, grade, grade_level)
                for threshold, ease, grade, grade_level in _FLESCH_RANGES
                if score >= threshold
            ),
            _FLESCH_DEFAULT,
        )
        return list(grades)

    @property
    def grade_level(self) -> int:
        """Return the primary grade level as an integer."""
        score = self._score()
        _, _, grade_level = next(
            (
                (ease, grade, grade_level)
                for threshold, ease, grade, grade_level in _FLESCH_RANGES
                if score >= threshold
            ),
            _FLESCH_DEFAULT,
        )
        return grade_level

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return _FLESCH_ABOUT


__all__ = ("Flesch",)
