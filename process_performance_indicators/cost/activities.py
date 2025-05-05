from typing import Literal

import pandas as pd

import process_performance_indicators.cost.instances as instances_cost_indicators
import process_performance_indicators.helpers.activities as activities_helpers


def fixed_cost(
    event_log: pd.DataFrame, activity_name: str, aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the fixed cost for an activity.

    Args:
        event_log: The event log.
        activity_name: The activity name.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The fixed cost for an activity.

    """
    aggregation_function = {
        "sgl": instances_cost_indicators.fixed_cost_for_single_events_of_activity_instances,
        "sum": instances_cost_indicators.fixed_cost_for_sum_of_all_events_of_activity_instances,
    }
    fixed_cost = 0

    for instance_id in activities_helpers.inst(event_log, activity_name):
        fixed_cost += aggregation_function[aggregation_mode](event_log, instance_id)

    return fixed_cost


def inventory_cost(
    event_log: pd.DataFrame, activity_name: str, aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the inventory cost for an activity.

    Args:
        event_log: The event log.
        activity_name: The activity name.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The inventory cost for an activity.

    """
    aggregation_function = {
        "sgl": instances_cost_indicators.inventory_cost_for_single_events_of_activity_instances,
        "sum": instances_cost_indicators.inventory_cost_for_sum_of_all_events_of_activity_instances,
    }
    inventory_cost = 0

    for instance_id in activities_helpers.inst(event_log, activity_name):
        inventory_cost += aggregation_function[aggregation_mode](event_log, instance_id)

    return inventory_cost
