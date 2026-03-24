# Draft Methods Note (v0) — Governed Validation and Causality Attribution in GRQM Minisuperspace Toys

## Candidate Titles
1. **Governed Validation and Causality Attribution in Minisuperspace Quantum-Correction Toy Models**
2. **From Numerical Stress to Structural Attribution: A Governance-First Workflow for FRW/WdW Toy Cosmology**
3. **When the Envelope Fails: Reproducible Causality Gates for Semiclassical Minisuperspace Diagnostics**

## One-Paragraph Abstract (v1)
We present a governance-first methodology for evaluating speculative quantum-cosmology toy models under strict reproducibility and falsification constraints. Using an FRW-inspired ODE minisuperspace baseline with small quantum-gravity correction terms and a Bohmian quantum-potential adaptation lane, we run a staged causality protocol combining refinement/null gates, solver-stress probes, local shoulder mapping, and variant-sensitivity tests. Across independent diagnostics, failures concentrate in a narrow transition shoulder (approximately \(\Omega_m\sim0.307\text{–}0.315\)), while form perturbations fail to shift the boundary materially. The resulting attribution favors a model-intrinsic envelope limit over pure numerical artifact. We contribute not a broad physical claim, but an auditable governance framework that cleanly separates numerical fragility from structural model limits and prevents overclaiming in speculative settings.

## Core Claim Boundaries
- **In scope:**
  - Reproducible diagnostics and attribution logic in a toy minisuperspace regime.
  - Evidence-backed distinction between numerical and structural failure modes.
- **Out of scope:**
  - Observational-fit claims.
  - Dark-sector unification confirmation.
  - Singularity-resolution claims beyond in-core numerics.

## Paper Skeleton

### 1. Introduction
- Problem: speculative models often conflate numerical instability with physical signal.
- Contribution: governance+causality protocol with explicit gates and promotion controls.
- Context: FRW toy + Bohmian adaptation as controlled testbed.

### 2. Model and Lanes
- Baseline lane: additive \(\alpha_{qg}\) correction.
- Adaptation lane: Bohmian guidance with configurable \(Q\) models (off/gaussian/plateau/proxy unified).
- Domain and assumptions (minisuperspace truncation caveats).

### 3. Governance Protocol
- Claim matrix and promotion ledger.
- Gate definitions:
  - refinement error threshold
  - correction-ratio threshold
  - null equivalence checks
  - stability/blowup checks
- Causality sprint protocol (numerics falsification, form falsification, dense shoulder map, decision gate).

### 4. Diagnostics and Instrumentation
- Boundary and stress tables.
- Shoulder density maps.
- Variant sensitivity and null-check receipts.
- Graph augmentation (PecanPy clustering/separability as secondary evidence channel).

### 5. Results
- Persistent shoulder concentration near \(\Omega_m\approx0.307\text{–}0.315\).
- Cross-lane agreement (\(\alpha_{qg}\) and Bohmian-Q).
- Minimal shoulder shift under form perturbations.
- Decision-gate attribution (Numerical/Intrinsic/Mixed rubric + confidence).

### 6. Interpretation
- Why current evidence leans intrinsic.
- What remains uncertain (finite-time effects, truncation dependence, ansatz bias).
- What would falsify the intrinsic interpretation.

### 7. Reproducibility and Auditability
- Artifact contract and deterministic receipts.
- Config hashing + environment fingerprint.
- Fail-fast behavior and missing-artifact policy.

### 8. Limitations and Future Work
- Re-ansatz pathways (nonlocal/curvature-coupled/alternative WdW separable forms).
- Extension to perturbations/extra fields only after gate clearance.
- Portability of governance protocol beyond this toy model.

### 9. Conclusion
- Main payload: reliable attribution discipline under speculative uncertainty.

## Figure / Table Plan

### Figures
1. **Workflow diagram**: governance gates + causality sprint sequence.
2. **Shoulder map**: failure density by \(\Omega_m\) (0.305–0.317).
3. **Continuity panel**: max ratio / stiffness / divergence vs \(\Omega_m\).
4. **Cross-lane comparison**: \(\alpha_{qg}\) vs Bohmian-Q envelope behavior.
5. **Attribution gate panel**: invariance score vs form-shift delta with verdict regions.

### Tables
1. Gate thresholds and pass/fail definitions.
2. Solver-stress invariance summary.
3. Form-perturbation sensitivity summary.
4. Final decision matrix with confidence rubric.

## Minimal Artifact Bundle for Submission
- `decision.json`
- `summary.json` and `summary.md`
- `01_numerics_invariance.csv`
- `02_physics_form_sensitivity.csv`
- `03_bifurcation_map.csv`
- `failure_density_by_omega.csv`
- `invariance_scores.json`
- run `receipt.json` (with config/repro hashes)

## Next Writing Steps (Fast Path)
1. Freeze one confirmatory rerun receipt.
2. Export final figure-ready CSV subsets from latest two runs.
3. Draft 900–1200 word short methods note.
4. Add appendix with exact gate pseudocode + file schema contract.
