import pandas as pd

import process_performance_indicators.helpers.cases as cases_helpers


def activity_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Counts the number of activities in the event log of a given case based on id.

    Args:
        event_log (pd.DataFrame): The event log.
        case_id (str): The case id.

    Returns:
        int: The number of activities.

    """
    return len(cases_helpers.act(event_log, case_id))


def activity_instance_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Counts the number of activity instances in the event log of a given case based on id.

    Args:
        event_log (pd.DataFrame): The event log.
        case_id (str): The case id.

    Returns:
        int: The number of activity instances.

    """
    return len(cases_helpers.inst(event_log, case_id))


def human_resource_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Counts the number of human resources in the event log of a given case based on id.

    Args:
        event_log (pd.DataFrame): The event log.
        case_id (str): The case id.

    Returns:
        int: The number of human resources.

    """
    return len(cases_helpers.hres(event_log, case_id))


def resource_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Counts the number of resources in the event log of a given case based on id.

    Args:
        event_log (pd.DataFrame): The event log.
        case_id (str): The case id.

    Returns:
        int: The number of resources.

    """
    return len(cases_helpers.res(event_log, case_id))


def role_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Counts the number of roles in the event log of a given case based on id.

    Args:
        event_log (pd.DataFrame): The event log.
        case_id (str): The case id.

    Returns:
        int: The number of roles.

    """
    return len(cases_helpers.role(event_log, case_id))
