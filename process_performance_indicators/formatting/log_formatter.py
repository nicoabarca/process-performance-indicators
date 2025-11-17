import pandas as pd

from process_performance_indicators.constants import (
    StandardColumnNames,
)
from process_performance_indicators.formatting.column_mapping import (
    StandardColumnMapping,
    convert_to_standard_mapping,
    validate_column_mapping,
)
from process_performance_indicators.formatting.instance_id_generator import id_generator


def event_log_formatter(
    event_log: pd.DataFrame,
    column_mapping: dict[str, str] | StandardColumnMapping,
    date_format: str | None = None,
    *,
    dayfirst: bool = False,
) -> pd.DataFrame:
    """
    Format an event log into a pandas DataFrame with standardized column names.
    If start_timestamp_key is present, splits each row into two separate rows:
    one for the start event and one for the complete event.
    If instance_key is None, a new instance ID is assigned to each pair of rows.

    Args:
        event_log: The event log to format.
        column_mapping: Either a dictionary mapping standard column names to log column names,
                        or a StandardColumnMapping instance.
        date_format: The datetime format to use when parsing timestamp columns.
                    Can be a specific format string (e.g., "%d-%m-%Y %H:%M:%S"),
                    "ISO8601" for ISO8601 format, "mixed" for automatic inference,
                    or None to use pandas default parsing.
        dayfirst: Whether to interpret the first value in an ambiguous date
                 (e.g., 01/05/09) as the day (True) or month (False).
                 Only used when date_format is None or "mixed".

    Returns:
        pd.DataFrame: The formatted event log with standardized column names and split events.

    """
    event_log = event_log.copy()

    # Validate column mapping with standard column names
    standard_mapping = convert_to_standard_mapping(column_mapping)
    validate_column_mapping(standard_mapping)

    # Rename columns to standard column names
    inverted_mapping = {v: k for k, v in standard_mapping.items()}
    standard_named_log = event_log.rename(columns=inverted_mapping)

    # Convert case id to string
    standard_named_log[StandardColumnNames.CASE_ID] = standard_named_log[StandardColumnNames.CASE_ID].astype(str)

    # Convert activity name to string
    standard_named_log[StandardColumnNames.ACTIVITY] = standard_named_log[StandardColumnNames.ACTIVITY].astype(str)

    # Convert instance to string if present
    if StandardColumnNames.INSTANCE in standard_named_log.columns:
        standard_named_log[StandardColumnNames.INSTANCE] = standard_named_log[StandardColumnNames.INSTANCE].astype(str)

    # If start timestamp is not present, return the standard named log
    if StandardColumnNames.START_TIMESTAMP not in standard_named_log.columns:
        return standard_named_log

    # Add missing columns
    if StandardColumnNames.INSTANCE not in standard_named_log.columns:
        standard_named_log[StandardColumnNames.INSTANCE] = [
            id_generator.get_next_id() for _ in range(len(standard_named_log))
        ]

    # Convert instance to string
    standard_named_log[StandardColumnNames.INSTANCE] = standard_named_log[StandardColumnNames.INSTANCE].astype(str)

    # Convert timestamp columns to datetime
    if date_format is not None:
        standard_named_log[StandardColumnNames.TIMESTAMP] = pd.to_datetime(
            standard_named_log[StandardColumnNames.TIMESTAMP], format=date_format, utc=True
        )
        standard_named_log[StandardColumnNames.START_TIMESTAMP] = pd.to_datetime(
            standard_named_log[StandardColumnNames.START_TIMESTAMP], format=date_format, utc=True
        )
    else:
        standard_named_log[StandardColumnNames.TIMESTAMP] = pd.to_datetime(
            standard_named_log[StandardColumnNames.TIMESTAMP], dayfirst=dayfirst, utc=True
        )
        standard_named_log[StandardColumnNames.START_TIMESTAMP] = pd.to_datetime(
            standard_named_log[StandardColumnNames.START_TIMESTAMP], dayfirst=dayfirst, utc=True
        )

    # Create a copy of the log for start events
    start_events_log = standard_named_log.copy()
    start_events_log[StandardColumnNames.TIMESTAMP] = start_events_log[StandardColumnNames.START_TIMESTAMP]

    # Drop the start timestamp from both logs
    if StandardColumnNames.START_TIMESTAMP in standard_named_log.columns:
        standard_named_log = standard_named_log.drop(columns=[StandardColumnNames.START_TIMESTAMP])
        start_events_log = start_events_log.drop(columns=[StandardColumnNames.START_TIMESTAMP])

    # Add lifecycle transition column
    standard_named_log[StandardColumnNames.LIFECYCLE_TRANSITION] = "complete"
    start_events_log[StandardColumnNames.LIFECYCLE_TRANSITION] = "start"

    # Combine the start and complete events
    combined_df = pd.concat([start_events_log, standard_named_log], ignore_index=True)
    combined_df = combined_df.sort_values(by=[StandardColumnNames.CASE_ID, StandardColumnNames.TIMESTAMP])

    return combined_df.reset_index(drop=True)
