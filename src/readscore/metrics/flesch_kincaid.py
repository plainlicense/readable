# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Flesch-Kincaid Grade Level implementation."""

from dataclasses import dataclass

from readscore.constants.about_metric import FLESCH_KINCAID as _FLESCH_KINCAID_ABOUT
from readscore.types._interfaces import BaseMeasure
from readscore.types.results import FleschKincaidResult


@dataclass(frozen=True, slots=True)
class FleschKincaid(BaseMeasure):
    """Flesch-Kincaid Grade Level."""

    @property
    def score(self) -> FleschKincaidResult:
        """Calculate and return the score."""
        score = self._score()
        return FleschKincaidResult(score=score, grade_levels=self._grade_levels(score))

    def _score(self) -> float:
        """Internal method to compute the score."""
        stats = self._stats
        return (0.38 * stats.avg_words_per_sentence) + (11.8 * stats.avg_syllables_per_word) - 15.59

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return _FLESCH_KINCAID_ABOUT


__all__ = ("FleschKincaid",)
