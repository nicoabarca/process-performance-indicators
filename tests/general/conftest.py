import pandas as pd
import pytest

from process_performance_indicators.constants import StandardColumnNames


@pytest.fixture
def sample_event_log():
    """Create a sample event log for testing general module functions"""
    data = {
        StandardColumnNames.CASE_ID: ["case1", "case1", "case1", "case2", "case2", "case3"],
        StandardColumnNames.ACTIVITY: [
            "activity1",
            "activity2",
            "activity1",
            "activity2",
            "activity3",
            "activity1",
        ],
        StandardColumnNames.TIMESTAMP: [
            pd.Timestamp("2023-01-01 10:00:00"),
            pd.Timestamp("2023-01-01 11:00:00"),
            pd.Timestamp("2023-01-01 12:00:00"),
            pd.Timestamp("2023-01-02 10:00:00"),
            pd.Timestamp("2023-01-02 11:00:00"),
            pd.Timestamp("2023-01-03 10:00:00"),
        ],
        StandardColumnNames.INSTANCE: ["inst1", "inst2", "inst3", "inst4", "inst5", "inst6"],
        StandardColumnNames.HUMAN_RESOURCE: ["hr1", "hr2", "hr1", "hr3", "hr2", "hr3"],
        StandardColumnNames.ROLE: ["role1", "role2", "role1", "role2", "role3", "role1"],
        StandardColumnNames.ORG_RESOURCE: ["res1", "res2", "res1", "res3", "res2", "res3"],
    }

    return pd.DataFrame(data)


@pytest.fixture
def empty_event_log():
    """Create an empty event log for testing error cases"""
    return pd.DataFrame()


@pytest.fixture
def event_log_missing_columns():
    """Create an event log missing required columns for testing error cases"""
    data = {
        StandardColumnNames.CASE_ID: ["case1", "case1", "case2"],
        StandardColumnNames.ACTIVITY: ["activity1", "activity2", "activity1"],
        StandardColumnNames.TIMESTAMP: [
            pd.Timestamp("2023-01-01 10:00:00"),
            pd.Timestamp("2023-01-01 11:00:00"),
            pd.Timestamp("2023-01-02 10:00:00"),
        ],
    }

    return pd.DataFrame(data)
