# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Text tokenization utilities."""

import nltk
from pathlib import Path as _Path

_BUNDLED_NLTK_DATA = str(_Path(__file__).parent.parent / "resources" / "nltk_data")
if _BUNDLED_NLTK_DATA not in nltk.data.path:
    nltk.data.path.insert(0, _BUNDLED_NLTK_DATA)

from nltk.tokenize import TweetTokenizer, sent_tokenize


class Tokenizer:
    """A class for tokenizing text into sentences and words."""

    def __init__(self):
        """Initialize the tokenizer."""
        self._tweet_tokenizer = TweetTokenizer()

    def tokenize_sentences(self, text: str) -> list[str]:
        """
        Tokenize text into sentences.

        Args:
            text: The text to tokenize.

        Returns:
            A list of sentences.
        """
        return sent_tokenize(text)

    def tokenize_words(self, text: str) -> list[str]:
        """
        Tokenize text into words.

        Args:
            text: The text to tokenize.

        Returns:
            A list of words.
        """
        return self._tweet_tokenizer.tokenize(text)


__all__ = ("Tokenizer",)
