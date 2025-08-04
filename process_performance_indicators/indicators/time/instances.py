import pandas as pd

import process_performance_indicators.utils.instances as instances_utils


def lead_time(event_log: pd.DataFrame, instance_id: str) -> pd.Timedelta:
    """
    The total elapsed time of the activity instance, measured as the sum of the elapsed time
    between the start and complete events of the activity instance, and the elapsed time between
    the complete event of the activity instance that precedes the current activity instance,
    and the start event of the current activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    """
    raise NotImplementedError("Lead time is not implemented yet.")


def service_and_lead_time_ratio(event_log: pd.DataFrame, instance_id: str) -> float:
    """
    The ratio between the elapsed time between the start and complete events of the activity instance,
    and the total elapsed time of the activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    """
    raise NotImplementedError("Service and lead time ratio is not implemented yet.")


def service_time(event_log: pd.DataFrame, instance_id: str) -> pd.Timedelta:
    """
    The elapsed time between the start and complete events of the activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    """
    complete_time = instances_utils.ctime(event_log, instance_id)
    start_time = instances_utils.stime(event_log, instance_id)
    return complete_time - start_time


def waiting_time(event_log: pd.DataFrame, instance_id: str) -> pd.Timedelta:
    """
    The elapsed time between the complete event of the activity instance that
    precedes the current activity instance, and the start event of the current
    activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    """
    raise NotImplementedError("Waiting time is not implemented yet.")
