from typing import Literal

import pandas as pd

import process_performance_indicators.utils.activities as activities_utils
import process_performance_indicators.utils.instances as instances_utils


def activity_instance_count_by_human_resource(
    event_log: pd.DataFrame, activity_name: str, human_resource_name: str
) -> int:
    """
    The number of times that a specific activity is instantiated by a specific human resource in the event log.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.
        human_resource_name: The name of the human resource.

    """
    activity_instances = activities_utils.inst(event_log, activity_name)
    activity_instances_instantiated_by_human_resource = set()
    for instance_id in activity_instances:
        if instances_utils.hres(event_log, instance_id) == human_resource_name:
            activity_instances_instantiated_by_human_resource.add(instance_id)
    return len(activity_instances_instantiated_by_human_resource)


def client_count_and_total_cost_ratio(
    event_log: pd.DataFrame, activity_name: str, aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The ratio between the number of distinct clients associated with cases where the activity is instantiated,
    and the total cost associated with all instantiations of the activity.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def human_resource_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    The number of human resources that are involved in the execution of the activity.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def outcome_unit_count(event_log: pd.DataFrame, activity_name: str, aggregation_mode: Literal["sgl", "sum"]) -> int:
    """
    The outcome units associated with all instantiations of the activity.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    The number of times that the activity has been instantiated again, after its first instantiation, in any case.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_count_by_value(event_log: pd.DataFrame, activity_name: str, value: str) -> int:
    """
    The number of times that the activity has been instantiated again, after it has been instantiated a certain number of times, in any case.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.
        value: The certain number of times that the activity has been instantiated.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_percentage(event_log: pd.DataFrame, activity_name: str) -> float:
    """
    The percentage of times that the activity has been instantiated again, after its first instantiation, in any case.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_percentage_by_value(event_log: pd.DataFrame, activity_name: str, value: str) -> float:
    """
    The percentage of times that the activity has been instantiated again, after it has been instantiated
    a certain number of times, in any case.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.
        value: The certain number of times that the activity has been instantiated.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_time(event_log: pd.DataFrame, activity_name: str, case_id: str) -> float:
    """
    The total elapsed time for all times that the activity has been instantiated again, after its first instantiation, in any case.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def successful_outcome_unit_count(
    event_log: pd.DataFrame, activity_name: str, aggregation_mode: Literal["sgl", "sum"]
) -> int:
    """
    The outcome units associated with all instantiations of the activity, after deducting those that were unsuccessfully completed.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def successful_outcome_unit_percentage(
    event_log: pd.DataFrame, activity_name: str, aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The percentage of outcome units associated with all instantiations of the activity that were successfully completed.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")
