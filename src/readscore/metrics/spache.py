# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Spache Readability Formula implementation."""

from dataclasses import dataclass

from readscore.constants.about_metric import SPACHE as _SPACHE_ABOUT
from readscore.types._interfaces import BaseMeasure
from readscore.types.results import SpacheResult


@dataclass(frozen=True, slots=True)
class Spache(BaseMeasure):
    """Spache Readability Formula."""

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

    @property
    def about(self) -> str:
        """Return a description of the measure."""
        return _SPACHE_ABOUT


__all__ = ("Spache",)
