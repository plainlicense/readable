# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Resource loading utilities for word lists and other static data."""

from functools import cache
from pathlib import Path


@cache
def _load_word_set(file_path: Path) -> set[str]:
    """Internal function to load and cache a word set."""
    with file_path.open("r", encoding="utf-8") as f:
        return {line.strip().lower() for line in f if line.strip()}


class ResourceLoader:
    """A class for loading resources like word lists."""

    def __init__(self):
        """Initialize the resource loader."""
        self._base_path = Path(__file__).parent.resolve()
        self._data_path = self._base_path / "data"

    def load_word_set(self, filename: str) -> set[str]:
        """
        Load a word set from a file.

        Args:
            filename: The name of the file to load from.

        Returns:
            A set of words from the file.
        """
        file_path = self._data_path / filename
        return _load_word_set(file_path)


__all__ = ("ResourceLoader",)
