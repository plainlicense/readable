# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Syllable counting utilities."""

import re


_TRAILING_E_PATTERN = re.compile(r"(?:[^laeiouy]es|[^laeiouy]e)$", re.IGNORECASE)
_INITIAL_Y_PATTERN = re.compile(r"^y", re.IGNORECASE)
_VOWEL_CLUSTER_PATTERN = re.compile(r"[aeiouy]{1,2}", re.IGNORECASE)


def count_syllables(word: str) -> int:
    """
    Count the number of syllables in a word.

    Args:
        word: The word to count syllables for.

    Returns:
        The number of syllables in the word.
    """
    word = word.lower()

    if len(word) <= 3:
        return 1

    # Remove trailing 'e' or 'es' that aren't usually pronounced as a syllable
    # (unless preceded by 'l')
    word = _TRAILING_E_PATTERN.sub("", word)
    # Remove initial 'y' which acts as a consonant
    word = _INITIAL_Y_PATTERN.sub("", word)
    # Count vowel clusters
    matches = _VOWEL_CLUSTER_PATTERN.findall(word)
    return len(matches)


__all__ = ("count_syllables",)
