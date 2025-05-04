import pandas as pd

import process_performance_indicators.helpers.cases as cases_helpers
import process_performance_indicators.time.instances as instances_time_indicators


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
        instances_time_indicators.service_time(event_log, instance_id).total_seconds()
        for instance_id in cases_helpers.inst(event_log, activity_name)
    )
    return pd.Timedelta(seconds=sum_of_service_times_in_seconds)
