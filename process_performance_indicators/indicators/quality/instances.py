from typing import Literal

import pandas as pd


def outcome_unit_count_considering_single_events_of_activity_instances(
    event_log: pd.DataFrame, instance_id: str
) -> int:
    """
    The outcome units associated with an activity instance, measured as the latest recorded value among the events of the activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    """
    raise NotImplementedError("Not implemented yet.")


def outcome_unit_count_considering_sum_of_all_events_of_activity_instances(
    event_log: pd.DataFrame, instance_id: str
) -> int:
    """
    The outcome units associated with an activity instance, measured as the sum of all values among the events of the activity instance.

    Args:
        event_log: The event log.
        instance_id: The instance id.

    """
    raise NotImplementedError("Not implemented yet.")


def successful_outcome_unit_count(
    event_log: pd.DataFrame, instance_id: str, aggregation_mode: Literal["sgl", "sum"]
) -> int:
    """
    The outcome units associated with an activity instance, after deducting those that were unsuccessfully completed.

    Args:
        event_log: The event log.
        instance_id: The instance id.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def successful_outcome_unit_percentage(
    event_log: pd.DataFrame, instance_id: str, aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The percentage of outcome units associated with an activity instance that were successfully completed.

    Args:
        event_log: The event log.
        instance_id: The instance id.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")


def total_cost_and_client_count_ratio(
    event_log: pd.DataFrame, instance_id: str, aggregation_mode: Literal["sgl", "sum"]
) -> float:
    """
    The ratio between the total cost associated with all instantiations of the activity, and the number of distinct clients associated with cases where the activity is instantiated.

    Args:
        event_log: The event log.
        instance_id: The instance id.
        aggregation_mode: The aggregation mode.
            "sgl": Considers single events of activity instances for outcome unit count calculations.
            "sum": Considers the sum of all events of activity instances for outcome unit count calculations.

    """
    raise NotImplementedError("Not implemented yet.")
