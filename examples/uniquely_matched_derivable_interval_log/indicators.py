"""
Uniquely Matched Derivable Interval Event Log - Indicator Analysis Example

This script demonstrates indicator analysis on a uniquely matched derivable interval event log,
where activity intervals can be derived because timestamps are unique (no ambiguity in matching).

Dataset characteristics:
- Has lifecycle transitions (start/complete)
- No explicit instance IDs but timestamps are unique (unambiguous matching)
- Has human resources, roles, and organizational resources
- Has outcome units and costs
"""

import pandas as pd

from process_performance_indicators import StandardColumnMapping, StandardColumnNames, event_log_formatter
from process_performance_indicators.execution import IndicatorArguments, run_indicators_to_csv, summary_to_csv

# =============================================================================
# CONFIGURATION - CUSTOMIZE THESE FOR YOUR DATASET
# =============================================================================

# Step 1: Define file paths
DATASET_PATH = "timestamp_unique_derivable_interval_event_log.csv"
FORMATTED_DATASET_PATH = "timestamp_unique_derivable_interval_event_log_formatted.csv"
RESULTS_CSV_PATH = "timestamp_unique_derivable_interval_event_log_results.csv"
SUMMARY_CSV_PATH = "timestamp_unique_derivable_interval_event_log_summary.csv"

# Step 2: Map your column names to standard names
# Uniquely matched derivable interval log: has lifecycle transitions, unique timestamps allow unambiguous matching
COLUMN_MAPPING = StandardColumnMapping(
    case_id_key="case:concept:name",
    activity_key="concept:name",
    timestamp_key="time:timestamp",
    lifecycle_type_key="lifecycle:transition",
    resource_key="org:resource",
    human_resource_key="human_resource",
    role_key="org:role",
    outcome_unit_key="outcome_unit",
    unsuccessful_outcome_unit_key="unsuccessful_outcome_unit",
    total_cost_key="cost:total",
    fixed_cost_key="cost:fixed",
    variable_cost_key="cost:variable",
    labor_cost_key="cost:labor",
    inventory_cost_key="cost:inventory",
    maintenance_cost_key="cost:maintenance",
    missed_deadline_cost_key="cost:missed_deadline",
    transportation_cost_key="cost:transportation",
    warehousing_cost_key="cost:warehousing",
    client_key="client",
    quality_key="quality",
)

# Step 3: Filter which indicators to run (None = run all)
DIMENSIONS: list[str] | None = None
# Example: ["time", "quality"] to run only time and quality indicators

GRANULARITIES: list[str] | None = None
# Example: ["cases", "activities"] to run case-level and activity-level indicators

# Step 4: Choose which approach to use for indicator arguments
USE_AUTO_SAMPLING = False  # Set to False to use hard-coded values instead


# =============================================================================
# INDICATOR ARGUMENTS GUIDE
# =============================================================================
# Not all indicators use all parameters. Each indicator uses only what it needs.
#
# Parameter Groups:
# -----------------
# - Single entities: case_id, activity_name, instance_id, human_resource_name
#   → Used by indicators that analyze one specific entity
#
# - Entity sets: case_ids, automated_activities, desired_activities, etc.
#   → Used by indicators that analyze groups or compare subsets
#
# - Relationships: activity_a, activity_b
#   → Used by indicators that measure relationships between activities
#
# - Time windows: start_time, end_time
#   → Used by indicators that filter events by time period
#
# - Thresholds: deadline, expectation, value
#   → Used by indicators that measure compliance or deviation
#
# Don't worry about providing "wrong" values - indicators will only use
# what they need and ignore the rest.
# =============================================================================


def build_indicator_arguments_simple() -> IndicatorArguments:
    """
    Simple approach: Hard-code the values you need.
    Replace these with values from YOUR dataset.

    To find valid values for your dataset, inspect the formatted event log CSV
    or use event_log[StandardColumnNames.ACTIVITY].unique() to see unique activities, etc.
    """
    return IndicatorArguments(
        # Single entity identifiers - for entity-specific indicators
        case_id="0",  # Replace with an actual case ID from your log
        activity_name="A",  # Replace with an activity from your log
        instance_id="i_1",  # Will be auto-derived from lifecycle transitions
        human_resource_name="Ed",  # Replace with a resource name
        # Multiple entities - for subset/comparison indicators
        case_ids={"0", "1", "2"},
        automated_activities={"A", "B"},  # Activities performed by machines
        desired_activities={"C", "D"},  # Activities you want to see
        unwanted_activities=set(),  # Activities to avoid
        direct_cost_activities={"A", "C"},  # Activities with direct costs
        activities_subset={"A", "C"},  # Subset for specific analysis
        # Cross-activity parameters - for sequence/relationship indicators
        activity_a="A",  # First activity in a sequence
        activity_b="C",  # Second activity in a sequence
        # Time window parameters - for time-bounded indicators
        start_time=pd.Timestamp("2025-01-01 10:00:00"),  # Dataset starts at 2025-01-01 10:00:05
        end_time=pd.Timestamp("2025-01-01 10:19:00"),  # Dataset ends at 2025-01-01 10:18:39
        # Organizational parameters
        role_name="Boss",  # Optional: "Manager" or "Operator" (if you have role column)
        # Threshold/expectation parameters - for compliance indicators
        deadline=pd.Timedelta(days=1),  # Expected maximum time
        expectation=pd.Timedelta(hours=12),  # Expected typical time
        value=1,  # Threshold value for rework counting
        # Aggregation mode
        aggregation_mode="sgl",  # "sgl" (single event per instance) or "sum" (sum across events)
    )


def build_indicator_arguments_auto(event_log: pd.DataFrame) -> IndicatorArguments:
    """
    Advanced approach: Auto-sample values from your formatted log.
    Useful for quick testing, but review the sampled values!

    This approach randomly samples values from your event log to populate
    the indicator arguments. It's great for getting started quickly, but
    you should verify that the sampled values make sense for your analysis.
    """

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
        case_ids=sample(StandardColumnNames.CASE_ID, n=3),
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
        value=1,  # Default rework threshold
        deadline=avg_case_duration * 2,  # 2x average duration as deadline
        expectation=avg_case_duration,  # Average duration as expectation
        activity_a=sample(StandardColumnNames.ACTIVITY),
        activity_b=sample(StandardColumnNames.ACTIVITY),
        start_time=None,
        end_time=None,
        role_name=sample(StandardColumnNames.ROLE) if StandardColumnNames.ROLE in event_log.columns else None,
        aggregation_mode="sgl",
    )

    # Print sampled values so user can review them
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
    """Main execution function."""
    print("=" * 70)
    print("STEP 1: Loading and formatting event log...")
    print("=" * 70)
    raw_event_log = pd.read_csv(DATASET_PATH, sep=";")
    print(f"✓ Loaded {len(raw_event_log)} events from {DATASET_PATH}")

    formatted_event_log = event_log_formatter(raw_event_log, column_mapping=COLUMN_MAPPING)
    formatted_event_log.to_csv(FORMATTED_DATASET_PATH, index=False)
    print(f"✓ Formatted log saved to {FORMATTED_DATASET_PATH}")
    print(f"  Cases: {formatted_event_log[StandardColumnNames.CASE_ID].nunique()}")
    print(f"  Activities: {formatted_event_log[StandardColumnNames.ACTIVITY].nunique()}")
    if StandardColumnNames.INSTANCE in formatted_event_log.columns:
        print(f"  Activity instances: {formatted_event_log[StandardColumnNames.INSTANCE].nunique()}")
    print()

    print("=" * 70)
    print("STEP 2: Setting up indicator arguments...")
    print("=" * 70)
    if USE_AUTO_SAMPLING:
        print("Using auto-sampling approach (review sampled values below)")
        indicator_args = build_indicator_arguments_auto(formatted_event_log)
    else:
        print("Using hard-coded approach")
        indicator_args = build_indicator_arguments_simple()
        print("✓ Indicator arguments configured")
    print()

    print("=" * 70)
    print("STEP 3: Running indicators...")
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

    run_indicators_to_csv(
        formatted_event_log,
        indicator_args,
        csv_path=RESULTS_CSV_PATH,
        dimension=DIMENSIONS,
        granularity=GRANULARITIES,
        verbose=True,
    )
    print(f"\n✓ Results saved to {RESULTS_CSV_PATH}")
    print()

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

    print("=" * 70)
    print("DONE! Check the output files for your results:")
    print("=" * 70)
    print(f"  1. {FORMATTED_DATASET_PATH} - Your formatted event log")
    print(f"  2. {RESULTS_CSV_PATH} - Detailed indicator results")
    print(f"  3. {SUMMARY_CSV_PATH} - Summary of results")
    print("=" * 70)


if __name__ == "__main__":
    main()
