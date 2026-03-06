# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Base classes for readability scoring system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, order=True, slots=True)
class BaseResult(ABC):
    """Base class for all result types."""

    score: float


@dataclass(frozen=True, order=True, slots=True)
class BaseStatSummary(ABC):
    """Base class for all statistics types."""

    num_letters: int
    num_words: int
    num_sentences: int
    num_syllables: int
    num_poly_syllable_words: int
    avg_words_per_sentence: float
    avg_syllables_per_word: float
    num_gunning_complex: int
    num_dale_chall_complex: int
    num_spache_complex: int

    @abstractmethod
    def __post_init__(self):
        """Post-initialization checks or setup."""


@dataclass(frozen=True, slots=True)
class BaseMeasure(ABC):
    """Base class for all measures."""

    _stats: BaseStatSummary
    _min_words: int = 100

    def __post_init__(self):
        """Validate minimum word count. Override for metrics with different requirements."""
        if self._stats.num_words < self._min_words:
            raise ValueError(f"{self._min_words} words required.")

    @property
    @abstractmethod
    def score(self) -> BaseResult:
        """Calculate and return the score."""

    @abstractmethod
    def _score(self) -> float:
        """Internal method to compute the score."""

    def _grade_levels(self, score: float) -> list[str]:
        """Return grade levels as a rounded score string. Override for range-based mappings."""
        return [str(round(score))]

    @property
    def grade_level(self) -> int:
        """Return the primary grade level as an integer. Override for range-based mappings."""
        return round(self._score())

    @property
    @abstractmethod
    def about(self) -> str:
        """Return a description of the measure."""


__all__ = ("BaseMeasure", "BaseResult", "BaseStatSummary")
