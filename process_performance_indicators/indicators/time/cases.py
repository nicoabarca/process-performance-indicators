import pandas as pd

import process_performance_indicators.indicators.time.instances as time_instances_indicators
import process_performance_indicators.utils.cases as cases_utils
import process_performance_indicators.utils.instances as instances_utils
from process_performance_indicators.utils.safe_division import safe_division


def active_time(event_log: pd.DataFrame, case_id: str) -> pd.Timedelta:
    """
    Todo: Implement this function. Ask for explanation.
    """
    raise NotImplementedError("Not implemented yet")


def activity_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of activities that occur in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    return len(cases_utils.act(event_log, case_id))


def activity_instance_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of times that any activity has been instantiated in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    return len(cases_utils.inst(event_log, case_id))


def automated_activity_count(event_log: pd.DataFrame, case_id: str, automated_activities: set[str]) -> int:
    """
    The number of automated activities that occur in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        automated_activities: The set of automated activities.

    """
    case_activities = cases_utils.act(event_log, case_id)
    return len(automated_activities.intersection(case_activities))


def automated_activity_instance_count(event_log: pd.DataFrame, case_id: str, automated_activities: set[str]) -> int:
    """
    The number of times that an automated activity is instantiated in the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        automated_activities: The set of automated activities.

    """
    case_instances = cases_utils.inst(event_log, case_id)
    instances_of_automated_activities = set()
    for instance in case_instances:
        if instances_utils.act(event_log, instance) in automated_activities:
            instances_of_automated_activities.add(instance)
    return len(instances_of_automated_activities)


def automated_activity_service_time(
    event_log: pd.DataFrame, case_id: str, automated_activities: set[str]
) -> pd.Timedelta:
    """
    The sum of elapsed times for all instantiations of automated activities in the case.

    Args:
        event_log: The event log.
        case_id: The case ID.
        automated_activities: The set of automated activities.

    """
    raise NotImplementedError("Not implemented yet")


def handover_count(event_log: pd.DataFrame, case_id: str) -> int:
    """
    The number of times that a human resource associated with an activity instance
    differs from the human resource associated with the preceding activity instance
    within the case.

    Args:
        event_log: The event log.
        case_id: The case ID.

    """
    raise NotImplementedError("Not implemented yet")


def idle_time(event_log: pd.DataFrame, case_id: str) -> pd.Timedelta:
    """
    TODO: Implement this function. Ask for explanation.
    """
    raise NotImplementedError("Not implemented yet")


def lead_time(event_log: pd.DataFrame, case_id: str) -> pd.Timedelta:
    """
    The total elapsed time between the earliest and latest timestamps in the case.

    Args:
        event_log: The event log.
        case_id: The case id.

    """
    return cases_utils.endt(event_log, case_id) - cases_utils.startt(event_log, case_id)


def lead_time_deviation_from_deadline(event_log: pd.DataFrame, case_id: str, deadline: pd.Timedelta) -> pd.Timedelta:
    """
    The difference between the time that the case is expected to take, and the actual elapsed time between
    its earliest and latest timestamps. Negative values indicate that the case took less time than expected.

    Args:
        event_log: The event log.
        case_id: The case id.
        deadline: The expected time the case is expected to take.

    """
    return deadline - lead_time(event_log, case_id)


def lead_time_deviation_from_expectation(
    event_log: pd.DataFrame, case_id: str, expectation: pd.Timedelta
) -> pd.Timedelta:
    """
    The absolute value of the difference between the time that the case is expected to take,
    and the actual elapsed time between its earliest and latest timestamps.

    Args:
        event_log: The event log.
        case_id: The case id.
        expectation: The time delta the case is expected to take.

    """
    return abs(expectation - lead_time(event_log, case_id))


def lead_time_from_activity_a(event_log: pd.DataFrame, case_id: str, activity_a: str) -> pd.Timedelta:
    """
    The total elapsed time between the earliest instantiations of a specific activity, and
    the latest activity instance, in the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        activity_a: The specific activity name.

    """
    raise NotImplementedError("Not implemented yet")


def lead_time_from_activity_a_to_b(
    event_log: pd.DataFrame, case_id: str, activity_a: str, activity_b: str
) -> pd.Timedelta:
    """
    The total elapsed time between the earliest instantiations of a specific activity, and the earliest
    instantiations of another specific activity that precedes the other, in the case. Here "activity a precedes activity b".

    Args:
        event_log: The event log.
        case_id: The case id.
        activity_a: The specific activity name that precedes activity b.
        activity_b: The specific activity name that follows activity a.

    """
    raise NotImplementedError("Not implemented yet")


def lead_time_to_activity_a(event_log: pd.DataFrame, case_id: str, activity_a: str) -> pd.Timedelta:
    """
    The total elapsed time between the earliest activity instance, and the earliest instantiations of a specific activity,
    in the case.

    Args:
        event_log: The event log.
        case_id: The case id.
        activity_a: The specific activity name.

    """
    raise NotImplementedError("Not implemented yet")


def service_and_lead_time_ratio(event_log: pd.DataFrame, case_id: str) -> float:
    """
    The ratio between the sum of elapsed times between the start and complete events of
    all activity instance of the case, and the total elapsed time between the earliest and latest timestamps in the case.

    Args:
        event_log: The event log.
        case_id: The case id.

    """
    return safe_division(service_time(event_log, case_id), lead_time(event_log, case_id))


def service_time(event_log: pd.DataFrame, case_id: str) -> pd.Timedelta:
    """
    The sum of elapsed times between the start and complete events of all activity instances of the case.

    Args:
        event_log: The event log.
        case_id: The case id.

    """
    sum_of_service_times_in_minutes = 0
    for instance_id in cases_utils.inst(event_log, case_id):
        sum_of_service_times_in_minutes += time_instances_indicators.service_time(
            event_log, instance_id
        ) / pd.Timedelta(minutes=1)
    return pd.Timedelta(minutes=sum_of_service_times_in_minutes)


def service_time_from_activity_a_to_b(
    event_log: pd.DataFrame, case_id: str, activity_a: str, activity_b: str
) -> pd.Timedelta:
    """
    The sum elapsed times between the start and complete events of all activity instances of the case,
    which occur between the earliest instantiations of a specific activity, and the earliest instantiations
    of another specific activity that precedes the other. Here "activity a precedes activity b".

    Args:
        event_log: The event log.
        case_id: The case id.
        activity_a: The specific activity name that precedes activity b.
        activity_b: The specific activity name that follows activity a.

    """
    raise NotImplementedError("Not implemented yet")


def waiting_time(event_log: pd.DataFrame, case_id: str) -> pd.Timedelta:
    """
    The sum, for every activity instance in the case, of the elapsed time between
    the complete event of the activity instance that precedes it, and its start event.
    """
    raise NotImplementedError("Not implemented yet")


def waiting_time_from_activity_a_to_b(
    event_log: pd.DataFrame, case_id: str, activity_a: str, activity_b: str
) -> pd.Timedelta:
    """
    The sum, for every activity instance in the case that occurs between the earliest
    instantiations of a specific activity, and the earliest instantiations of another specific activity
    that precedes the other, of the elapsed time between the complete event of the activity instance that precedes it,
    and its start event.

    Args:
        event_log: The event log.
        case_id: The case id.
        activity_a: The specific activity name that precedes activity b.
        activity_b: The specific activity name that follows activity a.

    """
    raise NotImplementedError("Not implemented yet")
