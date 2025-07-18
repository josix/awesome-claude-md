"""Priority grouper for organizing evaluations by score."""

from typing import Any


class PriorityGrouper:
    """Groups evaluations by priority based on scores."""

    def __init__(self):
        self.high_threshold = 7
        self.medium_threshold = 4

    def group_evaluations(self, evaluations: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Group evaluations by priority level."""
        sorted_evaluations = sorted(evaluations, key=lambda x: x['score'], reverse=True)

        return {
            'high': [e for e in sorted_evaluations if e['score'] >= self.high_threshold],
            'medium': [e for e in sorted_evaluations if self.medium_threshold <= e['score'] < self.high_threshold],
            'low': [e for e in sorted_evaluations if e['score'] < self.medium_threshold]
        }

    def get_priority_counts(self, evaluations: list[dict[str, Any]]) -> dict[str, int]:
        """Get counts for each priority level."""
        groups = self.group_evaluations(evaluations)
        return {
            'high': len(groups['high']),
            'medium': len(groups['medium']),
            'low': len(groups['low']),
            'total': len(evaluations)
        }
