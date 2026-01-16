"""
Production Event Log - Cached Indicator Analysis Example

This script demonstrates the cached runner that uses function-level memoization
to avoid redundant calculations when indicators call other indicators internally.

PERFORMANCE COMPARISON:
-----------------------
Compare this cached version with the standard runner to see performance improvements,
especially for cost indicators that share dependencies like total_cost, labor_cost, etc.

USAGE:
------
1. Run this script: python indicators_cached.py
2. Compare execution time with the standard indicators.py
3. Check the cache statistics printed at the end

OUTPUT FILES:
-------------
- production_formatted.csv: Formatted event log
- production_results_cached.csv: Detailed indicator results (cached execution)
- production_summary_cached.csv: Summary of results
"""

import time

import pandas as pd

from process_performance_indicators import StandardColumnMapping, StandardColumnNames, event_log_formatter
from process_performance_indicators.execution import IndicatorArguments, summary_to_csv
from process_performance_indicators.execution.runner_cached import run_indicators_to_csv_cached

# =============================================================================
# CONFIGURATION
# =============================================================================

# File paths
DATASET_PATH = "production.csv"
FORMATTED_DATASET_PATH = "production_formatted.csv"
RESULTS_CSV_PATH = "production_results_cached.csv"
SUMMARY_CSV_PATH = "production_summary_cached.csv"

# Column mapping - same as standard indicators.py
COLUMN_MAPPING = StandardColumnMapping(
    case_id_key="Case ID",
    activity_key="Activity",
    timestamp_key="Complete Timestamp",
    start_timestamp_key="Start Timestamp",
    resource_key="Resource",
    human_resource_key="Worker ID",
    unsuccessful_outcome_unit_key="Qty Rejected",
    outcome_unit_key="Qty Completed",
)

# Filter which indicators to run (None = run all)
DIMENSIONS: list[str] | None = None
# Example: ["cost", "time"] to run only cost and time indicators

GRANULARITIES: list[str] | None = None
# Example: ["cases", "activities"] to run case-level and activity-level indicators

# Use auto-sampling for quick testing
USE_AUTO_SAMPLING = True


def build_indicator_arguments_auto(event_log: pd.DataFrame) -> IndicatorArguments:
    """Auto-sample indicator arguments from the event log."""

    def sample(column: str, *, n: int = 1, random_state: int = 25):
        """Sample n unique values from a column in the event log."""
        unique_values = event_log[column].drop_duplicates()
        sampled = unique_values.sample(n=min(n, len(unique_values)), random_state=random_state)
        if n == 1:
            return sampled.iloc[0]
        return set(sampled.to_list())

    # Sample time values for thresholds
    timestamps = event_log[StandardColumnNames.TIMESTAMP]
    time_range = timestamps.max() - timestamps.min()
    avg_case_duration = time_range / event_log[StandardColumnNames.CASE_ID].nunique()

    # Build arguments with sampled values
    args = IndicatorArguments(
        case_id=sample(StandardColumnNames.CASE_ID),
        case_ids=list(sample(StandardColumnNames.CASE_ID, n=3)),
        activity_name=sample(StandardColumnNames.ACTIVITY),
        instance_id=sample(StandardColumnNames.INSTANCE) if StandardColumnNames.INSTANCE in event_log.columns else None,
        human_resource_name=sample(StandardColumnNames.HUMAN_RESOURCE)
        if StandardColumnNames.HUMAN_RESOURCE in event_log.columns
        else None,
        automated_activities=sample(StandardColumnNames.ACTIVITY, n=3),
        desired_activities=sample(StandardColumnNames.ACTIVITY, n=3),
        unwanted_activities=sample(StandardColumnNames.ACTIVITY, n=3),
        direct_cost_activities=sample(StandardColumnNames.ACTIVITY, n=3),
        activities_subset=sample(StandardColumnNames.ACTIVITY, n=3),
        value=1,
        deadline=avg_case_duration * 2,
        expectation=avg_case_duration,
        activity_a=sample(StandardColumnNames.ACTIVITY),
        activity_b=sample(StandardColumnNames.ACTIVITY),
        start_time=None,
        end_time=None,
        role_name=sample(StandardColumnNames.ROLE) if StandardColumnNames.ROLE in event_log.columns else None,
        aggregation_mode="sgl",
    )

    # Print sampled values
    print("\n" + "=" * 70)
    print("Auto-sampled indicator arguments:")
    print("=" * 70)
    print(f"  case_id: {args.case_id}")
    print(f"  case_ids: {args.case_ids}")
    print(f"  activity_name: {args.activity_name}")
    print(f"  instance_id: {args.instance_id}")
    print(f"  human_resource_name: {args.human_resource_name}")
    print(f"  automated_activities: {args.automated_activities}")
    print(f"  desired_activities: {args.desired_activities}")
    print(f"  unwanted_activities: {args.unwanted_activities}")
    print(f"  direct_cost_activities: {args.direct_cost_activities}")
    print(f"  activities_subset: {args.activities_subset}")
    print(f"  activity_a: {args.activity_a}")
    print(f"  activity_b: {args.activity_b}")
    print(f"  deadline: {args.deadline}")
    print(f"  expectation: {args.expectation}")
    print(f"  value: {args.value}")
    print(f"  role_name: {args.role_name}")
    print(f"  aggregation_mode: {args.aggregation_mode}")
    print("=" * 70 + "\n")

    return args


def main() -> None:
    """Main execution function with performance timing."""
    overall_start = time.time()

    print("=" * 70)
    print("CACHED INDICATOR RUNNER - Production Dataset")
    print("=" * 70)
    print()

    # Step 1: Load and format event log
    print("=" * 70)
    print("STEP 1: Loading and formatting event log...")
    print("=" * 70)
    raw_event_log = pd.read_csv(DATASET_PATH)
    print(f"✓ Loaded {len(raw_event_log)} events from {DATASET_PATH}")

    formatted_event_log = event_log_formatter(raw_event_log, column_mapping=COLUMN_MAPPING)
    formatted_event_log.to_csv(FORMATTED_DATASET_PATH, index=False)
    print(f"✓ Formatted log saved to {FORMATTED_DATASET_PATH}")
    print(f"  Cases: {formatted_event_log[StandardColumnNames.CASE_ID].nunique()}")
    print(f"  Activities: {formatted_event_log[StandardColumnNames.ACTIVITY].nunique()}")
    print(f"  Activity instances: {formatted_event_log[StandardColumnNames.INSTANCE].nunique()}")
    print()

    # Step 2: Set up indicator arguments
    print("=" * 70)
    print("STEP 2: Setting up indicator arguments...")
    print("=" * 70)
    print("Using auto-sampling approach (review sampled values below)")
    indicator_args = build_indicator_arguments_auto(formatted_event_log)

    # Step 3: Run indicators with caching
    print("=" * 70)
    print("STEP 3: Running indicators WITH CACHING...")
    print("=" * 70)
    if DIMENSIONS:
        print(f"  Dimensions: {', '.join(DIMENSIONS)}")
    else:
        print("  Dimensions: ALL (cost, time, quality, flexibility, general)")

    if GRANULARITIES:
        print(f"  Granularities: {', '.join(GRANULARITIES)}")
    else:
        print("  Granularities: ALL (activities, cases, groups, instances)")
    print()

    execution_start = time.time()
    run_indicators_to_csv_cached(
        formatted_event_log,
        indicator_args,
        csv_path=RESULTS_CSV_PATH,
        dimension=DIMENSIONS,
        granularity=GRANULARITIES,
        verbose=True,
    )
    execution_time = time.time() - execution_start

    print(f"✓ Results saved to {RESULTS_CSV_PATH}")
    print(f"⏱  Execution time: {execution_time:.2f} seconds")
    print()

    # Step 4: Generate summary
    print("=" * 70)
    print("STEP 4: Generating summary...")
    print("=" * 70)
    summary_to_csv(
        results_csv_path=RESULTS_CSV_PATH,
        output_csv_path=SUMMARY_CSV_PATH,
        formatted_event_log_path=FORMATTED_DATASET_PATH,
    )
    print(f"✓ Summary saved to {SUMMARY_CSV_PATH}")
    print()

    overall_time = time.time() - overall_start

    # Final summary
    print("=" * 70)
    print("DONE! Performance Summary:")
    print("=" * 70)
    print(f"  Total execution time: {overall_time:.2f} seconds")
    print(f"  Indicator calculation time: {execution_time:.2f} seconds")
    print()
    print("Output files:")
    print(f"  1. {FORMATTED_DATASET_PATH} - Your formatted event log")
    print(f"  2. {RESULTS_CSV_PATH} - Detailed indicator results (cached)")
    print(f"  3. {SUMMARY_CSV_PATH} - Summary of results")
    print()
    print("TIP: Compare this execution time with indicators.py to see the")
    print("     performance improvement from caching!")
    print("=" * 70)


if __name__ == "__main__":
    main()
