"""Stemming utilities for text analysis."""

from nltk.stem.porter import PorterStemmer


class Stemmer:
    """A class for stemming words."""

    def __init__(self):
        """Initialize the stemmer."""
        self._porter_stemmer = PorterStemmer()

    def stem(self, word: str) -> str:
        """
        Stem a word.

        Args:
            word: The word to stem.

        Returns:
            The stemmed word.
        """
        return self._porter_stemmer.stem(word.lower())
