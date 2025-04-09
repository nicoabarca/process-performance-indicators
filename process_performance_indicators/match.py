import pandas as pd

from process_performance_indicators.constants import StandardColumnNames


# TODO: Fix return type
def match_all(case_log: pd.DataFrame) -> list[tuple[pd.Series, pd.Series]]:
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


def match(case_log: pd.DataFrame, complete_event: pd.Series) -> pd.Series:
    """
    Transform an event log into an explicit interval event log

    Args:
        case_log: The case log of the complete event to match.
        complete_event: The complete event to match

    Returns:
        The explicit interval event log.

    """
    if complete_event[StandardColumnNames.LIFECYCLE_TRANSITION] != "complete":
        error_message = "The provided event is not a complete event"
        raise ValueError(error_message)

    compatible_start_events = _compatible_start_events(case_log, complete_event)

    print("complete_event", complete_event.to_dict())
    print("compatible_start_events")
    for event in compatible_start_events:
        print(event)

    breakpoint()
    if len(compatible_start_events) == 0:
        return complete_event

    return compatible_start_events


def _compatible_start_events(case_log: pd.DataFrame, complete_event: pd.Series) -> list[dict]:
    """
    Find all start events in the case log that are compatible with the complete event.

    Args:
        case_log: The event log to search.
        complete_event: The complete event to match.

    """
    case_id = complete_event[StandardColumnNames.CASE_ID]
    activity = complete_event[StandardColumnNames.ACTIVITY]
    complete_timestamp = complete_event[StandardColumnNames.TIMESTAMP]

    potential_matches = case_log[
        (case_log[StandardColumnNames.CASE_ID] == case_id)
        & (case_log[StandardColumnNames.ACTIVITY] == activity)
        & (case_log[StandardColumnNames.LIFECYCLE_TRANSITION] == "start")
        & (case_log[StandardColumnNames.TIMESTAMP] <= complete_timestamp)
    ]
    return potential_matches.sort_values(by=StandardColumnNames.TIMESTAMP, ascending=False).to_dict(
        orient="records"
    )
