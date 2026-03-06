from __future__ import annotations

from grqm.symbolic import validate_correction_term_symbolic


def test_symbolic_validation_expected_scaling_default_power():
    result = validate_correction_term_symbolic(correction_power=5)
    assert result.leading_exponent == -5
    assert result.ratio_exponent == -3
    assert result.derivation_ok is True


def test_symbolic_validation_expected_scaling_alt_power():
    result = validate_correction_term_symbolic(correction_power=4)
    assert result.leading_exponent == -4
    assert result.ratio_exponent == -2
    assert result.derivation_ok is True
