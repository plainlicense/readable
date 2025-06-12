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
    num_poly_syllable_words: int
    avg_words_per_sentence: float

    @abstractmethod
    def __post_init__(self):
        """Post-initialization checks or setup."""
        if self.num_words < 100:
            raise ValueError("Document must contain at least 100 words for scoring.")


@dataclass(frozen=True, slots=True)
class BaseMeasure(ABC):
    """Base class for all measures."""

    _stats: BaseStatSummary

    @abstractmethod
    def __post_init__(self):
        """Post-initialization checks or setup."""
        if not hasattr(self._stats, "num_words") or self._stats.num_words < 100:
            raise ValueError("Document must contain at least 100 words for scoring.")

    @property
    @abstractmethod
    def score(self) -> BaseResult:
        """Calculate and return the score."""

    @abstractmethod
    def _score(self) -> float:
        """Internal method to compute the score."""

    @abstractmethod
    def _grade_levels(self, score: float) -> list[str]:
        """Internal method to calculate grade levels based on the score."""

    @property
    @abstractmethod
    def grade_level(self) -> int:
        """Return the grade level based on the score."""
        """Return grade levels based on the score."""

    @property
    @abstractmethod
    def about(self) -> str:
        """Return a description of the measure."""
