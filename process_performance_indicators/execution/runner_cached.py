"""
Cached indicator execution with function-level memoization.

This module provides an alternative to the standard runner that wraps
indicator functions with a caching layer to avoid redundant calculations.
"""

import inspect
from dataclasses import asdict
from typing import Any

import pandas as pd
from tqdm import tqdm

from process_performance_indicators.execution._cache import unwrap_module_functions, wrap_module_functions
from process_performance_indicators.execution._helpers import missing_required_args, normalize_result
from process_performance_indicators.execution._registry import select_indicators
from process_performance_indicators.execution.models import IndicatorArguments


def run_indicators_cached(
    event_log: pd.DataFrame,
    args: IndicatorArguments,
    *,
    dimension: list[str] | None = None,
    granularity: list[str] | None = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Runs process performance indicators with function-level caching enabled.

    This function wraps all indicator functions with a caching layer before execution,
    allowing indicators that call other indicators internally to reuse previously
    calculated results. This can significantly speed up execution for indicators
    with shared dependencies (e.g., cost indicators that all use total_cost).

    The caching is transparent - indicators are called normally and don't need
    any modifications. After execution, all functions are restored to their
    original unwrapped state.

    Args:
        event_log (pd.DataFrame): The formatted event log on which to run the indicators.
        args (IndicatorArguments): Parameter values to supply to indicators as needed.
        dimension (list[str] | None, optional): Filter to include only specified dimensions
            (e.g., ["cost", "time"]). Use None to include all.
        granularity (list[str] | None, optional): Filter to include only specified granularities
            (e.g., ["cases", "groups"]). Use None to include all.
        verbose (bool, optional): If True, logs progress of indicator execution and cache statistics.

    Returns:
        pd.DataFrame: DataFrame with one row per indicator execution, including columns for
        dimension, granularity, indicator name, status (success/error), error message, and result.

    Example:
        >>> from process_performance_indicators.execution.runner_cached import run_indicators_cached
        >>> results = run_indicators_cached(
        ...     event_log,
        ...     args,
        ...     dimension=["cost", "time"],
        ...     verbose=True
        ... )

    """
    selected = select_indicators(dimension=dimension, granularity=granularity)
    args_dict = {k: v for k, v in asdict(args).items() if v is not None}

    # Set up caching - wrap all indicator modules
    cache: dict = {}
    wrapped_modules: dict = {}

    # Import all indicator modules that need wrapping
    import process_performance_indicators.indicators.cost.activities as cost_activities
    import process_performance_indicators.indicators.cost.cases as cost_cases
    import process_performance_indicators.indicators.cost.groups as cost_groups
    import process_performance_indicators.indicators.cost.instances as cost_instances
    import process_performance_indicators.indicators.flexibility.activities as flex_activities
    import process_performance_indicators.indicators.flexibility.cases as flex_cases
    import process_performance_indicators.indicators.flexibility.groups as flex_groups
    import process_performance_indicators.indicators.general.activities as gen_activities
    import process_performance_indicators.indicators.general.cases as gen_cases
    import process_performance_indicators.indicators.general.groups as gen_groups
    import process_performance_indicators.indicators.quality.activities as quality_activities
    import process_performance_indicators.indicators.quality.cases as quality_cases
    import process_performance_indicators.indicators.quality.groups as quality_groups
    import process_performance_indicators.indicators.quality.instances as quality_instances
    import process_performance_indicators.indicators.time.activities as time_activities
    import process_performance_indicators.indicators.time.cases as time_cases
    import process_performance_indicators.indicators.time.groups as time_groups
    import process_performance_indicators.indicators.time.instances as time_instances

    # Wrap all indicator modules with caching
    modules_to_wrap = [
        cost_activities,
        cost_cases,
        cost_groups,
        cost_instances,
        time_activities,
        time_cases,
        time_groups,
        time_instances,
        quality_activities,
        quality_cases,
        quality_groups,
        quality_instances,
        flex_activities,
        flex_cases,
        flex_groups,
        gen_activities,
        gen_cases,
        gen_groups,
    ]

    for module in modules_to_wrap:
        wrapped_modules[module] = wrap_module_functions(module, cache)

    if verbose:
        print(f"✓ Caching enabled for {len(modules_to_wrap)} indicator modules")

    try:
        # Execute indicators (same as original runner)
        rows: list[dict[str, Any]] = []
        total = len(selected)

        iterator = tqdm(
            selected,
            total=total,
            desc="Running indicators (cached)",
            disable=not verbose,
            unit="indicator",
        )

        for spec in iterator:
            if verbose:
                iterator.set_postfix_str(f"Calculating {spec.name}")

            indicator = spec.callable
            sig = inspect.signature(indicator)

            # Build kwargs: always provide event_log; provide args matching parameter names
            kwargs: dict[str, Any] = {"event_log": event_log}
            for param_name in sig.parameters:
                if param_name == "event_log":
                    continue
                if param_name in args_dict:
                    kwargs[param_name] = args_dict[param_name]

            missing = missing_required_args(sig, kwargs)

            base_row = {
                "dimension": spec.dimension,
                "granularity": spec.granularity,
                "indicator_name": spec.name,
            }

            if missing:
                rows.append(
                    {
                        **base_row,
                        "status": "error",
                        "error": f"Missing required args: {missing}",
                        **normalize_result(None),
                    }
                )
                continue

            try:
                result = indicator(**kwargs)
                rows.append(
                    {
                        **base_row,
                        "status": "success",
                        "error": "",
                        **normalize_result(result),
                    }
                )
            except Exception as e:  # noqa: BLE001
                rows.append(
                    {
                        **base_row,
                        "status": "error",
                        "error": str(e),
                        **normalize_result(None),
                    }
                )

        # Print cache statistics
        if verbose:
            print(f"\n{'=' * 70}")
            print("Cache Statistics:")
            print(f"{'=' * 70}")
            print(f"  Total cached function calls: {len(cache)}")
            print("  Cache entries saved redundant calculations")
            print(f"{'=' * 70}\n")

        return pd.DataFrame(rows)

    finally:
        # Always unwrap functions (cleanup)
        for module, originals in wrapped_modules.items():
            unwrap_module_functions(module, originals)


def run_indicators_to_csv_cached(
    event_log: pd.DataFrame,
    args: IndicatorArguments,
    *,
    csv_path: str,
    dimension: list[str] | None = None,
    granularity: list[str] | None = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Runs indicators with caching and saves the results to CSV.

    This is a convenience function that combines run_indicators_cached with
    CSV export. It runs indicators with function-level caching enabled and
    saves the results to the specified CSV file.

    Args:
        event_log (pd.DataFrame): The formatted event log on which to run the indicators.
        args (IndicatorArguments): Parameter values to supply to indicators as needed.
        csv_path (str): The path to the CSV file to save the results to.
        dimension (list[str] | None, optional): Filter to include only specified dimensions
            (e.g., ["cost", "time"]). Use None to include all.
        granularity (list[str] | None, optional): Filter to include only specified granularities
            (e.g., ["cases", "groups"]). Use None to include all.
        verbose (bool, optional): If True, logs progress of indicator execution and cache statistics.

    Returns:
        pd.DataFrame: DataFrame with one row per indicator execution, including columns for
        dimension, granularity, indicator name, status (success/error), error message, and result.

    Example:
        >>> from process_performance_indicators.execution.runner_cached import run_indicators_to_csv_cached
        >>> results = run_indicators_to_csv_cached(
        ...     event_log,
        ...     args,
        ...     csv_path="results_cached.csv",
        ...     verbose=True
        ... )

    """
    results_df = run_indicators_cached(
        event_log,
        args,
        dimension=dimension,
        granularity=granularity,
        verbose=verbose,
    )
    results_df.to_csv(csv_path, index=False)
    return results_df
