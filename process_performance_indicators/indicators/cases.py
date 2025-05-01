"""
Module containing all performance indicators related to case granularity.

The performance indicators are defined as functions that take an event log and a case id as input and return a value.
"""

import pandas as pd

import process_performance_indicators.helpers.cases as cases_helpers
from process_performance_indicators.constants import StandardColumnNames
from process_performance_indicators.exceptions import CaseIdNotFoundError


def activity_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Counts the number of activities in the event log.

    Args:
        event_log (pd.DataFrame): The event log.
        case_id (str): The case id.

    Returns:
        int: The number of activities.

    """
    return len(cases_helpers.act(event_log, case_id))


def activity_instance_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Counts the number of activity instances in the event log.

    Args:
        event_log (pd.DataFrame): The event log.
        case_id (str): The case id.

    Returns:
        int: The number of activity instances.

    """
    _is_case_id_in_event_log(event_log, case_id)

    return len(cases_helpers.inst(event_log, case_id))


def human_resource_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Counts the number of human resources in the event log.

    Args:
        event_log (pd.DataFrame): The event log.
        case_id (str): The case id.

    Returns:
        int: The number of human resources.

    """
    _is_case_id_in_event_log(event_log, case_id)
    return len(cases_helpers.hres(event_log, case_id))


def resource_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Counts the number of resources in the event log.

    Args:
        event_log (pd.DataFrame): The event log.
        case_id (str): The case id.

    Returns:
        int: The number of resources.

    """
    _is_case_id_in_event_log(event_log, case_id)
    return len(cases_helpers.res(event_log, case_id))


def role_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Counts the number of roles in the event log.

    Args:
        event_log (pd.DataFrame): The event log.
        case_id (str): The case id.

    Returns:
        int: The number of roles.

    """
    _is_case_id_in_event_log(event_log, case_id)
    return len(cases_helpers.role(event_log, case_id))


def _is_case_id_in_event_log(event_log: pd.DataFrame, case_id: str) -> None:
    """
    Checks if the case id is in the event log.

    Args:
        event_log (pd.DataFrame): The event log.
        case_id (str): The case id.

    Raises:
        CaseIdNotFoundError: If the case id is not in the event log.

    """
    if case_id not in event_log[StandardColumnNames.CASE_ID].unique():
        raise CaseIdNotFoundError(f"Case id '{case_id}' not found in event log.")
