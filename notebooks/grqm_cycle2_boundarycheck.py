import csv, json
from pathlib import Path
from datetime import datetime
import numpy as np

src = Path(r"C:\Users\arren\.openclaw\workspace\Physics\notebooks\outputs\grqm_cycle2_dense_followup_20260301_215901\omega_passrate.csv")
rows = list(csv.DictReader(open(src, encoding="utf-8")))
oms = np.array([float(r["omega_m"]) for r in rows])
maxsens = np.array([float(r["max_q1_hardened"]) for r in rows])
coef = np.polyfit(oms, np.log10(maxsens + 1e-12), 1)

x1 = 0.300
y1 = float([r for r in rows if abs(float(r["omega_m"]) - 0.300) < 1e-9][0]["max_q1_hardened"])
x2 = 0.305
y2 = float([r for r in rows if abs(float(r["omega_m"]) - 0.305) < 1e-9][0]["max_q1_hardened"])
xb = x1 + (0.2 - y1) * (x2 - x1) / (y2 - y1)

out = Path(r"C:\Users\arren\.openclaw\workspace\Physics\notebooks\outputs") / f"grqm_cycle2_boundarycheck_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
out.mkdir(parents=True, exist_ok=True)
with open(out / "boundary_fit.json", "w", encoding="utf-8") as f:
    json.dump({
        "omega": oms.tolist(),
        "max_q1_hardened": maxsens.tolist(),
        "log10_fit_slope": float(coef[0]),
        "log10_fit_intercept": float(coef[1]),
        "interpolated_omega_at_q1_hardened_0p2": float(xb),
        "recommended_core_upper": 0.300,
        "recommended_formal_upper": 0.305,
    }, f, indent=2)

print(json.dumps({"out_dir": str(out), "omega_at_0p2": float(xb)}, indent=2))
