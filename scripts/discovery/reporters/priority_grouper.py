"""Priority grouper for organizing evaluations by score."""

from typing import Any


class PriorityGrouper:
    """Groups evaluations by priority based on scores."""

    def __init__(self):
        # Updated thresholds for 100-point scoring system
        self.high_threshold = 85  # Exceptional
        self.medium_threshold = 70  # High Quality
        self.low_threshold = 60  # Good Quality (minimum acceptance)

    def group_evaluations(
        self, evaluations: list[dict[str, Any]]
    ) -> dict[str, list[dict[str, Any]]]:
        """Group evaluations by priority level."""
        sorted_evaluations = sorted(evaluations, key=lambda x: x["score"], reverse=True)

        return {
            "exceptional": [
                e for e in sorted_evaluations if e["score"] >= self.high_threshold
            ],
            "high": [
                e
                for e in sorted_evaluations
                if self.medium_threshold <= e["score"] < self.high_threshold
            ],
            "good": [
                e
                for e in sorted_evaluations
                if self.low_threshold <= e["score"] < self.medium_threshold
            ],
            "below_threshold": [
                e for e in sorted_evaluations if e["score"] < self.low_threshold
            ],
        }

    def get_priority_counts(self, evaluations: list[dict[str, Any]]) -> dict[str, int]:
        """Get counts for each priority level."""
        groups = self.group_evaluations(evaluations)
        return {
            "exceptional": len(groups["exceptional"]),
            "high": len(groups["high"]),
            "good": len(groups["good"]),
            "below_threshold": len(groups["below_threshold"]),
            "total": len(evaluations),
        }
