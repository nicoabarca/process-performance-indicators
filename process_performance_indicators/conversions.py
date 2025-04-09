import pandas as pd

from process_performance_indicators.constants import StandardColumnNames
from process_performance_indicators.match import match_all


def convert_to_derivable_interval_log(event_log: pd.DataFrame) -> pd.DataFrame:
    """
    Convert an event log into a derivable log.

    Args:
        event_log: The event log to convert.

    Returns:
        The converted event log.

    """
    if StandardColumnNames.LIFECYCLE_TRANSITION in event_log.columns:
        error_message = (
            "Event log is not an atomic log and can't be converted derivable interval log"
        )
        raise ValueError(error_message)

    grouped_by_case_id_log = event_log.groupby(StandardColumnNames.CASE_ID)

    for case_id, case_log in grouped_by_case_id_log:
        print("CASE_ID", case_id)
        print("\n")
        case_matched_events = match_all(case_log)
        breakpoint()


def convert_to_explicit_interval_log(event_log: pd.DataFrame) -> pd.DataFrame:
    """
    Convert an event log into an explicit interval log.

    Args:
        event_log: The event log to convert.

    Returns:
        The converted event log.

    """
    grouped_by_case_id_log = event_log.groupby(StandardColumnNames.CASE_ID)

    for case_id, case_log in grouped_by_case_id_log:
        case_matched_events = match_all(case_log)
        print("CASE_ID", case_id)
        print("\n")
        print("case_matched_events", case_matched_events)
        breakpoint()
