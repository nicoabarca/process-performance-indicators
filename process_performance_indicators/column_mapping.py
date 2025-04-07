from dataclasses import asdict, dataclass
from typing import ClassVar

from process_performance_indicators.constants import STANDARD_COLUMN_NAMES


@dataclass
class StandardColumnMapping:
    """
    Dataclass for mapping log columns to standard column names.
    Each field represents a standard column name, and the value is the corresponding column name in the log.
    """

    # Mandatory columns
    case_id_key: str
    activity_key: str
    timestamp_key: str

    # Optional columns
    start_timestamp_key: str | None = None
    total_cost_key: str | None = None
    human_resource_key: str | None = None
    role_key: str | None = None
    resource_key: str | None = None
    outcome_unit_key: str | None = None
    fixed_cost_key: str | None = None
    variable_cost_key: str | None = None
    labor_cost_key: str | None = None
    inventory_cost_key: str | None = None
    client_key: str | None = None
    maintenance_cost_key: str | None = None
    missed_deadline_cost_key: str | None = None
    transportation_cost_key: str | None = None
    warehousing_cost_key: str | None = None
    quality_key: str | None = None
    lifecycle_type_key: str | None = None
    instance_key: str | None = None

    _field_to_standard: ClassVar[dict[str, str]] = {
        "case_id_key": "case:concept:name",
        "activity_key": "concept:name",
        "timestamp_key": "time:timestamp",
        "start_timestamp_key": "start_timestamp",
        "total_cost_key": "cost:total",
        "human_resource_key": "human_resource",
        "role_key": "org:role",
        "resource_key": "org:resource",
        "outcome_unit_key": "outcome_unit",
        "fixed_cost_key": "cost:fixed",
        "variable_cost_key": "cost:variable",
        "labor_cost_key": "cost:labor",
        "inventory_cost_key": "cost:inventory",
        "client_key": "client",
        "maintenance_cost_key": "cost:maintenance",
        "missed_deadline_cost_key": "cost:missed_deadline",
        "transportation_cost_key": "cost:transportation",
        "warehousing_cost_key": "cost:warehousing",
        "quality_key": "quality",
        "lifecycle_type_key": "lifecycle:transition",
        "instance_key": "concept:instance",
    }

    def to_standard_mapping(self) -> dict[str, str]:
        """
        Convert the dataclass to a log-to-standard mapping dictionary.

        Returns:
            Dict[str, str]: A dictionary where keys are standard column names and values are log column names.

        """
        mapping = {}
        for field_name, field_value in asdict(self).items():
            if field_value is not None and field_name in self._field_to_standard:
                standard_name = self._field_to_standard[field_name]
                mapping[standard_name] = field_value
        return mapping


def convert_to_standard_mapping(mapping: dict[str, str] | StandardColumnMapping) -> dict[str, str]:
    """
    Convert either a dictionary or StandardColumnMapping instance to a standard column mapping dictionary.

    Args:
        mapping: Either a dictionary mapping standard column names to log column names,
                or a StandardColumnMapping instance.

    Returns:
        Dict[str, str]: A dictionary where keys are standard column names and values are log column names.

    """
    if isinstance(mapping, dict):
        return mapping
    return mapping.to_standard_mapping()


def validate_column_mapping(mapping: dict[str, str]) -> bool:
    """
    Validate the column mapping to ensure all keys are standard column names.

    Args:
        mapping: The column mapping to validate with standard column names as keys.

    Returns:
        bool: True if the mapping is valid.

    Raises:
        ValueError: If any key in the mapping is not a standard column name.

    """
    for key in mapping:
        if key not in STANDARD_COLUMN_NAMES:
            raise ValueError(f"Column name {key} is not a standard column name.")
    return True
