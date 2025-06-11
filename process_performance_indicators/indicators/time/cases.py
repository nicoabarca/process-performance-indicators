import pandas as pd

import process_performance_indicators.time.instances as instances_time_indicators
import process_performance_indicators.utils.cases as cases_helpers
import process_performance_indicators.utils.instances as instances_helpers


def automated_activity_count(event_log: pd.DataFrame, case_id: str, automated_activities: list[str] | set[str]) -> int:
    """
    Counts the number of automated activities in a case.

    Args:
        event_log: The event log.
        case_id: The case id.
        automated_activities: The list or set of automated activities.

    Returns:
        int: The number of automated activities in the case.

    """
    automated_activities = set(automated_activities)
    case_activities = cases_helpers.act(event_log, case_id)
    return len(automated_activities.intersection(case_activities))


def automated_activity_instance_count(
    event_log: pd.DataFrame, case_id: str, automated_activities: list[str] | set[str]
) -> int:
    """
    Counts the number of automated activity instances in a case.

    Args:
        event_log: The event log.
        case_id: The case id.
        automated_activities: The list or set of automated activities.

    Returns:
        int: The number of automated activity instances in the case.

    """
    automated_activities = set(automated_activities)
    case_instances = cases_helpers.inst(event_log, case_id)
    instances_of_automated_activities = set()
    for instance in case_instances:
        if instances_helpers.act(event_log, instance) in automated_activities:
            instances_of_automated_activities.add(instance)
    return len(instances_of_automated_activities)


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


def service_and_lead_time_ratio(event_log: pd.DataFrame, case_id: str) -> float:
    """
    Calculate the service and lead time ratio of a case.

    Args:
        event_log: The event log.
        case_id: The case id.

    Returns:
        float: The service and lead time ratio of the case.

    """
    return service_time(event_log, case_id).total_seconds() / lead_time(event_log, case_id).total_seconds()
