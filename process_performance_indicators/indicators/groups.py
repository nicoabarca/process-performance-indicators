import pandas as pd

import process_performance_indicators.helpers.cases as cases_helpers


def activity_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    Counts the number of activities in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list of case ids.

    Returns:
        int: The number of activities.

    """
    count = 0
    for case_id in case_ids:
        count += len(cases_helpers.act(event_log, case_id))
    return count
