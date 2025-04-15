import pandas as pd

from process_performance_indicators.constants import (
    LifecycleTransitionType,
    StandardColumnNames,
)
from process_performance_indicators.exceptions import InstanceIdNotFoundError


def str(event_log: pd.DataFrame, instance_id: str) -> pd.DataFrame:  # ignore: A001
    """
    Get the start event of an event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)

    # TODO: here call paper defined Match function
    return event_log[
        (event_log[StandardColumnNames.INSTANCE] == instance_id)
        & (event_log[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.START)
    ]


def cpl(event_log: pd.DataFrame, instance_id: str) -> pd.DataFrame:
    """
    Get the complete event of an event based on the instance id.
    """
    _is_instance_id_valid(event_log, instance_id)

    # TODO: here call paper defined Match function
    return event_log[
        (event_log[StandardColumnNames.INSTANCE] == instance_id)
        & (event_log[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.COMPLETE)
    ]


def _is_instance_id_valid(event_log: pd.DataFrame, instance_id: str) -> None:
    """
    Check if the instance id is valid.
    """
    if instance_id not in event_log[StandardColumnNames.INSTANCE].unique():
        raise InstanceIdNotFoundError(f"Instance id {instance_id} not found in event log.")
