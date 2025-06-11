import pandas as pd

import process_performance_indicators.general.cases as cases_general_indicators
import process_performance_indicators.utils.cases as cases_helpers
from process_performance_indicators.constants import StandardColumnNames


def activity_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    Counts the number of different activities for each case in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list or set of case ids.

    Returns:
        int: The number of activities.

    """
    _is_case_ids_empty(case_ids)
    count = 0
    for case_id in case_ids:
        count += len(cases_helpers.act(event_log, case_id))
    return count


def expected_activity_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected number of different activities for each case in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list or set of case ids.

    Returns:
        int | float: The expected number of activities.

    """
    _is_case_ids_empty(case_ids)
    count = 0
    for case_id in case_ids:
        count += len(cases_helpers.act(event_log, case_id))
    return count / case_count(event_log, case_ids)


def activity_instance_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    Counts the number of activity instances for each case in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list or set of case ids.

    Returns:
        int: The number of activity instances.

    """
    _is_case_ids_empty(case_ids)
    count = 0
    for case_id in case_ids:
        count += cases_general_indicators.activity_instance_count(event_log, case_id)
    return count


def expected_activity_instance_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected number of activity instances for each case in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list or set of case ids.

    Returns:
        int | float: The expected number of activity instances.

    """
    _is_case_ids_empty(case_ids)
    cases_activity_instance_count = 0
    for case_id in case_ids:
        cases_activity_instance_count += cases_general_indicators.activity_instance_count(event_log, case_id)
    return cases_activity_instance_count / case_count(event_log, case_ids)


def case_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    Counts the number of cases in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list or set of case ids.

    Returns:
        int: The number of cases.

    """
    _is_case_ids_empty(case_ids)
    event_log_unique_case_ids = set(event_log[StandardColumnNames.CASE_ID].unique())
    case_ids = set(case_ids)  # sanity check to ensure no duplicates if input is a list
    return len(case_ids.intersection(event_log_unique_case_ids))


def human_resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    Counts the number of human resources in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list or set of case ids.

    Returns:
        int: The number of human resources.

    """
    _is_case_ids_empty(case_ids)
    count = 0
    for case_id in case_ids:
        count += len(cases_helpers.hres(event_log, case_id))
    return count


def expected_human_resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected number of human resources in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list or set of case ids.

    Returns:
        int | float: The expected number of human resources.

    """
    _is_case_ids_empty(case_ids)
    numerator = 0
    for case_id in case_ids:
        numerator += cases_general_indicators.human_resource_count(event_log, case_id)
    return numerator / case_count(event_log, case_ids)


def resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    Counts the number of resources in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list or set of case ids.

    Returns:
        int: The number of resources.

    """
    _is_case_ids_empty(case_ids)
    count = 0
    for case_id in case_ids:
        count += len(cases_helpers.res(event_log, case_id))
    return count


def expected_resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected number of resources in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list or set of case ids.

    Returns:
        int | float: The expected number of resources.

    """
    _is_case_ids_empty(case_ids)
    numerator = 0
    for case_id in case_ids:
        numerator += cases_general_indicators.resource_count(event_log, case_id)
    return numerator / case_count(event_log, case_ids)


def role_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    Counts the number of roles in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list or set of case ids.

    Returns:
        int: The number of roles.

    """
    _is_case_ids_empty(case_ids)
    count = 0
    for case_id in case_ids:
        count += len(cases_helpers.role(event_log, case_id))
    return count


def expected_role_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected number of roles in the event log for a given list or set of case ids.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The list or set of case ids.

    Returns:
        int | float: The expected number of roles.

    """
    _is_case_ids_empty(case_ids)
    numerator = 0
    for case_id in case_ids:
        numerator += cases_general_indicators.role_count(event_log, case_id)
    return numerator / case_count(event_log, case_ids)


def _is_case_ids_empty(case_ids: list[str] | set[str]) -> None:
    """
    Raises a ValueError if the case ids are empty.
    """
    if len(case_ids) == 0:
        raise ValueError("case_ids is empty. Please provide a valid list of case ids.")
