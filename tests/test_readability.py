# SPDX-FileCopyrightText: 2026 PlainLicense
#
# SPDX-License-Identifier: LicenseRef-PlainMIT OR MIT

"""Unit tests for the readable library."""

import pytest

from readable import Readability


class TestReadability:
    """Test cases for the Readability class."""

    @pytest.fixture
    def readability(self):
        """Fixture for the Readability object."""
        text = """
        In linguistics, the Gunning fog index is a readability test for English writing. The index estimates the years of formal education a person needs to understand the text on the first reading. For instance, a fog index of 12 requires the reading level of a United States high school senior (around 18 years old). The test was developed in 1952 by Robert Gunning, an American businessman who had been involved in newspaper and textbook publishing.
        The fog index is commonly used to confirm that text can be read easily by the intended audience. Texts for a wide audience generally need a fog index less than 12. Texts requiring near-universal understanding generally need an index less than 8.
        """
        return Readability(text)

    def test_ari(self, readability):
        """Test the ARI score."""
        r = readability.ari()
        assert r.score == 9.551245421245422
        assert r.grade_levels == ["10"]
        assert r.ages == [15, 16]

    def test_coleman_liau(self, readability):
        """Test the Coleman-Liau score."""
        r = readability.coleman_liau()
        assert pytest.approx(r.score, abs=1e-7) == 10.673162393162393
        assert r.grade_level == "11"

    def test_dale_chall(self, readability):
        """Test the Dale-Chall score."""
        r = readability.dale_chall()
        assert pytest.approx(r.score, abs=1e-7) == 9.32399010989011
        assert r.grade_levels == ["college"]

    def test_flesch(self, readability):
        """Test the Flesch score."""
        r = readability.flesch()
        assert pytest.approx(r.score, abs=1e-7) == 51.039230769230784
        assert r.grade_levels == ["10", "11", "12"]
        assert r.ease == "fairly_difficult"

    def test_flesch_kincaid(self, readability):
        """Test the Flesch-Kincaid score."""
        r = readability.flesch_kincaid()
        assert pytest.approx(r.score, abs=1e-7) == 10.125531135531137
        assert r.grade_level == "10"

    def test_gunning_fog(self, readability):
        """Test the Gunning Fog score."""
        r = readability.gunning_fog()
        assert pytest.approx(r.score, abs=1e-7) == 12.4976800976801
        assert r.grade_level == "12"

    def test_linsear_write(self, readability):
        """Test the Linsear Write score."""
        r = readability.linsear_write()
        assert pytest.approx(r.score, abs=1e-7) == 11.214285714285714
        assert r.grade_level == "11"

    def test_smog(self):
        """Test the SMOG score."""
        text = """
        In linguistics, the Gunning fog index is a readability test for English writing. The index estimates the years of formal education a person needs to understand the text on the first reading. For instance, a fog index of 12 requires the reading level of a United States high school senior (around 18 years old). The test was developed in 1952 by Robert Gunning, an American businessman who had been involved in newspaper and textbook publishing.
        The fog index is commonly used to confirm that text can be read easily by the intended audience. Texts for a wide audience generally need a fog index less than 12. Texts requiring near-universal understanding generally need an index less than 8.
        """
        text = " ".join(text for i in range(5))

        readability = Readability(text)

        # Test SMOG with 30 sentences
        r1 = readability.smog()

        # Test SMOG with all sentences
        r2 = readability.smog(all_sentences=True)

        assert pytest.approx(r1.score, abs=1e-7) == 12.516099999999998
        assert r1.grade_level == "13"

        assert pytest.approx(r2.score, abs=1e-7) == 12.785403640627713
        assert r2.grade_level == "13"

    def test_spache(self, readability):
        """Test the Spache score."""
        r = readability.spache()
        assert pytest.approx(r.score, abs=1e-7) == 7.164945054945054
        assert r.grade_level == "7"

    def test_print_stats(self, readability):
        """Test the statistics method."""
        stats = readability.statistics()
        assert stats["num_letters"] == 562
        assert stats["num_words"] == 117
        assert stats["num_sentences"] == 7
        assert stats["num_polysyllabic_words"] == 20
