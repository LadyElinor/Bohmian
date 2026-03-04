# GR_QM Hardening Expansion Plan — 2026-03-03

Objective: reduce directional-selection bias in assumption robustness checks.

## Upgrade
Move from sparse hand-picked perturbation directions to expanded sampling:
- baseline + existing hardening set retained
- add bias-reduced sample set (target 8-12 directions minimum)
- include joint perturbations across dt, ic_scale, selected ordering proxy, and alpha sub-corridor

## Deliverables
- script extension or new runner for expanded hardening sample set
- summary table with pass rates + max sensitivity + distribution quantiles
- explicit comparison against prior n=5 direction result

## Governance usage
- Informative for OPEN claims (C-GRQM-001/002) and maintenance confidence for C-WDW-001.
- Does not alter existing claim status without explicit promotion/reopen decision.
