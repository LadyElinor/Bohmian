from __future__ import annotations

import sympy as sp

from grqm.bohmian_probe.symbolic_core import (
    build_minisuperspace_hamiltonian,
    build_operator_set,
    build_symbols,
    decompose_psi,
    symbolic_receipt,
    wdw_operator,
)


def test_hamiltonian_finite_on_nominal_point():
    s = build_symbols()
    H = build_minisuperspace_hamiltonian(s)
    val = complex(
        H.evalf(
            subs={
                s.a: 1.0,
                s.phi: 0.1,
                s.p_a: 0.2,
                s.p_phi: 0.05,
                s.omega_m: 0.3,
                s.omega_l: 0.7,
                s.m_phi: 1.0,
            }
        )
    )
    assert abs(val) < float("inf")


def test_operator_set_components_are_finite_on_nominal_point():
    s = build_symbols()
    psi = sp.exp(-(s.a - 1) ** 2 - s.phi**2) * sp.exp(sp.I * (s.a + s.phi) / s.hbar)
    ops = build_operator_set(psi, s)
    subs = {s.a: 1.0, s.phi: 0.1, s.omega_m: 0.3, s.omega_l: 0.7, s.m_phi: 1.0, s.hbar: 1.0, s.nu: 1.0}
    assert abs(complex(ops.kinetic_a.evalf(subs=subs))) < float("inf")
    assert abs(complex(ops.kinetic_phi.evalf(subs=subs))) < float("inf")
    assert abs(complex(ops.potential.evalf(subs=subs))) < float("inf")


def test_rs_decomposition_reconstructs_psi_modulus():
    s = build_symbols()
    psi = sp.exp(-(s.a - 1) ** 2 - s.phi**2) * sp.exp(sp.I * (s.a + s.phi) / s.hbar)
    R, _S = decompose_psi(psi, s.hbar)
    assert sp.simplify(psi * sp.conjugate(psi) - R**2) == 0


def test_wdw_residual_small_on_reference_ansatz():
    s = build_symbols()
    psi = sp.exp(-(s.a - 1) ** 2 - s.phi**2) * sp.exp(sp.I * (s.a + s.phi) / s.hbar)
    w = wdw_operator(psi, s)
    val = complex(
        w.evalf(
            subs={
                s.a: 1.0,
                s.phi: 0.1,
                s.omega_m: 0.3,
                s.omega_l: 0.7,
                s.m_phi: 1.0,
                s.hbar: 1.0,
                s.nu: 1.0,
            }
        )
    )
    assert abs(val) < 20.0


def test_symbolic_receipt_flags_true_on_nominal_setup():
    r = symbolic_receipt()
    assert r.hamiltonian_finite_on_nominal_point is True
    assert r.decomposition_reconstruction_ok is True
    assert r.wdw_residual_nominal_finite is True
    assert any("Factor-ordering" in a for a in r.assumptions)
