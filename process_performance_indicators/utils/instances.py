import pandas as pd

from process_performance_indicators.constants import (
    LifecycleTransitionType,
    StandardColumnNames,
)
from process_performance_indicators.exceptions import (
    ColumnNotFoundError,
    InstanceIdNotFoundError,
)
from process_performance_indicators.utils import cases as cases_utils
from process_performance_indicators.utils.safe_division import safe_division


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


def stime(event_log: pd.DataFrame, instance_id: str) -> pd.Timestamp:
    """
    Get the start time of an event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)
    start_event = start(event_log, instance_id)
    return start_event[StandardColumnNames.TIMESTAMP].unique()[0]


def ctime(event_log: pd.DataFrame, instance_id: str) -> pd.Timestamp:
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
        error_message = (
            "RESOURCE column not found in event log. Please ensure the event log contains the resource column."
        )
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


def prev_instances(event_log: pd.DataFrame, instance_id: str) -> set[str]:
    """
    Get the activity instances that occurred right before after activity instances.
    """
    _is_instance_id_valid(event_log, instance_id)
    start_time = stime(event_log, instance_id)
    case_id_val = case(event_log, instance_id)
    instance_ids = cases_utils.inst(event_log, case_id_val)
    completed_before = {}
    for other in instance_ids:
        if other == instance_id:
            continue
        ct = ctime(event_log, other)
        if ct < start_time:
            completed_before[other] = ct
    if not completed_before:
        return set()
    latest_ct = max(completed_before.values())
    return {iid for iid, t in completed_before.items() if t == latest_ct}


def next_instances(event_log: pd.DataFrame, instance_id: str) -> set[str]:
    """
    Get the activity instances that occurred right after activity instances.
    """
    _is_instance_id_valid(event_log, instance_id)
    complete_time = ctime(event_log, instance_id)
    case_id_val = case(event_log, instance_id)
    instance_ids = cases_utils.inst(event_log, case_id_val)
    started_after = {}
    for other in instance_ids:
        if other == instance_id:
            continue
        st = stime(event_log, other)
        if st > complete_time:
            started_after[other] = st
    if not started_after:
        return set()
    earliest_st = min(started_after.values())
    return {iid for iid, t in started_after.items() if t == earliest_st}


def prevstr(event_log: pd.DataFrame, instance_id: str) -> set[str]:
    """
    Get the activity instances that start before but finish after activity instances
    """
    _is_instance_id_valid(event_log, instance_id)
    instance_ids = cases_utils.inst(event_log, case(event_log, instance_id))
    prevstr_instances = set()
    for other in instance_ids:
        if other == instance_id:
            continue
        if stime(event_log, other) < stime(event_log, instance_id) and ctime(event_log, other) > stime(
            event_log, instance_id
        ):
            prevstr_instances.add(other)
    return prevstr_instances


def concstr(event_log: pd.DataFrame, instance_id: str) -> set[str]:
    """
    Get the activity instances that start at the same time as activity instances
    """
    _is_instance_id_valid(event_log, instance_id)
    instance_ids = cases_utils.inst(event_log, case(event_log, instance_id))
    concurrent_instances = set()
    for other in instance_ids:
        if other == instance_id:
            continue
        if stime(event_log, other) == stime(event_log, instance_id):
            concurrent_instances.add(other)
    return concurrent_instances


def dres(event_log: pd.DataFrame, instance_id: str) -> float:
    """
    Delegation of work for activity intances.
    If all activity instances that were completed right before the activity instances
    were associated with the same human resource as the activity instance, returns 0.
    If none of the activity instances that were complete right before the activity instance were
    associated with that human resource, returns 1.
    """
    _is_instance_id_valid(event_log, instance_id)
    previous_instances = prev_instances(event_log, instance_id)
    if not previous_instances:
        return 0

    instances_with_different_human_resource = 0
    for previous_instance in previous_instances:
        if hres(event_log, previous_instance) != hres(event_log, instance_id):
            instances_with_different_human_resource += 1

    return safe_division(instances_with_different_human_resource, len(previous_instances))


def instbetween_s(event_log: pd.DataFrame, instance_id_one: str, instance_id_two: str) -> set[str]: ...


def instbetween_c(event_log: pd.DataFrame, instance_id_one: str, instance_id_two: str) -> set[str]: ...


def instbetween_sc(event_log: pd.DataFrame, instance_id_one: str, instance_id_two: str) -> set[str]: ...


def instbetween_w(event_log: pd.DataFrame, instance_id_one: str, instance_id_two: str) -> set[str]: ...


def timew(event_log: pd.DataFrame, first_pair: tuple[str, str], second_pair: tuple[str, str]) -> pd.Timedelta:
    """
    Time between pairs of activity instances
    """


def lt(event_log: pd.DataFrame, earliest_instance_id: str, latest_instance_id: str) -> pd.Timedelta:
    """
    Lead time between pairs of activity instances.
    """
    _is_instance_id_valid(event_log, earliest_instance_id)
    _is_instance_id_valid(event_log, latest_instance_id)
    earliest_instance_start_time = stime(event_log, earliest_instance_id)
    latest_instance_complete_time = ctime(event_log, latest_instance_id)
    return latest_instance_complete_time - earliest_instance_start_time


def _is_instance_id_valid(event_log: pd.DataFrame, instance_id: str) -> None:
    """
    Check if the instance id is valid.

    Raises:
        InstanceIdNotFoundError: If the instance id is not found in the event log.

    """
    if instance_id not in event_log[StandardColumnNames.INSTANCE].unique():
        raise InstanceIdNotFoundError(f"Instance id {instance_id} not found in event log.")


def _match(event_log: pd.DataFrame, complete_event: pd.DataFrame) -> pd.DataFrame:
    """
    Match the event log to the instance id.
    """
    complete_event_instance_id: str = complete_event[StandardColumnNames.INSTANCE].unique()[0]

    start_event = event_log[
        (event_log[StandardColumnNames.INSTANCE] == complete_event_instance_id)
        & (event_log[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.START)
    ]
    if start_event.empty:
        return complete_event

    return start_event
