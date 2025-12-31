from __future__ import annotations

import inspect
import json
from dataclasses import asdict, dataclass
from importlib import import_module
from typing import Any, Literal

import pandas as pd

AllowedDimension = Literal["cost", "time", "quality", "flexibility", "general"]
AllowedGranularity = Literal["activities", "cases", "groups", "instances"]


@dataclass(frozen=True)
class IndicatorSpec:
    dimension: AllowedDimension
    granularity: AllowedGranularity
    name: str
    callable: Any
    module: str


@dataclass(frozen=True)
class IndicatorArguments:
    # Core entities
    case_id: str | None = None
    case_ids: list[str] | set[str] | None = None
    activity_name: str | None = None
    instance_id: str | None = None

    # Cross-activity / time-window params
    activity_a: str | None = None
    activity_b: str | None = None
    start_time: Any | None = None  # typically pd.Timestamp
    end_time: Any | None = None  # typically pd.Timestamp

    # Resources / org
    human_resource_name: str | None = None
    role_name: str | None = None

    # Sets of activities
    automated_activities: set[str] | None = None
    desired_activities: set[str] | None = None
    unwanted_activities: set[str] | None = None
    direct_costs_activities: set[str] | None = None
    direct_cost_activities: set[str] | None = None
    activities_subset: set[str] | None = None

    # Thresholds / expectations
    deadline: int | float | None = None
    expectation: int | float | None = None
    value: str | int | float | None = None

    # Generic modes
    aggregation_mode: Literal["sgl", "sum"] | None = None


_DIMENSIONS: tuple[AllowedDimension, ...] = ("cost", "time", "quality", "flexibility", "general")
_GRANULARITIES: tuple[AllowedGranularity, ...] = ("activities", "cases", "groups", "instances")


def _iter_indicator_specs_for_module(
    *, dimension: AllowedDimension, granularity: AllowedGranularity, module_name: str
) -> list[IndicatorSpec]:
    module = import_module(module_name)
    specs: list[IndicatorSpec] = []

    for func_name, func in inspect.getmembers(module, inspect.isfunction):
        if func_name.startswith("_"):
            continue
        # Only functions actually defined in this module (ignore imported helpers).
        if getattr(func, "__module__", None) != module.__name__:
            continue
        specs.append(
            IndicatorSpec(
                dimension=dimension,
                granularity=granularity,
                name=func_name,
                callable=func,
                module=module.__name__,
            )
        )

    specs.sort(key=lambda s: s.name)
    return specs


def build_indicator_registry() -> list[IndicatorSpec]:
    """Build the explicit indicator registry by enumerating indicator modules."""
    registry: list[IndicatorSpec] = []

    for dimension in _DIMENSIONS:
        for granularity in _GRANULARITIES:
            # flexibility/general don't have instances
            if dimension in {"flexibility", "general"} and granularity == "instances":
                continue
            module_name = f"process_performance_indicators.indicators.{dimension}.{granularity}"
            registry.extend(
                _iter_indicator_specs_for_module(
                    dimension=dimension,
                    granularity=granularity,
                    module_name=module_name,
                )
            )

    registry.sort(key=lambda s: (s.dimension, s.granularity, s.name))
    return registry


INDICATOR_REGISTRY: list[IndicatorSpec] = build_indicator_registry()


def select_indicators(
    *,
    dimension: list[str] | None = None,
    granularity: list[str] | None = None,
) -> list[IndicatorSpec]:
    """Filter the registry by dimension and/or granularity (strings-only include filters)."""
    if dimension is not None:
        unknown = sorted(set(dimension).difference(_DIMENSIONS))
        if unknown:
            raise ValueError(f"Unknown dimension(s): {unknown}. Allowed: {list(_DIMENSIONS)}")
    if granularity is not None:
        unknown = sorted(set(granularity).difference(_GRANULARITIES))
        if unknown:
            raise ValueError(f"Unknown granularity(s): {unknown}. Allowed: {list(_GRANULARITIES)}")

    selected: list[IndicatorSpec] = []
    for spec in INDICATOR_REGISTRY:
        if dimension is not None and spec.dimension not in set(dimension):
            continue
        if granularity is not None and spec.granularity not in set(granularity):
            continue
        selected.append(spec)
    return selected


def _json_dumps_safe(value: Any) -> str:
    def default(o: Any) -> Any:
        if isinstance(o, set):
            return sorted(o)
        if isinstance(o, (pd.Timestamp, pd.Timedelta)):
            return str(o)
        return str(o)

    return json.dumps(value, default=default, ensure_ascii=False)


def _normalize_result(value: Any) -> dict[str, Any]:
    """Normalize arbitrary indicator outputs into CSV-friendly columns."""
    result: str = ""
    result_type: str = "NoneType"
    result_numeric: int | float | None = None
    result_seconds: float | None = None

    if value is None:
        pass
    elif isinstance(value, pd.Timedelta):
        result = str(value)
        result_type = "Timedelta"
        result_seconds = float(value.total_seconds())
    elif isinstance(value, pd.Timestamp):
        result = value.isoformat()
        result_type = "Timestamp"
    elif isinstance(value, bool):
        result = str(value)
        result_type = "bool"
        result_numeric = int(value)
    elif isinstance(value, int):
        result = str(value)
        result_type = "int"
        result_numeric = value
    elif isinstance(value, float):
        result = str(value)
        result_type = "float"
        result_numeric = value
    elif isinstance(value, (set, list, tuple, dict)):
        result = _json_dumps_safe(value)
        result_type = type(value).__name__
    else:
        result = str(value)
        result_type = type(value).__name__

    return {
        "result": result,
        "result_type": result_type,
        "result_numeric": result_numeric,
        "result_seconds": result_seconds,
    }


def _missing_required_args(sig: inspect.Signature, kwargs: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for name, param in sig.parameters.items():
        if name == "event_log":
            continue
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        if param.default is not inspect.Parameter.empty:
            continue
        if name not in kwargs:
            missing.append(name)
    return missing


_ARG_ALIASES: dict[str, tuple[str, ...]] = {
    # Allow common naming variations between indicator signatures and user args.
    # Map: indicator_param_name -> possible IndicatorArguments field names (in priority order).
    "direct_costs_activities": ("direct_costs_activities", "direct_cost_activities"),
    "direct_cost_activities": ("direct_cost_activities", "direct_costs_activities"),
}


def run_indicators(
    event_log: pd.DataFrame,
    args: IndicatorArguments,
    *,
    dimension: list[str] | None = None,
    granularity: list[str] | None = None,
) -> pd.DataFrame:
    """Run selected indicators and return a results DataFrame."""
    selected = select_indicators(dimension=dimension, granularity=granularity)

    args_dict = {k: v for k, v in asdict(args).items() if v is not None}

    rows: list[dict[str, Any]] = []

    for spec in selected:
        indicator = spec.callable
        sig = inspect.signature(indicator)

        # Build kwargs: always provide event_log; provide args matching parameter names.
        kwargs: dict[str, Any] = {"event_log": event_log}
        for param_name in sig.parameters:
            if param_name == "event_log":
                continue
            if param_name in args_dict:
                kwargs[param_name] = args_dict[param_name]
                continue
            aliases = _ARG_ALIASES.get(param_name)
            if not aliases:
                continue
            for arg_key in aliases:
                if arg_key in args_dict:
                    kwargs[param_name] = args_dict[arg_key]
                    break

        missing = _missing_required_args(sig, kwargs)

        base_row = {
            "dimension": spec.dimension,
            "granularity": spec.granularity,
            "module": spec.module,
            "indicator_name": spec.name,
        }

        if missing:
            rows.append(
                {
                    **base_row,
                    "status": "error",
                    "error_type": "missing_args",
                    "missing_args": _json_dumps_safe(missing),
                    "error": f"Missing required args: {missing}",
                    **_normalize_result(None),
                }
            )
            continue

        try:
            result = indicator(**kwargs)
            rows.append(
                {
                    **base_row,
                    "status": "success",
                    "error_type": "",
                    "missing_args": "",
                    "error": "",
                    **_normalize_result(result),
                }
            )
        except Exception as e:  # noqa: BLE001
            rows.append(
                {
                    **base_row,
                    "status": "error",
                    "error_type": "exception",
                    "missing_args": "",
                    "error": str(e),
                    **_normalize_result(None),
                }
            )

    return pd.DataFrame(rows)


def run_indicators_to_csv(
    event_log: pd.DataFrame,
    args: IndicatorArguments,
    *,
    csv_path: str,
    dimension: list[str] | None = None,
    granularity: list[str] | None = None,
) -> pd.DataFrame:
    """Convenience wrapper that runs indicators and saves the results to CSV."""
    results_df = run_indicators(event_log, args, dimension=dimension, granularity=granularity)
    results_df.to_csv(csv_path, index=False)
    return results_df
