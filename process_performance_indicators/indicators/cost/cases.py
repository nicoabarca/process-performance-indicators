from typing import Literal

import pandas as pd

import process_performance_indicators.indicators.cost.instances as cost_instances_indicators
import process_performance_indicators.utils.cases as cases_utils
import process_performance_indicators.utils.cases_activities as cases_activities_utils
import process_performance_indicators.utils.instances as instances_utils
from process_performance_indicators.constants import StandardColumnNames
from process_performance_indicators.utils.safe_division import safe_divide


def automated_activity_cost(
    event_log: pd.DataFrame, case_id: str, automated_activities: set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float:
    """
    The total cost associated with all instantiations of automated activities in the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        automated_activities: The set of automated activities.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    aggregation_function = {
        "sgl": cost_instances_indicators.total_cost_for_single_events_of_activity_instances,
        "sum": cost_instances_indicators.total_cost_for_sum_of_all_events_of_activity_instances,
    }

    total_cost = 0
    for instance_id in cases_utils.inst(event_log, case_id):
        if instances_utils.act(event_log, instance_id) in automated_activities:
            total_cost += aggregation_function[aggregation_mode](event_log, instance_id) or 0

    return total_cost


def desired_activity_count(event_log: pd.DataFrame, case_id: str, desired_activities: set[str]) -> int:
    """
    The number of instantiated activities whose occurrences is desirable in the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        desired_activities: The set of desired activities.

    Returns:
        The number of instantiated activities whose occurrences is desirable in the case.

    """
    return len(desired_activities.intersection(cases_utils.act(event_log, case_id)))


def direct_cost(
    event_log: pd.DataFrame, case_id: str, direct_costs_activities: set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float:
    """
    The total cost associated with all instantiations of activities that have a direct effect
    on the outcome of the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        direct_costs_activities: The set of activities that have a direct effect
            on the outcome of the case.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    aggregation_function = {
        "sgl": cost_instances_indicators.total_cost_for_single_events_of_activity_instances,
        "sum": cost_instances_indicators.total_cost_for_sum_of_all_events_of_activity_instances,
    }

    total_cost = 0
    for instance_id in cases_utils.inst(event_log, case_id):
        if instances_utils.act(event_log, instance_id) in direct_costs_activities:
            total_cost += aggregation_function[aggregation_mode](event_log, instance_id) or 0

    return total_cost


def fixed_cost(event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]) -> float:
    """
    The fixed cost associated with all activity instances of the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        aggregation_mode: The aggregation mode.
            "sgl" considers single events of activity instances for cost calculations.
            "sum" considers the sum of all events of activity intances for cost calculations.

    """
    aggregation_function = {
        "sgl": cost_instances_indicators.fixed_cost_for_single_events_of_activity_instances,
        "sum": cost_instances_indicators.fixed_cost_for_sum_of_all_events_of_activity_instances,
    }

    total_fixed_cost = 0
    for instance_id in cases_utils.inst(event_log, case_id):
        total_fixed_cost += aggregation_function[aggregation_mode](event_log, instance_id) or 0

    return total_fixed_cost


def human_resource_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of human resources that are involved in the execution of the case.

    Args:
        event_log: The event log.
        case_id: The case id.

    """
    return len(cases_utils.hres(event_log, case_id))


def inventory_cost(event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]) -> float:
    """
    The inventory cost associated with all activity instances of the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        aggregation_mode: The aggregation mode.
            "sgl" considers single events of activity instances for cost calculations.
            "sum" considers the sum of all events of activity intances for cost calculations.

    """
    aggregation_function = {
        "sgl": cost_instances_indicators.inventory_cost_for_single_events_of_activity_instances,
        "sum": cost_instances_indicators.inventory_cost_for_sum_of_all_events_of_activity_instances,
    }
    total_inventory_cost = 0

    for instance_id in cases_utils.inst(event_log, case_id):
        total_inventory_cost += aggregation_function[aggregation_mode](event_log, instance_id) or 0

    return total_inventory_cost


def labor_cost_and_total_cost_ratio(
    event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The ratio between the labor cost associated with all activity instances of the case,
    and the total cost associated with all activity instances of the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    return safe_divide(
        labor_cost(event_log, case_id, aggregation_mode),
        total_cost(event_log, case_id, aggregation_mode),
    )


def labor_cost(event_log: pd.DataFrame, case_id: str, aggregation_mode: Literal["sgl", "sum"]) -> float:
    """
    The labor cost associated with all activity instances of the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        aggregation_mode: The aggregation mode.
            "sgl" considers single events of activity instances for cost calculations.
            "sum" considers the sum of all events of activity intances for cost calculations.

    """
    aggregation_function = {
        "sgl": cost_instances_indicators.labor_cost_for_single_events_of_activity_instances,
        "sum": cost_instances_indicators.labor_cost_for_sum_of_all_events_of_activity_instances,
    }
    total_labor_cost = 0

    for instance_id in cases_utils.inst(event_log, case_id):
        total_labor_cost += aggregation_function[aggregation_mode](event_log, instance_id) or 0

    return total_labor_cost


def maintenance_cost(event_log: pd.DataFrame, case_id: str) -> float:
    """
    The maintenance cost associated with the case.

    Args:
        event_log: The event log.
        case_id: The case id.

    """
    case_events = event_log[event_log[StandardColumnNames.CASE_ID] == case_id]
    if not case_events[StandardColumnNames.MAINTENANCE_COST].empty:
        return float(case_events[StandardColumnNames.MAINTENANCE_COST].unique()[0])
    return 0


def missed_deadline_cost(event_log: pd.DataFrame, case_id: str) -> float:
    """
    The cost for missing deadlines associated with the case.

    Args:
        event_log: The event log.
        case_id: The case id.

    """
    case_events = event_log[event_log[StandardColumnNames.CASE_ID] == case_id]
    if not case_events[StandardColumnNames.MISSED_DEADLINE_COST].empty:
        return float(case_events[StandardColumnNames.MISSED_DEADLINE_COST].unique()[0])
    return 0


def overhead_cost(
    event_log: pd.DataFrame, case_id: str, direct_cost_activities: set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The total cost associated with all instantiations of activities that do not
    have a direct effect on the outcome of the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        direct_cost_activities: The set of activities that have a direct cost
            on the outcome of the case.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    aggregation_function = {
        "sgl": cost_instances_indicators.total_cost_for_single_events_of_activity_instances,
        "sum": cost_instances_indicators.total_cost_for_sum_of_all_events_of_activity_instances,
    }
    total_cost = 0
    for instance_id in cases_utils.inst(event_log, case_id):
        if instances_utils.act(event_log, instance_id) not in direct_cost_activities:
            total_cost += aggregation_function[aggregation_mode](event_log, instance_id) or 0

    return total_cost


def resource_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of resources that are involved in the execution of the case.

    Args:
        event_log: The event log.
        case_id: The case id.

    """
    return len(cases_utils.res(event_log, case_id))


def rework_cost(event_log: pd.DataFrame, case_id: str) -> float:
    """
    The total cost of all times that any activity has been instantiated again, after its first
    instantiation, in the case.
    """
    raise NotImplementedError("Not implemented yet")


def rework_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of times that any activity has been instantiated again, after its first
    intantiation, in the case.
    """
    rework_count = 0
    for activity_name in event_log[StandardColumnNames.ACTIVITY_NAME].unique():
        rework_count += max(0, cases_activities_utils.count(event_log, case_id, activity_name) - 1)
    return rework_count


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
        "sgl": cost_instances_indicators.total_cost_for_single_events_of_activity_instances,
        "sum": cost_instances_indicators.total_cost_for_sum_of_all_events_of_activity_instances,
    }
    total_cost: int | float = 0

    for instance_id in cases_utils.inst(event_log, case_id):
        instance_cost = aggregation_function[aggregation_mode](event_log, instance_id)
        if instance_cost is None:
            raise ValueError(f"Total cost calculation for instance {instance_id} returned None")
        total_cost += instance_cost

    return total_cost
