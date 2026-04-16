"""Tests for the ToolPriorityGrouper module."""

import pytest

from scripts.tool_discovery.reporters.priority_grouper import ToolPriorityGrouper


class TestToolPriorityGrouper:
    """Test the ToolPriorityGrouper class."""

    @pytest.fixture
    def priority_grouper(self):
        return ToolPriorityGrouper()

    def test_init_thresholds(self, priority_grouper):
        """Test initialization with correct thresholds."""
        # Exceptional threshold
        assert priority_grouper.high_threshold == 80
        # High quality threshold
        assert priority_grouper.medium_threshold == 65
        # Good quality threshold
        assert priority_grouper.low_threshold == 50

    def test_group_evaluations_empty(self, priority_grouper):
        """Test grouping empty evaluations."""
        groups = priority_grouper.group_evaluations([])

        assert len(groups["exceptional"]) == 0
        assert len(groups["high"]) == 0
        assert len(groups["good"]) == 0
        assert len(groups["below_threshold"]) == 0

    def test_group_evaluations_exceptional(self, priority_grouper):
        """Test grouping a single exceptional evaluation."""
        evaluations = [{"score": 85}]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 1
        assert len(groups["high"]) == 0
        assert len(groups["good"]) == 0
        assert len(groups["below_threshold"]) == 0

    def test_group_evaluations_high(self, priority_grouper):
        """Test grouping a single high-quality evaluation."""
        evaluations = [{"score": 72}]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 0
        assert len(groups["high"]) == 1
        assert len(groups["good"]) == 0
        assert len(groups["below_threshold"]) == 0

    def test_group_evaluations_good(self, priority_grouper):
        """Test grouping a single good-quality evaluation."""
        evaluations = [{"score": 57}]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 0
        assert len(groups["high"]) == 0
        assert len(groups["good"]) == 1
        assert len(groups["below_threshold"]) == 0

    def test_group_evaluations_below_threshold(self, priority_grouper):
        """Test grouping a single below-threshold evaluation."""
        evaluations = [{"score": 35}]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 0
        assert len(groups["high"]) == 0
        assert len(groups["good"]) == 0
        assert len(groups["below_threshold"]) == 1

    def test_group_evaluations_boundary_exceptional(self, priority_grouper):
        """Test boundary at exceptional threshold (80)."""
        evaluations = [
            {"score": 80},  # exactly at exceptional threshold
            {"score": 79},  # just below exceptional threshold
        ]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 1
        assert groups["exceptional"][0]["score"] == 80

        assert len(groups["high"]) == 1
        assert groups["high"][0]["score"] == 79

    def test_group_evaluations_boundary_high(self, priority_grouper):
        """Test boundary at high threshold (65)."""
        evaluations = [
            {"score": 65},  # exactly at high threshold
            {"score": 64},  # just below high threshold
        ]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["high"]) == 1
        assert groups["high"][0]["score"] == 65

        assert len(groups["good"]) == 1
        assert groups["good"][0]["score"] == 64

    def test_group_evaluations_boundary_good(self, priority_grouper):
        """Test boundary at good threshold (50)."""
        evaluations = [
            {"score": 50},  # exactly at good threshold
            {"score": 49},  # just below good threshold
        ]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["good"]) == 1
        assert groups["good"][0]["score"] == 50

        assert len(groups["below_threshold"]) == 1
        assert groups["below_threshold"][0]["score"] == 49

    def test_group_evaluations_mixed(self, priority_grouper):
        """Test grouping mixed priority evaluations."""
        evaluations = [
            {"score": 90},  # exceptional
            {"score": 72},  # high
            {"score": 55},  # good
            {"score": 82},  # exceptional
            {"score": 40},  # below_threshold
            {"score": 67},  # high
        ]

        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups["exceptional"]) == 2
        assert len(groups["high"]) == 2
        assert len(groups["good"]) == 1
        assert len(groups["below_threshold"]) == 1

    def test_group_evaluations_sorted_descending(self, priority_grouper):
        """Test that evaluations are sorted by score descending within groups."""
        evaluations = [
            {"score": 72},  # high
            {"score": 90},  # exceptional
            {"score": 40},  # below_threshold
            {"score": 82},  # exceptional
        ]

        groups = priority_grouper.group_evaluations(evaluations)

        # Exceptional group should be sorted 90, 82
        assert groups["exceptional"][0]["score"] == 90
        assert groups["exceptional"][1]["score"] == 82

        # High group should have 72
        assert groups["high"][0]["score"] == 72

        # Below threshold group should have 40
        assert groups["below_threshold"][0]["score"] == 40

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
            {"score": 88},  # exceptional
            {"score": 70},  # high
            {"score": 52},  # good
            {"score": 83},  # exceptional
            {"score": 30},  # below_threshold
        ]

        counts = priority_grouper.get_priority_counts(evaluations)

        assert counts["total"] == 5
        assert counts["exceptional"] == 2
        assert counts["high"] == 1
        assert counts["good"] == 1
        assert counts["below_threshold"] == 1

    def test_get_priority_counts_all_exceptional(self, priority_grouper):
        """Test getting priority counts when all are exceptional."""
        evaluations = [{"score": 85}, {"score": 90}, {"score": 95}]

        counts = priority_grouper.get_priority_counts(evaluations)

        assert counts["total"] == 3
        assert counts["exceptional"] == 3
        assert counts["high"] == 0
        assert counts["good"] == 0
        assert counts["below_threshold"] == 0
