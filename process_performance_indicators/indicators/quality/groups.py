from typing import Literal

import pandas as pd

import process_performance_indicators.indicators.general.groups as general_groups_indicators
import process_performance_indicators.indicators.quality.cases as quality_cases_indicators
from process_performance_indicators.utils.safe_division import safe_divide


def activity_instance_count_by_human_resource(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], human_resource_name: str
) -> int:
    """
    The number of times that any activity is instantiated by a specific human resource in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        human_resource_name: The name of the human resource.

    """
    count = 0
    for case_id in case_ids:
        count += quality_cases_indicators.activity_instance_count_by_human_resource(
            event_log, case_id, human_resource_name
        )
    return count


def expected_activity_instance_count_by_human_resource(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], human_resource_name: str
) -> float:
    """
    The expected number of times that any activity is instantiated by a specific human resource in a case belonging to the group of cases

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        human_resource_name: The name of the human resource.

    """
    numerator = activity_instance_count_by_human_resource(event_log, case_ids, human_resource_name)
    denominator = general_groups_indicators.activity_instance_count(event_log, case_ids)

    return safe_divide(numerator, denominator)


def activity_instance_count_by_role(event_log: pd.DataFrame, case_ids: list[str] | set[str], role_name: str) -> int:
    """
    The number of times that any activity is instantiated by a specific role in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        role_name: The name of the role.

    """
    count = 0
    for case_id in case_ids:
        count += quality_cases_indicators.activity_instance_count_by_role(event_log, case_id, role_name)
    return count


def expected_activity_instance_count_by_role(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], role_name: str
) -> int | float:
    """
    The expected number of times that any activity is instantiated by a specific role in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        role_name: The name of the role.

    """
    numerator = activity_instance_count_by_role(event_log, case_ids, role_name)
    denominator = general_groups_indicators.activity_instance_count(event_log, case_ids)

    return safe_divide(numerator, denominator)


def automated_activity_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of automated activities that occur in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_automated_activity_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected number of automated activities that occur in a case belonging to the group of cases.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The case IDs.

    Returns:
        int | float: The expected number of automated activities that occur in a case belonging to the group of cases.

    """
    raise NotImplementedError("Not implemented yet.")


def automated_activity_instance_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of times that an automated activity is instantiated in the group of cases.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The case IDs.

    Returns:
        int: The number of times that an automated activity is instantiated in the group of cases.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_automated_activity_instance_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected number of times that an automated activity is instantiated in a case belonging to the group of cases.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The case IDs.

    Returns:
        int | float: The expected number of times that an automated activity is instantiated in a case belonging to the group of cases.

    """
    raise NotImplementedError("Not implemented yet.")


def case_and_client_count_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The ratio between the number of cases belonging to the group of cases, and the number of distinct clients associated with cases in the group of cases.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def case_count_where_activity_after_time_frame(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], activity_name: str, end_time: pd.Timestamp
) -> int:
    """
    The number of cases belonging to the group of cases where a certain activity has occurred after a specific time frame.

    Args:
        event_log (pd.DataFrame): The event log.
        case_ids (list[str] | set[str]): The case IDs.
        activity_name (str): The name of the activity.
        end_time (pd.Timestamp): The end time.

    """
    raise NotImplementedError("Not implemented yet.")


def case_count_where_activity_before_time_frame(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], activity_name: str, start_time: pd.Timestamp
) -> int:
    """
    The number of cases belonging to the group of cases where a certain activity has occurred before a specific time frame.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        activity_name: The name of the activity.
        start_time: The start time.

    """
    raise NotImplementedError("Not implemented yet.")


def case_count_where_activity_during_time_frame(
    event_log: pd.DataFrame,
    case_ids: list[str] | set[str],
    activity_name: str,
    start_time: pd.Timestamp,
    end_time: pd.Timestamp,
) -> int:
    """
    The number of cases belonging to the group of cases where a certain activity has occurred within a specific time frame.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        activity_name: The name of the activity.
        start_time: The start time.
        end_time: The end time.

    """
    raise NotImplementedError("Not implemented yet.")


def case_count_where_end_activity_is_a(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], a_activity_name: str
) -> int:
    """
    The number of cases belonging to the group of cases where a specific activity is the last instantiated one.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        a_activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def case_count_where_start_activity_is_a(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], a_activity_name: str
) -> int:
    """
    The number of cases belonging to the group of cases where a specific activity is the first instantiated one.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        a_activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def case_count_with_rework(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of cases belonging to the group of cases where there has been rework.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def case_percentage_where_activity_after_time_frame(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], end_time: pd.Timestamp
) -> float:
    """
    The percentage of cases belonging to the group of cases where a certain activity has occurred after a specific time frame.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        end_time: The end time.

    """
    raise NotImplementedError("Not implemented yet.")


def case_percentage_where_activity_before_time_frame(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], start_time: pd.Timestamp
) -> float:
    """
    The percentage of cases belonging to the group of cases where a certain activity has occurred before a specific time frame.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        start_time: The start time.

    """
    raise NotImplementedError("Not implemented yet.")


def case_percentage_where_activity_during_time_frame(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], start_time: pd.Timestamp, end_time: pd.Timestamp
) -> float:
    """
    The percentage of cases belonging to the group of cases where a certain activity has occurred within a specific time frame.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        start_time: The start time.
        end_time: The end time.

    """
    raise NotImplementedError("Not implemented yet.")


def case_percentage_where_end_activity_is_a(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], a_activity_name: str
) -> float:
    """
    The percentage of cases belonging to the group of cases where a specific activity is the last instantiated one.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        a_activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def case_percentage_where_start_activity_is_a(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], a_activity_name: str
) -> float:
    """
    The percentage of cases belonging to the group of cases where a specific activity is the first instantiated one.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        a_activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def case_percentage_with_missed_deadline(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], deadline: pd.Timestamp
) -> float:
    """
    The percentage of cases belonging to the group of cases whose latest event occurs after a given deadline.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        deadline: The deadline.

    """
    raise NotImplementedError("Not implemented yet.")


def case_percentage_with_rework(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The percentage of cases belonging to the group of cases where there has been rework.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def client_count_and_total_cost_ratio(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The ratio between the number of distinct clients associated with cases in the group of cases,
    and the total cost associated with all activity instances of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_client_count_and_total_cost_ratio(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The ratio between the number of distinct clients associated with cases in the group of cases,
    and the total cost associated with all activity instances of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def desired_activity_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of instantiated activities whose occurence is desirable in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_desired_activity_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected number of instantiated activities whose occurrence is desirable in a case belonging to the groupd of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def human_resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of human resources that are involved in the execution of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_human_resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected number of human resources that are involved in the execution of a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def non_automated_activity_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of non-automated activities that occur in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_non_automated_activity_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected number of non-automated activities that occur in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def non_automated_activity_instance_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of times that an non-automated activity is instantiated in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_non_automated_activity_instance_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str]
) -> int | float:
    """
    The expected number of times that an non-automated activity is instantiated in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def outcome_unit_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int:
    """
    The outcome units associated with all instantiations of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_outcome_unit_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float:
    """
    The expected outcome units associated with all activity instances of a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        aggregation_mode: The aggregation mode.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_overall_quality(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The overall quality associated with the outcome of a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def repeatability(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The inverted ratio between the number of activities that occur in the group of cases, and the number of times
    that an activity has been instantiated in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_repeatability(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected inverted ratio between the number of activities that occur in a case belonging to the group of cases,
    and the number of times that an activity has been instantiated in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of times that any activity has been instantiated again, after its first instantiation, in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_rework_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float:
    """
    The expected number of times that any activity has been instantiated again, after its first instantiation, in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_count_by_value(event_log: pd.DataFrame, case_ids: list[str] | set[str], value: str) -> int:
    """
    The number of times that the activity has been instantiated again, after it has been instantiated a certain number of times, in every case of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        value: The certain number of times that the activity has been instantiated.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_rework_count_by_value(event_log: pd.DataFrame, case_ids: list[str] | set[str], value: str) -> int | float:
    """
    The expected number of times that the activity has been instantiated again, after it has been instantiated a certain number of times,
    in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        value: The certain number of times that the activity has been instantiated.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_of_activities_subset(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], activities_subset: set[str]
) -> int:
    """
    The number of times that any activity belonging to a subset of activities has been instantiated again, after its first instantiation,
    in every case of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        activities_subset: The subset of activities.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_rework_of_activities_subset(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], activities_subset: set[str]
) -> int | float:
    """
    The expected number of times that any activity belonging to a subset of activities has been instantiated again, after its first instantiation,
    in a case belonging to the group of cases.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_percentage(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The percentage of times that any activity has been instantiated again, after its first instantiation,
    in every case of the group of cases.


    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_rework_percentage(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The expected percentage of times that any activity has been instantiated again, after its first instantiation,
    in a case belonging to the group of cases.


    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_percentage_by_value(event_log: pd.DataFrame, case_ids: list[str] | set[str], value: str) -> float:
    """
    The percentage of times that any activity has been instantiated again, after it has been instantiated a certain number of times,
    in every case of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        value: The certain number of times that the activity has been instantiated.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_rework_percentage_by_value(event_log: pd.DataFrame, case_ids: list[str] | set[str], value: str) -> float:
    """
    The expected percentage of times that any activity has been instantiated again, after it has been instantiated a certain number of times, in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        value: The certain number of times that the activity has been instantiated.

    """
    raise NotImplementedError("Not implemented yet.")


def rework_time(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> pd.Timedelta:
    """
    The total elapsed time for all times that any activity has been instantiated again, after its first instantiation,
    in every case of group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_rework_time(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> pd.Timedelta:
    """
    The expected total elapsed time for all times that any activity has been instantiated again, after its first instantiation,
    in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def successful_outcome_unit_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int:
    """
    The outcome units associated with all activity instances of the group of cases, after deducting those that were unsuccessfully completed.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_successful_outcome_unit_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float:
    """
    The expected outcome units associated with all activity instances of a case belonging to the group of cases, after deducting those that were unsuccessfully completed.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.


    """
    raise NotImplementedError("Not implemented yet.")


def successful_outcome_unit_percentage(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The percentage of outcome units associated with all activity instances of the group of cases that were successfully completed.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_successful_outcome_unit_percentage(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The expected percentage of outcome units associated with all activity instances of a case belonging to the group of cases that were successfully completed.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def total_cost_and_client_count_ratio(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The ratio between the total cost associated with all activity instances of the group of cases, and the number of distinct clients associated with cases in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_total_cost_and_client_count_ratio(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The expected ratio between the total cost associated with all activity instances of the group of cases, and the number of distinct clients associated with cases in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def unwanted_activity_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], unwanted_activities: set[str]
) -> int:
    """
    The number of unwanted activities that occur in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_unwanted_activity_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], unwanted_activities: set[str]
) -> int:
    """
    The expected number of unwanted activities that occur in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")


def unwanted_activity_percentage(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], unwanted_activities: set[str]
) -> float:
    """
    The percentage of unwanted activities that occur in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_unwanted_activity_percentage(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], unwanted_activities: set[str]
) -> float:
    """
    The expected percentage of unwanted activities that occur in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")


def unwanted_activity_instance_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], unwanted_activities: set[str]
) -> int:
    """
    The number of times that an unwanted activity is instantiated in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_unwanted_activity_instance_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], unwanted_activities: set[str]
) -> int:
    """
    The expected number of times that an unwanted activity is instantiated in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")


def unwanted_activity_instance_percentage(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], unwanted_activities: set[str]
) -> float:
    """
    The percentage of times that an unwanted activity is instantiated in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_unwanted_activity_instance_percentage(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], unwanted_activities: set[str]
) -> float:
    """
    The expected percentage of times that an unwanted activity is instantiated in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.
        unwanted_activities: The set of unwanted activities names.

    """
    raise NotImplementedError("Not implemented yet.")
