from typing import Literal

import pandas as pd

import process_performance_indicators.cost.instances as instances_cost_indicators
import process_performance_indicators.utils.cases as cases_helpers
import process_performance_indicators.utils.instances as instances_helpers
from process_performance_indicators.constants import StandardColumnNames


def automated_activity_cost(
    event_log: pd.DataFrame,
    case_id: str,
    aggregation_mode: Literal["sgl", "sum"],
    automated_activities: list[str] | set[str],
) -> int | float | None:
    """
    The total cost associated with all instantiations of automated activities in the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.
        automated_activities: The list or set of automated activities.

    Returns:
        The total cost associated with all instantiations of automated activities in the case.
        None: If no automated activity cost is found.

    """
    aggregation_function = {
        "sgl": instances_cost_indicators.total_cost_for_single_events_of_activity_instances,
        "sum": instances_cost_indicators.total_cost_for_sum_of_all_events_of_activity_instances,
    }
    automated_activities = set(automated_activities)
    activity_instances = set()
    for instance_id in cases_helpers.inst(event_log, case_id):
        activity_instances.update(instances_helpers.act(event_log, instance_id))
    automated_activity_instances = automated_activities.intersection(activity_instances)

    total_cost = 0
    for instance_id in automated_activity_instances:
        total_cost += aggregation_function[aggregation_mode](event_log, instance_id)
    return total_cost


def desired_activity_count(event_log: pd.DataFrame, case_id: str, desired_activities: list[str] | set[str]) -> int:
    """
    The number of instantiated activities whose occurrences is desirable in the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        desired_activities: The list or set of desired activities.

    Returns:
        The number of instantiated activities whose occurrences is desirable in the case.

    """
    desired_activities = set(desired_activities)
    case_activities = cases_helpers.act(event_log, case_id)
    return len(desired_activities.intersection(case_activities))


def direct_cost(
    event_log: pd.DataFrame,
    case_id: str,
    aggregation_mode: Literal["sgl", "sum"],
    direct_costs_activities: list[str] | set[str],
) -> int | float | None:
    """
    The total cost associated with all instantiations of activities that have a direct effect
    on the outcome of cases in the group of cases.

    Args:
        event_log: The event log.
        case_id: The case id.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.
        direct_costs_activities: The list or set of activities that have a direct effect
            on the outcome of cases in the group of cases.

    Returns:
        The total cost associated with all instantiations of activities that have a direct effect
        on the outcome of cases in the group of cases.

    """
    aggregation_function = {
        "sgl": instances_cost_indicators.total_cost_for_single_events_of_activity_instances,
        "sum": instances_cost_indicators.total_cost_for_sum_of_all_events_of_activity_instances,
    }
    direct_costs_activities = set(direct_costs_activities)
    activity_instances = set()
    for instance_id in cases_helpers.inst(event_log, case_id):
        activity_instances.update(instances_helpers.act(event_log, instance_id))
    direct_costs_activity_instances = direct_costs_activities.intersection(activity_instances)

    total_cost = 0
    for instance_id in direct_costs_activity_instances:
        total_cost += aggregation_function[aggregation_mode](event_log, instance_id)
    return total_cost


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
    sorted_events = case_events.sort_values(by=StandardColumnNames.TIMESTAMP, ascending=False)
    non_null_costs = sorted_events[StandardColumnNames.MAINTENANCE_COST].dropna()
    return non_null_costs.iloc[0] if len(non_null_costs) > 0 else None


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
    case_events = event_log[event_log[StandardColumnNames.CASE_ID] == case_id]
    sorted_events = case_events.sort_values(by=StandardColumnNames.TIMESTAMP, ascending=False)
    non_null_costs = sorted_events[StandardColumnNames.MISSED_DEADLINE_COST].dropna()
    return non_null_costs.iloc[0] if len(non_null_costs) > 0 else None


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


def labor_cost_and_total_cost_ratio(
    event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]
) -> float | None:
    """
    The ratio between the labor cost associated with all activity instances of the case,
    and the total cost associated with all activity instances of the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The labor cost and total cost ratio for a case.
        None: If the labor cost or the total cost is None.

    """
    _labor_cost = labor_cost(event_log, case_id, aggregation_mode)
    _total_cost = total_cost(event_log, case_id, aggregation_mode)
    return _labor_cost / _total_cost
