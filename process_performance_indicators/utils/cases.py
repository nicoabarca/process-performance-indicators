import pandas as pd

from process_performance_indicators.constants import LifecycleTransitionType, StandardColumnNames
from process_performance_indicators.exceptions import (
    ColumnNotFoundError,
    NoCompleteEventFoundError,
    NoStartEventFoundError,
)


def events(event_log: pd.DataFrame, case_id: str) -> pd.DataFrame:
    """
    Get the events dataframe of a case.
    """
    _is_case_id_valid(event_log, case_id)

    return event_log[event_log[StandardColumnNames.CASE_ID] == case_id]


def act(event_log: pd.DataFrame, case_id: str) -> set[str]:
    """
    Get the activities names set of a case.
    """
    _is_case_id_valid(event_log, case_id)
    activities = event_log[event_log[StandardColumnNames.CASE_ID] == case_id][StandardColumnNames.ACTIVITY].unique()
    return set(activities)


def res(event_log: pd.DataFrame, case_id: str) -> set[str]:
    """
    Get the resources names set of a case.
    """
    _is_case_id_valid(event_log, case_id)
    if StandardColumnNames.ORG_RESOURCE not in event_log.columns:
        error_message = "RESOURCE column not found in event log. Check your event log for possible columns."
        raise ColumnNotFoundError(error_message)

    resources = event_log[event_log[StandardColumnNames.CASE_ID] == case_id][StandardColumnNames.ORG_RESOURCE].unique()
    return set(resources)


def hres(event_log: pd.DataFrame, case_id: str) -> set[str]:
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


def role(event_log: pd.DataFrame, case_id: str) -> set[str]:
    """
    Get the roles names set of a case.
    """
    _is_case_id_valid(event_log, case_id)
    if StandardColumnNames.ROLE not in event_log.columns:
        error_message = "ROLE column not found in event log. Check your event log for possible columns."
        raise ColumnNotFoundError(error_message)

    roles = event_log[event_log[StandardColumnNames.CASE_ID] == case_id][StandardColumnNames.ROLE].unique()
    return set(roles)


def inst(event_log: pd.DataFrame, case_id: str) -> set[str]:
    """
    Get the instances ids set of a case.
    """
    _is_case_id_valid(event_log, case_id)
    if StandardColumnNames.INSTANCE not in event_log.columns:
        error_message = "INSTANCE column not found in event log. Check your event log for possible columns."
        raise ColumnNotFoundError(error_message)

    instances = event_log[event_log[StandardColumnNames.CASE_ID] == case_id][StandardColumnNames.INSTANCE].unique()
    return set(instances)


def strin(event_log: pd.DataFrame, case_id: str) -> set[str]:
    """
    Get the instance(s) that start first in the given case.
    """
    _is_case_id_valid(event_log, case_id)

    case_events = event_log[event_log[StandardColumnNames.CASE_ID] == case_id]
    start_events = case_events[case_events[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.START]

    min_start_time = start_events[StandardColumnNames.TIMESTAMP].min()
    earliest_instances = start_events[start_events[StandardColumnNames.TIMESTAMP] == min_start_time][
        StandardColumnNames.INSTANCE
    ].unique()
    return set(earliest_instances.tolist())


def endin(event_log: pd.DataFrame, case_id: str) -> set[str]:
    """
    Get the instance(s) that end last in the given case.
    """
    _is_case_id_valid(event_log, case_id)

    case_events = event_log[event_log[StandardColumnNames.CASE_ID] == case_id]
    complete_events = case_events[
        case_events[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.COMPLETE
    ]

    max_complete_time = complete_events[StandardColumnNames.TIMESTAMP].max()
    latest_instances = complete_events[complete_events[StandardColumnNames.TIMESTAMP] == max_complete_time][
        StandardColumnNames.INSTANCE
    ].unique()

    return set(latest_instances.tolist())


def startt(event_log: pd.DataFrame, case_id: str) -> pd.Timestamp:
    """
    Get the start timestamp of a case start activity instances
    """
    _is_case_id_valid(event_log, case_id)
    earliest_instances_events = strin(event_log, case_id)
    if earliest_instances_events.empty:
        raise NoStartEventFoundError(f"No start event found for case {case_id}.")

    return earliest_instances_events[StandardColumnNames.TIMESTAMP].min()


def endt(event_log: pd.DataFrame, case_id: str) -> pd.Timestamp:
    """
    Get the end timestamp of a case end activity instances
    """
    _is_case_id_valid(event_log, case_id)
    latest_instances_events = endin(event_log, case_id)
    if latest_instances_events.empty:
        raise NoCompleteEventFoundError(f"No complete event found for case {case_id}.")
    return latest_instances_events[StandardColumnNames.TIMESTAMP].max()


def _is_case_id_valid(event_log: pd.DataFrame, case_id: str) -> None:
    """
    Raise an error if the case id is not found in the event log.

    Args:
        event_log: The event log.
        case_id: The case id of the corresponding case.

    Raises:
        ValueError: If the case id is not found in the event log.

    """
    if case_id == "" or case_id is None:
        raise ValueError("case_id is empty. Please provide a valid case id.")
    if case_id not in list(event_log[StandardColumnNames.CASE_ID].unique()):
        raise ValueError(
            f"CASE_ID = '{case_id}' not found in event log. Check your event log CASE_ID column for possible values."
        )
