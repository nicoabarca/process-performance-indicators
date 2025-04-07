import pandas as pd

from process_performance_indicators.column_mapping import (
    StandardColumnMapping,
    convert_to_standard_mapping,
    validate_column_mapping,
)


def log_formatter(
    event_log: pd.DataFrame, column_mapping: dict[str, str] | StandardColumnMapping
) -> pd.DataFrame:
    """
    Format an event log into a pandas DataFrame with standardized column names.

    Args:
        event_log: The event log to format.
        column_mapping: Either a dictionary mapping standard column names to log column names,
                        or a StandardColumnMapping instance.

    Returns:
        pd.DataFrame: The formatted event log with standardized column names.

    """
    standard_mapping = convert_to_standard_mapping(column_mapping)
    validate_column_mapping(standard_mapping)
    inverted_mapping = {v: k for k, v in standard_mapping.items()}
    return event_log.rename(columns=inverted_mapping)
