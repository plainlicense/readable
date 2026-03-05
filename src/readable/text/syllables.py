"""Syllable counting utilities."""

import re


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
    word = re.sub(r'(?:[^laeiouy]es|[^laeiouy]e)$', '', word)
    # Remove initial 'y' which acts as a consonant
    word = re.sub(r'^y', '', word)
    # Count vowel clusters
    matches = re.findall(r'[aeiouy]{1,2}', word)
    return len(matches)
