import csv, json
from datetime import datetime
from pathlib import Path
import numpy as np
from grqm_batch_runner_tiered import q1_delta, q1_refinement_max, q2_metrics
from grqm_proxy_toymodel_v1 import IC, Params


def main():
    alpha_values = np.logspace(np.log10(2e-7), np.log10(2e-6), 4).tolist()
    omega_values = np.linspace(0.28, 0.32, 3).tolist()

    thresholds = {
        "q1_effect_persist_min": 1e-4,
        "q1_refinement_max": 5e-3,
        "q1_assumption_sensitivity_hardened_max": 0.2,
        "q2_Dstar_min": 1e-4,
        "q2_true_replication_rel_diff_max": 1e-2,
        "q2_D_p95_max": 0.5,
        "q2_D_p99_max": 0.8,
    }

    hardened_perturbations = [
        dict(ic_scale=0.999, dt=1e-3, n=5),
        dict(ic_scale=1.001, dt=1e-3, n=5),
        dict(ic_scale=1.0, dt=9e-4, n=5),
        dict(ic_scale=1.0, dt=1.1e-3, n=5),
    ]

    root = Path(__file__).resolve().parents[1]
    out_root = root / "notebooks" / "outputs"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = out_root / f"grqm_cycle2_envelope_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    rows=[]; rid=0
    for om in omega_values:
        for a in alpha_values:
            p = Params(omega_m=float(om), omega_l=1.0-float(om), alpha_qg=float(a))
            ic = IC()
            base = q1_delta(p, ic)
            hs=[]
            for cfg in hardened_perturbations:
                ic2=IC(a0=ic.a0*cfg['ic_scale'], v0=ic.v0, t0=ic.t0, t1=ic.t1)
                d=q1_delta(p, ic2, dt_main=cfg['dt'], correction_power=cfg['n'])
                hs.append(abs(d-base)/(abs(base)+1e-15))
            q1ref=q1_refinement_max(p,ic)
            q2=q2_metrics(p)
            row={"run_id":rid,"alpha_qg":a,"omega_m":om,"q1_delta_proxy_l2":base,"q1_refinement_max_obs":q1ref,
                 "q1_assumption_sensitivity_hardened":float(max(hs)),**q2}
            row['pass_q2_robust_bulk']=((row['q2_D_p95']<thresholds['q2_D_p95_max'] and row['q2_D_p99']<thresholds['q2_D_p99_max']) or row['q2_spike_detected'])
            row['pass_all_envelope']=all([
                row['q1_delta_proxy_l2']>=thresholds['q1_effect_persist_min'],
                row['q1_refinement_max_obs']<=thresholds['q1_refinement_max'],
                row['q1_assumption_sensitivity_hardened']<=thresholds['q1_assumption_sensitivity_hardened_max'],
                row['q2_D_star']>=thresholds['q2_Dstar_min'],
                row['q2_true_replication_rel_diff']<=thresholds['q2_true_replication_rel_diff_max'],
                row['pass_q2_robust_bulk'],
            ])
            rows.append(row); rid+=1

    with open(out_dir/'summary.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    agg={"n_runs":len(rows),"n_pass_all_envelope":int(sum(r['pass_all_envelope'] for r in rows)),
         "q2_spike_any":bool(any(r['q2_spike_detected'] for r in rows))}
    with open(out_dir/'aggregate.json','w',encoding='utf-8') as f: json.dump(agg,f,indent=2)
    with open(out_dir/'manifest.json','w',encoding='utf-8') as f: json.dump({"out_dir":str(out_dir),"alpha_values":alpha_values,"omega_values":omega_values,"thresholds":thresholds,"aggregate":agg},f,indent=2)
    print(json.dumps({"out_dir":str(out_dir),"aggregate":agg},indent=2))

if __name__=='__main__':
    main()
