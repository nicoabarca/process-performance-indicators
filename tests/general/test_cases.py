import pytest

from process_performance_indicators.exceptions import ColumnNotFoundError
from process_performance_indicators.general.cases import (
    activity_count,
    activity_instance_count,
    human_resource_count,
    resource_count,
    role_count,
)


class TestCases:
    def test_activity_count(self, sample_event_log):
        """Test counting activities for a specific case"""
        # Test case with multiple activities
        assert activity_count(sample_event_log, "case1") == 2  # activity1, activity2

        # Test case with a single activity
        assert activity_count(sample_event_log, "case3") == 1  # activity1

    def test_activity_count_invalid_case(self, sample_event_log):
        """Test activity_count with non-existent case"""
        # Empty result for non-existent case, not an error
        with pytest.raises(
            ValueError,
            match="CASE_ID = 'non_existent_case' not found in event log. Check your event log CASE_ID column for possible values.",
        ):
            activity_count(sample_event_log, "non_existent_case")

    def test_activity_instance_count(self, sample_event_log):
        """Test counting activity instances for a specific case"""
        # Test case with multiple activity instances
        assert activity_instance_count(sample_event_log, "case1") == 3  # inst1, inst2, inst3

        # Test case with a single activity instance
        assert activity_instance_count(sample_event_log, "case3") == 1  # inst6

    def test_activity_instance_count_missing_column(self, event_log_missing_columns):
        """Test activity_instance_count with missing instance column"""
        with pytest.raises(ColumnNotFoundError):
            activity_instance_count(event_log_missing_columns, "case1")

    def test_activity_instance_count_invalid_case(self, sample_event_log):
        """Test activity_instance_count with non-existent case"""
        # Non-existent case should result in 0 instances, not an error
        with pytest.raises(
            ValueError,
            match="CASE_ID = 'non_existent_case' not found in event log. Check your event log CASE_ID column for possible values.",
        ):
            activity_instance_count(sample_event_log, "non_existent_case")

    def test_human_resource_count(self, sample_event_log):
        """Test counting human resources for a specific case"""
        # Test case with multiple human resources
        assert human_resource_count(sample_event_log, "case1") == 2  # hr1, hr2

        # Test case with a single human resource
        assert human_resource_count(sample_event_log, "case3") == 1  # hr3

    def test_human_resource_count_missing_column(self, event_log_missing_columns):
        """Test human_resource_count with missing human resource column"""
        with pytest.raises(ColumnNotFoundError):
            human_resource_count(event_log_missing_columns, "case1")

    def test_human_resource_count_invalid_case(self, sample_event_log):
        """Test human_resource_count with non-existent case"""
        # Non-existent case should result in 0 human resources, not an error
        with pytest.raises(
            ValueError,
            match="CASE_ID = 'non_existent_case' not found in event log. Check your event log CASE_ID column for possible values.",
        ):
            human_resource_count(sample_event_log, "non_existent_case")

    def test_resource_count(self, sample_event_log):
        """Test counting resources for a specific case"""
        # Test case with multiple resources
        assert resource_count(sample_event_log, "case1") == 2  # res1, res2

        # Test case with a single resource
        assert resource_count(sample_event_log, "case3") == 1  # res3

    def test_resource_count_missing_column(self, event_log_missing_columns):
        """Test resource_count with missing resource column"""
        with pytest.raises(ColumnNotFoundError):
            resource_count(event_log_missing_columns, "case1")

    def test_resource_count_invalid_case(self, sample_event_log):
        """Test resource_count with non-existent case"""
        # Non-existent case should result in 0 resources, not an error
        with pytest.raises(
            ValueError,
            match="CASE_ID = 'non_existent_case' not found in event log. Check your event log CASE_ID column for possible values.",
        ):
            resource_count(sample_event_log, "non_existent_case")

    def test_role_count(self, sample_event_log):
        """Test counting roles for a specific case"""
        # Test case with multiple roles
        assert role_count(sample_event_log, "case1") == 2  # role1, role2

        # Test case with a single role
        assert role_count(sample_event_log, "case3") == 1  # role1

    def test_role_count_missing_column(self, event_log_missing_columns):
        """Test role_count with missing role column"""
        with pytest.raises(ColumnNotFoundError):
            role_count(event_log_missing_columns, "case1")

    def test_role_count_invalid_case(self, sample_event_log):
        """Test role_count with non-existent case"""
        # Non-existent case should result in 0 roles, not an error
        with pytest.raises(
            ValueError,
            match="CASE_ID = 'non_existent_case' not found in event log. Check your event log CASE_ID column for possible values.",
        ):
            role_count(sample_event_log, "non_existent_case")
