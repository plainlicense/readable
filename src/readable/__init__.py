# SPDX-FileCopyrightText: 2026 PlainLicense <https://plainlicense.org>
#
# SPDX-License-Identifier: LicenseRef-PlainMIT or MIT

"""The readable library for modern readability scoring."""

from __future__ import annotations

from types import MappingProxyType

# === MANAGED EXPORTS ===
# Exportify manages this section. It contains lazy-loading infrastructure
# for the package: imports and runtime declarations (__all__, __getattr__,
# __dir__). Manual edits will be overwritten by `exportify fix`.
from typing import TYPE_CHECKING

from lateimport import create_late_getattr


if TYPE_CHECKING:
    from readable.metrics.ari import ARI
    from readable.metrics.coleman_liau import ColemanLiau
    from readable.metrics.dale_chall import DaleChall
    from readable.metrics.flesch import Flesch
    from readable.metrics.flesch_kincaid import FleschKincaid
    from readable.metrics.gunning_fog import GunningFog
    from readable.metrics.linsear_write import LinsearWrite
    from readable.metrics.smog import Smog
    from readable.metrics.spache import Spache
    from readable.readability import Readability
    from readable.resources.loader import ResourceLoader
    from readable.resources.stemmer import Stemmer
    from readable.text.analyzer import TextAnalyzer
    from readable.text.statistics import StatSummary
    from readable.text.tokenizer import Tokenizer
    from readable.types._interfaces import BaseMeasure, BaseResult, BaseStatSummary
    from readable.types.enums import Metric, ReadabilityMetric
    from readable.types.results import (
        ARIResult,
        ColemanLiauResult,
        DaleChallResult,
        FleschKincaidResult,
        FleschResult,
        GradeResult,
        GunningFogResult,
        LinsearWriteResult,
        ScoreResult,
        SmogResult,
        SpacheResult,
    )

_dynamic_imports: MappingProxyType[str, tuple[str, str]] = MappingProxyType({
    "ARI": (__spec__.parent, "metrics.ari"),
    "BaseMeasure": (__spec__.parent, "types._interfaces"),
    "BaseResult": (__spec__.parent, "types._interfaces"),
    "BaseStatSummary": (__spec__.parent, "types._interfaces"),
    "ColemanLiau": (__spec__.parent, "metrics.coleman_liau"),
    "ColemanLiauResult": (__spec__.parent, "types.results"),
    "DaleChall": (__spec__.parent, "metrics.dale_chall"),
    "DaleChallResult": (__spec__.parent, "types.results"),
    "Flesch": (__spec__.parent, "metrics.flesch"),
    "FleschKincaid": (__spec__.parent, "metrics.flesch_kincaid"),
    "FleschKincaidResult": (__spec__.parent, "types.results"),
    "FleschResult": (__spec__.parent, "types.results"),
    "GradeResult": (__spec__.parent, "types.results"),
    "GunningFog": (__spec__.parent, "metrics.gunning_fog"),
    "GunningFogResult": (__spec__.parent, "types.results"),
    "LinsearWrite": (__spec__.parent, "metrics.linsear_write"),
    "LinsearWriteResult": (__spec__.parent, "types.results"),
    "Metric": (__spec__.parent, "types.enums"),
    "Readability": (__spec__.parent, "readability"),
    "ReadabilityMetric": (__spec__.parent, "types.enums"),
    "ResourceLoader": (__spec__.parent, "resources.loader"),
    "ScoreResult": (__spec__.parent, "types.results"),
    "Smog": (__spec__.parent, "metrics.smog"),
    "SmogResult": (__spec__.parent, "types.results"),
    "Spache": (__spec__.parent, "metrics.spache"),
    "SpacheResult": (__spec__.parent, "types.results"),
    "StatSummary": (__spec__.parent, "text.statistics"),
    "Stemmer": (__spec__.parent, "resources.stemmer"),
    "TextAnalyzer": (__spec__.parent, "text.analyzer"),
    "Tokenizer": (__spec__.parent, "text.tokenizer"),
    "ARIResult": (__spec__.parent, "types.results"),
})

__getattr__ = create_late_getattr(_dynamic_imports, globals(), __name__)

__all__ = (
    "ARI",
    "ARIResult",
    "BaseMeasure",
    "BaseResult",
    "BaseStatSummary",
    "ColemanLiau",
    "ColemanLiauResult",
    "DaleChall",
    "DaleChallResult",
    "Flesch",
    "FleschKincaid",
    "FleschKincaidResult",
    "FleschResult",
    "GradeResult",
    "GunningFog",
    "GunningFogResult",
    "LinsearWrite",
    "LinsearWriteResult",
    "Metric",
    "Readability",
    "ReadabilityMetric",
    "ResourceLoader",
    "ScoreResult",
    "Smog",
    "SmogResult",
    "Spache",
    "SpacheResult",
    "StatSummary",
    "Stemmer",
    "TextAnalyzer",
    "Tokenizer",
)


def __dir__() -> list[str]:
    """List available attributes for the package."""
    return list(__all__)
