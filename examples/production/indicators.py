import pandas as pd

from process_performance_indicators import StandardColumnMapping, StandardColumnNames, event_log_formatter
from process_performance_indicators.execution import IndicatorArguments, run_indicators_to_csv, summary_to_csv

# DATASET PARAMETERS
DATASET_PATH = "production.csv"
FORMATTED_DATASET_PATH = "production_formatted.csv"
RESULTS_CSV_PATH = "production_results.csv"
SUMMARY_CSV_PATH = "production_summary.csv"

# COLUMN MAPPING (keep dataset-specific details here)
COLUMN_MAPPING = StandardColumnMapping(
    case_id_key="Case ID",
    activity_key="Activity",
    timestamp_key="Complete Timestamp",
    start_timestamp_key="Start Timestamp",
    resource_key="Resource",
    human_resource_key="Worker ID",
)

# INDICATOR SELECTION (strings-only include filters; None means “all”)
DIMENSIONS: list[str] | None = None  # e.g. ["cost", "time"]
GRANULARITIES: list[str] | None = None  # e.g. ["cases", "groups"]


def build_indicator_arguments(event_log: pd.DataFrame) -> IndicatorArguments:
    """
    Set the indicator arguments here.

    If you want a fully explicit interface, replace the sampling with hard-coded values.
    """

    def sample(column: str, *, n: int = 1, random_state: int = 25):
        unique_values = event_log[column].drop_duplicates()
        sampled = unique_values.sample(n=min(n, len(unique_values)), random_state=random_state)
        if n == 1:
            return sampled.iloc[0]
        return set(sampled.to_list())

    return IndicatorArguments(
        case_id=sample(StandardColumnNames.CASE_ID),
        case_ids=list(sample(StandardColumnNames.CASE_ID, n=3)),
        activity_name=sample(StandardColumnNames.ACTIVITY),
        instance_id=sample(StandardColumnNames.INSTANCE),
        human_resource_name=sample(StandardColumnNames.HUMAN_RESOURCE),
        automated_activities=sample(StandardColumnNames.ACTIVITY, n=3),
        desired_activities=sample(StandardColumnNames.ACTIVITY, n=3),
        unwanted_activities=sample(StandardColumnNames.ACTIVITY, n=3),
        direct_cost_activities=sample(StandardColumnNames.ACTIVITY, n=3),
        activities_subset=sample(StandardColumnNames.ACTIVITY, n=3),
        value="rework_value",
        deadline=500000,
        expectation=250000,
        activity_a=sample(StandardColumnNames.ACTIVITY),
        activity_b=sample(StandardColumnNames.ACTIVITY),
        start_time=None,
        end_time=sample(StandardColumnNames.TIMESTAMP),
        role_name=None,
        aggregation_mode="sgl",
    )


def main() -> None:
    raw_event_log = pd.read_csv(DATASET_PATH)
    formatted_event_log = event_log_formatter(raw_event_log, column_mapping=COLUMN_MAPPING)
    formatted_event_log.to_csv(FORMATTED_DATASET_PATH, index=False)

    indicator_args = build_indicator_arguments(formatted_event_log)
    run_indicators_to_csv(
        formatted_event_log,
        indicator_args,
        csv_path=RESULTS_CSV_PATH,
        dimension=DIMENSIONS,
        granularity=GRANULARITIES,
        verbose=True,
    )
    summary_to_csv(
        results_csv_path=RESULTS_CSV_PATH,
        output_csv_path=SUMMARY_CSV_PATH,
        formatted_event_log_path=FORMATTED_DATASET_PATH,
    )


if __name__ == "__main__":
    main()
