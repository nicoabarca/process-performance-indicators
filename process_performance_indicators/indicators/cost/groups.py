from typing import Literal

import pandas as pd

import process_performance_indicators.cost.cases as cases_cost_indicators
import process_performance_indicators.general.groups as groups_general_indicators


def fixed_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the fixed cost for a group of case.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The fixed cost for a group of cases.

    Raises:
        ValueError: If any of the aggregation function calls return None.

    """
    fixed_cost: int | float = 0

    for case_id in case_ids:
        case_fixed_cost = cases_cost_indicators.fixed_cost(event_log, case_id, aggregation_mode)
        if case_fixed_cost is None:
            raise ValueError(f"Fixed cost calculation for case {case_id} returned None")
        fixed_cost += case_fixed_cost

    return fixed_cost


def expected_fixed_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the expected fixed cost for a group of case.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The expected fixed cost for a group of cases.

    """
    group_fixed_cost = fixed_cost(event_log, case_ids, aggregation_mode)
    if group_fixed_cost is None:
        raise ValueError("Fixed cost calculation for group of cases returned None")
    case_group_count = groups_general_indicators.case_count(event_log, case_ids)
    return group_fixed_cost / case_group_count


def inventory_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the inventory cost for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The inventory cost for a group of cases.

    Raises:
        ValueError: If any of the aggregation function calls return None.

    """
    inventory_cost: int | float = 0

    for case_id in case_ids:
        case_inventory_cost = cases_cost_indicators.inventory_cost(event_log, case_id, aggregation_mode)
        if case_inventory_cost is None:
            raise ValueError(f"Inventory cost calculation for case {case_id} returned None")
        inventory_cost += case_inventory_cost

    return inventory_cost


def expected_inventory_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the expected inventory cost for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The expected inventory cost for a group of cases.

    """
    group_inventory_cost = inventory_cost(event_log, case_ids, aggregation_mode)
    if group_inventory_cost is None:
        raise ValueError("Inventory cost calculation for group of cases returned None")
    case_group_count = groups_general_indicators.case_count(event_log, case_ids)
    return group_inventory_cost / case_group_count


def labor_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the labor cost for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The labor cost for a group of cases.

    Raises:
        ValueError: If any of the aggregation function calls return None.

    """
    labor_cost: int | float = 0

    for case_id in case_ids:
        case_labor_cost = cases_cost_indicators.labor_cost(event_log, case_id, aggregation_mode)
        if case_labor_cost is None:
            raise ValueError(f"Labor cost calculation for case {case_id} returned None")
        labor_cost += case_labor_cost

    return labor_cost


def expected_labor_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the expected labor cost for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The expected labor cost for a group of cases.

    """
    group_labor_cost = labor_cost(event_log, case_ids, aggregation_mode)
    if group_labor_cost is None:
        raise ValueError("Labor cost calculation for group of cases returned None")
    case_group_count = groups_general_indicators.case_count(event_log, case_ids)
    return group_labor_cost / case_group_count


def maintenance_cost(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float | None:
    """
    Calculate the maintenance cost for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        The maintenance cost for a group of cases.

    Raises:
        ValueError: If any of the cases has no maintenance cost.

    """
    maintenance_cost: int | float = 0

    for case_id in case_ids:
        case_maintenance_cost = cases_cost_indicators.maintenance_cost(event_log, case_id)
        if case_maintenance_cost is None:
            raise ValueError(f"Maintenance cost calculation for case {case_id} returned None")
        maintenance_cost += case_maintenance_cost

    return maintenance_cost


def expected_maintenance_cost(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float | None:
    """
    Calculate the expected maintenance cost for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        The expected maintenance cost for a group of cases.

    Raises:
        ValueError: If any of the cases has no maintenance cost.

    """
    group_maintenance_cost = maintenance_cost(event_log, case_ids)
    if group_maintenance_cost is None:
        raise ValueError("Maintenance cost calculation for group of cases returned None")
    case_group_count = groups_general_indicators.case_count(event_log, case_ids)
    return group_maintenance_cost / case_group_count


def missed_deadline_cost(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float | None:
    """
    Calculate the missed deadline cost for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        The missed deadline cost for a group of cases.

    Raises:
        ValueError: If any of the cases has no missed deadline cost.

    """
    missed_deadline_cost: int | float = 0

    for case_id in case_ids:
        case_missed_deadline_cost = cases_cost_indicators.missed_deadline_cost(event_log, case_id)
        if case_missed_deadline_cost is None:
            raise ValueError(f"Missed deadline cost calculation for case {case_id} returned None")
        missed_deadline_cost += case_missed_deadline_cost

    return missed_deadline_cost


def expected_missed_deadline_cost(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float | None:
    """
    Calculate the expected missed deadline cost for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        The expected missed deadline cost for a group of cases.

    Raises:
        ValueError: If any of the cases has no missed deadline cost.

    """
    group_missed_deadline_cost = missed_deadline_cost(event_log, case_ids)
    if group_missed_deadline_cost is None:
        raise ValueError("Missed deadline cost calculation for group of cases returned None")
    case_group_count = groups_general_indicators.case_count(event_log, case_ids)
    return group_missed_deadline_cost / case_group_count


def total_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the total cost for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The total cost for a group of cases.

    Raises:
        ValueError: If any of the aggregation function calls return None.

    """
    total_cost: int | float = 0

    for case_id in case_ids:
        case_total_cost = cases_cost_indicators.total_cost(event_log, case_id, aggregation_mode)
        if case_total_cost is None:
            raise ValueError(f"Total cost calculation for case {case_id} returned None")
        total_cost += case_total_cost

    return total_cost


def expected_total_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    Calculate the expected total cost for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The expected total cost for a group of cases.

    Raises:
        ValueError: If any of the cases has no total cost.

    """
    group_total_cost = total_cost(event_log, case_ids, aggregation_mode)
    if group_total_cost is None:
        raise ValueError("Total cost calculation for group of cases returned None")
    case_group_count = groups_general_indicators.case_count(event_log, case_ids)
    return group_total_cost / case_group_count


def resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    Calculate the resource count for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        The resource count for a group of cases.

    """
    resource_count: int = 0

    for case_id in case_ids:
        case_resource_count = cases_cost_indicators.resource_count(event_log, case_id)
        resource_count += case_resource_count

    return resource_count


def expected_resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    Calculate the expected resource count for a group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        The expected resource count for a group of cases.

    """
    group_resource_count = resource_count(event_log, case_ids)
    case_group_count = groups_general_indicators.case_count(event_log, case_ids)

    return group_resource_count / case_group_count


def labor_cost_and_total_cost_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float | None:
    """
    The ratio between the labor cost associated with all activity instances of the group of cases,
    and the total cost associated with all activity instances of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        The labor cost and total cost ratio of the group of cases.
        None: If the labor cost or the total cost is None.

    """
    _labor_cost = labor_cost(event_log, case_ids)
    _total_cost = total_cost(event_log, case_ids)
    if _labor_cost is None or _total_cost is None:
        return None
    return _labor_cost / _total_cost


def expected_labor_cost_and_total_cost_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float | None:
    """
    The expected ratio between the labor cost associated with all activity instances of the group of cases, and
    the total cost associated with all activity instances of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    Returns:
        The expected labor cost and total cost ratio of the group of cases.
        None: If the labor cost or the total cost is None.

    """
    # TODO: Check if this formula is correct.
    # Follow this format of checking for None or 0, for all ratio functions.
    _labor_cost = labor_cost(event_log, case_ids)
    _total_cost = total_cost(event_log, case_ids)
    if _labor_cost is None or _total_cost in [None, 0]:
        return None
    return _labor_cost / _total_cost


def automated_activity_cost(
    event_log: pd.DataFrame,
    case_ids: list[str] | set[str],
    aggregation_mode: Literal["sgl", "sum"],
    automated_activities: list[str] | set[str],
) -> int | float | None:
    """
    The total cost associated with all instantiations of automated activities in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        automated_activities: The list or set of automated activities.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The total cost associated with all instantiations of automated activities in the group of cases.
        None: If no automated activity cost is found.

    """
    automated_activities = set(automated_activities)

    total_cost = 0
    for case_id in case_ids:
        total_cost += cases_cost_indicators.automated_activity_cost(
            event_log, case_id, aggregation_mode, automated_activities
        )
    return total_cost


def expected_automated_activity_cost(
    event_log: pd.DataFrame,
    case_ids: list[str] | set[str],
    aggregation_mode: Literal["sgl", "sum"],
    automated_activities: list[str] | set[str],
) -> int | float | None:
    """
    The expected total cost associated with all instantiations of automated activities
    in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        automated_activities: The list or set of automated activities.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The expected total cost associated with all instantiations of automated activities
        in a case belonging to the group of cases.
        None: If no automated activity cost is found.

    """
    group_automated_activity_cost = automated_activity_cost(event_log, case_ids, aggregation_mode, automated_activities)
    if group_automated_activity_cost is None:
        return None
    case_group_count = groups_general_indicators.case_count(event_log, case_ids)
    return group_automated_activity_cost / case_group_count


def desired_activity_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], desired_activities: list[str] | set[str]
) -> int:
    """
    The number of instantiated activities whose occurrences is desirable in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        desired_activities: The list or set of desired activities.

    Returns:
        The number of instantiated activities whose occurrences is desirable in the group of cases.

    """
    desired_activities = set(desired_activities)
    desired_activity_count = 0
    for case_id in case_ids:
        desired_activity_count += cases_cost_indicators.desired_activity_count(event_log, case_id, desired_activities)
    return desired_activity_count


def expected_desired_activity_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], desired_activities: list[str] | set[str]
) -> int:
    """
    The expected number of instantiated activities whose occurence is desirable in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        desired_activities: The list or set of desired activities.

    Returns:
        The expected number of instantiated activities whose occurence is desirable in a case belonging to the group of cases.

    """
    group_desired_activity_count = desired_activity_count(event_log, case_ids, desired_activities)
    case_group_count = groups_general_indicators.case_count(event_log, case_ids)
    return group_desired_activity_count / case_group_count


def direct_cost(
    event_log: pd.DataFrame,
    case_ids: list[str] | set[str],
    aggregation_mode: Literal["sgl", "sum"],
    direct_costs_activities: list[str] | set[str],
) -> int | float | None:
    """
    The total cost associated with all instantiations of activities that have a
    direct effect on the outcome of a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        direct_costs_activities: The list or set of activities that have a direct effect on the outcome of cases in the group of cases.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    Returns:
        The total cost associated with all instantiations of activities that have a
        direct effect on the outcome of a case belonging to the group of cases.

    """
    total_cost = 0
    for case_id in case_ids:
        total_cost += cases_cost_indicators.direct_cost(event_log, case_id, aggregation_mode, direct_costs_activities)
    return total_cost


def expected_direct_cost(
    event_log: pd.DataFrame,
    case_ids: list[str] | set[str],
    aggregation_mode: Literal["sgl", "sum"],
    direct_costs_activities: list[str] | set[str],
) -> int | float | None:
    """
    The expected total cost associated with all instantiations of activities that have a
    direct effect on the outcome of a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.
        direct_costs_activities: The list or set of activities that have a direct effect on the outcome of cases in the group of cases.

    Returns:
        The expected total cost associated with all instantiations of activities that have a
        direct effect on the outcome of a case belonging to the group of cases.

    """
    group_direct_cost = direct_cost(event_log, case_ids, aggregation_mode, direct_costs_activities)
    if group_direct_cost is None:
        return None
    return group_direct_cost / groups_general_indicators.case_count(event_log, case_ids)
