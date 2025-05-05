from typing import Literal

import pandas as pd

import process_performance_indicators.cost.instances as instances_cost_indicators
import process_performance_indicators.helpers.cases as cases_helpers


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

    """
    aggregation_function = {
        "sgl": instances_cost_indicators.fixed_cost_for_single_events_of_activity_instances,
        "sum": instances_cost_indicators.fixed_cost_for_sum_of_all_events_of_activity_instances,
    }
    fixed_cost = 0

    for instance_id in cases_helpers.inst(event_log, case_id):
        fixed_cost += aggregation_function[aggregation_mode](event_log, instance_id)

    return fixed_cost
