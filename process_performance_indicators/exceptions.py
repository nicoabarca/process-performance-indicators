class ColumnNotFoundError(Exception):
    """
    Exception raised when a column is not found in the event log.
    """


class ActivityNameNotFoundError(Exception):
    """
    Exception raised when an activity name is not found in the event log.
    """


class InstanceIdNotFoundError(Exception):
    """
    Exception raised when an instance id is not found in the event log.
    """
