import csv, json
from datetime import datetime
from pathlib import Path
import numpy as np
from grqm_batch_runner_tiered import q1_delta
from grqm_proxy_toymodel_v1 import IC, Params


def main():
    alpha_values = np.logspace(np.log10(2e-7), np.log10(2e-6), 6).tolist()
    omega_values = np.linspace(0.28, 0.32, 5).tolist()
    rows=[]
    for om in omega_values:
        for a in alpha_values:
            ic=IC()
            p1=Params(omega_m=float(om), omega_l=1-float(om), alpha_qg=float(a))
            p2=Params(omega_m=float(om), omega_l=1-float(om), alpha_qg=float(2*a))
            d1=q1_delta(p1,ic)
            d2=q1_delta(p2,ic)
            ratio=d2/(d1+1e-15)
            rows.append({"omega_m":om,"alpha_qg":a,"q1_delta_alpha":d1,"q1_delta_2alpha":d2,"ratio_2a_over_a":ratio,"abs_ratio_err_from2":abs(ratio-2.0)})

    root=Path(__file__).resolve().parents[1]
    out_root=root/"notebooks"/"outputs"
    ts=datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir=out_root/f"grqm_cycle2_proxycheck_{ts}"
    out_dir.mkdir(parents=True,exist_ok=True)
    with open(out_dir/'summary.csv','w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    agg={"n_runs":len(rows),"ratio_mean":float(np.mean([r['ratio_2a_over_a'] for r in rows])),"ratio_min":float(np.min([r['ratio_2a_over_a'] for r in rows])),"ratio_max":float(np.max([r['ratio_2a_over_a'] for r in rows])),"max_abs_ratio_err_from2":float(np.max([r['abs_ratio_err_from2'] for r in rows]))}
    with open(out_dir/'aggregate.json','w',encoding='utf-8') as f: json.dump(agg,f,indent=2)
    print(json.dumps({"out_dir":str(out_dir),"aggregate":agg},indent=2))

if __name__=='__main__':
    main()
