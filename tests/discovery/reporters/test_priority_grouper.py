"""Tests for the PriorityGrouper module."""

import pytest

from scripts.discovery.reporters.priority_grouper import PriorityGrouper


class TestPriorityGrouper:
    """Test the PriorityGrouper class."""

    @pytest.fixture
    def priority_grouper(self):
        return PriorityGrouper()

    def test_init(self, priority_grouper):
        """Test initialization of PriorityGrouper."""
        assert priority_grouper.high_threshold == 85  # Exceptional
        assert priority_grouper.medium_threshold == 70  # High Quality
        assert priority_grouper.low_threshold == 60  # Good Quality

    def test_group_evaluations_empty(self, priority_grouper):
        """Test grouping empty evaluations."""
        groups = priority_grouper.group_evaluations([])

        assert len(groups["exceptional"]) == 0
        assert len(groups["high"]) == 0
        assert len(groups["good"]) == 0
        assert len(groups["below_threshold"]) == 0

    def test_group_evaluations_single_exceptional(self, priority_grouper):
        """Test grouping single exceptional evaluation."""
        evaluations = [{"score": 90}]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 1
        assert len(groups["high"]) == 0
        assert len(groups["good"]) == 0
        assert len(groups["below_threshold"]) == 0

    def test_group_evaluations_single_high(self, priority_grouper):
        """Test grouping single high-priority evaluation."""
        evaluations = [{"score": 75}]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 0
        assert len(groups["high"]) == 1
        assert len(groups["good"]) == 0
        assert len(groups["below_threshold"]) == 0

    def test_group_evaluations_single_good(self, priority_grouper):
        """Test grouping single good-priority evaluation."""
        evaluations = [{"score": 65}]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 0
        assert len(groups["high"]) == 0
        assert len(groups["good"]) == 1
        assert len(groups["below_threshold"]) == 0

    def test_group_evaluations_single_below_threshold(self, priority_grouper):
        """Test grouping single below-threshold evaluation."""
        evaluations = [{"score": 50}]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 0
        assert len(groups["high"]) == 0
        assert len(groups["good"]) == 0
        assert len(groups["below_threshold"]) == 1

    def test_group_evaluations_mixed(self, priority_grouper):
        """Test grouping mixed priority evaluations."""
        evaluations = [
            {"score": 90},  # exceptional
            {"score": 75},  # high
            {"score": 65},  # good
            {"score": 85},  # exceptional
            {"score": 50},  # below_threshold
            {"score": 70},  # high
        ]

        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 2
        assert len(groups["high"]) == 2
        assert len(groups["good"]) == 1
        assert len(groups["below_threshold"]) == 1

    def test_group_evaluations_sorted(self, priority_grouper):
        """Test that evaluations are sorted by score descending."""
        evaluations = [
            {"score": 75},  # high
            {"score": 90},  # exceptional
            {"score": 50},  # below_threshold
            {"score": 85},  # exceptional
        ]

        groups = priority_grouper.group_evaluations(evaluations)

        # Check that exceptional items are sorted (90, 85)
        assert groups["exceptional"][0]["score"] == 90
        assert groups["exceptional"][1]["score"] == 85

        # Check that high priority item is there
        assert groups["high"][0]["score"] == 75

        # Check that below_threshold item is there
        assert groups["below_threshold"][0]["score"] == 50

    def test_group_evaluations_boundary_values(self, priority_grouper):
        """Test grouping with boundary values."""
        evaluations = [
            {"score": 85},  # exactly exceptional threshold
            {"score": 84},  # just below exceptional threshold
            {"score": 70},  # exactly high threshold
            {"score": 69},  # just below high threshold
            {"score": 60},  # exactly good threshold
            {"score": 59},  # just below good threshold
        ]

        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 1
        assert groups["exceptional"][0]["score"] == 85

        assert len(groups["high"]) == 2
        assert groups["high"][0]["score"] == 84
        assert groups["high"][1]["score"] == 70

        assert len(groups["good"]) == 2
        assert groups["good"][0]["score"] == 69
        assert groups["good"][1]["score"] == 60

        assert len(groups["below_threshold"]) == 1
        assert groups["below_threshold"][0]["score"] == 59

    def test_get_priority_counts_empty(self, priority_grouper):
        """Test getting priority counts for empty evaluations."""
        counts = priority_grouper.get_priority_counts([])

        assert counts["total"] == 0
        assert counts["exceptional"] == 0
        assert counts["high"] == 0
        assert counts["good"] == 0
        assert counts["below_threshold"] == 0

    def test_get_priority_counts_mixed(self, priority_grouper):
        """Test getting priority counts for mixed evaluations."""
        evaluations = [
            {"score": 90},  # exceptional
            {"score": 75},  # high
            {"score": 65},  # good
            {"score": 85},  # exceptional
            {"score": 50},  # below_threshold
        ]

        counts = priority_grouper.get_priority_counts(evaluations)

        assert counts["total"] == 5
        assert counts["exceptional"] == 2
        assert counts["high"] == 1
        assert counts["good"] == 1
        assert counts["below_threshold"] == 1
