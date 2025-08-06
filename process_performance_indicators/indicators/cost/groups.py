from typing import Literal

import pandas as pd

import process_performance_indicators.indicators.cost.cases as cost_cases_indicators
import process_performance_indicators.indicators.general.cases as cases_utils
import process_performance_indicators.indicators.general.groups as general_groups_indicators
from process_performance_indicators.utils.safe_division import safe_divide


def automated_activity_cost(
    event_log: pd.DataFrame,
    case_ids: list[str] | set[str],
    automated_activities: set[str],
    aggregation_mode: Literal["sgl", "sum"],
) -> int | float:
    """
    The total cost associated with all instantiations of automated activities in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        automated_activities: The set of automated activities.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    total_cost = 0
    for case_id in case_ids:
        total_cost += cost_cases_indicators.automated_activity_cost(
            event_log, case_id, automated_activities, aggregation_mode
        )
    return total_cost


def expected_automated_activity_cost(
    event_log: pd.DataFrame,
    case_ids: list[str] | set[str],
    automated_activities: set[str],
    aggregation_mode: Literal["sgl", "sum"],
) -> int | float:
    """
    The expected total cost associated with all instantiations of automated activities
    in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        automated_activities: The set of automated activities.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    group_automated_activity_cost = automated_activity_cost(event_log, case_ids, automated_activities, aggregation_mode)
    case_group_count = general_groups_indicators.case_count(event_log, case_ids)
    return safe_divide(group_automated_activity_cost, case_group_count)


def desired_activity_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], desired_activities: set[str]
) -> int:
    """
    The number of instantiated activities whose occurrence is desirable in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        desired_activities: The set of desired activities.

    """
    desired_activity_count = 0
    for case_id in case_ids:
        desired_activity_count += cost_cases_indicators.desired_activity_count(event_log, case_id, desired_activities)
    return desired_activity_count


def expected_desired_activity_count(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], desired_activities: set[str]
) -> int:
    """
    The expected number of instantiated activities whose occurrence is desirable in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        desired_activities: The set of desired activities.

    """
    numerator = desired_activity_count(event_log, case_ids, desired_activities)
    denominator = general_groups_indicators.case_count(event_log, case_ids)
    return safe_divide(numerator, denominator)


def direct_cost(
    event_log: pd.DataFrame,
    case_ids: list[str] | set[str],
    direct_costs_activities: set[str],
    aggregation_mode: Literal["sgl", "sum"],
) -> int | float:
    """
    The total cost associated with all instantiations of activities that have a
    direct effect on the outcome of a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        direct_costs_activities: The set of activities that have a direct effect on the outcome of the group of cases.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    total_cost = 0
    for case_id in case_ids:
        total_cost += cost_cases_indicators.direct_cost(event_log, case_id, direct_costs_activities, aggregation_mode)
    return total_cost


def expected_direct_cost(
    event_log: pd.DataFrame,
    case_ids: list[str] | set[str],
    direct_costs_activities: set[str],
    aggregation_mode: Literal["sgl", "sum"],
) -> int | float:
    """
    The expected total cost associated with all instantiations of activities that have a
    direct effect on the outcome of a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        direct_costs_activities: The set of activities that have a direct effect on the outcome of the group of cases.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    numerator = direct_cost(event_log, case_ids, direct_costs_activities, aggregation_mode)
    denominator = general_groups_indicators.case_count(event_log, case_ids)
    return safe_divide(numerator, denominator)


def fixed_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The fixed cost associated with all activity instances of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    total_fixed_cost = 0

    for case_id in case_ids:
        total_fixed_cost += cost_cases_indicators.fixed_cost(event_log, case_id, aggregation_mode)

    return total_fixed_cost


def expected_fixed_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    The expected fixed cost associated with all activity instances of a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    numerator = fixed_cost(event_log, case_ids, aggregation_mode)
    denominator = general_groups_indicators.case_count(event_log, case_ids)
    return safe_divide(numerator, denominator)


def human_resource_and_case_count_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float | None:
    """
    The ratio between the number of human resources that are involved in the execution
    of cases in the group of cases, and the number of cases belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    """
    numerator = human_resource_count(event_log, case_ids)
    denominator = general_groups_indicators.case_count(event_log, case_ids)
    return safe_divide(numerator, denominator)


def human_resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of human resources that are involved in the execution of cases in
    the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    """
    count = 0
    for case_id in case_ids:
        count += len(cases_utils.hres(event_log, case_id))
    return count


def expected_human_resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The expected number of human resources that are involved in the execution of cases
    belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    """
    count = 0
    for case_id in case_ids:
        count += cost_cases_indicators.human_resource_count(event_log, case_id)

    numerator = count
    denominator = general_groups_indicators.case_count(event_log, case_ids)
    return safe_divide(numerator, denominator)


def inventory_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The inventory cost associated with all activity instances of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    total_inventory_cost = 0

    for case_id in case_ids:
        total_inventory_cost += cost_cases_indicators.inventory_cost(event_log, case_id, aggregation_mode)

    return total_inventory_cost


def expected_inventory_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The expected inventory cost associated with all activity instances of a case
    belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    numerator = inventory_cost(event_log, case_ids, aggregation_mode)
    denominator = general_groups_indicators.case_count(event_log, case_ids)
    return safe_divide(numerator, denominator)


def labor_cost_and_total_cost_ratio(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The ratio between the labor cost associated with all activity instances of the group of cases,
    and the total cost associated with all activity instances of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    return safe_divide(
        labor_cost(event_log, case_ids, aggregation_mode),
        total_cost(event_log, case_ids, aggregation_mode),
    )


def expected_labor_cost_and_total_cost_ratio(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The expected ratio between the labor cost associated with all activity instances of the group of cases,
    and the total cost associated with all activity instances of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    return safe_divide(
        labor_cost(event_log, case_ids, aggregation_mode),
        total_cost(event_log, case_ids, aggregation_mode),
    )


def labor_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The labor cost associated with all activity instances of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    total_labor_cost = 0

    for case_id in case_ids:
        total_labor_cost += cost_cases_indicators.labor_cost(event_log, case_id, aggregation_mode)

    return total_labor_cost


def expected_labor_cost(
    event_log: pd.DataFrame, case_ids: list[str] | set[str], aggregation_mode: Literal["sgl", "sum"]
) -> int | float | None:
    """
    The expected labor cost associated with all activity instances of a case
    belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    return safe_divide(
        labor_cost(event_log, case_ids, aggregation_mode),
        general_groups_indicators.case_count(event_log, case_ids),
    )


def maintenance_cost(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The maintenance cost associated with all cases in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    """
    total_maintenance_cost = 0

    for case_id in case_ids:
        total_maintenance_cost += cost_cases_indicators.maintenance_cost(event_log, case_id)

    return total_maintenance_cost


def expected_maintenance_cost(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The expected maintenance cost associated with a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    """
    return safe_divide(maintenance_cost(event_log, case_ids), general_groups_indicators.case_count(event_log, case_ids))


def missed_deadline_cost(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float | None:
    """
    The cost for missing deadlines associated with all cases in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    """
    total_missed_deadline_cost = 0

    for case_id in case_ids:
        total_missed_deadline_cost += cost_cases_indicators.missed_deadline_cost(event_log, case_id)

    return total_missed_deadline_cost


def expected_missed_deadline_cost(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int | float | None:
    """
    The expected cost for missing deadlines associated with a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    """
    return safe_divide(
        missed_deadline_cost(event_log, case_ids),
        general_groups_indicators.case_count(event_log, case_ids),
    )


def overhead_cost(
    event_log: pd.DataFrame,
    case_ids: list[str] | set[str],
    direct_cost_activities: set[str],
    aggregation_mode: Literal["sgl", "sum"],
) -> float:
    """
    The total cost associated with all instantiations of activities that do not
    have a direct effect on the outcome of the cases in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        direct_cost_activities: The set of activities that have a direct cost
            on the outcome of the cases.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    total_overhead_cost = 0
    for case_id in case_ids:
        total_overhead_cost += cost_cases_indicators.overhead_cost(
            event_log, case_id, direct_cost_activities, aggregation_mode
        )
    return total_overhead_cost


def expected_overhead_cost(
    event_log: pd.DataFrame,
    case_ids: list[str] | set[str],
    direct_cost_activities: set[str],
    aggregation_mode: Literal["sgl", "sum"],
) -> float:
    """
    The total cost associated with all instantiations of activities that do not have a
    direct effect on the outcome of case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.
        direct_cost_activities: The set of activities that have a direct cost
            on the outcome of the cases.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for cost calculations.
            "sum": Considers the sum of all events of activity instances for cost calculations.

    """
    return safe_divide(
        overhead_cost(event_log, case_ids, direct_cost_activities, aggregation_mode),
        general_groups_indicators.case_count(event_log, case_ids),
    )


def resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of resources that are involved in the execution of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    """
    resources = set()
    for case_id in case_ids:
        resources.update(cases_utils.res(event_log, case_id))
    return len(resources)


def expected_resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The expected number of resources that are involved in the execution of a case belonging
    to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    """
    resource_count = 0
    for case_id in case_ids:
        resource_count += cost_cases_indicators.resource_count(event_log, case_id)
    return safe_divide(resource_count, general_groups_indicators.case_count(event_log, case_ids))


def rework_cost(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The total cost of all times that any activity has been instantiated again, after its first
    instantiation, in every case of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    """
    raise NotImplementedError("Not implemented yet")


def expected_rework_cost(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The expected total cost of all times that any activity has been instantiated again, after
    its first instantiation, in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case ids.

    """
    raise NotImplementedError("Not implemented yet")


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
        case_total_cost = cost_cases_indicators.total_cost(event_log, case_id, aggregation_mode)
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
    case_group_count = general_groups_indicators.case_count(event_log, case_ids)
    return group_total_cost / case_group_count
