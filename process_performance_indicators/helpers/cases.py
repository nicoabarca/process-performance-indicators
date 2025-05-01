import pandas as pd

from process_performance_indicators.constants import LifecycleTransitionType, StandardColumnNames
from process_performance_indicators.exceptions import ColumnNotFoundError


def events(event_log: pd.DataFrame, case_id: str) -> pd.DataFrame:
    """
    Get the events dataframe of a case.
    """
    _is_case_id_valid(event_log, case_id)

    return event_log[event_log[StandardColumnNames.CASE_ID] == case_id]


def act(event_log: pd.DataFrame, case_id: str) -> set:
    """
    Get the activities names set of a case.
    """
    _is_case_id_valid(event_log, case_id)
    activities = event_log[event_log[StandardColumnNames.CASE_ID] == case_id][
        StandardColumnNames.ACTIVITY
    ].unique()
    return set(activities)


def res(event_log: pd.DataFrame, case_id: str) -> set:
    """
    Get the resources names set of a case.
    """
    _is_case_id_valid(event_log, case_id)
    if StandardColumnNames.ORG_RESOURCE not in event_log.columns:
        error_message = (
            "RESOURCE column not found in event log. Check your event log for possible columns."
        )
        raise ColumnNotFoundError(error_message)

    resources = event_log[event_log[StandardColumnNames.CASE_ID] == case_id][
        StandardColumnNames.ORG_RESOURCE
    ].unique()
    return set(resources)


def hres(event_log: pd.DataFrame, case_id: str) -> set:
    """
    Get the human resources names set of a case.
    """
    _is_case_id_valid(event_log, case_id)
    if StandardColumnNames.HUMAN_RESOURCE not in event_log.columns:
        error_message = "HUMAN_RESOURCE column not found in event log. Check your event log for possible columns."
        raise ColumnNotFoundError(error_message)

    human_resources = event_log[event_log[StandardColumnNames.CASE_ID] == case_id][
        StandardColumnNames.HUMAN_RESOURCE
    ].unique()
    return set(human_resources)


def role(event_log: pd.DataFrame, case_id: str) -> set:
    """
    Get the roles names set of a case.
    """
    _is_case_id_valid(event_log, case_id)
    if StandardColumnNames.ROLE not in event_log.columns:
        error_message = (
            "ROLE column not found in event log. Check your event log for possible columns."
        )
        raise ColumnNotFoundError(error_message)

    roles = event_log[event_log[StandardColumnNames.CASE_ID] == case_id][
        StandardColumnNames.ROLE
    ].unique()
    return set(roles)


def inst(event_log: pd.DataFrame, case_id: str) -> set:
    """
    Get the instances ids set of a case.
    """
    _is_case_id_valid(event_log, case_id)
    if StandardColumnNames.INSTANCE not in event_log.columns:
        error_message = (
            "INSTANCE column not found in event log. Check your event log for possible columns."
        )
        raise ColumnNotFoundError(error_message)

    instances = event_log[event_log[StandardColumnNames.CASE_ID] == case_id][
        StandardColumnNames.INSTANCE
    ].unique()
    return set(instances)


def strin(event_log: pd.DataFrame, case_id: str) -> pd.DataFrame:
    """
    Get the start activity instances of a case
    """
    _is_case_id_valid(event_log, case_id)
    return event_log[
        (event_log[StandardColumnNames.CASE_ID] == case_id)
        & (event_log[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.START)
    ]


def endin(event_log: pd.DataFrame, case_id: str) -> pd.DataFrame:
    """
    Get the end activity instances of a case
    """
    _is_case_id_valid(event_log, case_id)
    return event_log[
        (event_log[StandardColumnNames.CASE_ID] == case_id)
        & (event_log[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.COMPLETE)
    ]


def startt(event_log: pd.DataFrame, case_id: str) -> pd.DataFrame:
    """
    Get the start timestamp of a case start activity instances
    """
    _is_case_id_valid(event_log, case_id)
    start_activity_instances = strin(event_log, case_id)
    return start_activity_instances[StandardColumnNames.TIMESTAMP]


def endt(event_log: pd.DataFrame, case_id: str) -> pd.DataFrame:
    """
    Get the end timestamp of a case end activity instances
    """
    _is_case_id_valid(event_log, case_id)
    end_activity_instances = endin(event_log, case_id)
    return end_activity_instances[StandardColumnNames.TIMESTAMP]


def _is_case_id_valid(event_log: pd.DataFrame, case_id: str) -> None:
    """
    Raise an error if the case id is not found in the event log.

    Args:
        event_log: The event log.
        case_id: The case id of the corresponding case.

    Raises:
        ValueError: If the case id is not found in the event log.

    """
    if case_id not in event_log[StandardColumnNames.CASE_ID].unique():
        raise ValueError(
            f"CASE_ID = {case_id} not found in event log. Check your event log CASE_ID column for possible values."
        )
