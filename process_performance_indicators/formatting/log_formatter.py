import uuid

import pandas as pd

from process_performance_indicators.formatting.column_mapping import (
    StandardColumnMapping,
    convert_to_standard_mapping,
    validate_column_mapping,
)
from process_performance_indicators.formatting.constants import (
    UUID_LENGTH,
    EventLogClassification,
    StandardColumnNames,
)


def event_log_formatter(
    event_log: pd.DataFrame, column_mapping: dict[str, str] | StandardColumnMapping
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

    # If start timestamp is not present, return the standard named log
    if StandardColumnNames.START_TIMESTAMP not in standard_named_log.columns:
        return standard_named_log

    # Convert case id to string
    standard_named_log[StandardColumnNames.CASE_ID] = standard_named_log[
        StandardColumnNames.CASE_ID
    ].astype(str)

    # Add missing columns
    if StandardColumnNames.INSTANCE not in standard_named_log.columns:
        standard_named_log[StandardColumnNames.INSTANCE] = [
            str(uuid.uuid4())[:UUID_LENGTH] for _ in range(len(standard_named_log))
        ]

    # Convert timestamp columns to datetime
    standard_named_log[StandardColumnNames.TIMESTAMP] = pd.to_datetime(
        standard_named_log[StandardColumnNames.TIMESTAMP], utc=True
    )
    standard_named_log[StandardColumnNames.START_TIMESTAMP] = pd.to_datetime(
        standard_named_log[StandardColumnNames.START_TIMESTAMP], utc=True
    )

    # Create a copy of the log for start events
    start_events_log = standard_named_log.copy()
    start_events_log[StandardColumnNames.TIMESTAMP] = start_events_log[
        StandardColumnNames.START_TIMESTAMP
    ]

    # Drop the start timestamp from both logs
    if StandardColumnNames.START_TIMESTAMP in standard_named_log.columns:
        standard_named_log = standard_named_log.drop(columns=[StandardColumnNames.START_TIMESTAMP])
        start_events_log = start_events_log.drop(columns=[StandardColumnNames.START_TIMESTAMP])

    # Add lifecycle transition column
    standard_named_log[StandardColumnNames.LIFECYCLE_TRANSITION] = "complete"
    start_events_log[StandardColumnNames.LIFECYCLE_TRANSITION] = "start"

    # Combine the start and complete events
    combined_df = pd.concat([start_events_log, standard_named_log], ignore_index=True)
    combined_df = combined_df.sort_values(
        by=[StandardColumnNames.CASE_ID, StandardColumnNames.TIMESTAMP]
    )

    return combined_df.reset_index(drop=True)


def _event_log_classifier(event_log: pd.DataFrame) -> EventLogClassification:
    """
    Classify the event log into one of the following categories based on its columns:

    - ATOMIC: Only has case ID, activity name, and timestamp columns
      Format: case | activity | timestamp

    - DERIVABLE: Has either lifecycle transition or start timestamp columns
      Format: case | activity | timestamp | lifecycle_transition

    - ACTIVITY_LOG: Has timestamp and start_timestamp columns
      Format: case | activity | timestamp | start_timestamp

    - EXPLICIT: Has both instance ID and lifecycle transition columns
      Format: case | activity | timestamp | instance_id | lifecycle_transition

    Args:
        event_log: The event log to classify

    Returns:
        EventLogClassification: The classification of the event log

    """
    columns = set(event_log.columns)

    # Define classification rules with their required columns
    classification_rules = [
        (
            EventLogClassification.EXPLICIT,
            {StandardColumnNames.INSTANCE, StandardColumnNames.LIFECYCLE_TRANSITION},
        ),
        (
            EventLogClassification.DERIVABLE,
            {StandardColumnNames.START_TIMESTAMP} | {StandardColumnNames.LIFECYCLE_TRANSITION},
        ),
        (
            EventLogClassification.ACTIVITY_LOG,
            {StandardColumnNames.TIMESTAMP, StandardColumnNames.START_TIMESTAMP},
        ),
        (EventLogClassification.ATOMIC, set()),  # Default case
    ]

    # Return first matching classification
    for classification, required_columns in classification_rules:
        if required_columns.issubset(columns):
            return classification

    return EventLogClassification.ATOMIC
