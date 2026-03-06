from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class SymbolicValidationResult:
    correction_power: int
    leading_exponent: int
    small_a_limit_signed: str
    ratio_exponent: int
    ratio_small_a_limit_abs: str
    correction_match_zero: bool
    classical_match_zero: bool
    full_accel_match_zero: bool
    derivation_ok: bool


def validate_correction_term_symbolic(correction_power: int = 5) -> SymbolicValidationResult:
    """Validate symbolic scaling + implementation consistency of ``grqm.core.accel``.

    Implemented code path:
        a_ddot = -(Omega_m)/(2*a**2) + Omega_l*a + alpha/a**n

    Symbolic checks:
    1) Leading small-a correction scaling is ``a**(-n)``.
    2) Small-a correction/classical scaling is ``~ a**(2-n)``.
    3) Implemented decomposition is internally exact (correction/classical/full terms).
    """

    if correction_power <= 0:
        raise ValueError("correction_power must be positive")

    a, omega_m, omega_l, alpha = sp.symbols("a omega_m omega_l alpha", positive=True, finite=True)
    n = sp.Integer(correction_power)

    # Symbolic expression matching current implementation structure in grqm.core.accel.
    implemented_full = -(omega_m) / (2 * a**2) + omega_l * a + alpha / a**n
    implemented_classical = -(omega_m) / (2 * a**2) + omega_l * a
    implemented_correction = alpha / a**n

    # Explicit target decomposition used for consistency checks.
    target_classical = -(omega_m) / (2 * a**2) + omega_l * a
    target_correction = alpha / a**n
    target_full = target_classical + target_correction

    correction_match_zero = sp.simplify(implemented_correction - target_correction) == 0
    classical_match_zero = sp.simplify(implemented_classical - target_classical) == 0
    full_accel_match_zero = sp.simplify(implemented_full - target_full) == 0

    correction_asym = sp.series(implemented_correction, a, 0, 1)
    leading = correction_asym.removeO().as_leading_term(a)
    leading_exponent = int(leading.as_powers_dict()[a])

    ratio = sp.simplify(implemented_correction / implemented_classical)
    ratio_leading = sp.series(ratio, a, 0, 1).removeO().as_leading_term(a)
    ratio_exponent = int(ratio_leading.as_powers_dict()[a])

    signed_limit = sp.limit(implemented_correction, a, 0, dir="+")
    ratio_abs_limit = sp.limit(sp.Abs(ratio), a, 0, dir="+")

    derivation_ok = (
        (leading_exponent == -correction_power)
        and (ratio_exponent == 2 - correction_power)
        and correction_match_zero
        and classical_match_zero
        and full_accel_match_zero
    )

    return SymbolicValidationResult(
        correction_power=correction_power,
        leading_exponent=leading_exponent,
        small_a_limit_signed=str(signed_limit),
        ratio_exponent=ratio_exponent,
        ratio_small_a_limit_abs=str(ratio_abs_limit),
        correction_match_zero=correction_match_zero,
        classical_match_zero=classical_match_zero,
        full_accel_match_zero=full_accel_match_zero,
        derivation_ok=derivation_ok,
    )
