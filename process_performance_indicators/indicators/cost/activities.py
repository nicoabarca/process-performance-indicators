from typing import Literal

import pandas as pd

import process_performance_indicators.indicators.cost.instances as cost_instances_indicators
import process_performance_indicators.utils.activities as activities_utils
import process_performance_indicators.utils.cases_activities as cases_activities_utils
from process_performance_indicators.constants import StandardColumnNames
from process_performance_indicators.utils.safe_division import safe_divide


def fixed_cost(event_log: pd.DataFrame, activity_name: str, aggregation_mode: Literal["sgl", "sum"]) -> float:
    """
    The fixed cost associated with all instantiations of the activity.

    Args:
        event_log: The event log.
        activity_name: The activity name.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    aggregation_function = {
        "sgl": cost_instances_indicators.fixed_cost_for_single_events_of_activity_instances,
        "sum": cost_instances_indicators.fixed_cost_for_sum_of_all_events_of_activity_instances,
    }
    total_fixed_cost = 0

    for instance_id in activities_utils.inst(event_log, activity_name):
        total_fixed_cost += aggregation_function[aggregation_mode](event_log, instance_id) or 0

    return total_fixed_cost


def human_resource_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    The number of human resources that are involved in the execution of the activity.

    Args:
        event_log: The event log.
        activity_name: The activity name.

    """
    return len(activities_utils.hres(event_log, activity_name))


def inventory_cost(event_log: pd.DataFrame, activity_name: str, aggregation_mode: Literal["sgl", "sum"]) -> float:
    """
    The inventory cost associated with all instantiations of the activity.

    Args:
        event_log: The event log.
        activity_name: The activity name.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    aggregation_function = {
        "sgl": cost_instances_indicators.inventory_cost_for_single_events_of_activity_instances,
        "sum": cost_instances_indicators.inventory_cost_for_sum_of_all_events_of_activity_instances,
    }
    total_inventory_cost = 0

    for instance_id in activities_utils.inst(event_log, activity_name):
        total_inventory_cost += aggregation_function[aggregation_mode](event_log, instance_id) or 0

    return total_inventory_cost


def labor_cost_and_total_cost_ratio(
    event_log: pd.DataFrame, activity_name: str, aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The ratio between the labor cost associated with all instantiations of the activity,
    and the total cost associated with all instantiations of the activity.

    Args:
        event_log: The event log.
        activity_name: The activity name.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    return safe_divide(
        labor_cost(event_log, activity_name, aggregation_mode),
        total_cost(event_log, activity_name, aggregation_mode),
    )


def labor_cost(
    event_log: pd.DataFrame, activity_name: str, aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    The labor cost associated with all instantiations of the activity.

    Args:
        event_log: The event log.
        activity_name: The activity name.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    aggregation_function = {
        "sgl": cost_instances_indicators.labor_cost_for_single_events_of_activity_instances,
        "sum": cost_instances_indicators.labor_cost_for_sum_of_all_events_of_activity_instances,
    }
    labor_cost = 0

    for instance_id in activities_utils.inst(event_log, activity_name):
        labor_cost += aggregation_function[aggregation_mode](event_log, instance_id) or 0

    return labor_cost


def resource_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    The number of resources that are involved in the execution of the activity.

    Args:
        event_log: The event log.
        activity_name: The activity name.

    """
    return len(activities_utils.res(event_log, activity_name))


def rework_cost(event_log: pd.DataFrame, activity_name: str) -> float:
    """
    The total cost of all times that the activity has been instantiated again, after its
    first instantiation, in any case.

    Args:
        event_log: The event log.
        activity_name: The activity name.

    """
    raise NotImplementedError("Not implemented yet")


def rework_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    The number of times that the activity has been instantiated again, after its first
    intantiation, in any case.

    Args:
        event_log: The event log.
        activity_name: The activity name.

    """
    rework_count = 0

    for case_id in event_log[StandardColumnNames.CASE_ID].unique():
        rework_count += max(0, cases_activities_utils.count(event_log, case_id, activity_name) - 1)
    return rework_count


def total_cost(
    event_log: pd.DataFrame, activity_name: str, aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the total cost for an activity.

    Args:
        event_log: The event log.
        activity_name: The activity name.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The total cost for an activity.

    Raises:
        ValueError: If any of the aggregation function calls return None.

    """
    aggregation_function = {
        "sgl": cost_instances_indicators.total_cost_for_single_events_of_activity_instances,
        "sum": cost_instances_indicators.total_cost_for_sum_of_all_events_of_activity_instances,
    }
    total_cost: int | float = 0

    for instance_id in activities_utils.inst(event_log, activity_name):
        instance_cost = aggregation_function[aggregation_mode](event_log, instance_id)
        if instance_cost is None:
            raise ValueError(f"Total cost calculation for instance {instance_id} returned None")
        total_cost += instance_cost

    return total_cost
