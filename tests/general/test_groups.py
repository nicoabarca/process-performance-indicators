import pytest

from process_performance_indicators.exceptions import ColumnNotFoundError
from process_performance_indicators.general.groups import (
    activity_count,
    activity_instance_count,
    case_count,
    expected_activity_count,
    expected_activity_instance_count,
    expected_human_resource_count,
    expected_resource_count,
    expected_role_count,
    human_resource_count,
    resource_count,
    role_count,
)


class TestGroups:
    def test_activity_count(self, sample_event_log):
        """Test counting activities for a group of cases"""
        # Test with multiple cases
        assert (
            activity_count(sample_event_log, ["case1", "case2"]) == 5
        )  # 2 from case1 + 3 from case2

        # Test with a single case
        assert activity_count(sample_event_log, ["case3"]) == 1

        # Test with a set of cases
        assert activity_count(sample_event_log, {"case1", "case3"}) == 3

        # Test with non-existent case
        assert activity_count(sample_event_log, ["case1", "non_existent_case"]) == 2

    def test_expected_activity_count(self, sample_event_log):
        """Test expected activity count for a group of cases"""
        # Test with multiple cases
        assert expected_activity_count(sample_event_log, ["case1", "case2"]) == 2.5  # (2+3)/2

        # Test with a single case
        assert expected_activity_count(sample_event_log, ["case3"]) == 1.0

    def test_activity_instance_count(self, sample_event_log):
        """Test counting activity instances for a group of cases"""
        # Test with multiple cases
        assert (
            activity_instance_count(sample_event_log, ["case1", "case2"]) == 5
        )  # 3 from case1 + 2 from case2

        # Test with a single case
        assert activity_instance_count(sample_event_log, ["case3"]) == 1

    def test_activity_instance_count_missing_column(self, event_log_missing_columns):
        """Test activity_instance_count with missing instance column"""
        with pytest.raises(ColumnNotFoundError):
            activity_instance_count(event_log_missing_columns, ["case1"])

    def test_expected_activity_instance_count(self, sample_event_log):
        """Test expected activity instance count for a group of cases"""
        # Test with multiple cases
        assert (
            expected_activity_instance_count(sample_event_log, ["case1", "case2"]) == 2.5
        )  # (3+2)/2

        # Test with a single case
        assert expected_activity_instance_count(sample_event_log, ["case3"]) == 1.0

    def test_case_count(self, sample_event_log):
        """Test counting cases in a group"""
        # Test with all existing cases
        assert case_count(sample_event_log, ["case1", "case2", "case3"]) == 3

        # Test with some non-existent cases
        assert case_count(sample_event_log, ["case1", "non_existent_case"]) == 1

        # Test with all non-existent cases
        assert case_count(sample_event_log, ["non_existent_case1", "non_existent_case2"]) == 0

    def test_human_resource_count(self, sample_event_log):
        """Test counting human resources for a group of cases"""
        # Test with multiple cases
        assert human_resource_count(sample_event_log, ["case1", "case2"]) == 3  # hr1, hr2, hr3

        # Test with a single case
        assert human_resource_count(sample_event_log, ["case3"]) == 1  # hr3

    def test_human_resource_count_missing_column(self, event_log_missing_columns):
        """Test human_resource_count with missing human resource column"""
        with pytest.raises(ColumnNotFoundError):
            human_resource_count(event_log_missing_columns, ["case1"])

    def test_expected_human_resource_count(self, sample_event_log):
        """Test expected human resource count for a group of cases"""
        # Test with multiple cases
        assert expected_human_resource_count(sample_event_log, ["case1", "case2"]) == 2.5  # (2+3)/2

        # Test with a single case
        assert expected_human_resource_count(sample_event_log, ["case3"]) == 1.0

    def test_resource_count(self, sample_event_log):
        """Test counting resources for a group of cases"""
        # Test with multiple cases
        assert resource_count(sample_event_log, ["case1", "case2"]) == 3  # res1, res2, res3

        # Test with a single case
        assert resource_count(sample_event_log, ["case3"]) == 1  # res3

    def test_resource_count_missing_column(self, event_log_missing_columns):
        """Test resource_count with missing resource column"""
        with pytest.raises(ColumnNotFoundError):
            resource_count(event_log_missing_columns, ["case1"])

    def test_expected_resource_count(self, sample_event_log):
        """Test expected resource count for a group of cases"""
        # Test with multiple cases
        assert expected_resource_count(sample_event_log, ["case1", "case2"]) == 2.5  # (2+3)/2

        # Test with a single case
        assert expected_resource_count(sample_event_log, ["case3"]) == 1.0

    def test_role_count(self, sample_event_log):
        """Test counting roles for a group of cases"""
        # Test with multiple cases
        assert role_count(sample_event_log, ["case1", "case2"]) == 3  # role1, role2, role3

        # Test with a single case
        assert role_count(sample_event_log, ["case3"]) == 1  # role1

    def test_role_count_missing_column(self, event_log_missing_columns):
        """Test role_count with missing role column"""
        with pytest.raises(ColumnNotFoundError):
            role_count(event_log_missing_columns, ["case1"])

    def test_expected_role_count(self, sample_event_log):
        """Test expected role count for a group of cases"""
        # Test with multiple cases
        assert expected_role_count(sample_event_log, ["case1", "case2"]) == 2.5  # (2+3)/2

        # Test with a single case
        assert expected_role_count(sample_event_log, ["case3"]) == 1.0

    def test_group_with_empty_cases(self, sample_event_log):
        """Test group functions with empty case list"""
        assert activity_count(sample_event_log, []) == 0
        assert case_count(sample_event_log, []) == 0

        # The following functions should raise exceptions with empty case lists
        # since they involve division by case_count
        with pytest.raises(ZeroDivisionError):
            expected_activity_count(sample_event_log, [])

        with pytest.raises(ZeroDivisionError):
            expected_activity_instance_count(sample_event_log, [])
