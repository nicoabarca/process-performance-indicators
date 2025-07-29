import pandas as pd


def activity_instance_and_human_resource_count_ratio(event_log: pd.DataFrame, activity_name: str) -> float:
    """
    The ratio between the number of times that a specific activity has been instantiated in the event log, and the number of human resources that are involved in the execution of the activity.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def client_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    The number of distinct clients associated with cases where the activity is instantiated.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def directly_follows_relations_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    The number of activities that have been instantiated directly after the activity of interest in the event log.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")


def human_resource_count(event_log: pd.DataFrame, activity_name: str) -> int:
    """
    The number of human resources that are involved in the execution of the activity.

    Args:
        event_log: The event log.
        activity_name: The name of the activity.

    """
    raise NotImplementedError("Not implemented yet.")
