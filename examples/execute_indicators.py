"""
This script provides a single entry point for running process performance indicators
on any dataset with a corresponding configuration in dataset_configs.json.

Usage:
    # Basic usage with auto-generated output folder
    uv run examples/execute_indicators.py \\
        --dataset examples/production/production.csv \\
        --config examples/dataset_configs.json

    # With custom output folder
    uv run examples/execute_indicators.py \\
        --dataset examples/italian_help_desk/italian-help-desk_100.csv \\
        --config examples/dataset_configs.json \\
        --out examples/my_custom_results

Features:
    - Automatic CSV separator detection
    - Dynamic column mapping from JSON config
    - Auto-sampling of indicator arguments from formatted log
    - Configurable output directory
    - Full pipeline execution (format, indicators, summary)
"""

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

from process_performance_indicators import StandardColumnMapping, StandardColumnNames, event_log_formatter
from process_performance_indicators.execution import IndicatorArguments, run_indicators_to_csv, summary_to_csv


def build_indicator_arguments_simple() -> IndicatorArguments:
    """
    Simple approach: Returns IndicatorArguments with all fields set to None.

    This is a placeholder for users who want to manually set specific values.
    For most use cases, build_indicator_arguments_auto() is recommended.

    Returns:
        IndicatorArguments: All fields set to None

    """
    return IndicatorArguments(
        case_id=None,
        case_ids=None,
        activity_name=None,
        instance_id=None,
        human_resource_name=None,
        activity_a=None,
        activity_b=None,
        start_time=None,
        end_time=None,
        a_activity_name=None,
        role_name=None,
        automated_activities=None,
        desired_activities=None,
        unwanted_activities=None,
        direct_cost_activities=None,
        activities_subset=None,
        deadline=None,
        expectation=None,
        value=None,
        aggregation_mode=None,
    )


def build_indicator_arguments_auto(event_log: pd.DataFrame) -> IndicatorArguments:
    """
    Advanced approach: Auto-sample values from the formatted log.

    This approach randomly samples values from your event log to populate
    the indicator arguments. It's great for getting started quickly and
    exploring indicators across different datasets.

    Args:
        event_log: The formatted event log DataFrame

    Returns:
        IndicatorArguments: Populated with sampled values from the log

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

    # Sample time window for time-bounded indicators
    min_time = timestamps.min()
    quarter_point = min_time + (time_range * 0.25)
    three_quarter_point = min_time + (time_range * 0.75)

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
        a_activity_name=sample(StandardColumnNames.ACTIVITY),
        start_time=quarter_point,  # 25% into the log timeframe
        end_time=three_quarter_point,  # 75% into the log timeframe
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
    print(f"  a_activity_name: {args.a_activity_name}")
    print(f"  start_time: {args.start_time}")
    print(f"  end_time: {args.end_time}")
    print(f"  deadline: {args.deadline}")
    print(f"  expectation: {args.expectation}")
    print(f"  value: {args.value}")
    print(f"  role_name: {args.role_name}")
    print(f"  aggregation_mode: {args.aggregation_mode}")
    print("=" * 70 + "\n")

    return args


def load_config(config_path: Path, dataset_name: str) -> tuple[StandardColumnMapping, dict]:
    """
    Load column mapping configuration for a specific dataset.

    Args:
        config_path: Path to the dataset_configs.json file
        dataset_name: Name of the dataset (filename)

    Returns:
        tuple: (StandardColumnMapping, dict with format settings)
            Format settings dict contains: separator, date_format, dayfirst

    Raises:
        FileNotFoundError: If config file doesn't exist
        KeyError: If dataset is not in config file
        json.JSONDecodeError: If config file is not valid JSON

    """
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        config_data = json.load(f)

    if dataset_name not in config_data:
        available = ", ".join(config_data.keys())
        raise KeyError(f"Dataset '{dataset_name}' not found in config file.\nAvailable datasets: {available}")

    dataset_config = config_data[dataset_name]

    # Extract format settings (with defaults)
    format_settings = {
        "separator": dataset_config.pop("separator", ","),
        "date_format": dataset_config.pop("date_format", None),
        "dayfirst": dataset_config.pop("dayfirst", True),
    }

    # Create column mapping from remaining config
    column_mapping = StandardColumnMapping(**dataset_config)

    return column_mapping, format_settings


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Execute process performance indicators on an event log dataset.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  uv run examples/execute_indicators.py \\
      --dataset examples/production/production.csv \\
      --config examples/dataset_configs.json

  # Custom output folder
  uv run examples/execute_indicators.py \\
      --dataset examples/italian_help_desk/italian-help-desk_100.csv \\
      --config examples/dataset_configs.json \\
      --out examples/my_results
        """,
    )

    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Path to the raw CSV dataset file (e.g., examples/production/production.csv)",
    )

    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the dataset configuration JSON file (e.g., examples/dataset_configs.json)",
    )

    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Output directory for results. Default: out_<dataset_basename> in examples/ folder",
    )

    return parser.parse_args()


def main():
    """Main execution function."""
    # Parse arguments
    args = parse_arguments()

    # Convert paths
    dataset_path = Path(args.dataset)
    config_path = Path(args.config)

    # Validate dataset file exists
    if not dataset_path.exists():
        print(f"ERROR: Dataset file not found: {dataset_path}")
        sys.exit(1)

    # Determine output directory
    if args.out:
        output_dir = Path(args.out)
    else:
        # Default: out_<dataset_basename> in examples/ folder
        dataset_stem = dataset_path.stem  # filename without extension
        examples_dir = Path(__file__).parent  # examples/ directory
        output_dir = examples_dir / f"out_{dataset_stem}"

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define output file paths
    dataset_basename = dataset_path.stem
    formatted_path = output_dir / f"formatted_{dataset_basename}.csv"
    results_path = output_dir / f"results_{dataset_basename}.csv"
    summary_path = output_dir / f"summary_{dataset_basename}.csv"

    print("=" * 70)
    print("PROCESS PERFORMANCE INDICATORS - UNIFIED EXECUTION")
    print("=" * 70)
    print(f"Dataset: {dataset_path}")
    print(f"Config: {config_path}")
    print(f"Output: {output_dir}")
    print("=" * 70)
    print()

    # =========================================================================
    # STEP 1: Load configuration
    # =========================================================================
    print("=" * 70)
    print("STEP 1: Loading configuration...")
    print("=" * 70)
    try:
        column_mapping, format_settings = load_config(config_path, dataset_path.name)
        print(f"✓ Loaded configuration for: {dataset_path.name}")
        print(f"  Separator: {repr(format_settings['separator'])}")
        print(f"  Date format: {format_settings['date_format']}")
        print(f"  Day first: {format_settings['dayfirst']}")
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    print()

    # =========================================================================
    # STEP 2: Load and format event log
    # =========================================================================
    print("=" * 70)
    print("STEP 2: Loading and formatting event log...")
    print("=" * 70)

    # Read CSV with separator from config
    try:
        raw_event_log = pd.read_csv(dataset_path, sep=format_settings["separator"])
        print(f"✓ Loaded {len(raw_event_log)} events from {dataset_path}")
    except Exception as e:
        print(f"ERROR loading dataset: {e}")
        sys.exit(1)

    # Format the event log using settings from config
    try:
        # Apply formatting with settings from config
        date_format = format_settings["date_format"]
        dayfirst = format_settings["dayfirst"]

        if date_format is not None:
            formatted_event_log = event_log_formatter(
                raw_event_log, column_mapping=column_mapping, date_format=date_format, dayfirst=dayfirst
            )
        else:
            formatted_event_log = event_log_formatter(raw_event_log, column_mapping=column_mapping, dayfirst=dayfirst)

        formatted_event_log.to_csv(formatted_path, index=False)
        print(f"✓ Formatted log saved to {formatted_path}")
        print(f"  Cases: {formatted_event_log[StandardColumnNames.CASE_ID].nunique()}")
        print(f"  Activities: {formatted_event_log[StandardColumnNames.ACTIVITY].nunique()}")
        if StandardColumnNames.INSTANCE in formatted_event_log.columns:
            print(f"  Activity instances: {formatted_event_log[StandardColumnNames.INSTANCE].nunique()}")
    except Exception as e:
        print(f"ERROR formatting event log: {e}")
        sys.exit(1)
    print()

    # =========================================================================
    # STEP 3: Build indicator arguments (auto-sampling)
    # =========================================================================
    print("=" * 70)
    print("STEP 3: Setting up indicator arguments...")
    print("=" * 70)
    print("Using auto-sampling approach (review sampled values below)")

    try:
        indicator_args = build_indicator_arguments_auto(formatted_event_log)
    except Exception as e:
        print(f"ERROR building indicator arguments: {e}")
        sys.exit(1)

    # =========================================================================
    # STEP 4: Run indicators
    # =========================================================================
    print("=" * 70)
    print("STEP 4: Running indicators...")
    print("=" * 70)
    print("  Dimensions: ALL (cost, time, quality, flexibility, general)")
    print("  Granularities: ALL (activities, cases, groups, instances)")
    print()

    try:
        run_indicators_to_csv(
            formatted_event_log,
            indicator_args,
            csv_path=str(results_path),
            dimension=None,  # Run all dimensions
            granularity=None,  # Run all granularities
            verbose=True,
        )
        print(f"\n✓ Results saved to {results_path}")
    except Exception as e:
        print(f"ERROR running indicators: {e}")
        sys.exit(1)
    print()

    # =========================================================================
    # STEP 5: Generate summary
    # =========================================================================
    print("=" * 70)
    print("STEP 5: Generating summary...")
    print("=" * 70)

    try:
        summary_to_csv(
            results_csv_path=str(results_path),
            output_csv_path=str(summary_path),
            formatted_event_log_path=str(formatted_path),
        )
        print(f"✓ Summary saved to {summary_path}")
    except Exception as e:
        print(f"ERROR generating summary: {e}")
        sys.exit(1)
    print()

    # =========================================================================
    # DONE
    # =========================================================================
    print("=" * 70)
    print("DONE! Check the output files for your results:")
    print("=" * 70)
    print(f"  1. {formatted_path}")
    print("     → Your formatted event log")
    print(f"  2. {results_path}")
    print("     → Detailed indicator results")
    print(f"  3. {summary_path}")
    print("     → Summary of results")
    print("=" * 70)


if __name__ == "__main__":
    main()
