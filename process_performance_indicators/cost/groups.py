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

    """
    fixed_cost = 0

    for case_id in case_ids:
        fixed_cost += cases_cost_indicators.fixed_cost(event_log, case_id, aggregation_mode)

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

    """
    inventory_cost = 0

    for case_id in case_ids:
        inventory_cost += cases_cost_indicators.inventory_cost(event_log, case_id, aggregation_mode)

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
    case_group_count = groups_general_indicators.case_count(event_log, case_ids)
    return group_inventory_cost / case_group_count
