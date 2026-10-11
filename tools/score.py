#!/usr/bin/env python3
"""Score the Senát 2026 series against official ČSÚ results (round 1 now, round 2 after 17. 10.).

Usage:
  score.py fetch [--round 1]       download all district results -> data/senat-results/r{round}-{stamp}.json
  score.py r1 <results.json>       partial scoring after round 1 (markdown report to stdout + JSON next to results)

Series predict P(win the seat). After round 1 only these are fully resolved:
  * districts decided in round 1 (someone > 50 %)  -> full multi-class Brier and log score;
  * otherwise -> mass on eliminated candidates, whether the series' favourite advanced, the Brier part that is
    already fixed (sum of p^2 over eliminated) and the Brier range over the two possible round-2 winners.
"""
from __future__ import annotations
import datetime as dt
import json
import math
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT.parent / "senat-2026-forecast"
SNAP = WEB / "data" / "snapshots"
MK = ROOT / "data" / "senat-market"
RES = ROOT / "data" / "senat-results"
BASE = "https://www.volbyhned.cz/appdata/senat/20261009"
DISTRICTS = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81]
PREREG = [3, 9, 15, 21, 27, 30, 63, 66, 69]     # deník 5. 10.
FREEZE_DISPUTED = [3, 9, 15, 21, 30, 63, 66]    # deník 9. 10.
HOME_BASE = {15: "Kozar", 27: "J_Cizinsky", 36: "Volfova", 42: "Kaspar", 63: "Vrana", 75: "Brzyszkowska"}

sys.path.insert(0, str(ROOT / "site" / "senat2026"))


def fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


def get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch(rnd: int = 1) -> Path:
    cr = get(f"{BASE}/vysled/cr.json")
    out = {"round": rnd, "fetched": dt.datetime.now().isoformat(timespec="seconds"), "source": BASE,
           "cr": cr, "districts": {}}
    for n in DISTRICTS:
        d = get(f"{BASE}/vysled/obvod/{n}.json")
        prehled = d["prehled"][rnd - 1] if len(d["prehled"]) >= rnd else None
        out["districts"][n] = {
            "name": d["obvodNazev"], "generated": d["generovano"],
            "counted_pct": prehled[3] if prehled else 0.0, "turnout_pct": prehled[6] if prehled else None,
            "candidates": [{"no": v[0], "name": v[1], "party": v[2], "votes": v[5 if rnd == 1 else 7],
                            "pct": v[6 if rnd == 1 else 8]} for v in d["vysledky"]],
            "advancing": d["postupuje"], "elected": d["zvoleny"], "raw": d}
    RES.mkdir(parents=True, exist_ok=True)
    f = RES / f"r{rnd}-{dt.datetime.now():%Y-%m-%d-%H%M}.json"
    f.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    return f


def key_for(name: str, names: dict[str, str]) -> str:
    """ČSÚ 'Příjmení [Příjmení2] Jméno Tituly' -> AI key; unmatched -> Someone_else.
    Matches the AI display name's surname (last word) anywhere among the ČSÚ name tokens (double surnames)."""
    toks = [fold(t) for t in name.replace(",", " ").split() if not t.endswith(".") and t[0].isupper()]
    hits = [k for k, nm in names.items() if k != "Someone_else" and fold(nm).split()[-1] in toks
            and (len(nm.split()) < 2 or fold(nm).split()[0] in toks)]   # given name must match (homonyms: J./P. Čižinský)
    if len(hits) > 1:
        hits = [k for k in hits if fold(names[k]).split()[0] in toks] or hits
    return hits[0] if hits else "Someone_else"


def load_series() -> tuple[dict, dict, dict]:
    from build import keyed_model, dist_of  # noqa: E402
    snaps = {s: json.loads((SNAP / f).read_text()) for s, f in [
        ("ai0", "2026-10-02-blind.json"), ("ai", "2026-10-09-ai.json"), ("model", "2026-10-03-model.json"),
        ("aimodel", "2026-10-09-aimodel.json"), ("market", "2026-10-09-market.json"), ("blend", "2026-10-09-blend.json")]}
    refs = {"ref_fortuna_close": Path(sys.argv[3]) if len(sys.argv) > 3 else None,
            "ref_evening": MK / "2026-10-09e.json", "ref_morning": MK / "2026-10-10m.json"}
    for k, f in refs.items():
        if f and f.exists():
            snaps[k] = json.loads(f.read_text())
    names = {d["n"]: {c["key"]: c["name"] for c in d["candidates"]} for d in snaps["ai"]["districts"]}
    dists: dict[str, dict[int, dict[str, float]]] = {}
    for s, snap in snaps.items():
        dists[s] = {}
        for d in snap["districts"]:
            n = d["n"]
            dd = keyed_model(d, list(names[n]), names[n]) if s == "model" else dist_of(d)
            tot = sum(dd.values()) or 1.0
            dists[s][n] = {k: dd.get(k, 0.0) / tot for k in names[n]}
    model_r1 = {d["n"]: {c["name"]: c for c in d["candidates"]} for d in snaps["model"]["districts"]}
    return dists, names, model_r1


SERIES = ["ai0", "ai", "model", "aimodel", "market", "blend"]
REFS = ["ref_fortuna_close", "ref_evening", "ref_morning"]
LABEL = {"ai0": "AI 2. 10.", "ai": "AI", "model": "Stat. model", "aimodel": "AI s modelem", "market": "Sázky (freeze)",
         "blend": "Blend", "ref_fortuna_close": "ref: Fortuna close", "ref_evening": "ref: večer 9. 10.",
         "ref_morning": "ref: ráno 10. 10."}


def score_r1(path: Path) -> None:
    res = json.loads(path.read_text())
    dists, names, model_r1 = load_series()
    series = [s for s in SERIES + REFS if s in dists]
    rows, per = [], {s: [] for s in series}
    for n in DISTRICTS:
        r = res["districts"][str(n)] if str(n) in res["districts"] else res["districts"][n]
        cands = sorted(r["candidates"], key=lambda c: -c["pct"])
        if not cands:
            continue
        for c in cands:
            c["key"] = key_for(c["name"], names[n])
        top = cands[0]
        decided = top["pct"] > 50.0
        if decided:
            alive = [top["key"]]
        else:
            alive = [c["key"] for c in cands[:2]]
        rec = {"n": n, "name": r["name"], "counted": r["counted_pct"], "decided": decided,
               "top": [(c["name"], c["pct"], c["key"]) for c in cands[:3]], "s": {}}
        for s in series:
            p = dists[s].get(n)
            if not p:
                continue
            fav = max(p, key=p.get)
            p_alive = sum(p.get(k, 0.0) for k in set(alive))
            fixed = sum(v * v for k, v in p.items() if k not in alive)
            if decided:
                w = alive[0]
                brier = sum((v - (1.0 if k == w else 0.0)) ** 2 for k, v in p.items())
                rng = (brier, brier)
                logs = -math.log(max(p.get(w, 0.0), 1e-4))
            else:
                a, b = alive[0], alive[1]
                def br(w):  # noqa: E306
                    return sum((v - (1.0 if k == w else 0.0)) ** 2 for k, v in p.items())
                rng = (br(a), br(b)) if a != b else (br(a), br(a))
                brier, logs = None, None
            x = {"fav": fav, "fav_alive": fav in alive, "p_alive": p_alive, "mass_elim": 1 - p_alive,
                 "brier_fixed": fixed, "brier_if_1st": rng[0], "brier_if_2nd": rng[1], "brier": brier, "log": logs}
            rec["s"][s] = x
            per[s].append((n, x))
        rows.append(rec)
    out = {"results_file": str(path), "counted_cr": res["cr"].get("spocteno"), "rows": rows}

    # --- report ---
    P = print
    P(f"# Senát 2026 — průběžné hodnocení po 1. kole\n\nVýsledky: `{path.name}`, sečteno ČR {res['cr'].get('spocteno')} %.\n")
    def agg(sel, title):  # noqa: E306
        P(f"\n## {title} (n={len(sel)})\n")
        P("| série | fav. postoupil | hmota na vyřazené (Σ) | Brier pevná část (Σ) | Brier když vyhraje 1. z r1 (Σ) | Brier když 2. (Σ) | rozhodnuto v r1: Brier / log |")
        P("|---|---|---|---|---|---|---|")
        for s in series:
            xs = [x for n, x in per[s] if n in sel]
            if not xs:
                continue
            dec = [x for x in xs if x["brier"] is not None]
            dec_s = f"{sum(x['brier'] for x in dec):.3f} / {sum(x['log'] for x in dec):.2f} (n={len(dec)})" if dec else "—"
            P(f"| {LABEL[s]} | {sum(x['fav_alive'] for x in xs)}/{len(xs)} | {sum(x['mass_elim'] for x in xs):.2f} | "
              f"{sum(x['brier_fixed'] for x in xs):.3f} | {sum(x['brier_if_1st'] for x in xs):.2f} | "
              f"{sum(x['brier_if_2nd'] for x in xs):.2f} | {dec_s} |")
    agg(DISTRICTS, "Všech 27 obvodů")
    agg(PREREG, "9 předregistrovaných sporných (5. 10.)")
    agg(FREEZE_DISPUTED, "7 sporných při freeze (9. 10.)")

    P("\n## Po obvodech (P na postoupivší / vítěze; * = favorit série vypadl)\n")
    P("| obvod | sečteno | 1. | 2. | " + " | ".join(LABEL[s] for s in series) + " |")
    P("|---|---|---|---|" + "---|" * len(series))
    for r in rows:
        t = r["top"]
        first = f"{t[0][0].split()[0]} {t[0][1]:.1f}" + (" ✔" if r["decided"] else "")
        second = f"{t[1][0].split()[0]} {t[1][1]:.1f}" if len(t) > 1 else ""
        cells = []
        for s in series:
            x = r["s"].get(s)
            cells.append("—" if not x else f"{x['p_alive']*100:.0f}" + ("" if x["fav_alive"] else "*"))
        P(f"| {r['n']} {r['name']} | {r['counted']:.0f} % | {first} | {second} | " + " | ".join(cells) + " |")

    # model round-1 % vs actual, home-base hypothesis
    P("\n## Statistický model: r1 % vs skutečnost\n")
    errs, hb, ctrl = [], [], []
    for n in DISTRICTS:
        r = res["districts"][str(n)] if str(n) in res["districts"] else res["districts"][n]
        mr = model_r1.get(n, {})
        for c in r["candidates"]:
            toks = [fold(t) for t in c["name"].split() if not t.endswith(".") and t[0].isupper()]
            cand = [v for k, v in mr.items() if fold(k).split()[-1] in toks]
            if len(cand) > 1:
                cand = [v for k, v in mr.items() if fold(k).split()[-1] in toks and fold(k).split()[0] in toks] or cand
            m = cand[0] if cand else None
            if not m:
                continue
            e = c["pct"] - m["r1_mean"]
            errs.append(abs(e))
            k = key_for(c["name"], names[n])
            if HOME_BASE.get(n) == k:
                hb.append((n, k, m["r1_mean"], c["pct"], e))
            elif m["r1_mean"] >= 15:
                ctrl.append(e)
    if errs:
        P(f"MAE všech kandidátů: **{sum(errs)/len(errs):.1f} p.b.** (n={len(errs)})\n")
    P("Hypotéza bašt (předregistrováno 8. 10.): skutečnost − model\n")
    for n, k, mm, a, e in hb:
        P(f"- {n} {k}: model {mm:.1f} → {a:.1f} ({e:+.1f})")
    if hb and ctrl:
        d = sum(x[4] for x in hb) / len(hb) - sum(ctrl) / len(ctrl)
        P(f"\nBašty průměr {sum(x[4] for x in hb)/len(hb):+.1f}, srovnávací skupina (model ≥15 %, n={len(ctrl)}) "
          f"{sum(ctrl)/len(ctrl):+.1f} → rozdíl **{d:+.1f} p.b.** → "
          + ("potvrzeno (≥3)" if d >= 3 else "vyvráceno (≤0)" if d <= 0 else "nerozhodné (0–3)"))
    # Seznam Zprávy benchmark (pre-registered 6. 10.): ANO advancement, Brier on advance + MAE of r1 %
    sz = json.loads((ROOT / "data" / "sz-model" / "2026-10-06.json").read_text())
    P("\n## Benchmark Seznam Zpráv (kandidáti ANO; předregistrováno 6. 10.)\n")
    adv_n, rows_sz = 0, []
    for c in sz["candidates"]:
        n = next((x for x in DISTRICTS if fold(res["districts"][str(x)]["name"]) == fold(c["obvod_name"])), None)
        if n is None:
            continue
        r = res["districts"][str(n)]
        cs = sorted(r["candidates"], key=lambda v: -v["pct"])
        top_out = cs and cs[0]["pct"] > 50
        adv_names = [cs[0]["name"]] if top_out else [v["name"] for v in cs[:2]]
        me = next((v for v in r["candidates"] if fold(v["name"]).startswith(fold(c["surname"]) + " ")), None)
        if not me:
            continue
        adv = me["name"] in adv_names
        adv_n += adv
        mr = model_r1.get(n, {})
        m = next((v for k, v in mr.items() if fold(k).endswith(" " + fold(c["surname"]))), None)
        sz_mid = (c["r1_unfav"] + c["r1_fav"]) / 2
        rows_sz.append((n, c["surname"], adv, c["adv_mid"] / 100, m["p_advance"] if m else None, sz_mid,
                        m["r1_mean"] if m else None, me["pct"]))
    if rows_sz:
        def b(i):  # noqa: E306
            xs = [(r[i] - r[2]) ** 2 for r in rows_sz if r[i] is not None]
            return sum(xs) / len(xs)
        def mae(i):  # noqa: E306
            xs = [abs(r[i] - r[7]) for r in rows_sz if r[i] is not None]
            return sum(xs) / len(xs)
        P(f"Postoupilo kandidátů ANO: **{adv_n} z {len(rows_sz)}** (SZ: 13,4 / 17,3 / 21,2; náš model 14,5).\n")
        P(f"| | SZ střední | Stat. model |\n|---|---|---|\n| Brier na postup | {b(3):.3f} | {b(4):.3f} |\n"
          f"| MAE 1. kola (p.b.) | {mae(5):.1f} | {mae(6):.1f} |\n")
        P("| obvod | ANO | postoupil | SZ P(post.) | model P(post.) | SZ % | model % | skutečnost % |\n|---|---|---|---|---|---|---|---|")
        for r in rows_sz:
            P(f"| {r[0]} | {r[1]} | {'ano' if r[2] else 'ne'} | {r[3]*100:.0f} | {r[4]*100 if r[4] is not None else float('nan'):.0f} | "
              f"{r[5]:.1f} | {r[6] if r[6] is not None else float('nan'):.1f} | {r[7]:.1f} |")

    # Wikipedia benchmark (pre-registered 8. 10.): most-read candidate wins -> after r1 only "advanced?"
    WIKI = {3: "Tsoukernik", 6: "Steiner", 9: "Řehka", 12: "Ušatý", 15: "Chalupský", 18: "Štěpánek", 21: "Šarapatka",
            24: "Pecková", 27: "Čižinský Jan", 30: "Gerloch", 33: "Linhart", 36: "Půta", 39: "Sobotka", 42: "Sehnal",
            45: "Nebeská", 48: "Grulich", 51: "Šmarda", 54: "Rédová Fajmonová", 57: "Grolich", 60: "Papoušek",
            63: "Obrtel", 66: "Kohajda", 69: "Lisková", 72: "Šimetka", 75: "Szyja", 78: "Goláň", 81: "Balaštíková"}
    ok, won = 0, 0
    for n, who in WIKI.items():
        r = res["districts"][str(n)]
        cs = sorted(r["candidates"], key=lambda v: -v["pct"])
        alive = cs[:1] if cs and cs[0]["pct"] > 50 else cs[:2]
        hit = any(fold(v["name"]).startswith(fold(who)) for v in alive)
        ok += hit
        won += hit and len(alive) == 1
    P(f"\n## Benchmark Wikipedie (nejčtenější vyhraje)\n\nNejčtenější kandidát postoupil/vyhrál v **{ok} z 27** obvodů "
      f"(z toho vyhrál už v 1. kole {won}).")
    json_out = path.with_name(path.stem + "-score.json")
    json_out.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch":
        print(fetch(int(sys.argv[2]) if len(sys.argv) > 2 else 1))
    elif cmd == "r1":
        score_r1(Path(sys.argv[2]))
