from collections import defaultdict, deque

import pandas as pd

from process_performance_indicators.constants import (
    LifecycleTransitionType,
    StandardColumnNames,
)
from process_performance_indicators.formatting.instance_id_generator import id_generator


def match_all(case_log: pd.DataFrame) -> None:
    """
    Match all complete events in the case log to their corresponding start events.

    Algorithm:
        1. Sort all start events by timestamp and group them by activity into
           per-activity deques (earliest start at the front).
        2. Iterate complete events in their original order. For each complete
           event, pop the front of its activity's deque when the timestamp is
           compatible (≤ complete timestamp). This is O(1) per lookup.
        3. Collect all (index → instance_id) assignments and apply them in a
           single batch write to the DataFrame.

    Args:
        case_log: The event log to match. Modified in place (INSTANCE column).

    """
    instance_col = StandardColumnNames.INSTANCE.value

    # --- Build per-activity deques of unmatched start events (sorted ascending) ---
    start_mask = case_log[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.START
    starts_sorted = case_log[start_mask].sort_values(StandardColumnNames.TIMESTAMP, ascending=True)

    # pending[activity] = deque of (timestamp, row_index) in ascending timestamp order
    pending: dict[str, deque[tuple]] = defaultdict(deque)
    for idx, row in starts_sorted.iterrows():
        pending[row[StandardColumnNames.ACTIVITY]].append((row[StandardColumnNames.TIMESTAMP], idx))

    # --- Iterate complete events and match greedily ---
    complete_mask = case_log[StandardColumnNames.LIFECYCLE_TRANSITION] == LifecycleTransitionType.COMPLETE
    complete_events = case_log[complete_mask]

    # Collect assignments to apply in one batch
    assignments: dict[int, str] = {}

    for idx, row in complete_events.iterrows():
        activity = row[StandardColumnNames.ACTIVITY]
        ts = row[StandardColumnNames.TIMESTAMP]

        instance_id = id_generator.get_next_id()
        assignments[idx] = instance_id

        candidates = pending[activity]
        if candidates and candidates[0][0] <= ts:
            _, start_idx = candidates.popleft()
            assignments[start_idx] = instance_id

    # --- Batch-write all instance IDs at once ---
    if assignments:
        case_log.loc[list(assignments.keys()), instance_col] = list(assignments.values())
