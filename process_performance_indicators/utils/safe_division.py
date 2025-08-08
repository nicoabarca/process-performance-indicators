"""
Safe division utilities for process performance indicators.

This module provides a simple function for performing division operations
with appropriate error handling.
"""

from process_performance_indicators.exceptions import ProcessPerformanceIndicatorDivisionError


def safe_division(
    numerator: float,
    denominator: float,
    exception_class: type[Exception] = ProcessPerformanceIndicatorDivisionError,
) -> float:
    """
    Safely perform division with automatic error handling.

    Args:
        numerator: The numerator value.
        denominator: The denominator value.
        exception_class: The exception class to raise (defaults to ProcessPerformanceIndicatorDivisionError).

    Returns:
        float: The result of the division.

    Raises:
        exception_class: When denominator is zero, with a message showing both values.

    """
    if denominator == 0:
        error_message = (
            f"Error performing indicator division. Numerator value={numerator}, denominator value={denominator}"
        )
        raise exception_class(error_message)
    return numerator / denominator
