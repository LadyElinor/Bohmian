import ast
import csv
import json
from datetime import datetime
from pathlib import Path
from statistics import mean


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        rr = {}
        for k, v in r.items():
            if v in ("True", "False"):
                rr[k] = (v == "True")
            else:
                try:
                    rr[k] = float(v)
                except Exception:
                    rr[k] = v
        out.append(rr)
    return out


def _eval_node(node):
    try:
        return ast.literal_eval(node)
    except Exception:
        pass

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "dict":
        out = {}
        for kw in node.keywords:
            out[kw.arg] = _eval_node(kw.value)
        return out

    if isinstance(node, ast.List):
        return [_eval_node(e) for e in node.elts]

    if isinstance(node, ast.Tuple):
        return tuple(_eval_node(e) for e in node.elts)

    return "<non-literal>"


def parse_script_knobs(py_path: Path):
    src = py_path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    wanted = {
        "omega_list",
        "alpha_list",
        "thresholds",
        "hardened_perturbations",
        "policy_perturbations",
    }
    vals = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in wanted:
                    vals[t.id] = _eval_node(node.value)
    return vals


def flatten(d, prefix=""):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            out.update(flatten(v, f"{prefix}{k}."))
    else:
        out[prefix[:-1]] = d
    return out


def main():
    root = Path(__file__).resolve().parents[1]
    pass_dir = root / "notebooks/outputs/grqm_cycle3_core_confirm_20260302_172931"
    fail_dir = root / "notebooks/outputs/grqm_cycle4_inpolicy_confirm_20260302_180311"

    pass_agg = load_json(pass_dir / "aggregate.json")
    fail_agg = load_json(fail_dir / "aggregate.json")

    pass_summary = load_csv(pass_dir / "cycle3_core_confirm_summary.csv")
    fail_summary = load_csv(fail_dir / "cycle4_inpolicy_confirm_summary.csv")

    pass_proxy = load_csv(pass_dir / "proxy_agreement_v3.csv")
    fail_proxy = load_csv(fail_dir / "proxy_agreement_v4_inpolicy.csv")

    cycle3_knobs = parse_script_knobs(root / "notebooks/cycle3_core_confirm.py")
    cycle4_knobs = parse_script_knobs(root / "notebooks/cycle4_inpolicy_confirm.py")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = root / f"notebooks/outputs/grqm_delta_autopsy_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Config diff (aggregate + script knobs)
    config_rows = []
    a = flatten(pass_agg)
    b = flatten(fail_agg)
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            config_rows.append({"source": "aggregate.json", "key": k, "passing": a.get(k), "failed": b.get(k)})

    for k in sorted(set(cycle3_knobs) | set(cycle4_knobs)):
        if cycle3_knobs.get(k) != cycle4_knobs.get(k):
            config_rows.append({"source": "runner_script", "key": k, "passing": cycle3_knobs.get(k), "failed": cycle4_knobs.get(k)})

    # Per-point deltas
    join = {}
    for r in pass_summary:
        join[(r["omega_m"], r["alpha_qg"])] = {"pass": r}
    for r in fail_summary:
        join.setdefault((r["omega_m"], r["alpha_qg"]), {})["fail"] = r

    numeric_cols = [
        "q1_delta_proxy_l2",
        "q1_refinement_max_obs",
        "q1_assumption_sensitivity_hardened",
        "q2_D_star",
        "q2_D_p95",
        "q2_D_p99",
        "q2_true_replication_rel_diff",
        "q2_method_disagreement_rel_diff",
    ]

    point_rows = []
    for (omega, alpha), pair in sorted(join.items()):
        if "pass" not in pair or "fail" not in pair:
            continue
        p = pair["pass"]
        f = pair["fail"]
        row = {"omega_m": omega, "alpha_qg": alpha}
        for c in numeric_cols:
            dv = f[c] - p[c]
            row[f"delta_{c}"] = dv
        row["pass_all_envelope_pass"] = p["pass_all_envelope"]
        row["pass_all_envelope_fail"] = f["pass_all_envelope"]
        row["gate_flip"] = int(bool(p["pass_all_envelope"]) and not bool(f["pass_all_envelope"]))
        point_rows.append(row)

    # Smoking gun: first gate flip and first sensitivity blowout
    first_flip = next((r for r in point_rows if r["gate_flip"] == 1), None)
    sens_sorted = sorted(point_rows, key=lambda r: abs(r["delta_q1_assumption_sensitivity_hardened"]), reverse=True)
    top_sens = sens_sorted[0] if sens_sorted else None

    smoke_rows = []
    if first_flip:
        smoke_rows.append({"type": "first_gate_flip", **first_flip})
    if top_sens:
        smoke_rows.append({"type": "max_sensitivity_delta", **top_sens})

    # Ranked plausible contributors by effect size
    effects = []
    for c in numeric_cols:
        vals = [abs(r[f"delta_{c}"]) for r in point_rows]
        effects.append({"metric": c, "mean_abs_delta": mean(vals) if vals else 0.0, "max_abs_delta": max(vals) if vals else 0.0})
    effects.sort(key=lambda x: (x["mean_abs_delta"], x["max_abs_delta"]), reverse=True)

    # write csvs
    def write_csv(path: Path, rows):
        if not rows:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)

    write_csv(out_dir / "config_diff.csv", config_rows)
    write_csv(out_dir / "point_deltas.csv", point_rows)
    write_csv(out_dir / "smoking_gun.csv", smoke_rows)
    write_csv(out_dir / "ranked_effects.csv", effects)

    # concise note
    note = []
    note.append("# GRQM Delta Autopsy")
    note.append("")
    note.append(f"- Passing: `{pass_dir}`")
    note.append(f"- Failed: `{fail_dir}`")
    note.append(f"- Compared points: {len(point_rows)}")
    note.append("")
    note.append("## Smoking gun")
    if first_flip:
        note.append(
            f"- First gate flip at omega_m={first_flip['omega_m']}, alpha_qg={first_flip['alpha_qg']}: "
            f"q1_assumption_sensitivity_hardened delta={first_flip['delta_q1_assumption_sensitivity_hardened']:.6f}, "
            f"pass_all_envelope {first_flip['pass_all_envelope_pass']} -> {first_flip['pass_all_envelope_fail']}."
        )
    else:
        note.append("- No gate flip detected in comparable rows.")

    note.append("")
    note.append("## Top contributors by effect size (mean |delta|)")
    for i, e in enumerate(effects[:3], start=1):
        note.append(f"{i}. {e['metric']}: mean|delta|={e['mean_abs_delta']:.6g}, max|delta|={e['max_abs_delta']:.6g}")

    note.append("")
    note.append("## Config/assumption knobs changed")
    for r in config_rows:
        note.append(f"- [{r['source']}] {r['key']}: {r['passing']} -> {r['failed']}")

    (out_dir / "AUTOPSY_NOTE.md").write_text("\n".join(note) + "\n", encoding="utf-8")

    print(json.dumps({"out_dir": str(out_dir), "n_point_rows": len(point_rows), "n_config_diffs": len(config_rows)}, indent=2))


if __name__ == "__main__":
    main()
