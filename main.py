import pandas as pd

import process_performance_indicators as ppi

# Load event log
event_log = pd.read_csv("sample_logs/minimal_log_4.csv", sep=";")

print("Original event log:")
print(event_log.head())
print("\n")

standard_to_log_mapping = {
    "case:concept:name": "case",
    "concept:name": "activity",
    "time:timestamp": "complete",
    "cost:total": "cost",
}

formatted_log_dict = ppi.log_formatter(event_log, standard_to_log_mapping)
print("Formatted log using dictionary mapping:")
print(formatted_log_dict.head())
print("\n")

column_mapping = ppi.StandardColumnMapping(
    case_id_key="case",
    activity_key="activity",
    timestamp_key="complete",
    total_cost_key="cost",
)

formatted_log_dataclass = ppi.log_formatter(event_log, column_mapping)
print("Formatted log using dataclass mapping:")
print(formatted_log_dataclass.head())
