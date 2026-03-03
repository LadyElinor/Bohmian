import os
import pandas as pd

root = r"C:\Users\arren\.openclaw\workspace\Physics"
out_csv = os.path.join(root, "GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.csv")
out_md = os.path.join(root, "GR_QM_CONSECUTIVE_CYCLE_PROMOTION_LEDGER.md")
base = os.path.join(root, "notebooks", "outputs")
rows = []

thresholds = {
    "q1_effect_min": 1e-4,
    "q1_refine_max": 5e-3,
    "q1_assump_max": 0.20,
    "q2_rep_max": 1e-6,
    "q2_p95_max": 0.5,
    "q2_p99_max": 0.8,
}


def pack(cycle_id, scope, path, envelope_note, unresolved, blockers):
    df = pd.read_csv(path)
    n = len(df)

    def rate(col):
        return float(df[col].mean()) if col in df.columns else None

    g_proxy = rate("pass_q1_effect")
    if g_proxy is None and "q1_delta_proxy_l2" in df.columns:
        g_proxy = float((df["q1_delta_proxy_l2"] >= thresholds["q1_effect_min"]).mean())

    g_refine = rate("pass_q1_refinement")
    if g_refine is None and "q1_refinement_max_obs" in df.columns:
        g_refine = float((df["q1_refinement_max_obs"] <= thresholds["q1_refine_max"]).mean())

    g_rq1 = rate("pass_q1_assumption_hardened")
    if g_rq1 is None and "q1_assumption_sensitivity_hardened" in df.columns:
        g_rq1 = float((df["q1_assumption_sensitivity_hardened"] <= thresholds["q1_assump_max"]).mean())

    g_rq2 = rate("pass_q2_robust_bulk")
    if g_rq2 is None and "q2_D_p95" in df.columns and "q2_D_p99" in df.columns:
        g_rq2 = float(((df["q2_D_p95"] < thresholds["q2_p95_max"]) & (df["q2_D_p99"] < thresholds["q2_p99_max"])).mean())

    g_repl = rate("pass_q2_true_replication")
    if g_repl is None and "q2_true_replication_rel_diff" in df.columns:
        g_repl = float((df["q2_true_replication_rel_diff"] <= thresholds["q2_rep_max"]).mean())

    g_env = rate("pass_all_envelope")

    rows.append({
        "cycle_id": cycle_id,
        "artifact_path": path.replace(root + "\\", ""),
        "n_runs": n,
        "envelope_scope": scope,
        "gate_proxy_pass_rate": g_proxy,
        "gate_refine_pass_rate": g_refine,
        "gate_robust_q1_pass_rate": g_rq1,
        "gate_robust_q2_pass_rate": g_rq2,
        "gate_replication_pass_rate": g_repl,
        "gate_envelope_pass_rate": g_env,
        "unresolved_high_impact_assumptions": unresolved,
        "promotion_eligibility_flag": False,
        "blocker_notes": blockers,
        "envelope_note": envelope_note,
    })


pack(
    "cycle-1",
    "Omega_m≈0.300 corridor; alpha 2.154e-7..1.5e-6",
    os.path.join(base, "grqm_batch_tiered_20260301_193522", "summary.csv"),
    "tiered canonical close artifact",
    "A-001|A-002",
    "Q2 method-disagreement gate failed (0/6); assumption closure pending",
)
pack(
    "cycle-2",
    "Omega_m 0.280..0.310 dense follow-up; alpha 3e-7..1.3e-6",
    os.path.join(base, "grqm_cycle2_dense_followup_20260301_215901", "envelope_summary.csv"),
    "core slices pass; edge 0.305/0.310 fail",
    "A-001|A-002",
    "Envelope pass 25/35; not all-gate consecutive in same envelope",
)
pack(
    "cycle-3",
    "Omega_m 0.285..0.300 core corridor; alpha 3e-7..1.3e-6",
    os.path.join(base, "grqm_cycle3_core_confirm_20260301_223742", "cycle3_core_confirm_summary.csv"),
    "all gates pass in-core",
    "A-001|A-002",
    "Consecutive-cycle rule unmet due cycle-2 envelope miss and unresolved assumptions",
)
pack(
    "cycle-3-rerun-20260302",
    "Omega_m 0.285..0.300 core corridor; alpha 3e-7..1.3e-6",
    os.path.join(base, "grqm_cycle3_core_confirm_20260302_172931", "cycle3_core_confirm_summary.csv"),
    "revalidation rerun all pass in-core",
    "A-001|A-002",
    "Reproducibility strong; still not promotable without A-001/A-002 closure",
)

pack(
    "cycle-3-a001-policy-20260302",
    "A-001 local policy battery over prior closure points (Omega_m 0.295/0.300; alpha 5e-7/1e-6; n in {4,5}; dt 8e-4..1.2e-3)",
    os.path.join(base, "grqm_a001_policy_battery_rerun_20260302_175841", "a001_policy_battery_summary.csv"),
    "A-001 in-policy closure battery",
    "",
    "A-001 bounded closure demonstrated in-policy; promotion still blocked by consecutive-cycle envelope rule only",
)

pack(
    "cycle-4-inpolicy-20260302",
    "Omega_m 0.285..0.300 core corridor; alpha 3e-7..1.3e-6; explicit A-001/A-002 policy perturbations",
    os.path.join(base, "grqm_cycle4_inpolicy_confirm_20260302_180311", "cycle4_inpolicy_confirm_summary.csv"),
    "fresh full in-policy cycle after A-001/A-002 closure bounds",
    "",
    "G-ROBUST-Q1 failed under explicit in-policy perturbation mix (20/20 over threshold)",
)

pack(
    "cycle-4-reverted-hardening-20260302",
    "Omega_m 0.285..0.300 core corridor; alpha 3e-7..1.3e-6; reverted Cycle-3-equivalent hardening signature",
    os.path.join(base, "grqm_cycle3_core_confirm_20260302_215234", "cycle3_core_confirm_summary.csv"),
    "promotion-readiness confirmation cycle under reverted baseline hardening",
    "",
    "All gates pass under reverted baseline signature; promotion flag remains conservative pending explicit governance promotion decision",
)

pd.DataFrame(rows).to_csv(out_csv, index=False)


def pct(x):
    return "NA" if x is None else f"{100.0*x:.1f}%"

lines = [
    "# GR_QM Consecutive-Cycle Promotion Ledger (Canonical)",
    "",
    "Updated from auditable artifacts only. Unknowns are marked explicitly.",
    "",
    "| cycle_id | envelope scope | G-PROXY | G-REFINE | G-ROBUST-Q1 | G-ROBUST-Q2 | G-REPLICATION | G-ENVELOPE | unresolved high-impact assumptions | promotion eligible | blocker notes |",
    "|---|---|---:|---:|---:|---:|---:|---:|---|---|---|",
]

for r in rows:
    lines.append(
        "| {cycle_id} | {envelope_scope} | {p} | {r} | {rq1} | {rq2} | {rep} | {env} | {assump} | {elig} | {blk} |".format(
            cycle_id=r["cycle_id"],
            envelope_scope=r["envelope_scope"],
            p=pct(r["gate_proxy_pass_rate"]),
            r=pct(r["gate_refine_pass_rate"]),
            rq1=pct(r["gate_robust_q1_pass_rate"]),
            rq2=pct(r["gate_robust_q2_pass_rate"]),
            rep=pct(r["gate_replication_pass_rate"]),
            env=pct(r["gate_envelope_pass_rate"]),
            assump=r["unresolved_high_impact_assumptions"],
            elig=("YES" if r["promotion_eligibility_flag"] else "NO"),
            blk=r["blocker_notes"],
        )
    )

lines += [
    "",
    "## Notes",
    "- Pass rates are computed directly from each cycle artifact CSV.",
    "- Where a pass flag was absent, documented gate thresholds from current plan/scripts were applied deterministically.",
    "- Promotion eligibility is conservative: consecutive all-gate cycles in same envelope + no unresolved high-impact assumptions.",
]

with open(out_md, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(out_csv)
print(out_md)
