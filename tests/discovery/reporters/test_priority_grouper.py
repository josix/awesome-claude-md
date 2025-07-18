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
        assert priority_grouper.high_threshold == 7
        assert priority_grouper.medium_threshold == 4

    def test_group_evaluations_empty(self, priority_grouper):
        """Test grouping empty evaluations."""
        groups = priority_grouper.group_evaluations([])

        assert len(groups['high']) == 0
        assert len(groups['medium']) == 0
        assert len(groups['low']) == 0

    def test_group_evaluations_single_high(self, priority_grouper):
        """Test grouping single high-priority evaluation."""
        evaluations = [{'score': 8}]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups['high']) == 1
        assert len(groups['medium']) == 0
        assert len(groups['low']) == 0

    def test_group_evaluations_single_medium(self, priority_grouper):
        """Test grouping single medium-priority evaluation."""
        evaluations = [{'score': 5}]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups['high']) == 0
        assert len(groups['medium']) == 1
        assert len(groups['low']) == 0

    def test_group_evaluations_single_low(self, priority_grouper):
        """Test grouping single low-priority evaluation."""
        evaluations = [{'score': 2}]
        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups['high']) == 0
        assert len(groups['medium']) == 0
        assert len(groups['low']) == 1

    def test_group_evaluations_mixed(self, priority_grouper):
        """Test grouping mixed priority evaluations."""
        evaluations = [
            {'score': 8},  # high
            {'score': 5},  # medium
            {'score': 2},  # low
            {'score': 9},  # high
            {'score': 3},  # low
            {'score': 6},  # medium
        ]

        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups['high']) == 2
        assert len(groups['medium']) == 2
        assert len(groups['low']) == 2

    def test_group_evaluations_sorted(self, priority_grouper):
        """Test that evaluations are sorted by score descending."""
        evaluations = [
            {'score': 5},
            {'score': 8},
            {'score': 2},
            {'score': 9},
        ]

        groups = priority_grouper.group_evaluations(evaluations)

        # Check that high priority items are sorted (9, 8)
        assert groups['high'][0]['score'] == 9
        assert groups['high'][1]['score'] == 8

        # Check that medium priority item is there
        assert groups['medium'][0]['score'] == 5

        # Check that low priority item is there
        assert groups['low'][0]['score'] == 2

    def test_group_evaluations_boundary_values(self, priority_grouper):
        """Test grouping with boundary values."""
        evaluations = [
            {'score': 7},  # exactly high threshold
            {'score': 6},  # just below high threshold
            {'score': 4},  # exactly medium threshold
            {'score': 3},  # just below medium threshold
        ]

        groups = priority_grouper.group_evaluations(evaluations)

        assert len(groups['high']) == 1
        assert groups['high'][0]['score'] == 7

        assert len(groups['medium']) == 2
        assert groups['medium'][0]['score'] == 6
        assert groups['medium'][1]['score'] == 4

        assert len(groups['low']) == 1
        assert groups['low'][0]['score'] == 3

    def test_get_priority_counts_empty(self, priority_grouper):
        """Test getting priority counts for empty evaluations."""
        counts = priority_grouper.get_priority_counts([])

        assert counts['total'] == 0
        assert counts['high'] == 0
        assert counts['medium'] == 0
        assert counts['low'] == 0

    def test_get_priority_counts_mixed(self, priority_grouper):
        """Test getting priority counts for mixed evaluations."""
        evaluations = [
            {'score': 8},  # high
            {'score': 5},  # medium
            {'score': 2},  # low
            {'score': 9},  # high
            {'score': 3},  # low
        ]

        counts = priority_grouper.get_priority_counts(evaluations)

        assert counts['total'] == 5
        assert counts['high'] == 2
        assert counts['medium'] == 1
        assert counts['low'] == 2
