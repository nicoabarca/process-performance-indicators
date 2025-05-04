import pandas as pd

import process_performance_indicators.general.groups as general_groups_indicators
import process_performance_indicators.helpers.cases as cases_helpers
import process_performance_indicators.time.cases as time_cases_indicators


def case_count_lead_time_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    Calculate the case count lead time ratio of a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        float: The case count lead time ratio of the group of cases.

    """
    # INFO: lead_time is converted to total seconds a float for division
    case_count = general_groups_indicators.case_count(event_log, case_ids)

    return case_count / lead_time(event_log, case_ids).total_seconds()


def case_count_where_lead_time_over_value(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], value: pd.Timedelta
) -> int:
    """
    Calculate the number of cases in a group of cases where the lead time is over a given value.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        value: The threshold value.

    Returns:
        int: The number of cases in a group of cases where the lead time is over a given value.

    """
    return len([case_id for case_id in case_ids if time_cases_indicators.lead_time(event_log, case_id) > value])


def case_percentage_where_lead_time_over_value(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], value: pd.Timedelta
) -> float:
    """
    Calculate the percentage of cases in a group of cases where the lead time is over a given value.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        value: The threshold value.

    Returns:
        float: The percentage of cases in a group of cases where the lead time is over a given value.

    """
    return case_count_where_lead_time_over_value(event_log, case_ids, value) / general_groups_indicators.case_count(
        event_log, case_ids
    )


def case_percentage_with_missed_deadline(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], value: pd.Timestamp
) -> float:
    """
    Calculate the percentage of cases in a group of cases where the end time is over a given value (deadline).

    Args:
        event_log: The event log.
        case_ids: The case ids.
        value: The deadline value.

    Returns:
        float: The percentage of cases in a group of cases where the end time is over a given value (deadline).

    """
    cases_over_deadline = [case_id for case_id in case_ids if cases_helpers.endt(event_log, case_id) > value]
    return len(cases_over_deadline) / general_groups_indicators.case_count(event_log, case_ids)


def lead_time(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> pd.Timedelta:
    """
    Calculate the lead time of a group of cases based on max end timestamp value and min start timestamp value.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        pd.Timedelta: The lead time of the group of cases.

    """
    group_end_timestamps = [cases_helpers.endt(event_log, case_id) for case_id in case_ids]
    group_start_timestamps = [cases_helpers.startt(event_log, case_id) for case_id in case_ids]

    max_end_timestamp = max(group_end_timestamps)
    min_start_timestamp = min(group_start_timestamps)

    return max_end_timestamp - min_start_timestamp


def expected_lead_time(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> pd.Timedelta:
    """
    Calculate the expected lead time of a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        pd.Timedelta: The expected lead time of the group of cases.

    """
    group_total_lead_times_in_seconds = sum(
        time_cases_indicators.lead_time(event_log, case_id).total_seconds() for case_id in case_ids
    )
    case_count = general_groups_indicators.case_count(event_log, case_ids)
    expected_lead_time_in_seconds = group_total_lead_times_in_seconds / case_count
    return pd.Timedelta(seconds=expected_lead_time_in_seconds)


def lead_time_case_count_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> pd.Timedelta:
    """
    Calculate the lead time case count ratio of a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        float: The lead time case count ratio of the group of cases.

    """
    group_lead_time_in_seconds = lead_time(event_log, case_ids).total_seconds()
    case_count = general_groups_indicators.case_count(event_log, case_ids)
    ratio = group_lead_time_in_seconds / case_count
    return pd.Timedelta(seconds=ratio)


def expected_lead_time_deviation_from_deadline(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], deadline: pd.Timestamp
) -> pd.Timedelta:
    """
    Calculate the expected lead time deviation from deadline of a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        deadline: The deadline date timestamp.

    Returns:
        pd.Timedelta: The expected lead time deviation from deadline of the group of cases.

    """
    cases_lead_time_deviation_from_deadline = sum(
        time_cases_indicators.lead_time_deviation_from_deadline(event_log, case_id, deadline).total_seconds()
        for case_id in case_ids
    )
    group_case_count = general_groups_indicators.case_count(event_log, case_ids)
    expected_lead_time_deviation_from_deadline_in_seconds = cases_lead_time_deviation_from_deadline / group_case_count
    return pd.Timedelta(seconds=expected_lead_time_deviation_from_deadline_in_seconds)


def expected_lead_time_deviation_from_expectation(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], expectation: pd.Timedelta
) -> pd.Timedelta:
    """
    Calculate the expected lead time deviation from expectation of a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        expectation: The expectation.

    Returns:
        pd.Timedelta: The expected lead time deviation from expectation of the group of cases.

    """
    cases_lead_time_deviation_from_expectation = sum(
        time_cases_indicators.lead_time_deviation_from_expectation(event_log, case_id, expectation).total_seconds()
        for case_id in case_ids
    )
    group_case_count = general_groups_indicators.case_count(event_log, case_ids)
    expected_lead_time_deviation_from_expectation_in_seconds = (
        cases_lead_time_deviation_from_expectation / group_case_count
    )
    return pd.Timedelta(seconds=expected_lead_time_deviation_from_expectation_in_seconds)


def service_time(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> pd.Timedelta:
    """
    Calculate the service time of a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        pd.Timedelta: The service time of the group of cases.

    """
    sum_of_service_times_in_seconds = sum(
        time_cases_indicators.service_time(event_log, case_id).total_seconds() for case_id in case_ids
    )
    return pd.Timedelta(seconds=sum_of_service_times_in_seconds)


def expected_service_time(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> pd.Timedelta:
    """
    Calculate the expected service time of a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        pd.Timedelta: The expected service time of the group of cases.

    """
    group_service_time_in_seconds = service_time(event_log, case_ids).total_seconds()
    case_count = general_groups_indicators.case_count(event_log, case_ids)
    expected_service_time_in_seconds = group_service_time_in_seconds / case_count
    return pd.Timedelta(seconds=expected_service_time_in_seconds)


def service_and_lead_time_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    Calculate the service and lead time ratio of a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        float: The service and lead time ratio of the group of cases.

    Raises:
        ValueError: If case_ids is empty or if lead time is zero.

    """
    # TODO: fix index 0 error in future
    if not case_ids:
        raise ValueError("case_ids cannot be empty")

    service_time_seconds = service_time(event_log, case_ids).total_seconds()
    lead_time_seconds = lead_time(event_log, case_ids).total_seconds()

    return service_time_seconds / lead_time_seconds


def expected_service_and_lead_time_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    Calculate the expected service and lead time ratio of a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        float: The expected service and lead time ratio of the group of cases.

    Raises:
        ValueError: If case_ids is empty or if total lead time is zero.

    """
    # TODO: fix index 0 error in future
    if not case_ids:
        raise ValueError("case_ids cannot be empty")

    group_service_time_in_seconds = service_time(event_log, case_ids).total_seconds()
    group_total_lead_time_in_seconds = sum(
        time_cases_indicators.lead_time(event_log, case_id).total_seconds() for case_id in case_ids
    )
    return group_service_time_in_seconds / group_total_lead_time_in_seconds
