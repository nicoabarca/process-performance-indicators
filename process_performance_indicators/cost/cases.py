from typing import Literal

import pandas as pd

import process_performance_indicators.cost.instances as instances_cost_indicators
import process_performance_indicators.helpers.cases as cases_helpers
from process_performance_indicators.constants import StandardColumnNames


def fixed_cost(event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]) -> int | float | None:
    """
    Calculate the fixed cost for a case.

    Args:
        event_log: The event log.
        case_id: The case id.
        aggregation_mode: The aggregation mode.
            "sgl" considers single events of activity instances for cost calculations.
            "sum" considers the sum of all events of activity intances for cost calculations.

    Returns:
        The fixed cost for a case.

    Raises:
        ValueError: If any of the aggregation function calls return None.

    """
    aggregation_function = {
        "sgl": instances_cost_indicators.fixed_cost_for_single_events_of_activity_instances,
        "sum": instances_cost_indicators.fixed_cost_for_sum_of_all_events_of_activity_instances,
    }
    fixed_cost: int | float = 0

    for instance_id in cases_helpers.inst(event_log, case_id):
        instance_cost = aggregation_function[aggregation_mode](event_log, instance_id)
        if instance_cost is None:
            raise ValueError(f"Fixed cost calculation for instance {instance_id} returned None")
        fixed_cost += instance_cost

    return fixed_cost


def inventory_cost(
    event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the inventory cost for a case.

    Args:
        event_log: The event log.
        case_id: The case id.
        aggregation_mode: The aggregation mode.
            "sgl" considers single events of activity instances for cost calculations.
            "sum" considers the sum of all events of activity intances for cost calculations.

    Returns:
        The inventory cost for a case.

    Raises:
        ValueError: If any of the aggregation function calls return None.

    """
    aggregation_function = {
        "sgl": instances_cost_indicators.inventory_cost_for_single_events_of_activity_instances,
        "sum": instances_cost_indicators.inventory_cost_for_sum_of_all_events_of_activity_instances,
    }
    inventory_cost: int | float = 0

    for instance_id in cases_helpers.inst(event_log, case_id):
        instance_cost = aggregation_function[aggregation_mode](event_log, instance_id)
        if instance_cost is None:
            raise ValueError(f"Inventory cost calculation for instance {instance_id} returned None")
        inventory_cost += instance_cost

    return inventory_cost


def labor_cost(event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]) -> int | float | None:
    """
    Calculate the labor cost for a case.

    Args:
        event_log: The event log.
        case_id: The case id.
        aggregation_mode: The aggregation mode.
            "sgl" considers single events of activity instances for cost calculations.
            "sum" considers the sum of all events of activity intances for cost calculations.

    Returns:
        The labor cost for a case.

    Raises:
        ValueError: If any of the aggregation function calls return None.

    """
    aggregation_function = {
        "sgl": instances_cost_indicators.labor_cost_for_single_events_of_activity_instances,
        "sum": instances_cost_indicators.labor_cost_for_sum_of_all_events_of_activity_instances,
    }
    labor_cost: int | float = 0

    for instance_id in cases_helpers.inst(event_log, case_id):
        instance_cost = aggregation_function[aggregation_mode](event_log, instance_id)
        if instance_cost is None:
            raise ValueError(f"Labor cost calculation for instance {instance_id} returned None")
        labor_cost += instance_cost

    return labor_cost


def total_cost(event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]) -> int | float | None:
    """
    Calculate the total cost for a case.

    Args:
        event_log: The event log.
        case_id: The case id.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The total cost for a case.

    Raises:
        ValueError: If any of the aggregation function calls return None.

    """
    aggregation_function = {
        "sgl": instances_cost_indicators.total_cost_for_single_events_of_activity_instances,
        "sum": instances_cost_indicators.total_cost_for_sum_of_all_events_of_activity_instances,
    }
    total_cost: int | float = 0

    for instance_id in cases_helpers.inst(event_log, case_id):
        instance_cost = aggregation_function[aggregation_mode](event_log, instance_id)
        if instance_cost is None:
            raise ValueError(f"Total cost calculation for instance {instance_id} returned None")
        total_cost += instance_cost

    return total_cost


def maintenance_cost(event_log: pd.DataFrame, case_id: str) -> int | float | None:
    """
    Calculate the maintenance cost for a case.

    Args:
        event_log: The event log.
        case_id: The case id.

    Returns:
        The maintenance cost for a case.
        None: If no maintenance cost is found.

    """
    case_events = event_log[event_log[StandardColumnNames.CASE_ID] == case_id]
    cost_values = case_events[StandardColumnNames.MAINTENANCE_COST].isnotna().to_list()
    # TODO: Add support for multiple maintenance costs, choose the last one registered.
    # Complementarily, add a warning if multiple maintenance costs are found.
    return cost_values[-1] if len(cost_values) > 0 else None


def missed_deadline_cost(event_log: pd.DataFrame, case_id: str) -> int | float | None:
    """
    Calculate the missed deadline cost for a case.

    Args:
        event_log: The event log.
        case_id: The case id.

    Returns:
        The missed deadline cost for a case.
        None: If no missed deadline cost is found.

    """
    # TODO: Add support for multiple missed deadline costs, choose the last one registered.
    # Complementarily, add a warning if multiple missed deadline costs are found.
    case_events = event_log[event_log[StandardColumnNames.CASE_ID] == case_id]
    cost_values = case_events[StandardColumnNames.MISSED_DEADLINE_COST].isnotna().to_list()
    return cost_values[-1] if len(cost_values) > 0 else None


def resource_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    Calculate the resource count for a case.

    Args:
        event_log: The event log.
        case_id: The case id.

    Returns:
        The resource count for a case.

    """
    return len(cases_helpers.res(event_log, case_id))
