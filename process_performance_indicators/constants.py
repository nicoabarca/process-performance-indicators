from enum import Enum


class StandardColumnNames(str, Enum):
    """Enum representing standard column names in process mining event logs."""

    CASE_ID = "case:concept:name"
    ACTIVITY = "concept:name"
    TIMESTAMP = "time:timestamp"
    START_TIMESTAMP = "start_timestamp"
    TOTAL_COST = "cost:total"
    HUMAN_RESOURCE = "human_resource"
    ROLE = "org:role"
    ORG_RESOURCE = "org:resource"
    OUTCOME_UNIT = "outcome_unit"
    FIXED_COST = "cost:fixed"
    VARIABLE_COST = "cost:variable"
    LABOR_COST = "cost:labor"
    INVENTORY_COST = "cost:inventory"
    CLIENT = "client"
    MAINTENANCE_COST = "cost:maintenance"
    MISSED_DEADLINE_COST = "cost:missed_deadline"
    TRANSPORTATION_COST = "cost:transportation"
    WAREHOUSING_COST = "cost:warehousing"
    QUALITY = "quality"
    LIFECYCLE_TRANSITION = "lifecycle:transition"
    INSTANCE = "concept:instance"

    def __str__(self) -> str:
        return self.value

    def to_string(self) -> str:
        return self.__str__()


class LifecycleTransitionType(str, Enum):
    """Enum representing the lifecycle transition of an event."""

    START = "start"
    COMPLETE = "complete"

    def __str__(self) -> str:
        return self.value

    def to_string(self) -> str:
        return self.__str__()
