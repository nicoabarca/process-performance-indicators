import pandas as pd

import process_performance_indicators.helpers.cases as cases_helpers


def automated_activity_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Counts the number of automated activities in a case.

    Args:
        event_log: The event log.
        case_id: The case id.

    Returns:
        int: The number of automated activities in the case.

    """


def lead_time(event_log: pd.DataFrame, case_id: str) -> pd.Timedelta:
    """
    Calculates the lead time of a case.

    Args:
        event_log: The event log.
        case_id: The case id.

    Returns:
        pd.Timedelta: The lead time of the case.

    """
    return cases_helpers.endt(event_log, case_id) - cases_helpers.startt(event_log, case_id)


def lead_time_deviation_from_deadline(
    event_log: pd.DataFrame, case_id: str, deadline: pd.Timestamp
) -> pd.Timedelta:
    """
    Calculates the lead time deviation of a case from a deadline.

    Args:
        event_log: The event log.
        case_id: The case id.
        deadline: The deadline timestamp.

    Returns:
        float: The lead time deviation of the case.

    """
    return deadline - lead_time(event_log, case_id)
