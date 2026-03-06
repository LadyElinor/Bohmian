from __future__ import annotations

import pytest

from grqm.symbolic import validate_correction_term_symbolic


def test_symbolic_validation_expected_scaling_default_power():
    result = validate_correction_term_symbolic(correction_power=5)
    assert result.leading_exponent == -5
    assert result.ratio_exponent == -3
    assert result.correction_match_zero is True
    assert result.classical_match_zero is True
    assert result.full_accel_match_zero is True
    assert result.derivation_ok is True


def test_symbolic_validation_expected_scaling_alt_power():
    result = validate_correction_term_symbolic(correction_power=4)
    assert result.leading_exponent == -4
    assert result.ratio_exponent == -2
    assert result.correction_match_zero is True
    assert result.classical_match_zero is True
    assert result.full_accel_match_zero is True
    assert result.derivation_ok is True


@pytest.mark.parametrize("bad_power", [0, -1, -5])
def test_symbolic_validation_rejects_nonpositive_power(bad_power: int):
    with pytest.raises(ValueError):
        validate_correction_term_symbolic(correction_power=bad_power)
