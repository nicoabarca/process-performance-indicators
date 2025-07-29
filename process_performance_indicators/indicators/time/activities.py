import pandas as pd

import process_performance_indicators.indicators.time.instances as time_instances_indicators
import process_performance_indicators.utils.cases as cases_utils


def lead_time(event_log: pd.DataFrame, activity_name: str) -> pd.Timedelta:
    """
    Calculate the lead time of an activity instances accross all cases.
    """
    raise NotImplementedError("Not implemented yet.")


def service_and_lead_time_ratio(event_log: pd.DataFrame, activity_name: str) -> float:
    """
    Calculate the service and lead time ratio of an activity instances accross all cases.
    """
    raise NotImplementedError("Not implemented yet.")


def service_time(event_log: pd.DataFrame, activity_name: str) -> pd.Timedelta:
    """
    Calculate the service time of an activity instances accross all cases.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    Returns:
        pd.Timedelta: The service time of the activity.

    """
    sum_of_service_times_in_seconds = sum(
        time_instances_indicators.service_time(event_log, instance_id).total_seconds()
        for instance_id in cases_utils.inst(event_log, activity_name)
    )
    return pd.Timedelta(seconds=sum_of_service_times_in_seconds)


def waiting_time(event_log: pd.DataFrame, activity_name: str) -> pd.Timedelta:
    """
    Calculate the waiting time of an activity instances accross all cases.
    """
    raise NotImplementedError("Not implemented yet.")
