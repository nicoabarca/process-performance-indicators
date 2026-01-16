import pytest

from process_performance_indicators.constants import StandardColumnNames
from process_performance_indicators.exceptions import ActivityNameNotFoundError, ColumnNotFoundError
from process_performance_indicators.indicators.general.activities import (
    activity_instance_count,
    human_resource_count,
    resource_count,
)


class TestActivities:
    def test_activity_instance_count(self, sample_event_log):
        """Test counting activity instances for a specific activity"""
        # Test activity with multiple instances
        qty_of_activities = len(sample_event_log[StandardColumnNames.ACTIVITY])
        intances = 0
        for activity in sample_event_log[StandardColumnNames.ACTIVITY].unique():
            intances += activity_instance_count(sample_event_log, activity)
        assert intances == qty_of_activities

        # Test activity with a single instance
        assert activity_instance_count(sample_event_log, "activity3") == 1

    def test_activity_instance_count_invalid_activity(self, sample_event_log):
        """Test activity_instance_count with non-existent activity"""
        with pytest.raises(ActivityNameNotFoundError):
            activity_instance_count(sample_event_log, "non_existent_activity")

    def test_human_resource_count(self, sample_event_log):
        """Test counting human resources for a specific activity"""
        # Test activity with multiple human resources
        assert human_resource_count(sample_event_log, "activity1") == 2  # hr1, hr3

        # Test activity with a single human resource
        assert human_resource_count(sample_event_log, "activity3") == 1  # hr2

    def test_human_resource_count_missing_column(self, event_log_missing_columns):
        """Test human_resource_count with missing human resource column"""
        with pytest.raises(ColumnNotFoundError):
            human_resource_count(event_log_missing_columns, "activity1")

    def test_human_resource_count_invalid_activity(self, sample_event_log):
        """Test human_resource_count with non-existent activity"""
        with pytest.raises(ActivityNameNotFoundError):
            human_resource_count(sample_event_log, "non_existent_activity")

    def test_resource_count(self, sample_event_log):
        """Test counting resources for a specific activity"""
        # Test activity with multiple resources
        assert resource_count(sample_event_log, "activity1") == 2  # res1, res3

        # Test activity with a single resource
        assert resource_count(sample_event_log, "activity3") == 1  # res2

    def test_resource_count_missing_column(self, event_log_missing_columns):
        """Test resource_count with missing resource column"""
        with pytest.raises(ColumnNotFoundError):
            resource_count(event_log_missing_columns, "activity1")

    def test_resource_count_invalid_activity(self, sample_event_log):
        """Test resource_count with non-existent activity"""
        with pytest.raises(ActivityNameNotFoundError):
            resource_count(sample_event_log, "non_existent_activity")
