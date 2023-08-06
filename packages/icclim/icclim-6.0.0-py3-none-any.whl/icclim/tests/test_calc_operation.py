from __future__ import annotations

from typing import Callable
from unittest.mock import MagicMock, patch

import pytest

from icclim.icclim_exceptions import InvalidIcclimArgumentError
from icclim.models.constants import PRECIPITATION, TEMPERATURE
from icclim.models.frequency import FrequencyRegistry
from icclim.models.index_config import ClimateVariable
from icclim.models.operator import OperatorRegistry
from icclim.tests.testing_utils import stub_pr, stub_tas, stub_user_index
from icclim.user_indices import calc_operation
from icclim.user_indices.calc_operation import (
    CalcOperationRegistry,
    anomaly,
    compute_user_index,
    count_events,
    max_consecutive_event_count,
    run_mean,
    run_sum,
)


class Test_compute:
    def test_error_bad_operation(self):
        # GIVEN
        cf_var = ClimateVariable("tas", stub_tas(), stub_tas())
        user_index = stub_user_index([cf_var])
        user_index.calc_operation = "pouet pouet"
        user_index.frequency = FrequencyRegistry.MONTH
        # WHEN
        with pytest.raises(InvalidIcclimArgumentError):
            compute_user_index(user_index)

    def test_simple(self):
        # GIVEN
        cf_var = ClimateVariable("tas", stub_tas(), stub_tas())
        user_index = stub_user_index([cf_var])
        user_index.calc_operation = "max"
        user_index.frequency = FrequencyRegistry.MONTH
        # WHEN
        result = compute_user_index(user_index)
        # THEN
        assert result.data[0] == 1

    def test_simple_percentile_pr(self):
        # GIVEN
        cf_var = ClimateVariable("tas", stub_pr(5), stub_pr(5))
        cf_var.studied_data.data[15:30] += 10
        cf_var.studied_data.data[366 + 15 : 366 + 30] = 2  # Ignore because not in base
        cf_var.reference_da = cf_var.studied_data.sel(
            time=cf_var.studied_data.time.dt.year == 2042
        )
        user_index = stub_user_index([cf_var])
        user_index.calc_operation = CalcOperationRegistry.MIN
        user_index.thresh = "90p"
        user_index.logical_operation = OperatorRegistry.GREATER_OR_EQUAL
        user_index.var_type = PRECIPITATION
        user_index.frequency = FrequencyRegistry.YEAR
        # WHEN
        result = compute_user_index(user_index)
        # THEN
        assert result.data[0] == 5

    def test_simple_percentile_temp(self):
        cf_var = ClimateVariable("tas", stub_tas(5), stub_tas(5))
        cf_var.studied_data.data[15:30] = 1
        cf_var.reference_da = cf_var.studied_data.sel(
            time=cf_var.studied_data.time.dt.year.isin([2042, 2043])
        )
        user_index = stub_user_index([cf_var])
        user_index.calc_operation = "min"
        user_index.thresh = "10p"
        user_index.logical_operation = OperatorRegistry.LOWER_OR_EQUAL
        user_index.var_type = TEMPERATURE
        user_index.frequency = FrequencyRegistry.MONTH
        # WHEN
        result = compute_user_index(user_index)
        # THEN
        assert result.data[0] == 1
        assert result.data[1] == 5

    @patch("icclim.models.user_index_config.UserIndexConfig")
    @patch("icclim.models.index_config.CfVariable")
    def test_error_anomaly(self, config_mock: MagicMock, cf_var_mock: MagicMock):
        config_mock.cf_vars = [cf_var_mock]
        cf_var_mock.reference_da = None
        with pytest.raises(InvalidIcclimArgumentError):
            anomaly(config_mock)

    @patch("icclim.models.user_index_config.UserIndexConfig")
    @patch("icclim.user_indices.operators.anomaly")
    @patch("icclim.models.index_config.CfVariable")
    def test_success_anomaly(
        self, config_mock: MagicMock, op_mock: MagicMock, cf_var_mock: MagicMock
    ):
        config_mock.cf_vars = [cf_var_mock]
        cf_var_mock.reference_da = [1, 2, 3]  # no-op, just need to mock a valid length
        anomaly(config_mock)
        op_mock.assert_called_once()

    @patch("icclim.models.user_index_config.UserIndexConfig")
    def test_error_run_sum(self, config_mock: MagicMock):
        config_mock.extreme_mode = None
        with pytest.raises(InvalidIcclimArgumentError):
            run_sum(config_mock)
        config_mock.extreme_mode = {}
        config_mock.window_width = None
        with pytest.raises(InvalidIcclimArgumentError):
            run_sum(config_mock)

    @patch("icclim.user_indices.operators.run_sum")
    @patch("icclim.models.user_index_config.UserIndexConfig")
    def test_success_run_sum(self, config_mock: MagicMock, op_mock: MagicMock):
        run_sum(config_mock)
        op_mock.assert_called_once()

    @patch("icclim.models.user_index_config.UserIndexConfig")
    def test_error_run_mean(self, config_mock: MagicMock):
        config_mock.extreme_mode = None
        with pytest.raises(InvalidIcclimArgumentError):
            run_mean(config_mock)
        config_mock.extreme_mode = {}
        config_mock.window_width = None
        with pytest.raises(InvalidIcclimArgumentError):
            run_mean(config_mock)

    @patch("icclim.user_indices.operators.run_mean")
    @patch("icclim.models.user_index_config.UserIndexConfig")
    def test_success_run_mean(self, config_mock: MagicMock, op_mock: MagicMock):
        run_mean(config_mock)
        op_mock.assert_called_once()

    @patch("icclim.models.user_index_config.UserIndexConfig")
    def test_error_max_consecutive_event_count(self, config_mock: MagicMock):
        config_mock.logical_operation = None
        with pytest.raises(InvalidIcclimArgumentError):
            max_consecutive_event_count(config_mock)
        config_mock.logical_operation = {}
        config_mock.thresh = None
        with pytest.raises(InvalidIcclimArgumentError):
            max_consecutive_event_count(config_mock)
        config_mock.logical_operation = {}
        config_mock.thresh = []
        with pytest.raises(InvalidIcclimArgumentError):
            max_consecutive_event_count(config_mock)

    @patch("icclim.user_indices.operators.max_consecutive_event_count")
    @patch("icclim.models.user_index_config.UserIndexConfig")
    def test_success_max_consecutive_event_count(
        self, config_mock: MagicMock, op_mock: MagicMock
    ):
        max_consecutive_event_count(config_mock)
        op_mock.assert_called_once()

    @patch("icclim.models.user_index_config.UserIndexConfig")
    def test_error_count_events(self, config_mock: MagicMock):
        config_mock.nb_event_config = None
        with pytest.raises(InvalidIcclimArgumentError):
            count_events(config_mock)

    @patch("icclim.user_indices.operators.count_events")
    @patch("icclim.models.user_index_config.UserIndexConfig")
    def test_success_count_events(self, config_mock: MagicMock, op_mock: MagicMock):
        count_events(config_mock)
        op_mock.assert_called_once()

    @pytest.mark.parametrize(
        "reducer",
        [
            calc_operation.sum,
            calc_operation.mean,
            calc_operation.min,
            calc_operation.max,
        ],
    )
    @patch("icclim.models.user_index_config.UserIndexConfig")
    def test_error_simple_reducer(self, config_mock: MagicMock, reducer: Callable):
        config_mock.cf_vars = [1, 2, 3]
        with pytest.raises(InvalidIcclimArgumentError):
            reducer(config_mock)
        config_mock.cf_vars = [MagicMock()]
        config_mock.thresh = []
        with pytest.raises(InvalidIcclimArgumentError):
            reducer(config_mock)

    @pytest.mark.parametrize("reducer", ["sum", "mean", "min", "max"])
    @patch("icclim.models.user_index_config.UserIndexConfig")
    def test_success_simple_reducer(self, config_mock: MagicMock, reducer: str):
        config_mock.calc_operation = reducer
        config_mock.cf_vars = [MagicMock()]
        config_mock.thresh = 42
        with patch("icclim.user_indices.operators." + reducer) as op_mock:
            compute_user_index(config_mock)
            op_mock.assert_called_once()
