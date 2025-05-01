import pandas as pd

from process_performance_indicators.constants import StandardColumnNames
from process_performance_indicators.exceptions import ActivityNameNotFoundError, ColumnNotFoundError


def events(event_log: pd.DataFrame, activity_name: str) -> pd.DataFrame:
    """
    Get the events dataframe of an activity.
    """
    _is_activity_name_valid(event_log, activity_name)

    return event_log[event_log[StandardColumnNames.ACTIVITY] == activity_name]


def res(event_log: pd.DataFrame, activity_name: str) -> set:
    """
    Get the resources names set of an activity.
    """
    _is_activity_name_valid(event_log, activity_name)
    if StandardColumnNames.ORG_RESOURCE not in event_log.columns:
        error_message = (
            "RESOURCE column not found in event log. Check your event log for possible columns."
        )
        raise ColumnNotFoundError(error_message)

    resources = event_log[event_log[StandardColumnNames.ACTIVITY] == activity_name][
        StandardColumnNames.ORG_RESOURCE
    ].unique()
    return set(resources)


def hres(event_log: pd.DataFrame, activity_name: str) -> set:
    """
    Get the human resources names set of an activity.
    """
    _is_activity_name_valid(event_log, activity_name)
    if StandardColumnNames.HUMAN_RESOURCE not in event_log.columns:
        error_message = "HUMAN_RESOURCE column not found in event log. Check your event log for possible columns."
        raise ColumnNotFoundError(error_message)

    human_resources = event_log[event_log[StandardColumnNames.ACTIVITY] == activity_name][
        StandardColumnNames.HUMAN_RESOURCE
    ].unique()

    return set(human_resources)


def role(event_log: pd.DataFrame, activity_name: str) -> set:
    """
    Get the roles names set of an activity.
    """
    _is_activity_name_valid(event_log, activity_name)
    if StandardColumnNames.ROLE not in event_log.columns:
        error_message = (
            "ROLE column not found in event log. Check your event log for possible columns."
        )
        raise ColumnNotFoundError(error_message)

    roles = event_log[event_log[StandardColumnNames.ACTIVITY] == activity_name][
        StandardColumnNames.ROLE
    ].unique()

    return set(roles)


def inst(event_log: pd.DataFrame, activity_name: str) -> set:
    """
    Get the instances ids set of an activity.
    """
    _is_activity_name_valid(event_log, activity_name)
    if StandardColumnNames.INSTANCE not in event_log.columns:
        error_message = (
            "INSTANCE column not found in event log. Check your event log for possible columns."
        )
        raise ColumnNotFoundError(error_message)

    instances = event_log[event_log[StandardColumnNames.ACTIVITY] == activity_name][
        StandardColumnNames.INSTANCE
    ].unique()

    return set(instances)


def _is_activity_name_valid(event_log: pd.DataFrame, activity_name: str) -> None:
    """
    Check if the activity name is valid.
    """
    if activity_name not in event_log[StandardColumnNames.ACTIVITY].unique():
        raise ActivityNameNotFoundError(f"Activity name {activity_name} not found in event log.")
