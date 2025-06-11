from typing import Literal

import pandas as pd

import process_performance_indicators.utils.instances as instances_helpers
from process_performance_indicators.constants import StandardColumnNames


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
    complete_event = instances_helpers.cpl(event_log, instance_id)
    if not complete_event.empty:
        return complete_event[StandardColumnNames.TOTAL_COST].unique()[0]

    start_event = instances_helpers.start(event_log, instance_id)
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
    start_event = instances_helpers.start(event_log, instance_id)
    complete_event = instances_helpers.cpl(event_log, instance_id)

    if not start_event.empty and not complete_event.empty:
        return (
            start_event[StandardColumnNames.TOTAL_COST].unique()[0]
            + complete_event[StandardColumnNames.TOTAL_COST].unique()[0]
        )

    return None


def fixed_cost_for_single_events_of_activity_instances(event_log: pd.DataFrame, instance_id: str) -> int | float | None:
    """
    Calculate the fixed cost for single events of an activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        int |float: The fixed cost for single events of an activity instance.
        None: If no fixed cost is found.

    """
    complete_event = instances_helpers.cpl(event_log, instance_id)
    if not complete_event.empty:
        return complete_event[StandardColumnNames.FIXED_COST].unique()[0]

    start_event = instances_helpers.start(event_log, instance_id)
    if not start_event.empty:
        return start_event[StandardColumnNames.FIXED_COST].unique()[0]

    return None


def fixed_cost_for_sum_of_all_events_of_activity_instances(
    event_log: pd.DataFrame, instance_id: str
) -> int | float | None:
    """
    Calculate the fixed cost for the sum of all events of an activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        int | float: The fixed cost for the sum of all events of an activity instance.
        None: If no fixed cost is found.

    """
    start_event = instances_helpers.start(event_log, instance_id)
    complete_event = instances_helpers.cpl(event_log, instance_id)

    if not start_event.empty and not complete_event.empty:
        return (
            start_event[StandardColumnNames.FIXED_COST].unique()[0]
            + complete_event[StandardColumnNames.FIXED_COST].unique()[0]
        )

    return None


def inventory_cost_for_single_events_of_activity_instances(
    event_log: pd.DataFrame, instance_id: str
) -> int | float | None:
    """
    Calculate the inventory cost for single events of an activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        int | float: The inventory cost for single events of an activity instance.
        None: If no inventory cost is found.

    """
    complete_event = instances_helpers.cpl(event_log, instance_id)
    if not complete_event.empty:
        return complete_event[StandardColumnNames.INVENTORY_COST].unique()[0]

    start_event = instances_helpers.start(event_log, instance_id)
    if not start_event.empty:
        return start_event[StandardColumnNames.INVENTORY_COST].unique()[0]

    return None


def inventory_cost_for_sum_of_all_events_of_activity_instances(
    event_log: pd.DataFrame, instance_id: str
) -> int | float | None:
    """
    Calculate the inventory cost for the sum of all events of an activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        float: The inventory cost for the sum of all events of an activity instance.

    """
    start_event = instances_helpers.start(event_log, instance_id)
    complete_event = instances_helpers.cpl(event_log, instance_id)

    if not start_event.empty and not complete_event.empty:
        return (
            start_event[StandardColumnNames.INVENTORY_COST].unique()[0]
            + complete_event[StandardColumnNames.INVENTORY_COST].unique()[0]
        )

    return None


def labor_cost_for_single_events_of_activity_instances(event_log: pd.DataFrame, instance_id: str) -> int | float | None:
    """
    Calculate the labor cost for single events of an activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        int | float: The labor cost for single events of an activity instance.
        None: If no labor cost is found.

    """
    complete_event = instances_helpers.cpl(event_log, instance_id)
    if not complete_event.empty:
        return complete_event[StandardColumnNames.LABOR_COST].unique()[0]

    start_event = instances_helpers.start(event_log, instance_id)
    if not start_event.empty:
        return start_event[StandardColumnNames.LABOR_COST].unique()[0]

    return None


def labor_cost_for_sum_of_all_events_of_activity_instances(
    event_log: pd.DataFrame, instance_id: str
) -> int | float | None:
    """
    Calculate the labor cost for the sum of all events of an activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    Returns:
        int | float: The labor cost for the sum of all events of an activity instance.
        None: If no labor cost is found.

    """
    start_event = instances_helpers.start(event_log, instance_id)
    complete_event = instances_helpers.cpl(event_log, instance_id)

    if not start_event.empty and not complete_event.empty:
        return (
            start_event[StandardColumnNames.LABOR_COST].unique()[0]
            + complete_event[StandardColumnNames.LABOR_COST].unique()[0]
        )

    return None


def labor_cost_and_total_cost_ratio(
    event_log: pd.DataFrame, instance_id: str, aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    Calculate the labor cost and total cost ratio for an activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.
        aggregation_mode: The aggregation mode.
            "sgl": The aggregation mode for single events of an activity instance.
            "sum": The aggregation mode for the sum of all events of an activity instance.

    Returns:
        float: The labor cost and total cost ratio for an activity instance.

    """
    aggregation_function = {
        "sgl": (labor_cost_for_single_events_of_activity_instances, total_cost_for_single_events_of_activity_instances),
        "sum": (
            labor_cost_for_sum_of_all_events_of_activity_instances,
            total_cost_for_sum_of_all_events_of_activity_instances,
        ),
    }

    labor_cost = aggregation_function[aggregation_mode][0](event_log, instance_id)
    total_cost = aggregation_function[aggregation_mode][1](event_log, instance_id)

    return labor_cost / total_cost
