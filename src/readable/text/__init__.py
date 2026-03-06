# SPDX-FileCopyrightText: 2026 PlainLicense <https://plainlicense.org>
#
# SPDX-License-Identifier: LicenseRef-PlainMIT or MIT

"""Text analysis and processing utilities."""

from __future__ import annotations

from types import MappingProxyType

# === MANAGED EXPORTS ===
# Exportify manages this section. It contains lazy-loading infrastructure
# for the package: imports and runtime declarations (__all__, __getattr__,
# __dir__). Manual edits will be overwritten by `exportify fix`.
from typing import TYPE_CHECKING

from lateimport import create_late_getattr


if TYPE_CHECKING:
    from readable.text.analyzer import TextAnalyzer
    from readable.text.statistics import StatSummary
    from readable.text.syllables import count_syllables
    from readable.text.tokenizer import Tokenizer

_dynamic_imports: MappingProxyType[str, tuple[str, str]] = MappingProxyType({
    "StatSummary": (__spec__.parent, "statistics"),
    "TextAnalyzer": (__spec__.parent, "analyzer"),
    "Tokenizer": (__spec__.parent, "tokenizer"),
    "count_syllables": (__spec__.parent, "syllables"),
})

__getattr__ = create_late_getattr(_dynamic_imports, globals(), __name__)

__all__ = ("StatSummary", "TextAnalyzer", "Tokenizer", "count_syllables")


def __dir__() -> list[str]:
    """List available attributes for the package."""
    return list(__all__)
