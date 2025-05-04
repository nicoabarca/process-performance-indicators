import pandas as pd

from process_performance_indicators.constants import LifecycleTransitionType, StandardColumnNames
from process_performance_indicators.exceptions import (
    ActivityNameNotFoundError,
    CaseIdNotFoundError,
    NoCompleteEventFoundError,
    NoStartEventFoundError,
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
    Returns the first start event of an activity instance in a case.
    """
    instances = inst(event_log, case_id, activity_name)
    first_occurrence_index = instances[
        (instances[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.START)
    ].index.min()

    if first_occurrence_index.isna():
        raise NoStartEventFoundError(f"No start event found for activity {activity_name} in case {case_id}.")

    return instances.iloc[first_occurrence_index]


def fi_c(event_log: pd.DataFrame, case_id: str, activity_name: str) -> pd.DataFrame:
    """
    Returns the first complete event of an activity instance in a case.
    """
    instances = inst(event_log, case_id, activity_name)
    first_occurrence_index = instances[
        (instances[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.COMPLETE)
    ].index.min()

    if first_occurrence_index.isna():
        raise NoCompleteEventFoundError(f"No complete event found for activity {activity_name} in case {case_id}.")

    return instances.iloc[first_occurrence_index]


def fi(event_log: pd.DataFrame, case_id: str, activity_name: str) -> pd.DataFrame:
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
