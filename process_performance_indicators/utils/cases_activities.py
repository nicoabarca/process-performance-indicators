import pandas as pd

from process_performance_indicators.constants import LifecycleTransitionType, StandardColumnNames
from process_performance_indicators.exceptions import (
    ActivityNameNotFoundError,
    CaseIdNotFoundError,
)


def inst(event_log: pd.DataFrame, case_id: str, activity_name: str) -> pd.DataFrame:
    """
    Returns the instance of an activity in a case.
    """
    _is_case_id_activity_name_valid(event_log, case_id, activity_name)
    return event_log[
        (event_log[StandardColumnNames.CASE_ID] == case_id) & (event_log[StandardColumnNames.ACTIVITY] == activity_name)
    ]


def count(event_log: pd.DataFrame, case_id: str, activity_name: str) -> int:
    """
    Returns the number of times an activity occurs in a case.
    """
    return len(inst(event_log, case_id, activity_name))


def fi_s(event_log: pd.DataFrame, case_id: str, activity_name: str) -> pd.DataFrame:
    """
    Returns the first start events of an activity instance in a case.
    """
    instances = inst(event_log, case_id, activity_name)
    instances_start_events = instances[
        (instances[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.START)
    ]
    # Get the minimum timestamp from all start events
    min_timestamp = instances_start_events[StandardColumnNames.TIMESTAMP].min()
    # Get all events that have this minimum timestamp

    return instances_start_events[instances_start_events[StandardColumnNames.TIMESTAMP] == min_timestamp][
        StandardColumnNames.ACTIVITY
    ].tolist()


def fi_c(event_log: pd.DataFrame, case_id: str, activity_name: str) -> pd.DataFrame:
    """
    Returns the first complete event of an activity instance in a case.
    """
    instances = inst(event_log, case_id, activity_name)
    instances_complete_events = instances[
        (instances[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.COMPLETE)
    ]
    min_timestamp = instances_complete_events[StandardColumnNames.TIMESTAMP].min()
    return instances_complete_events[instances_complete_events[StandardColumnNames.TIMESTAMP] == min_timestamp][
        StandardColumnNames.ACTIVITY
    ].tolist()


def fi(event_log: pd.DataFrame, case_id: str, activity_name_1: str, activity_name_2: str) -> pd.DataFrame:
    activity_name_fi_s = fi_s(event_log, case_id, activity_name_1)
    raise NotImplementedError("First occurrence is not implemented yet.")


def _is_case_id_activity_name_valid(event_log: pd.DataFrame, case_id: str, activity_name: str) -> None:
    """
    Checks if the case_id and activity_name are valid.
    Raises an exception if they are not valid.
    """
    is_case_id_valid = case_id in event_log[StandardColumnNames.CASE_ID].unique()
    is_activity_name_valid = activity_name in event_log[StandardColumnNames.ACTIVITY].unique()

    if not is_case_id_valid:
        raise CaseIdNotFoundError(f"Case ID {case_id} not found in event log.")
    if not is_activity_name_valid:
        raise ActivityNameNotFoundError(f"Activity name {activity_name} not found in event log.")
