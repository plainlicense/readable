# SPDX-FileCopyrightText: 2026 PlainLicense <https://plainlicense.org>
#
# SPDX-License-Identifier: LicenseRef-PlainMIT or MIT

"""Type definitions and interfaces for the readable library."""

from __future__ import annotations

from types import MappingProxyType

# === MANAGED EXPORTS ===
# Exportify manages this section. It contains lazy-loading infrastructure
# for the package: imports and runtime declarations (__all__, __getattr__,
# __dir__). Manual edits will be overwritten by `exportify fix`.
from typing import TYPE_CHECKING

from lateimport import create_late_getattr


if TYPE_CHECKING:
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
    "BaseMeasure": (__spec__.parent, "_interfaces"),
    "BaseResult": (__spec__.parent, "_interfaces"),
    "BaseStatSummary": (__spec__.parent, "_interfaces"),
    "ColemanLiauResult": (__spec__.parent, "results"),
    "DaleChallResult": (__spec__.parent, "results"),
    "FleschKincaidResult": (__spec__.parent, "results"),
    "FleschResult": (__spec__.parent, "results"),
    "GradeResult": (__spec__.parent, "results"),
    "GunningFogResult": (__spec__.parent, "results"),
    "LinsearWriteResult": (__spec__.parent, "results"),
    "Metric": (__spec__.parent, "enums"),
    "ReadabilityMetric": (__spec__.parent, "enums"),
    "ScoreResult": (__spec__.parent, "results"),
    "SmogResult": (__spec__.parent, "results"),
    "SpacheResult": (__spec__.parent, "results"),
    "ARIResult": (__spec__.parent, "results"),
})

__getattr__ = create_late_getattr(_dynamic_imports, globals(), __name__)

__all__ = (
    "ARIResult",
    "BaseMeasure",
    "BaseResult",
    "BaseStatSummary",
    "ColemanLiauResult",
    "DaleChallResult",
    "FleschKincaidResult",
    "FleschResult",
    "GradeResult",
    "GunningFogResult",
    "LinsearWriteResult",
    "Metric",
    "ReadabilityMetric",
    "ScoreResult",
    "SmogResult",
    "SpacheResult",
)


def __dir__() -> list[str]:
    """List available attributes for the package."""
    return list(__all__)
