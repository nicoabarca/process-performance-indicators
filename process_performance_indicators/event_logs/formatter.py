import pandas as pd
from schema import EventLogColumns


def formatter(event_log: pd.DataFrame, columns: EventLogColumns) -> pd.DataFrame:
    """
    Format an event log into a pandas DataFrame.

    Args:
        event_log: The event log to format.
        columns: The columns to use in the event log.
    Returns: The formatted event log.

    """
    event_log = event_log.rename(columns=columns.model_dump(by_alias=True))
    print(event_log)

    breakpoint()
    return event_log
