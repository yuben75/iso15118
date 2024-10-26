import pytest
import sys
import os

# 動態添加專案根目錄的模組路徑
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', 'iso15118'))
sys.path.append(project_root)

from iso15118.shared.validators import one_field_must_be_set, validate_bytes_value_range


def test_validate_bytes_value_range():
    dummy_value = b"\x00\x02"

    assert validate_bytes_value_range("dummy", dummy_value, 0, 2)

    with pytest.raises(ValueError):
        validate_bytes_value_range("dummy", dummy_value, 0, 1)


def test_one_field_must_be_set():
    fields_to_test = ["ac_ev_charge_parameter", "dc_ev_charge_parameter"]

    just_one_set = {"ac_ev_charge_parameter": 123}

    assert one_field_must_be_set(fields_to_test, just_one_set, True)

    with pytest.raises(ValueError):
        two_values_set = {"ac_ev_charge_parameter": 123, "dc_ev_charge_parameter": 321}
        assert one_field_must_be_set(fields_to_test, two_values_set, True)

    with pytest.raises(ValueError):
        no_values_set = {"no_accepted_value": 1234}
        assert one_field_must_be_set(fields_to_test, no_values_set, True)
