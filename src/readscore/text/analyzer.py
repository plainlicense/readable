# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Main text analysis engine for readability measures."""

import re

from readscore.resources.loader import ResourceLoader
from readscore.resources.stemmer import Stemmer
from readscore.text.statistics import StatSummary
from readscore.text.syllables import count_syllables
from readscore.text.tokenizer import Tokenizer


class TextAnalyzer:
    """A class for analyzing text and calculating readability statistics."""

    def __init__(self):
        """Initialize the text analyzer."""
        self._tokenizer = Tokenizer()
        self._resource_loader = ResourceLoader()
        self._stemmer = Stemmer()
        self._dale_chall_vocabulary: set[str] = set()
        self._spache_vocabulary: set[str] = set()
        self._initialized = False

    def _ensure_initialized(self):
        """Load resources if not already loaded."""
        if not self._initialized:
            self._dale_chall_vocabulary = self._resource_loader.load_word_set(
                "dale_chall_porterstem.txt"
            )
            self._spache_vocabulary = self._resource_loader.load_word_set(
                "spache_easy_porterstem.txt"
            )
            self._initialized = True

    def analyze(self, text: str) -> StatSummary:
        """
        Analyze text and return a summary of statistics.

        Args:
            text: The text to analyze.

        Returns:
            A StatSummary object containing calculated statistics.
        """
        self._ensure_initialized()
        tokens = self._tokenizer.tokenize_words(text)
        sentences = self._tokenizer.tokenize_sentences(text)

        word_count = 0
        syllable_count = 0
        poly_syllable_count = 0
        letters_count = 0
        gunning_complex_count = 0
        dale_chall_complex_count = 0
        spache_complex_count = 0

        for token in tokens:
            if self._is_punctuation(token):
                continue

            word_count += 1
            word_syllable_count = count_syllables(token)
            syllable_count += word_syllable_count
            letters_count += len(token)

            if word_syllable_count >= 3:
                poly_syllable_count += 1

            if self._is_gunning_complex(token, word_syllable_count):
                gunning_complex_count += 1

            if self._is_dale_chall_complex(token):
                dale_chall_complex_count += 1

            if self._is_spache_complex(token):
                spache_complex_count += 1

        sentence_count = len(sentences)
        if sentence_count == 0:
            sentence_count = 1  # Avoid division by zero

        if word_count == 0:
            word_count = 1  # Avoid division by zero

        avg_words_per_sentence = word_count / sentence_count
        avg_syllables_per_word = syllable_count / word_count

        return StatSummary(
            num_letters=letters_count,
            num_words=word_count,
            num_sentences=sentence_count,
            num_syllables=syllable_count,
            num_poly_syllable_words=poly_syllable_count,
            avg_words_per_sentence=avg_words_per_sentence,
            avg_syllables_per_word=avg_syllables_per_word,
            num_gunning_complex=gunning_complex_count,
            num_dale_chall_complex=dale_chall_complex_count,
            num_spache_complex=spache_complex_count,
        )

    def _is_punctuation(self, token: str) -> bool:
        """Check if a token is a punctuation mark."""
        return re.match(r"^[.,\/#!$%\'\^&\*;:{}=\-_`~()]$", token) is not None

    def _is_gunning_complex(self, token: str, syllable_count: int) -> bool:
        """Check if a word is complex according to the Gunning Fog Index."""
        return syllable_count >= 3 and not (
            self._is_proper_noun(token) or self._is_compound_word(token)
        )

    def _is_proper_noun(self, token: str) -> bool:
        """Check if a token is a proper noun (simple heuristic)."""
        return token[0].isupper() if token else False

    def _is_compound_word(self, token: str) -> bool:
        """Check if a token is a compound word (contains a hyphen)."""
        return "-" in token

    def _is_dale_chall_complex(self, token: str) -> bool:
        """Check if a word is complex according to Dale-Chall."""
        stem = self._stemmer.stem(token)
        return stem not in self._dale_chall_vocabulary

    def _is_spache_complex(self, token: str) -> bool:
        """Check if a word is complex according to Spache."""
        stem = self._stemmer.stem(token)
        return stem not in self._spache_vocabulary


__all__ = ("TextAnalyzer",)
