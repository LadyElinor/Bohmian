# CURRENT TRUTH – GR↔QM Project Status (March 2026)

This is the single-page summary of what is proven, what is open, what is blocked, and the current validity envelope.

Updated after the adaptive-refinement edge mitigation packet completion (code 0, 20/20 cases).

## Proven Claims

**C-WDW-001** – **PROVEN (core envelope)** + **exploratory edge extension**

A semiclassical WDW-inspired correction produces a persistent, reproducible low-energy proxy signal within the declared core envelope.

- Core envelope: `Ω_m <= 0.300` (flat ΛCDM background)
- Exploratory extension: `Ω_m <= 0.31` under mandatory constraints
- Mandatory constraints for `Ω_m > 0.300`:
  - adaptive refinement
  - stiff solver (Radau baseline)
  - overlapping-time interpolation for refinement metrics
- Physical caveat (mandatory in edge lane): transient non-perturbative dominance occurs (`correction/classical ratio > 1` near `min_a ≈ 0.01`), which exits the perturbative semiclassical regime assumed by C-WDW-001.
- Boundary mini-sweep at `Ω_m = 0.31` (2026-03-08): 5/8 points pass q1 refinement at `1e-6`; transient dominance persists (`max ratio ≈ 3.912`).

**C-CORE-001** – **PROVEN (meta-process/study-system)**

EFT-first, gate-driven cycles with explicit blockers, validity envelopes, and regression-isolation loops improve testability and reduce self-deception.

**C-GRQM-002** – **PROVEN (in-core toy envelope)**

Exact-vs-approx divergence signal is validated in the in-core toy envelope under declared protocol; edge lane remains separately governed.

## Current Validity Envelope

- `Ω_m <= 0.300`: fully PROVEN (core envelope)
- `0.300 < Ω_m <= 0.31`: exploratory inclusion approved under mandatory adaptive refinement + Radau + interpolation constraints, with physical caveat required
- `Ω_m > 0.31`: BLOCKED (no mitigation evidence yet)

## Open Claims / Lanes

- **C-GRQM-001** – OPEN (process-level generalization still needs longer KPI hardening)
- Nonlinear scalar-clock branch – diagnostic/open
- LQC bounce alternative lane – conceptual/open

## Blocked Claims

- **C-WDW-002** – BLOCKED (overgeneralized equivalence-principle statement; no model-specific test path)

## Governance + Reproducibility

- Claims require consecutive-cycle evidence, explicit null-test handling, and governance sign-off.
- Golden artifacts are pinned; bulk timestamped outputs are excluded.
- CI + pytest invariants enforce reproducibility tiers.
- Audit trail is canonical: ledger → claim matrix → cycle journal → monthly gate report.

## Key receipt for latest edge closure

- `notebooks/outputs/grqm_edge_companion_inpolicy_adaptive_checkpointed_20260307_132048/edge_companion_aggregate.json`
  - `completed_cases=20/20`
  - `pass_all_packet_rate=1.0`
  - `max_q1_refinement=1.0475384872639079e-08`
  - `max_q1_hardened=0.1483037382017592`
  - `max_q2_p95=0.0`, `max_q2_p99=0.0`
  - `max_replication=0.0`

**Last updated:** March 08, 2026
**Next update trigger:** next nonlinear scalar or LQC lane phase result, or any claim-status mutation.
