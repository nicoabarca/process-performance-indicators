import pandas as pd

import process_performance_indicators.helpers.cases as cases_helpers
import process_performance_indicators.time.instances as instances_time_indicators


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


def lead_time_deviation_from_deadline(event_log: pd.DataFrame, case_id: str, deadline: pd.Timestamp) -> pd.Timedelta:
    """
    Calculates the lead time deviation of a case from a deadline.

    Args:
        event_log: The event log.
        case_id: The case id.
        deadline: The deadline timestamp.

    Returns:
        pd.Timedelta: The lead time deviation of the case.

    """
    # TODO: check the return value of this function Timestamp of Timedelta
    return deadline - lead_time(event_log, case_id)


def lead_time_deviation_from_expectation(
    event_log: pd.DataFrame, case_id: str, expectation: pd.Timedelta
) -> pd.Timedelta:
    """
    Calculates the lead time deviation of a case from an expectation.

    Args:
        event_log: The event log.
        case_id: The case id.
        expectation: The expectation.

    Returns:
        pd.Timedelta: The lead time deviation of the case from the expectation.

    """
    return expectation - lead_time(event_log, case_id)


def service_time(event_log: pd.DataFrame, case_id: str) -> pd.Timedelta:
    """
    Calculate the service time of all activity instances of a case.

    Args:
        event_log: The event log.
        case_id: The case id.

    Returns:
        pd.Timedelta: The service time of the case.

    """
    sum_of_service_times_in_seconds = sum(
        instances_time_indicators.service_time(event_log, instance_id).total_seconds()
        for instance_id in cases_helpers.inst(event_log, case_id)
    )
    return pd.Timedelta(seconds=sum_of_service_times_in_seconds)
