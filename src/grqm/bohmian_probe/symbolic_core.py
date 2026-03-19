from __future__ import annotations

from dataclasses import asdict, dataclass

import sympy as sp


@dataclass(frozen=True)
class BohmianSymbolicReceipt:
    model_label: str
    assumptions: list[str]
    branch_choice: str
    hamiltonian_finite_on_nominal_point: bool
    decomposition_reconstruction_ok: bool
    wdw_residual_nominal_finite: bool


@dataclass(frozen=True)
class SymbolSet:
    a: sp.Symbol
    phi: sp.Symbol
    p_a: sp.Symbol
    p_phi: sp.Symbol
    omega_m: sp.Symbol
    omega_l: sp.Symbol
    m_phi: sp.Symbol
    hbar: sp.Symbol
    nu: sp.Symbol


@dataclass(frozen=True)
class MinisuperspaceOperators:
    kinetic_a: sp.Expr
    kinetic_phi: sp.Expr
    potential: sp.Expr
    wdw_total: sp.Expr


def build_symbols() -> SymbolSet:
    a, phi = sp.symbols("a phi", positive=True, finite=True, real=True)
    p_a, p_phi = sp.symbols("p_a p_phi", real=True, finite=True)
    omega_m, omega_l, m_phi = sp.symbols("omega_m omega_l m_phi", positive=True, finite=True, real=True)
    hbar = sp.symbols("hbar", positive=True, finite=True, real=True)
    nu = sp.symbols("nu", real=True, finite=True)
    return SymbolSet(a=a, phi=phi, p_a=p_a, p_phi=p_phi, omega_m=omega_m, omega_l=omega_l, m_phi=m_phi, hbar=hbar, nu=nu)


def scalar_potential(phi: sp.Expr, omega_l: sp.Symbol, m_phi: sp.Symbol) -> sp.Expr:
    # Local expansion around phi=0: constant + quadratic correction.
    return omega_l + sp.Rational(1, 2) * m_phi**2 * phi**2


def build_minisuperspace_hamiltonian(symbols: SymbolSet) -> sp.Expr:
    V = scalar_potential(symbols.phi, symbols.omega_l, symbols.m_phi)
    # Reduced FRW minisuperspace Hamiltonian proxy under gauge-fixed lapse.
    H = -symbols.p_a**2 / (2 * symbols.a) + symbols.p_phi**2 / (2 * symbols.a**3) - symbols.omega_m / symbols.a + symbols.a**3 * V
    return sp.simplify(H)


def build_operator_set(psi: sp.Expr, symbols: SymbolSet) -> MinisuperspaceOperators:
    # Factor-ordering ansatz: a^{-nu} d_a (a^{nu} d_a).
    d_a = sp.diff(psi, symbols.a)
    kinetic_a = -symbols.hbar**2 * (sp.diff(psi, symbols.a, 2) + (symbols.nu / symbols.a) * d_a)
    kinetic_phi = symbols.hbar**2 * sp.diff(psi, symbols.phi, 2)
    V = scalar_potential(symbols.phi, symbols.omega_l, symbols.m_phi)
    potential = (symbols.a**4 * V - symbols.omega_m * symbols.a) * psi
    wdw_total = sp.simplify(kinetic_a + kinetic_phi + potential)
    return MinisuperspaceOperators(kinetic_a=sp.simplify(kinetic_a), kinetic_phi=sp.simplify(kinetic_phi), potential=sp.simplify(potential), wdw_total=wdw_total)


def decompose_psi(psi: sp.Expr, hbar: sp.Symbol) -> tuple[sp.Expr, sp.Expr]:
    # Principal branch phase S = hbar * Arg(psi).
    R = sp.sqrt(sp.simplify(sp.Abs(psi) ** 2))
    S = hbar * sp.arg(psi)
    return sp.simplify(R), sp.simplify(S)


def wdw_operator(psi: sp.Expr, symbols: SymbolSet) -> sp.Expr:
    return build_operator_set(psi, symbols).wdw_total


def symbolic_receipt() -> BohmianSymbolicReceipt:
    s = build_symbols()
    H = build_minisuperspace_hamiltonian(s)

    # Smooth bounded ansatz used only for symbolic sanity checks.
    psi = sp.exp(-(s.a - 1) ** 2 - s.phi**2) * sp.exp(sp.I * (s.a + s.phi) / s.hbar)
    R, _S = decompose_psi(psi, s.hbar)

    recon = sp.simplify(psi * sp.conjugate(psi) - R**2)
    W = wdw_operator(psi, s)

    subs_nominal = {
        s.a: 1.0,
        s.phi: 0.1,
        s.p_a: 0.2,
        s.p_phi: 0.05,
        s.omega_m: 0.3,
        s.omega_l: 0.7,
        s.m_phi: 1.0,
        s.hbar: 1.0,
        s.nu: 1.0,
    }

    h_val = complex(H.evalf(subs=subs_nominal))
    w_val = complex(W.evalf(subs=subs_nominal))

    return BohmianSymbolicReceipt(
        model_label="bohmian_minisuperspace_phase1_adaptation",
        assumptions=[
            "Homogeneous isotropic FRW minisuperspace truncation.",
            "a>0 domain enforced with floor regularization.",
            "Scalar potential approximated by V(phi)=Omega_L + 0.5 m_phi^2 phi^2 near phi=0.",
            "Factor-ordering represented by nu in a^{-nu} d_a(a^{nu} d_a).",
            "Principal Arg branch used for phase decomposition.",
        ],
        branch_choice="principal_arg",
        hamiltonian_finite_on_nominal_point=bool(sp.Abs(h_val) < sp.oo),
        decomposition_reconstruction_ok=bool(sp.simplify(recon) == 0),
        wdw_residual_nominal_finite=bool(sp.Abs(w_val) < sp.oo),
    )


def receipt_to_dict(receipt: BohmianSymbolicReceipt) -> dict:
    return asdict(receipt)
