"""
Module containing all performance indicators related to activity granularity.

The performance indicators are defined as functions that take an event log and an activity name as input and return a value.
"""

import pandas as pd

import process_performance_indicators.helpers.activities as activities_helpers
from process_performance_indicators.constants import StandardColumnNames
from process_performance_indicators.exceptions import ActivityNameNotFoundError


def activity_instance_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    Counts the number of times an activity occurs in an event log.

    Args:
        event_log (pd.DataFrame): The event log.
        activity_name (str): The name of the activity.

    Returns:
        int: The number of times the activity occurs in the event log.

    """
    _is_activity_name_valid(event_log, activity_name)
    return len(activities_helpers.inst(event_log, activity_name))


def human_resource_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    Counts the number of human resources that execute an activity.

    Args:
        event_log (pd.DataFrame): The event log.
        activity_name (str): The name of the activity.

    Returns:
        int: The number of human resources that execute the activity.

    """
    _is_activity_name_valid(event_log, activity_name)
    return len(activities_helpers.hres(event_log, activity_name))


def _is_activity_name_valid(event_log: pd.DataFrame, activity_name: str) -> None:
    """
    Checks if an activity name is valid.
    """
    if activity_name not in event_log[StandardColumnNames.ACTIVITY].unique():
        raise ActivityNameNotFoundError(f"Activity name {activity_name} not found in event log.")
