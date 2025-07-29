from typing import Literal

import pandas as pd

import process_performance_indicators.utils.cases as cases_utils
import process_performance_indicators.utils.instances as instances_utils


def activity_instance_count_by_human_resource(event_log: pd.DataFrame, case_id: str, human_resource_name: str) -> int:
    """
    The number of times that any activity is instantiated by a specific human resource in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        human_resource_name: The name of the human resource.

    """
    activity_instances = cases_utils.inst(event_log, case_id)
    activity_instances_instantiated_by_human_resource = set()
    for instance_id in activity_instances:
        if instances_utils.hres(event_log, instance_id) == human_resource_name:
            activity_instances_instantiated_by_human_resource.add(instance_id)
    return len(activity_instances_instantiated_by_human_resource)


def activity_instance_count_by_role(event_log: pd.DataFrame, case_id: str, role_name: str) -> int:
    """
    The number of times that any activity is instantiated by a specific role in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        role_name: The name of the role.

    """
    activity_instances = cases_utils.inst(event_log, case_id)
    activity_instances_instantiated_by_role = set()
    for instance_id in activity_instances:
        if instances_utils.role(event_log, instance_id) == role_name:
            activity_instances_instantiated_by_role.add(instance_id)
    return len(activity_instances_instantiated_by_role)


def automated_activity_count(event_log: pd.DataFrame, case_id: str, automated_activities: set[str]) -> int:
    """
    The number of automated activities that occur in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        automated_activities: The set of automated activities.

    """
    automated_activities = set(automated_activities)
    case_activities = cases_utils.act(event_log, case_id)
    return len(automated_activities.intersection(case_activities))


def automated_activity_instance_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of times that an automated activity is instantiated in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def desired_activity_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of instantiated activities whose occurence is desirable in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def human_resource_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of human resources that are involved in the execution of the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def non_automated_activity_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of non-automated activities that occur in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def non_automated_activity_instance_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of times that an non-automated activity is instantiated in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def outcome_unit_count(event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]) -> int:
    """
    The outcome units associated with all instantiations of the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def overall_quality(event_log: pd.DataFrame, case_id: str) -> int | float:
    """
    The overall quality associated with the outcome of the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def repeatability(event_log: pd.DataFrame, case_id: str) -> int | float:
    """
    The inverted ratio between the number of activities that occur in the case, and the number of times that an activity has been instantiated in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of times that any activity has been instantiated again, after its first instantiation, in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_count_by_value(event_log: pd.DataFrame, case_id: str, value: str) -> int:
    """
    The number of times that the activity has been instantiated again, after it has been instantiated a certain number of times, in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        value: The certain number of times that the activity has been instantiated.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_of_activities_subset(event_log: pd.DataFrame, case_id: str, activities_subset: set[str]) -> int:
    """
    The number of times that any activity belonging to a subset of activities has been instantiated again, after its first instantiation,
    in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        activities_subset: The subset of activities.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_percentage(event_log: pd.DataFrame, case_id: str) -> float:
    """
    The percentage of times that any activity has been instantiated again, after its first instantiation, in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_percentage_by_value(event_log: pd.DataFrame, case_id: str, value: str) -> float:
    """
    The percentage of times that any activity has been instantiated again, after it has been instantiated a certain number of times, in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        value: The certain number of times that the activity has been instantiated.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_time(event_log: pd.DataFrame, case_id: str, activity_name: str) -> float:
    """
    The total elapsed time for all times that any activity has been instantiated again, after its first instantiation, in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def successful_outcome_unit_count(
    event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]
) -> int:
    """
    The outcome units associated with all activity instances of the case, after deducting those that were unsuccessfully completed.

    Args:
        event_log: The event log.
        case_id: The case ID.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def successful_outcome_unit_percentage(
    event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The percentage of outcome units associated with all activity instances of the case that were successfully completed.

    Args:
        event_log: The event log.
        case_id: The case ID.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def unwanted_activity_count(event_log: pd.DataFrame, case_id: str, unwanted_activities: set[str]) -> int:
    """
    The number of unwanted activities that occur in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")


def unwanted_activity_percentage(event_log: pd.DataFrame, case_id: str, unwanted_activities: set[str]) -> float:
    """
    The percentage of unwanted activities that occur in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")


def unwanted_activity_instance_count(event_log: pd.DataFrame, case_id: str, unwanted_activities: set[str]) -> int:
    """
    The number of times that an unwanted activity is instantiated in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")


def unwanted_activity_instance_percentage(
    event_log: pd.DataFrame, case_id: str, unwanted_activities: set[str]
) -> float:
    """
    The percentage of times that an unwanted activity is instantiated in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")
