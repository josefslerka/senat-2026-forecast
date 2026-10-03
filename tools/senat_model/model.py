#!/usr/bin/env python3
"""Senate model, step 2: fit, validate (leave-one-cycle-out) and simulate 2026.

Layer 1  party base: Chamber-election share of the candidate's supporting parties (prep.py).
Layer 2  round-1 share: OLS  share_k1 ~ base + incumbent + local_exec + mp + gov + ano + n_support + n_cands.
Layer 3  runoff: OLS on (share_A - 50) ~ r1 margin + same-bloc reservoir diff + gov diff + ano diff (symmetrised).
Monte Carlo: common national party swing (shared across districts) + candidate residuals + runoff residuals.

Usage: python3 scripts/senat_model/model.py [--sims 20000] [--validate]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "senat-model"
RNG = np.random.default_rng(20261009)

# ── blocs (ASSUMPTION, needs operator review) ─────────────────────────────────
DEM = {53, 1, 721, 166, 720, 1187, 5, 795, 55}      # ODS, KDU, TOP 09, STAN, Piráti, SEN 21, Zelení, LES, Koruna Česká
NAT = {1114, 1227, 714, 1298, 47, 1178, 1245}       # SPD, Trikolora, Svobodní, Stačilo!, KSČM, Motoristé, PŘÍSAHA
ANO = 768

# ── national swing 2025 -> polls Jul–Sep 2026 ─────────────────────────────────────────────
# Source: cs.wikipedia "Předvolební průzkumy k volbám do Poslanecké sněmovny … 2029" (fetched 2026-10-03),
# latest poll per agency: Kantar 3.–21. 8., Median 1.–31. 8., NMS 28. 8.–2. 9., STEM 2.–7. 9. 2026.
# Averages vs 2025 result: ANO 31.65/34.51, SPOLU (ODS+TOP+KDU) 19.10/23.36, STAN 15.48/11.23,
# Piráti 8.05/8.97, SPD 7.63/7.78, Motoristé 4.70/6.77, Stačilo!/KSČM ~3.2/4.30.
# factor = poll avg / 2025; sd = relative uncertainty (poll spread + historical poll error), shared by all districts.
SWING = {768: (31.65 / 34.51, 0.06), 53: (19.10 / 23.36, 0.08), 1: (19.10 / 23.36, 0.08), 721: (19.10 / 23.36, 0.08),
         166: (15.48 / 11.23, 0.12), 720: (8.05 / 8.97, 0.12), 1114: (7.63 / 7.78, 0.12), 1178: (4.70 / 6.77, 0.15),
         1298: (3.2 / 4.30, 0.25), 47: (3.2 / 4.30, 0.25)}
DEFAULT_SWING_SD = 0.15

# Post-simulation calibration p ∝ p_raw^CALIB_EXP, fitted on leave-one-cycle-out predictions 2020–2024
# (raw model was overconfident: the 0.70–0.90 bucket won only 32 %).
CALIB_EXP = 0.55


def calibrate(p: np.ndarray) -> np.ndarray:
    q = np.clip(p, 2e-3, 1) ** CALIB_EXP
    return q / q.sum()


FEATURES = ["base", "base_gov", "local_extra", "incumbent", "former_senator", "local_exec", "mp", "gov", "ano", "stan", "kdu", "no_base", "n_support", "inv_n"]


def bloc(support: str) -> str:
    s = {int(x) for x in str(support).split() if x.strip().lstrip("-").isdigit()}
    if ANO in s:
        return "ANO"
    if s & DEM:
        return "DEM"
    if s & NAT:
        return "NAT"
    return "OTH"


def load() -> pd.DataFrame:
    c = pd.read_csv(DATA / "candidates.csv")
    c["base"] = c["base"] * 100
    c["local_extra"] = c["local_extra"] * 100
    c["inv_n"] = 1 / c["n_cands"]
    c["bloc"] = c["support"].map(bloc)
    sup = c["support"].map(lambda x: {int(v) for v in str(x).split()})
    c["stan"] = sup.map(lambda s: int(166 in s))
    c["kdu"] = sup.map(lambda s: int(1 in s))
    c["no_base"] = (c["base"] < 1).astype(int)
    c["base_gov"] = c["base"] * c["gov"]
    return c


def design(df: pd.DataFrame) -> np.ndarray:
    return np.column_stack([np.ones(len(df))] + [df[f].to_numpy(float) for f in FEATURES])


def fit_r1(train: pd.DataFrame):
    X, y = design(train), train["share_k1"].to_numpy(float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    return beta, float(resid.std(ddof=X.shape[1]))


def runoff_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (yr, ob), d in df.groupby(["year", "obvod"]):
        fin = d[d["share_k2"] > 0]
        if len(fin) != 2:
            continue
        for a, b in ((0, 1), (1, 0)):
            A, B = fin.iloc[a], fin.iloc[b]
            elim = d[~d.index.isin(fin.index)]
            res_a = elim.loc[elim["bloc"] == A["bloc"], "share_k1"].sum() if A["bloc"] != "OTH" else 0.0
            res_b = elim.loc[elim["bloc"] == B["bloc"], "share_k1"].sum() if B["bloc"] != "OTH" else 0.0
            rows.append(dict(year=yr, obvod=ob, y=A["share_k2"] - 50, margin=A["share_k1"] - B["share_k1"],
                             reservoir=res_a - res_b, gov=A["gov"] - B["gov"], ano=A["ano"] - B["ano"]))
    return pd.DataFrame(rows)


RUNOFF_X = ["margin", "reservoir", "gov", "ano"]


def fit_runoff(rt: pd.DataFrame):
    X, y = rt[RUNOFF_X].to_numpy(float), rt["y"].to_numpy(float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta, float((y - X @ beta).std(ddof=len(beta)))


def simulate_district(d: pd.DataFrame, beta, sd, rbeta, rsd, n: int, base_draws: np.ndarray | None = None,
                      stats: dict | None = None) -> np.ndarray:
    """Return win probabilities per candidate (row order of d)."""
    X = design(d)
    k = len(d)
    if base_draws is not None:
        Xs = np.repeat(X[None, :, :], n, axis=0)
        gi = 1 + FEATURES.index("base_gov")
        Xs[:, :, 1] = base_draws
        Xs[:, :, gi] = base_draws * d["gov"].to_numpy(float)[None, :]
        mu = Xs @ beta
    else:
        mu = np.repeat((X @ beta)[None, :], n, axis=0)
    r1 = np.clip(mu + RNG.normal(0, sd, size=(n, k)), 0.3, None)
    r1 = r1 / r1.sum(axis=1, keepdims=True) * 100
    wins = np.zeros(k)
    order = np.argsort(-r1, axis=1)
    if stats is not None:
        stats["r1_mean"] = r1.mean(axis=0)
        stats["r1_p10"] = np.percentile(r1, 10, axis=0)
        stats["r1_p90"] = np.percentile(r1, 90, axis=0)
        top2 = np.zeros(k)
        for j in range(k):
            top2[j] = np.mean((order[:, 0] == j) | ((order[:, 1] == j) & (r1[np.arange(n), order[:, 0]] <= 50)))
        stats["p_runoff_or_outright"] = top2
        stats["p_outright"] = np.array([np.mean((order[:, 0] == j) & (r1[np.arange(n), order[:, 0]] > 50)) for j in range(k)])
    blocs = d["bloc"].to_numpy()
    gov = d["gov"].to_numpy(float)
    ano = d["ano"].to_numpy(float)
    for s in range(n):
        a, b = order[s, 0], order[s, 1]
        if r1[s, a] > 50:
            wins[a] += 1
            continue
        elim = np.ones(k, bool)
        elim[[a, b]] = False
        ra = r1[s, elim & (blocs == blocs[a])].sum() if blocs[a] != "OTH" else 0.0
        rb = r1[s, elim & (blocs == blocs[b])].sum() if blocs[b] != "OTH" else 0.0
        x = np.array([r1[s, a] - r1[s, b], ra - rb, gov[a] - gov[b], ano[a] - ano[b]])
        ya = 50 + x @ rbeta + RNG.normal(0, rsd)
        wins[a if ya > 50 else b] += 1
    return calibrate(wins / n)


def winner_of(d: pd.DataFrame) -> int:
    if (d["share_k2"] > 0).any():
        return int(np.argmax(d["share_k2"].to_numpy()))
    return int(np.argmax(d["share_k1"].to_numpy()))


def validate(c: pd.DataFrame, n: int) -> dict:
    hist = c[c["year"] < 2026]
    out = {"cycles": {}}
    allb, allb_inc, allb_base, acc, acc_inc, acc_base, mae = [], [], [], [], [], [], []
    for test in (2020, 2022, 2024):
        tr, te = hist[hist["year"] != test], hist[hist["year"] == test]
        beta, sd = fit_r1(tr)
        rbeta, rsd = fit_runoff(runoff_table(tr))
        cyc = []
        for ob, d in te.groupby("obvod"):
            d = d.reset_index(drop=True)
            p = simulate_district(d, beta, sd, rbeta, rsd, n)
            w = winner_of(d)
            o = np.zeros(len(d)); o[w] = 1
            brier = float(((p - o) ** 2).sum())
            # baselines: strongest party base wins; incumbent wins else strongest base
            pb = np.zeros(len(d)); pb[int(np.argmax(d["base"]))] = 1
            inc = d.index[d["incumbent"] == 1]
            pi = np.zeros(len(d)); pi[inc[0] if len(inc) else int(np.argmax(d["base"]))] = 1
            mae.append(float(np.abs(design(d) @ beta - d["share_k1"]).mean()))
            allb.append(brier); allb_base.append(float(((pb - o) ** 2).sum())); allb_inc.append(float(((pi - o) ** 2).sum()))
            acc.append(int(np.argmax(p) == w)); acc_base.append(int(np.argmax(pb) == w)); acc_inc.append(int(np.argmax(pi) == w))
            cyc.append(brier)
        out["cycles"][test] = dict(brier=float(np.mean(cyc)), n=len(cyc))
    out.update(brier_model=float(np.mean(allb)), brier_base=float(np.mean(allb_base)), brier_incumbent=float(np.mean(allb_inc)),
               acc_model=float(np.mean(acc)), acc_base=float(np.mean(acc_base)), acc_incumbent=float(np.mean(acc_inc)),
               r1_mae=float(np.mean(mae)), districts=len(allb))
    return out


def party_shares_2026() -> dict[int, dict[int, float]]:
    s = pd.read_csv(DATA / "party_shares.csv")
    s = s[s["senate_year"] == 2026]
    out: dict[int, dict[int, float]] = {}
    for ob, p, sh in s[["obvod", "party", "share"]].itertuples(index=False):
        out.setdefault(int(ob), {})[int(p)] = float(sh)
    return out


def predict_2026(c: pd.DataFrame, n: int) -> list[dict]:
    hist = c[c["year"] < 2026]
    beta, sd = fit_r1(hist)
    rbeta, rsd = fit_runoff(runoff_table(hist))
    shares = party_shares_2026()
    parties = sorted({p for d in shares.values() for p in d})
    mu = np.array([SWING.get(p, (1.0, DEFAULT_SWING_SD))[0] for p in parties])
    sdv = np.array([SWING.get(p, (1.0, DEFAULT_SWING_SD))[1] for p in parties])
    factors = np.clip(RNG.normal(mu, sdv * mu, size=(n, len(parties))), 0.2, None)   # common national swing
    pidx = {p: i for i, p in enumerate(parties)}
    out = []
    for ob, d in c[c["year"] == 2026].groupby("obvod"):
        d = d.reset_index(drop=True)
        base_draws = np.zeros((n, len(d)))
        for j, sup in enumerate(d["support"]):
            for p in {int(x) for x in str(sup).split()}:
                if p in shares[ob]:
                    base_draws[:, j] += shares[ob][p] * factors[:, pidx[p]] * 100
        st: dict = {}
        p = simulate_district(d, beta, sd, rbeta, rsd, n, base_draws=base_draws, stats=st)
        out.append(dict(obvod=int(ob), candidates=[
            dict(name=r["name"], list=r["list"], bloc=r["bloc"], base=round(float(r["base"]), 1),
                 local_extra=round(float(r["local_extra"]), 1),
                 r1_mean=round(float(st["r1_mean"][j]), 1), r1_p10=round(float(st["r1_p10"][j]), 1),
                 r1_p90=round(float(st["r1_p90"][j]), 1), p_advance=round(float(st["p_runoff_or_outright"][j]), 4),
                 p_outright=round(float(st["p_outright"][j]), 4), p_win=round(float(p[j]), 4))
            for j, r in d.iterrows()]))
    return out, dict(beta=dict(zip(["const"] + FEATURES, map(float, beta))), r1_sd=sd,
                     runoff_beta=dict(zip(RUNOFF_X, map(float, rbeta))), runoff_sd=rsd)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sims", type=int, default=20000)
    ap.add_argument("--validate", action="store_true")
    a = ap.parse_args()
    c = load()
    res = {}
    if a.validate:
        res["validation"] = validate(c, min(a.sims, 5000))
        print(json.dumps(res["validation"], indent=2))
    pred, coefs = predict_2026(c, a.sims)
    res["coefficients"] = coefs
    res["prediction"] = pred
    (DATA / "model_2026.json").write_text(json.dumps(res, ensure_ascii=False, indent=2))
    print(json.dumps(coefs, indent=2))
    for d in pred:
        top = sorted(d["candidates"], key=lambda x: -x["p_win"])[:3]
        print(d["obvod"], " | ".join(f"{t['name']} {t['p_win']*100:.0f}% (R1 {t['r1_mean']})" for t in top))


if __name__ == "__main__":
    main()
