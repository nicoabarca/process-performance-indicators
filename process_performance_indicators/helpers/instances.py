import pandas as pd

from process_performance_indicators.constants import (
    LifecycleTransitionType,
    StandardColumnNames,
)
from process_performance_indicators.exceptions import (
    ColumnNotFoundError,
    InstanceIdNotFoundError,
)


def start(event_log: pd.DataFrame, instance_id: str) -> pd.DataFrame:  # ignore: A001
    """
    Get the start event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)
    complete_event = cpl(event_log, instance_id)

    return _match(event_log, complete_event)


def cpl(event_log: pd.DataFrame, instance_id: str) -> pd.DataFrame:
    """
    Get the complete event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)

    return event_log[
        (event_log[StandardColumnNames.INSTANCE] == instance_id)
        & (event_log[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.COMPLETE)
    ]


def stime(event_log: pd.DataFrame, instance_id: str) -> pd.DataFrame:
    """
    Get the start time of an event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)
    start_event = start(event_log, instance_id)
    return start_event[StandardColumnNames.TIMESTAMP].unique()[0]


def ctime(event_log: pd.DataFrame, instance_id: str) -> pd.Timestamp | str:
    """
    Get the complete time of an event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)
    complete_event = cpl(event_log, instance_id)
    return complete_event[StandardColumnNames.TIMESTAMP].unique()[0]


def case(event_log: pd.DataFrame, instance_id: str) -> str:
    """
    Get the case of a complete event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)
    complete_event = cpl(event_log, instance_id)
    return complete_event[StandardColumnNames.CASE_ID].unique()[0]


def act(event_log: pd.DataFrame, instance_id: str) -> str:
    """
    Get the activity of a complete event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)
    complete_event = cpl(event_log, instance_id)
    return complete_event[StandardColumnNames.ACTIVITY].unique()[0]


def res(event_log: pd.DataFrame, instance_id: str) -> str:
    """
    Get the resource of a complete event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)
    if StandardColumnNames.ORG_RESOURCE not in event_log.columns:
        error_message = "RESOURCE column not found in event log. Please ensure the event log contains the resource column."
        raise ColumnNotFoundError(error_message)

    complete_event = cpl(event_log, instance_id)
    return complete_event[StandardColumnNames.ORG_RESOURCE].unique()[0]


def hres(event_log: pd.DataFrame, instance_id: str) -> str:
    """
    Get the human resource of a complete event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)
    if StandardColumnNames.HUMAN_RESOURCE not in event_log.columns:
        error_message = "HUMAN_RESOURCE column not found in event log. Please ensure the event log contains the human resource column."
        raise ColumnNotFoundError(error_message)

    complete_event = cpl(event_log, instance_id)
    return complete_event[StandardColumnNames.HUMAN_RESOURCE].unique()[0]


def role(event_log: pd.DataFrame, instance_id: str) -> str:
    """
    Get the role of a complete event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)
    if StandardColumnNames.ROLE not in event_log.columns:
        error_message = "ROLE column not found in event log. Please ensure the event log contains the role column."
        raise ColumnNotFoundError(error_message)

    complete_event = cpl(event_log, instance_id)
    return complete_event[StandardColumnNames.ROLE].unique()[0]


def _is_instance_id_valid(event_log: pd.DataFrame, instance_id: str) -> None:
    """
    Check if the instance id is valid.

    Raises:
        InstanceIdNotFoundError: If the instance id is not found in the event log.

    """
    if instance_id not in event_log[StandardColumnNames.INSTANCE].unique():
        raise InstanceIdNotFoundError(f"Instance id {instance_id} not found in event log.")


# TODO: redo this function to use the paper defined match function
def _match(event_log: pd.DataFrame, complete_event: pd.DataFrame) -> pd.DataFrame:
    """
    Match the event log to the instance id.
    """
    complete_event_instance_id = complete_event[StandardColumnNames.INSTANCE].unique()[0]

    start_event = event_log[
        (event_log[StandardColumnNames.INSTANCE] == complete_event_instance_id)
        & (event_log[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.START)
    ]
    if start_event.empty:
        return complete_event

    return start_event
