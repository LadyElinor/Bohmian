# Ledger Note Template — Edge Mitigation Review

Cycle ID: `edge-mitigation-micro-YYYYMMDD`

## Scope
- Envelope tested: `Ω_m in [0.305, 0.31]` (edge lane)
- α corridor: `{3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6}`
- Methods: DOP853 (ref), LSODA, Radau

## Results snapshot
- q2_D_p95 max:
- q2_D_p99 max:
- q1_refine max:
- q1_assumption_sensitivity_hardened max:
- true replication rel diff max:

## Gate disposition
- G-ROBUST-Q2:
- G-REFINE:
- G-ROBUST-Q1:
- G-REPLICATION:
- G-ENVELOPE (edge lane):

## Decision
- [ ] Keep edge BLOCKED
- [ ] Allow exploratory edge inclusion (non-promoting)
- [ ] Escalate to governance review for policy change

## Notes
- This row does not mutate claim statuses by itself.
