import uuid

import pandas as pd

from process_performance_indicators.column_mapping import (
    StandardColumnMapping,
    convert_to_standard_mapping,
    validate_column_mapping,
)
from process_performance_indicators.constants import EventLogClassification, StandardColumnNames


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
    standard_mapping = convert_to_standard_mapping(column_mapping)
    validate_column_mapping(standard_mapping)
    inverted_mapping = {v: k for k, v in standard_mapping.items()}

    standard_named_log = event_log.rename(columns=inverted_mapping)

    start_timestamp_key = (
        StandardColumnNames.START_TIMESTAMP
        if StandardColumnNames.START_TIMESTAMP in standard_mapping
        else None
    )
    instance_key = (
        StandardColumnNames.INSTANCE if StandardColumnNames.INSTANCE in standard_mapping else None
    )

    if start_timestamp_key is None:
        return standard_named_log

    if instance_key is None:
        instance_key = StandardColumnNames.INSTANCE
        standard_named_log[instance_key] = [
            str(uuid.uuid4()) for _ in range(len(standard_named_log))
        ]

    start_events_log = standard_named_log.copy()
    start_events_log[StandardColumnNames.TIMESTAMP] = start_events_log[
        StandardColumnNames.START_TIMESTAMP
    ]

    if StandardColumnNames.START_TIMESTAMP in standard_named_log.columns:
        standard_named_log = standard_named_log.drop(columns=[StandardColumnNames.START_TIMESTAMP])
        start_events_log = start_events_log.drop(columns=[StandardColumnNames.START_TIMESTAMP])

    # standard_named_df[StandardColumnNames.LIFECYCLE_TRANSITION] = "complete"
    # start_events[StandardColumnNames.LIFECYCLE_TRANSITION] = "start"

    # Combine the start and complete events
    combined_df = pd.concat([start_events_log, standard_named_log], ignore_index=True)
    combined_df = combined_df.sort_values(
        by=[StandardColumnNames.CASE_ID, StandardColumnNames.TIMESTAMP]
    )

    print("types:")
    print(combined_df.dtypes)
    print("event log classification:")
    print(_event_log_classifier(combined_df))
    return combined_df.reset_index(drop=True)


def _event_log_classifier(event_log: pd.DataFrame) -> EventLogClassification:
    """
    Classify the event log into one of the following categories based on its columns:

    - ATOMIC: Only has case ID, activity name, and timestamp columns
      Format: case | activity | timestamp

    - DERIVABLE: Has either lifecycle transition or start timestamp columns
      Format: case | activity | timestamp | lifecycle_transition
      OR: case | activity | start_timestamp | complete_timestamp

    - EXPLICIT: Has both instance ID and lifecycle transition columns
      Format: case | activity | timestamp | instance_id | lifecycle_transition

    Args:
        event_log: The event log to classify

    Returns:
        EventLogClassification: The classification of the event log

    """
    columns = set(event_log.columns)
    if (
        StandardColumnNames.INSTANCE in columns
        and StandardColumnNames.LIFECYCLE_TRANSITION in columns
    ):
        return EventLogClassification.EXPLICIT

    if (
        StandardColumnNames.START_TIMESTAMP in columns
        or StandardColumnNames.LIFECYCLE_TRANSITION in columns
    ):
        return EventLogClassification.DERIVABLE

    return EventLogClassification.ATOMIC
