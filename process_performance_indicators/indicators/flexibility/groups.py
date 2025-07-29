import pandas as pd


def activity_and_role_count_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The ratio between the number of activities that occur in the group of cases, and the number of human resources that are involved in the execution of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_activity_and_role_count_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The ratio between the expected number of activities that occur in a case belonging to the group of cases, and the expected number of human resource roles that are involved in the execution of a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def activity_instance_and_human_resource_count_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The ratio between the number of times that any activity has been instantiated in the group of cases, and the number of human resources that are involved in the execution of cases in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_activity_instance_and_human_resource_count_ratio(
    event_log: pd.DataFrame, case_ids: list[str] | set[str]
) -> float:
    """
    The ratio between the expected number of times that any activity is instantiated in a case belonging to the group of cases, an the expected number of huma resources that are involed in the execution of a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def client_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of distinct clients associated with cases in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_client_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The ratio between the number of distinct clients associated with cases in the group cases, and the number of cases belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def directly_follows_relations_and_activity_count_ratio(
    event_log: pd.DataFrame, case_ids: list[str] | set[str]
) -> float:
    """
    The ratio between the number of activity pairs where one has been instantiated directly after the other in the group of cases, and the number of activities that occur in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_directly_follows_relations_and_activity_count_ratio(
    event_log: pd.DataFrame, case_ids: list[str] | set[str]
) -> float:
    """
    The ratio between the epected number of activity pairs where one has been instantiated directly after the other in a case belonging to the group of cases, and the expected number of activities that occur in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def directly_follows_relations_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of activity pairs where one has been instantiated directly after the other in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_directly_follows_relations_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The expected number of activity pairs where one has been instantiated directly after the other in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def human_resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of human resources that are involved in the execution of cases in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_human_resource_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The expected number of human resources that are involved in the execution of a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def optional_activity_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of optional activities that are instantiated in the group of cases. An activity is considered optional if there is at least one case in the event log where it does not occur.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_optional_activity_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The expected number of optional activities that are instantiated in a case belonging to the group of cases. An activity is considered optional if there is at least one case in the event log where it does not occur.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def optionality(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The ratio between the number of optional activities that are instantiated in the group of cases, and the number of activities that occur in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_optionality(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The ratio between the expected number of optional activities that are instantiated in a case belonging to the group of cases, and the expected number of activities that occur in a case belonging to the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def role_and_variant_count_ratio(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The ratio between the number of human resource roles that are involved in the execution of the case, and the number of variants that are observed for the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def role_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of human resource roles that are involed in the execution of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def expected_role_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The expected number of human resource roles that are involed in the execution of the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def variant_case_coverage(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> float:
    """
    The percentage of cases in the event log who possess the same variant as any case in the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")


def variant_count(event_log: pd.DataFrame, case_ids: list[str] | set[str]) -> int:
    """
    The number of variants that are observed for the group of cases.

    Args:
        event_log: The event log.
        case_ids: The case IDs.

    """
    raise NotImplementedError("Not implemented yet.")
