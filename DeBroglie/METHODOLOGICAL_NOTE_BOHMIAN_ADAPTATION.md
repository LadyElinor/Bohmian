# Methodological Note: Bohmian/de Broglie Adaptation Lane (Phase-1)

## Scope
This lane implements a **governance-first adaptation scaffold** for Bohmian/de Broglie-Bohm minisuperspace dynamics inside GRQM.
It is intended for internal stability diagnostics and method maturation, not observational inference.

## Source assumptions mapped to implementation
1. **Minisuperspace truncation**
   - Assumption: homogeneous, isotropic FRW-like configuration space with variables `(a, phi)`.
   - Implementation: `SymbolSet` and Hamiltonian in `src/grqm/bohmian_probe/symbolic_core.py`.

2. **Local scalar potential approximation**
   - Assumption: around `phi≈0`, potential can be approximated by
     `V(phi)=Omega_L + 0.5 m_phi^2 phi^2`.
   - Implementation: `scalar_potential()` in symbolic core and reused implicitly by guidance dynamics.

3. **Factor-ordering ambiguity represented explicitly**
   - Assumption: WdW-like kinetic term admits a factor-ordering family.
   - Implementation: parameter `nu` in operator ansatz
     `a^{-nu} d_a(a^{nu} d_a)` via `build_operator_set()`.

4. **Bohmian guidance with proxy quantum potential**
   - Assumption: exact quantum potential in canonical lane is not yet fixed; proxy profiles can stress-test numerics.
   - Implementation: configurable models (`off`, `gaussian`, `plateau`) in `guidance.py`.

5. **Guard rails for numerical governance**
   - Assumption: preliminary adaptation should prioritize controlled, auditable behavior over aggressive extrapolation.
   - Implementation: scale-factor floor, finite-state clipping checks, quantum acceleration clamp ratio.

## Why this is conservative
- No claim that the implemented WdW proxy is uniquely canonical.
- No claim of observational fit or parameter estimation.
- Evidence package is explicitly restricted to boundary stability, solver stress, null checks, and model-variant sensitivity.

## Next-step requirements before promotion
- Canonical derivation traceability from chosen action/constraint set to implemented operator ordering.
- Stronger stiffness analysis and adaptive-step cross-checks beyond fixed-step references.
- Data-facing separation: maintain strict barrier between internal numerical readiness and observational claims.
