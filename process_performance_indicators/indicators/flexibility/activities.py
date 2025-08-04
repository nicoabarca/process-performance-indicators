import pandas as pd

import process_performance_indicators.indicators.general.activities as general_activities_indicators
import process_performance_indicators.utils.activities as activities_utils
from process_performance_indicators.constants import StandardColumnNames
from process_performance_indicators.utils.safe_division import safe_divide


def activity_instance_and_human_resource_count_ratio(event_log: pd.DataFrame, activity_name: str) -> float:
    """
    The ratio between the number of times that a specific activity has been instantiated in the event log, and the number of human resources that are involved in the execution of the activity.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    """
    numerator = general_activities_indicators.activity_instance_count(event_log, activity_name)
    denominator = general_activities_indicators.human_resource_count(event_log, activity_name)
    return safe_divide(numerator, denominator)


def client_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    The number of distinct clients associated with cases where the activity is instantiated.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    """
    activity_events = event_log[event_log[StandardColumnNames.ACTIVITY] == activity_name]
    case_ids = set(activity_events[StandardColumnNames.CASE_ID].unique())
    cases_events = event_log[event_log[StandardColumnNames.CASE_ID].isin(case_ids)]
    return len(set(cases_events[StandardColumnNames.CLIENT].unique()))


def directly_follows_relations_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    The number of activities that have been instantiated directly after the activity of interest in the event log.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def human_resource_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    The number of human resources that are involved in the execution of the activity.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    """
    return len(activities_utils.hres(event_log, activity_name))
