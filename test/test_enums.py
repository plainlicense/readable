"""Unit tests for ReadabilityMetric enum."""

from readable.metrics.ari import ARI
from readable.metrics.flesch import Flesch
from readable.types.enums import ReadabilityMetric


class TestEnums:
    """Test cases for ReadabilityMetric enum."""

    def test_measure_class(self):
        """Test that measure_class property returns the correct class."""
        assert ReadabilityMetric.ARI.measure_class == ARI
        assert ReadabilityMetric.FLESCH.measure_class == Flesch

    def test_names(self):
        """Test that names property returns expected values."""
        assert ReadabilityMetric.ARI._names.short == "ARI"
        assert ReadabilityMetric.FLESCH._names.full == "Flesch Reading Ease"

    def test_all_names(self):
        """Test the generated alternative names."""
        ari_names = ReadabilityMetric.ARI._all_names
        assert "ari" in ari_names
        assert "ARI" in ari_names
        assert "Ari" in ari_names
        assert "a" in ari_names # Short name for ARI
