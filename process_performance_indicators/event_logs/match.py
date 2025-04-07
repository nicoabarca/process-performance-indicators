import pandas as pd


def match(event_log: pd.DataFrame) -> pd.DataFrame:
    """
    Transform an event log into an explicit interval event log

    Args:
        event_log: The event log to transform.

    Returns:
        The explicit interval event log.

    """
