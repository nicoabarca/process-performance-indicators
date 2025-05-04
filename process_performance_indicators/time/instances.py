import pandas as pd

import process_performance_indicators.helpers.instances as instances_helpers


def lead_time(event_log: pd.DataFrame, instance_id: str) -> pd.Timedelta:
    """
    Calculate the lead time of an activity based on instance id.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        pd.Timedelta: The lead time.

    """
    raise NotImplementedError("Lead time is not implemented yet.")


def service_time(event_log: pd.DataFrame, instance_id: str) -> pd.Timedelta:
    """
    Calculate the service time, i.e. the time between the start and the complete time of an activity based on instance id.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        pd.Timedelta: The service time.

    """
    complete_time = instances_helpers.ctime(event_log, instance_id)
    start_time = instances_helpers.stime(event_log, instance_id)
    return complete_time - start_time


def waiting_time(event_log: pd.DataFrame, instance_id: str) -> pd.Timedelta:
    """
    Calculate the waiting time of an activity based on instance id.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        pd.Timedelta: The waiting time.

    """
    raise NotImplementedError("Waiting time is not implemented yet.")
