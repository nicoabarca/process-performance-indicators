from typing import Literal

import pandas as pd

import process_performance_indicators.utils.instances as instances_utils
from process_performance_indicators.constants import StandardColumnNames
from process_performance_indicators.utils.safe_division import safe_divide


def fixed_cost_for_single_events_of_activity_instances(event_log: pd.DataFrame, instance_id: str) -> float | None:
    """
    The fixed cost associated with an activity instance, measured as the latest recorded value
    among the events of the activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        float: The fixed cost for single events of an activity instance.
        None: If no fixed cost is found.

    """
    complete_event = instances_utils.cpl(event_log, instance_id)
    if not complete_event.empty:
        return float(complete_event[StandardColumnNames.FIXED_COST].unique()[0])

    start_event = instances_utils.start(event_log, instance_id)
    if not start_event.empty:
        return float(start_event[StandardColumnNames.FIXED_COST].unique()[0])

    return None


def fixed_cost_for_sum_of_all_events_of_activity_instances(event_log: pd.DataFrame, instance_id: str) -> float | None:
    """
    The fixed cost associated with an activity instance, measured as the sum of
    all values among the events of the activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    """
    start_event = instances_utils.start(event_log, instance_id)
    complete_event = instances_utils.cpl(event_log, instance_id)

    if not start_event.empty and not complete_event.empty:
        return float(
            start_event[StandardColumnNames.FIXED_COST].unique()[0]
            + complete_event[StandardColumnNames.FIXED_COST].unique()[0]
        )

    return None


def inventory_cost_for_single_events_of_activity_instances(event_log: pd.DataFrame, instance_id: str) -> float | None:
    """
    The inventory cost associated with an activity instance, measured as the latest
    recorded value among the events of the activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    """
    complete_event = instances_utils.cpl(event_log, instance_id)
    if not complete_event.empty:
        return float(complete_event[StandardColumnNames.INVENTORY_COST].unique()[0])

    start_event = instances_utils.start(event_log, instance_id)
    if not start_event.empty:
        return float(start_event[StandardColumnNames.INVENTORY_COST].unique()[0])

    return None


def inventory_cost_for_sum_of_all_events_of_activity_instances(
    event_log: pd.DataFrame, instance_id: str
) -> float | None:
    """
    The inventory cost associated with an activity instance, measured as the sum of
    all values among the events of the activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    """
    start_event = instances_utils.start(event_log, instance_id)
    complete_event = instances_utils.cpl(event_log, instance_id)

    if not start_event.empty and not complete_event.empty:
        return float(
            start_event[StandardColumnNames.INVENTORY_COST].unique()[0]
            + complete_event[StandardColumnNames.INVENTORY_COST].unique()[0]
        )

    return None


def labor_cost_and_total_cost_ratio(
    event_log: pd.DataFrame, instance_id: str, aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The ratio between the labor cost associated with the activity instance, and the total cost
    associated with the activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.
        aggregation_mode: The aggregation mode.
            "sgl": The aggregation mode for single events of an activity instance.
            "sum": The aggregation mode for the sum of all events of an activity instance.

    """
    aggregation_functions = {
        "sgl": (
            labor_cost_for_single_events_of_activity_instances,
            total_cost_for_single_events_of_activity_instances,
        ),
        "sum": (
            labor_cost_for_sum_of_all_events_of_activity_instances,
            total_cost_for_sum_of_all_events_of_activity_instances,
        ),
    }

    labor_cost_func, total_cost_func = aggregation_functions[aggregation_mode]
    labor_cost = labor_cost_func(event_log, instance_id)
    total_cost = total_cost_func(event_log, instance_id)

    return safe_divide(labor_cost, total_cost)


def labor_cost_for_single_events_of_activity_instances(event_log: pd.DataFrame, instance_id: str) -> float | None:
    """
    The labor cost associated with an activity instance, measured as the lastest recorded value among the events
    of the activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    """
    complete_event = instances_utils.cpl(event_log, instance_id)
    if not complete_event.empty:
        return float(complete_event[StandardColumnNames.LABOR_COST].unique()[0])

    start_event = instances_utils.start(event_log, instance_id)
    if not start_event.empty:
        return float(start_event[StandardColumnNames.LABOR_COST].unique()[0])

    return None


def labor_cost_for_sum_of_all_events_of_activity_instances(event_log: pd.DataFrame, instance_id: str) -> float | None:
    """
    The labor cost associated with an activity instance, measured as the sum of
    all values among the events of the activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    """
    start_event = instances_utils.start(event_log, instance_id)
    complete_event = instances_utils.cpl(event_log, instance_id)

    if not start_event.empty and not complete_event.empty:
        return float(
            start_event[StandardColumnNames.LABOR_COST].unique()[0]
            + complete_event[StandardColumnNames.LABOR_COST].unique()[0]
        )

    return None


def total_cost_for_single_events_of_activity_instances(event_log: pd.DataFrame, instance_id: str) -> int | float | None:
    """
    Calculate the total cost for single events of an activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        int | float: The total cost for single events of an activity instance.
        None: If no total cost is found.

    """
    complete_event = instances_utils.cpl(event_log, instance_id)
    if not complete_event.empty:
        return complete_event[StandardColumnNames.TOTAL_COST].unique()[0]

    start_event = instances_utils.start(event_log, instance_id)
    if not start_event.empty:
        return start_event[StandardColumnNames.TOTAL_COST].unique()[0]

    return None


def total_cost_for_sum_of_all_events_of_activity_instances(
    event_log: pd.DataFrame, instance_id: str
) -> int | float | None:
    """
    Calculate the total cost for the sum of all events of an activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        int | float: The total cost for the sum of all events of an activity instance.
        None: If no total cost is found.

    """
    start_event = instances_utils.start(event_log, instance_id)
    complete_event = instances_utils.cpl(event_log, instance_id)

    if not start_event.empty and not complete_event.empty:
        return (
            start_event[StandardColumnNames.TOTAL_COST].unique()[0]
            + complete_event[StandardColumnNames.TOTAL_COST].unique()[0]
        )

    return None
