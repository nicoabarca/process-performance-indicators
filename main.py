import pandas as pd

import process_performance_indicators as ppi

# Load event log
event_log = pd.read_csv("sample_logs/match_log.csv", sep=",")

blasting_event_log = pd.read_csv("sample_logs/blasting_with_rework_event_log.csv", sep=";")

column_mapping = ppi.StandardColumnMapping(
    case_id_key="case",
    activity_key="activity",
    timestamp_key="timestamp",
    lifecycle_type_key="lifecycle_type",
)

blasting_mapping = ppi.StandardColumnMapping(
    case_id_key="Case ID",
    activity_key="Activity",
    timestamp_key="Complete",
    start_timestamp_key="Start",
    resource_key="Resource",
    total_cost_key="Cost",
)


formatted_log = ppi.event_log_formatter(event_log, column_mapping)
print("Formatted log using dataclass mapping:")
print(formatted_log)

derivable_log = ppi.convert_to_derivable_interval_log(formatted_log)
print("Derivable log:")
print(derivable_log)

explicit_log = ppi.convert_to_explicit_interval_log(derivable_log)
print("Explicit log:")
print(explicit_log)
