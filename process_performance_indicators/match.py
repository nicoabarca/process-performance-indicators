import pandas as pd
from constants import StandardColumnNames


def match(case_log: pd.DataFrame, complete_event: pd.Series) -> pd.DataFrame:
    """
    Transform an event log into an explicit interval event log

    Args:
        event_log: The event log to transform.

    Returns:
        The explicit interval event log.

    """
    if complete_event[StandardColumnNames.LIFECYCLE_TRANSITION] != "complete":
        raise ValueError("The provided event is not a complete event")

    # Extract relevant information from the complete event
    case_id = complete_event[StandardColumnNames.CASE_ID]
    activity = complete_event[StandardColumnNames.ACTIVITY]
    complete_timestamp = pd.to_datetime(complete_event[StandardColumnNames.TIMESTAMP])

    # Filter potential matching start events
    # Same case, same activity, lifecycle_transition is 'start', timestamp is earlier or equal
    potential_matches = case_log[
        (case_log[StandardColumnNames.CASE_ID] == case_id)
        & (case_log[StandardColumnNames.ACTIVITY] == activity)
        & (case_log[StandardColumnNames.LIFECYCLE_TRANSITION] == "start")
        & (pd.to_datetime(case_log[StandardColumnNames.TIMESTAMP]) <= complete_timestamp)
    ]

    if potential_matches.empty:
        # If no match found, return the complete event itself
        return complete_event

    # Find the most recent start event (highest timestamp)
    matching_start = potential_matches.loc[pd.to_datetime(potential_matches["timestamp"]).idxmax()]

    return matching_start


# TODO: Fix return type
def match_all(case_log: pd.DataFrame) -> list[tuple[str, str]]:
    """
    Match all complete events in the case log to their corresponding start events.

    Args:
        case_log: The event log to match.

    Returns:
        A list of tuples, where each tuple contains the case ID and the activity name of the start event.

    """
    matches = []
    complete_events = case_log[case_log[StandardColumnNames.LIFECYCLE_TRANSITION] == "complete"]
    for _, complete_event in complete_events.iterrows():
        start_event = match(case_log, complete_event)
        matches.append((start_event, complete_event))
    return matches


def compatible_start_events(case_log: pd.DataFrame, complete_event: pd.Series) -> list[pd.Series]:
    """
    Find all start events in the case log that are compatible with the complete event.

    Args:
        case_log: The event log to search.
        complete_event: The complete event to match.

    """
    case_id = complete_event[StandardColumnNames.CASE_ID]
    activity = complete_event[StandardColumnNames.ACTIVITY]
    complete_timestamp = pd.to_datetime(complete_event[StandardColumnNames.TIMESTAMP])

    potential_matches = case_log[
        (case_log[StandardColumnNames.CASE_ID] == case_id)
        & (case_log[StandardColumnNames.ACTIVITY] == activity)
        & (case_log[StandardColumnNames.LIFECYCLE_TRANSITION] == "start")
        & (pd.to_datetime(case_log[StandardColumnNames.TIMESTAMP]) <= complete_timestamp)
    ]
    potential_matches = potential_matches.sort_values(
        by=StandardColumnNames.TIMESTAMP, ascending=False
    )
