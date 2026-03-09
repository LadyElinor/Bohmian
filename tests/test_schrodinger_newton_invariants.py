from __future__ import annotations

from grqm.models.schrodinger_newton import SNParams, run_sn_1d


def test_sn_norm_drift_small():
    res = run_sn_1d(SNParams(kappa=0.02, dt=5e-4, t_max=0.2, n_grid=128), seed=0)
    assert res["q2"]["norm_drift_max"] < 1e-3


def test_sn_free_limit_small_signal():
    res = run_sn_1d(SNParams(kappa=0.0, dt=5e-4, t_max=0.2, n_grid=128), seed=0)
    assert res["q1"]["sigma_deviation_max"] < 1e-6


def test_sn_deterministic_seed():
    p = SNParams(kappa=0.02, dt=5e-4, t_max=0.2, n_grid=128)
    r1 = run_sn_1d(p, seed=123)
    r2 = run_sn_1d(p, seed=123)
    assert abs(r1["q1"]["sigma_deviation_max"] - r2["q1"]["sigma_deviation_max"]) < 1e-12
    assert abs(r1["q2"]["refinement_rel_diff"] - r2["q2"]["refinement_rel_diff"]) < 1e-12
