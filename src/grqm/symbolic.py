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
    derivation_ok: bool


def validate_correction_term_symbolic(correction_power: int = 5) -> SymbolicValidationResult:
    """Validate symbolic scaling of the correction channel used in ``grqm.core.accel``.

    Model channel in code:
        a_ddot = -(Omega_m)/(2*a**2) + Omega_l*a + alpha/a**n

    We verify two invariants symbolically:
    1) Leading small-a scaling of correction term is ``a**(-n)``.
    2) Relative-to-classical matter-dominated scaling is ``~ a**(2-n)``.
    """

    if correction_power <= 0:
        raise ValueError("correction_power must be positive")

    a, omega_m, omega_l, alpha = sp.symbols("a omega_m omega_l alpha", positive=True, finite=True)
    n = sp.Integer(correction_power)

    classical = -(omega_m) / (2 * a**2) + omega_l * a
    correction = alpha / a**n

    correction_asym = sp.series(correction, a, 0, 1)
    leading = correction_asym.removeO().as_leading_term(a)
    leading_exponent = int(leading.as_powers_dict()[a])

    ratio = sp.simplify(correction / classical)
    ratio_leading = sp.series(ratio, a, 0, 1).removeO().as_leading_term(a)
    ratio_exponent = int(ratio_leading.as_powers_dict()[a])

    signed_limit = sp.limit(correction, a, 0, dir="+")
    ratio_abs_limit = sp.limit(sp.Abs(ratio), a, 0, dir="+")

    derivation_ok = (leading_exponent == -correction_power) and (ratio_exponent == 2 - correction_power)

    return SymbolicValidationResult(
        correction_power=correction_power,
        leading_exponent=leading_exponent,
        small_a_limit_signed=str(signed_limit),
        ratio_exponent=ratio_exponent,
        ratio_small_a_limit_abs=str(ratio_abs_limit),
        derivation_ok=derivation_ok,
    )
