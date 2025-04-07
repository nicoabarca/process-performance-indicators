from pandas import Timestamp
from pydantic import BaseModel, Field


class EventLogColumns(BaseModel):
    # Mandatory columns
    case_id_key: str = Field(alias="case:concept:name")
    activity_key: str = Field(alias="concept:name")
    timestamp_key: Timestamp = Field(alias="time:timestamp")

    # Optional columns
    start_timestamp_key: Timestamp | None = Field(default=None, alias="start_timestamp")
    total_cost_key: int | float | None = Field(default=None, alias="cost:total")
    human_resource_key: str | None = Field(default=None, alias="human_resource")
    lifecycle_type_key: str | None = Field(default=None, alias="lifecycle:transition")
    instance_key: str | None = Field(default=None, alias="concept:instance")
    role_key: str | None = Field(default=None, alias="org:role")
    resource_key: str | None = Field(default=None, alias="org:resource")
    outcome_unit_key: str | None = Field(default=None, alias="outcome_unit")
    fixed_cost_key: int | float | None = Field(default=None, alias="cost:fixed")
    variable_cost_key: int | float | None = Field(default=None, alias="cost:variable")
    labor_cost_key: int | float | None = Field(default=None, alias="cost:labor")
    inventory_cost_key: int | float | None = Field(default=None, alias="cost:inventory")
    client_key: str | None = Field(default=None, alias="client")
    maintenance_cost_key: int | float | None = Field(default=None, alias="cost:maintenance")
    missed_deadline_cost_key: int | float | None = Field(default=None, alias="cost:missed_deadline")
    transportation_cost_key: int | float | None = Field(default=None, alias="cost:transportation")
    warehousing_cost_key: int | float | None = Field(default=None, alias="cost:warehousing")
    quality_key: str | None = Field(default=None, alias="quality")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
