from enum import Enum, auto

import pandas as pd

from process_performance_indicators.constants import (
    LifecycleTransitionType,
    StandardColumnNames,
)
from process_performance_indicators.formatting.column_mapping import (
    StandardColumnMapping,
    convert_to_standard_mapping,
    validate_column_mapping,
)
from process_performance_indicators.formatting.conversions import convert_to_explicit_interval_log


class EventLogType(Enum):
    """Enum representing the different types of event logs."""

    ATOMIC = auto()  # No lifecycle, no start_timestamp, no instance
    DERIVABLE_INTERVAL = auto()  # Has lifecycle, no instance
    PRODUCTION_STYLE = auto()  # Has start_timestamp, no lifecycle
    EXPLICIT_INTERVAL = auto()  # Has lifecycle AND instance


def _detect_log_type(column_mapping: StandardColumnMapping) -> EventLogType:
    """
    Detect the type of event log based on the column mapping.

    Args:
        column_mapping: The column mapping configuration.

    Returns:
        EventLogType: The detected log type.

    Detection logic:
        - If lifecycle_type_key AND instance_key provided --> Explicit interval
        - If lifecycle_type_key provided but NOT instance_key --> Derivable interval
        - If start_timestamp_key provided (no lifecycle_type_key) --> Production-style
        - None of above --> Atomic log

    """
    has_lifecycle = column_mapping.lifecycle_type_key is not None
    has_instance = column_mapping.instance_key is not None
    has_start_timestamp = column_mapping.start_timestamp_key is not None

    if has_lifecycle and has_instance:
        return EventLogType.EXPLICIT_INTERVAL
    if has_lifecycle and not has_instance:
        return EventLogType.DERIVABLE_INTERVAL
    if has_start_timestamp and not has_lifecycle:
        return EventLogType.PRODUCTION_STYLE
    return EventLogType.ATOMIC


def _convert_timestamp_column(
    log_df: pd.DataFrame,
    column_name: str,
    date_format: str | None,
    *,
    dayfirst: bool,
) -> None:
    """
    Convert a timestamp column to datetime in place.

    Args:
        log_df: The DataFrame containing the column.
        column_name: The name of the column to convert.
        date_format: The datetime format to use.
        dayfirst: Whether to interpret ambiguous dates as day-first.

    """
    if date_format is not None:
        log_df[column_name] = pd.to_datetime(log_df[column_name], format=date_format, utc=True)
    else:
        log_df[column_name] = pd.to_datetime(log_df[column_name], dayfirst=dayfirst, utc=True)


def _standardize_columns(
    event_log: pd.DataFrame,
    column_mapping: StandardColumnMapping,
) -> pd.DataFrame:
    """
    Rename columns to standard names and filter to only mapped columns.

    Args:
        event_log: The event log to standardize.
        column_mapping: The column mapping to use.

    Returns:
        pd.DataFrame: The standardized event log.

    """
    standard_mapping = convert_to_standard_mapping(column_mapping)
    validate_column_mapping(standard_mapping, set(event_log.columns))

    # Rename columns to standard column names
    inverted_mapping = {v: k for k, v in standard_mapping.items()}
    standard_named_log = event_log.rename(columns=inverted_mapping)

    # Keep only the columns that were mapped
    mapped_columns = list(inverted_mapping.values())
    return standard_named_log[mapped_columns]


def _convert_standard_types(log_df: pd.DataFrame) -> None:
    """
    Convert standard columns to their expected types in place.

    Args:
        log_df: The DataFrame to convert.

    """
    # Convert case id to string
    log_df[StandardColumnNames.CASE_ID] = log_df[StandardColumnNames.CASE_ID].astype(str)

    # Convert activity name to string
    log_df[StandardColumnNames.ACTIVITY] = log_df[StandardColumnNames.ACTIVITY].astype(str)

    # Convert instance to string if present
    if StandardColumnNames.INSTANCE in log_df.columns:
        log_df[StandardColumnNames.INSTANCE] = log_df[StandardColumnNames.INSTANCE].astype(str)


def _process_atomic_log(
    log_df: pd.DataFrame,
    date_format: str | None,
    *,
    dayfirst: bool,
) -> pd.DataFrame:
    """
    Process an atomic event log.

    Atomic logs have only case_id, activity, and timestamp.
    Each row represents an instantaneous event where start and complete are the same.

    Processing:
        1. Mark all rows as complete events
        2. Duplicate each row with start event type (same timestamp)
        3. Match start/complete pairs to assign instance IDs

    Args:
        log_df: The standardized event log.
        date_format: The datetime format.
        dayfirst: Whether to interpret ambiguous dates as day-first.

    Returns:
        pd.DataFrame: An explicit interval log.

    """
    # Convert timestamp to datetime
    _convert_timestamp_column(log_df, StandardColumnNames.TIMESTAMP, date_format, dayfirst=dayfirst)

    # Create complete events (original rows)
    complete_events = log_df.copy()
    complete_events[StandardColumnNames.LIFECYCLE_TRANSITION] = LifecycleTransitionType.COMPLETE

    # Create start events (duplicates with same timestamp)
    start_events = log_df.copy()
    start_events[StandardColumnNames.LIFECYCLE_TRANSITION] = LifecycleTransitionType.START

    # Combine start and complete events
    combined_log = pd.concat([start_events, complete_events], ignore_index=True)
    combined_log = combined_log.sort_values(by=[StandardColumnNames.CASE_ID, StandardColumnNames.TIMESTAMP])
    combined_log = combined_log.reset_index(drop=True)

    # Match start/complete pairs and assign instance IDs
    return convert_to_explicit_interval_log(combined_log)


def _process_derivable_interval_log(
    log_df: pd.DataFrame,
    date_format: str | None,
    *,
    dayfirst: bool,
) -> pd.DataFrame:
    """
    Process a derivable interval event log.

    Derivable logs have lifecycle_transition (start/complete) but no instance IDs.
    The match function is used to pair start and complete events.

    Args:
        log_df: The standardized event log.
        date_format: The datetime format.
        dayfirst: Whether to interpret ambiguous dates as day-first.

    Returns:
        pd.DataFrame: An explicit interval log.

    """
    # Convert timestamp to datetime
    _convert_timestamp_column(log_df, StandardColumnNames.TIMESTAMP, date_format, dayfirst=dayfirst)

    # Match start/complete pairs and assign instance IDs
    return convert_to_explicit_interval_log(log_df)


def _process_production_style_log(
    log_df: pd.DataFrame,
    date_format: str | None,
    *,
    dayfirst: bool,
) -> pd.DataFrame:
    """
    Process a production-style event log with start and end timestamps.

    Production logs have a start_timestamp and timestamp (end) for each row.
    Each row is split into start and complete events.

    Args:
        log_df: The standardized event log.
        date_format: The datetime format.
        dayfirst: Whether to interpret ambiguous dates as day-first.

    Returns:
        pd.DataFrame: An explicit interval log.

    """
    # Convert timestamp columns to datetime
    _convert_timestamp_column(log_df, StandardColumnNames.TIMESTAMP, date_format, dayfirst=dayfirst)
    _convert_timestamp_column(log_df, StandardColumnNames.START_TIMESTAMP, date_format, dayfirst=dayfirst)

    # Create start events (use start_timestamp as timestamp)
    start_events = log_df.copy()
    start_events[StandardColumnNames.TIMESTAMP] = start_events[StandardColumnNames.START_TIMESTAMP]
    start_events = start_events.drop(columns=[StandardColumnNames.START_TIMESTAMP])
    start_events[StandardColumnNames.LIFECYCLE_TRANSITION] = LifecycleTransitionType.START

    # Create complete events (use original timestamp)
    complete_events = log_df.drop(columns=[StandardColumnNames.START_TIMESTAMP])
    complete_events[StandardColumnNames.LIFECYCLE_TRANSITION] = LifecycleTransitionType.COMPLETE

    # Combine start and complete events
    combined_log = pd.concat([start_events, complete_events], ignore_index=True)
    combined_log = combined_log.sort_values(by=[StandardColumnNames.CASE_ID, StandardColumnNames.TIMESTAMP])
    combined_log = combined_log.reset_index(drop=True)

    # Match start/complete pairs and assign instance IDs
    return convert_to_explicit_interval_log(combined_log)


def _process_explicit_interval_log(
    log_df: pd.DataFrame,
    date_format: str | None,
    *,
    dayfirst: bool,
) -> pd.DataFrame:
    """
    Process an explicit interval event log.

    Explicit logs already have lifecycle_transition and instance IDs.
    Only column renaming and type conversion is needed.

    Args:
        log_df: The standardized event log.
        date_format: The datetime format.
        dayfirst: Whether to interpret ambiguous dates as day-first.

    Returns:
        pd.DataFrame: The explicit interval log (no matching needed).

    """
    # Convert timestamp to datetime
    _convert_timestamp_column(log_df, StandardColumnNames.TIMESTAMP, date_format, dayfirst=dayfirst)

    # Sort by case_id and timestamp for consistency
    log_df = log_df.sort_values(by=[StandardColumnNames.CASE_ID, StandardColumnNames.TIMESTAMP])

    return log_df.reset_index(drop=True)


def event_log_formatter(
    event_log: pd.DataFrame,
    column_mapping: StandardColumnMapping,
    date_format: str | None = None,
    *,
    dayfirst: bool = False,
) -> pd.DataFrame:
    """
    Format an event log into a pandas DataFrame with standardized column names
    and return an explicit interval log with instance IDs assigned.

    Handles four types of event logs:

    1. Atomic logs (no lifecycle, no start_timestamp, no instance):
       - Each row is an instantaneous event
       - Duplicates each row with start and complete events (same timestamp)
       - Matches pairs to assign instance IDs

    2. Derivable interval logs (has lifecycle, no instance):
       - Already has start/complete events
       - Uses matching to assign instance IDs to start/complete pairs

    3. Production-style logs (has start_timestamp, no lifecycle):
       - Each row has start_timestamp and timestamp (end)
       - Splits into start and complete events
       - Matches pairs to assign instance IDs

    4. Explicit interval logs (has lifecycle AND instance):
       - Already has all required information
       - Only renames columns and converts types

    Args:
        event_log: The event log to format.
        column_mapping: The column mapping to use.
        date_format: The datetime format to use when parsing timestamp columns.
                    Can be a specific format string (e.g., "%d-%m-%Y %H:%M:%S"),
                    "ISO8601" for ISO8601 format, "mixed" for automatic inference,
                    or None to use pandas default parsing.
        dayfirst: Whether to interpret the first value in an ambiguous date
                 (e.g., 01/05/09) as the day (True) or month (False).
                 Only used when date_format is None or "mixed".

    Returns:
        pd.DataFrame: An explicit interval log with instance IDs and lifecycle transitions.

    """
    event_log = event_log.copy()

    # Standardize columns and convert types
    standard_named_log = _standardize_columns(event_log, column_mapping)
    _convert_standard_types(standard_named_log)

    # Detect log type and process accordingly
    log_type = _detect_log_type(column_mapping)

    if log_type == EventLogType.EXPLICIT_INTERVAL:
        return _process_explicit_interval_log(standard_named_log, date_format, dayfirst=dayfirst)

    if log_type == EventLogType.DERIVABLE_INTERVAL:
        return _process_derivable_interval_log(standard_named_log, date_format, dayfirst=dayfirst)

    if log_type == EventLogType.PRODUCTION_STYLE:
        return _process_production_style_log(standard_named_log, date_format, dayfirst=dayfirst)

    return _process_atomic_log(standard_named_log, date_format, dayfirst=dayfirst)
