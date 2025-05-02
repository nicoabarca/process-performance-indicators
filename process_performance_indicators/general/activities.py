import pandas as pd

import process_performance_indicators.helpers.activities as activities_helpers


def activity_instance_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    Counts the number of times an activity instance occurs in an event log based on an activity name.

    Args:
        event_log (pd.DataFrame): The event log.
        activity_name (str): The name of the activity.

    Returns:
        int: The number of times the activity instance occurs in the event log.

    """
    return len(activities_helpers.inst(event_log, activity_name))


def human_resource_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    Counts the number of human resources in an event log based on an activity name.

    Args:
        event_log (pd.DataFrame): The event log.
        activity_name (str): The name of the activity.

    Returns:
        int: The number of human resources in the event log.

    """
    return len(activities_helpers.hres(event_log, activity_name))


def resource_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    Counts the number of resources in an event log based on an activity name.

    Args:
        event_log (pd.DataFrame): The event log.
        activity_name (str): The name of the activity.

    Returns:
        int: The number of resources in the event log.

    """
    return len(activities_helpers.res(event_log, activity_name))
