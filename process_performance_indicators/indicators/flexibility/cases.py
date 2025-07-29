import pandas as pd


def activity_and_role_count_ratio(event_log: pd.DataFrame, case_id: str) -> float:
    """
    The ratio between the number of activities that occur in the case, and the number of human resources
    that are involved in the execution of the case

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def activity_instance_and_human_resource_count_ratio(event_log: pd.DataFrame, case_id: str) -> float:
    """
    The ratio between the number of times that any activity has been instantiated in the case, and the number of human resources that are involved in the execution of the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def directly_follows_relations_and_activity_count_ratio(event_log: pd.DataFrame, case_id: str) -> float:
    """
    The ratio between the number of activity pairs where one has been instantiated directly after the other in the case, and the number of activities that occur in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def directly_follows_relations_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of activity pairs where one has been instantiated directly after the other in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def human_resource_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of human resources that are involved in the execution of the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def optional_activity_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of optional activities that are instantiated in the case. An activity is considered optional if there is at least one case in the event log where it does not occur.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def optionality(event_log: pd.DataFrame, case_id: str) -> float:
    """
    The ratio between the number of optional activities that are instantiated in the case, and the number of activities that occur in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def role_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of human resource roles that are involved in the execution of the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")


def variant_case_coverage(event_log: pd.DataFrame, case_id: str) -> float:
    """
    The percentage of cases in the event log who possess the same variant as the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet.")
