import csv, json
from datetime import datetime
from pathlib import Path
import numpy as np
from grqm_batch_runner_tiered import q1_delta
from grqm_proxy_toymodel_v1 import IC, Params

alpha_values = [3e-7, 5e-7, 7e-7, 1e-6, 1.3e-6]
omega_m = 0.305
rows = []
for a in alpha_values:
    ic = IC()
    p1 = Params(omega_m=omega_m, omega_l=1.0-omega_m, alpha_qg=a)
    p2 = Params(omega_m=omega_m, omega_l=1.0-omega_m, alpha_qg=2*a)
    d1 = q1_delta(p1, ic)
    d2 = q1_delta(p2, ic)
    ratio = d2/(d1+1e-15)
    rows.append({"omega_m":omega_m,"alpha_qg":a,"q1_delta_alpha":d1,"q1_delta_2alpha":d2,"ratio_2a_over_a":ratio})

x=np.array([r['q1_delta_alpha'] for r in rows],dtype=float)
y=np.array([r['q1_delta_2alpha'] for r in rows],dtype=float)
ratio=np.array([r['ratio_2a_over_a'] for r in rows],dtype=float)

out=Path(r"C:\Users\arren\.openclaw\workspace\Physics\notebooks\outputs")/f"grqm_cycle2_edge305_proxycheck_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
out.mkdir(parents=True,exist_ok=True)
with open(out/'summary.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
with open(out/'aggregate.json','w',encoding='utf-8') as f:
    json.dump({"omega_m":omega_m,"n":len(rows),"pearson":float(np.corrcoef(x,y)[0,1]),"ratio_mean":float(np.mean(ratio)),"ratio_std":float(np.std(ratio)),"ratio_min":float(np.min(ratio)),"ratio_max":float(np.max(ratio))},f,indent=2)
print(out)
