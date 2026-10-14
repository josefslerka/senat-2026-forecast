#!/usr/bin/env python3
"""Senát 2026 — pre-registered PAPER betting (no money). Rule: runs/_senat-2026-paper-bets-prereg.md (14. 10. 2026).

  python3 scripts/senat_model/paper_bets.py place r1             # freeze 9. 10. vs scored odds 9. 10.
  python3 scripts/senat_model/paper_bets.py place r2 <date>      # last locked snapshots vs scored odds of <date>
  python3 scripts/senat_model/paper_bets.py settle <bets.json>   # needs data/senat-results/final-winners.json {"n": "Key"}

The rule below must not change after the pre-registration commit; any bug fix is logged publicly with its diff.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from market import MK, SNAP, fold, parse, parse_h2h, surname_key  # noqa: E402
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
from forecast_math import power_fair  # noqa: E402

OUT = HERE.parents[1] / "data" / "senat-paper-bets"
RES = HERE.parents[1] / "data" / "senat-results"

# --- pre-registered constants (14. 10. 2026) ---
MIN_EV, MIN_EDGE, MAX_ODDS = 0.10, 0.03, 20.0
FLAT, BANKROLL, KELLY_FRAC, KELLY_CAP = 100, 10_000, 0.25, 0.02
SERIES = {"r1": {"ai": "2026-10-09-ai", "model": "2026-10-03-model", "aimodel": "2026-10-09-aimodel", "blend": "2026-10-09-blend"},
          "r2": {"ai": "{d}-ai", "model": "{d}-model-r2", "aimodel": "{d}-aimodel", "blend": "{d}-blend"}}
ODDS = {"r1": {"fortuna": "raw-fortuna-2026-10-09.txt", "tipsport": "raw-tipsport-2026-10-09.txt"},
        "r2": {"fortuna": "raw-fortuna-{d}-r2.txt", "tipsport": "raw-tipsport-{d}-r2.txt"}}
CLOSE = {"r1": {"fortuna": "raw-fortuna-2026-10-09-close.txt", "tipsport": "raw-tipsport-2026-10-10m.txt"}}


def keymap(district: dict):
    """Map a bookmaker token or a full name onto the AI key of this district."""
    keys = {c["key"]: c["name"] for c in district["candidates"] if c["key"] != "Someone_else"}
    def to_key(tok: str) -> str:
        sk = surname_key(tok)
        for k, name in keys.items():
            fn = fold(name)
            if sk and (sk in fn or fn.split()[-1] in sk):
                if "_" in tok and "." in tok and fold(tok.split("_")[1][0]) != fold(name.split()[0][0]):
                    continue  # same surname, different initial (Čižinský J./P.)
                return k
        return "Someone_else"
    return to_key


def probs(snap: dict, n: int, to_key) -> dict[str, float]:
    d = next((x for x in snap["districts"] if x["n"] == n), None)
    if d is None:
        return {}
    out: dict[str, float] = {}
    for c in d["candidates"]:
        k = c.get("key") or to_key(c["name"].replace(" ", "_"))
        out[k] = out.get(k, 0.0) + c["p"]
    return out


def offers(rnd: str, files: dict) -> dict[int, list]:
    """All prices on offer: (book, selection key-token, side, odds, fair) per district."""
    res: dict[int, list] = {}
    for bk, fn in files.items():
        path = MK / fn
        if not path.exists():
            continue
        if rnd == "r2":
            for n, row in parse_h2h(path).items():
                if any(o is None for _, o in row):
                    continue  # locked
                fair = power_fair({t: o for t, o in row})
                res.setdefault(n, []).extend((bk, t, "win", o, fair[t]) for t, o in row)
        elif bk == "fortuna":
            for n, row in parse(path, "fortuna").items():
                fair = power_fair({f"c{i}": o for i, (_, o) in enumerate(row)})
                res.setdefault(n, []).extend((bk, t, "win", o, fair[f"c{i}"]) for i, (t, o) in enumerate(row))
        else:
            for n, (t, ano, ne) in parse(path, "tipsport").items():
                fy = power_fair({"Y": ano, "N": ne})
                res.setdefault(n, []).extend([(bk, t, "win", ano, fy["Y"]), (bk, t, "lose", ne, fy["N"])])
    return res


def place(rnd: str, date: str | None = None) -> None:
    fmt = lambda s: s.format(d=date)
    snaps = {s: json.loads((SNAP / f"{fmt(f)}.json").read_text()) for s, f in SERIES[rnd].items()}
    ref = snaps["aimodel"]  # carries keys + names for every district
    offs = offers(rnd, {b: fmt(f) for b, f in ODDS[rnd].items()})
    close = offers(rnd, CLOSE[rnd]) if rnd in CLOSE else {}
    bets = []
    for d in ref["districts"]:
        n, to_key = d["n"], keymap(d)
        for s, snap in snaps.items():
            P = probs(snap, n, to_key)
            if not P or n not in offs:
                continue
            best = None
            for bk, tok, side, o, fair in offs[n]:
                k = to_key(tok)
                if k == "Someone_else":
                    continue  # minor candidates are pooled in our series -> no price for a single one
                p = P.get(k, 0.0) if side == "win" else 1 - P.get(k, 0.0)
                ev, edge = p * o - 1, p - fair
                if ev >= MIN_EV and edge >= MIN_EDGE and o <= MAX_ODDS and (best is None or ev > best["ev"]):
                    kelly = KELLY_FRAC * (p * o - 1) / (o - 1)
                    best = {"n": n, "series": s, "book": bk, "selection": k, "side": side, "odds": o,
                            "p": round(p, 4), "fair": round(fair, 4), "ev": round(ev, 4), "edge": round(edge, 4),
                            "stake_flat": FLAT, "stake_kelly": round(min(kelly, KELLY_CAP) * BANKROLL)}
            if best:
                cl = [o for bk, t, sd, o, _ in close.get(n, []) if bk == best["book"] and sd == best["side"] and to_key(t) == best["selection"]]
                best["close_odds"] = cl[0] if cl else None
                bets.append(best)
        # baseline: flat bet on the market favourite (lowest price on offer for a 'win' selection), best book
        wins = [(o, bk, to_key(t)) for bk, t, sd, o, _ in offs.get(n, []) if sd == "win"]
        if wins:
            fav = min(wins)[2]
            o = max(x[0] for x in wins if x[2] == fav)
            bets.append({"n": n, "series": "baseline_favourite", "book": [b for x, b, k in wins if k == fav and x == o][0],
                         "selection": fav, "side": "win", "odds": o, "stake_flat": FLAT, "stake_kelly": 0})
    OUT.mkdir(parents=True, exist_ok=True)
    tag = "r1-2026-10-09" if rnd == "r1" else f"r2-{date}"
    out = {"experiment": "senat-2026", "kind": "paper-bets", "round": rnd, "snapshot_date": date or "2026-10-09",
           "rule": "runs/_senat-2026-paper-bets-prereg.md", "bets": bets}
    (OUT / f"{tag}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    for s in list(SERIES[rnd]) + ["baseline_favourite"]:
        b = [x for x in bets if x["series"] == s]
        print(f"{s:20s} {len(b):2d} bets  flat {sum(x['stake_flat'] for x in b):5d} Kč  kelly {sum(x['stake_kelly'] for x in b):5d} Kč")
        for x in b if s != "baseline_favourite" else []:
            print(f"   {x['n']:2d} {x['book']:8s} {x['selection']:18s} {x['side']:4s} @{x['odds']:5.2f}  p {x['p']:.2f} fair {x['fair']:.2f} EV {x['ev']:+.0%}  kelly {x['stake_kelly']} Kč")


def settle(path: str) -> None:
    data = json.loads(Path(path).read_text())
    W = {int(k): v for k, v in json.loads((RES / "final-winners.json").read_text()).items()}
    rows = {}
    for b in data["bets"]:
        if b["n"] not in W:
            continue
        won = (W[b["n"]] == b["selection"]) == (b["side"] == "win")
        r = rows.setdefault(b["series"], {"bets": 0, "hits": 0, "flat_stake": 0, "flat_pl": 0.0, "kelly_stake": 0, "kelly_pl": 0.0, "clv": []})
        r["bets"] += 1; r["hits"] += won
        for m in ("flat", "kelly"):
            st = b[f"stake_{m}"]; r[f"{m}_stake"] += st; r[f"{m}_pl"] += st * (b["odds"] - 1) if won else -st
        if b.get("close_odds"):
            r["clv"].append(b["odds"] / b["close_odds"] - 1)
    for s, r in rows.items():
        roi = lambda m: r[f"{m}_pl"] / r[f"{m}_stake"] if r[f"{m}_stake"] else 0
        clv = f"  CLV {sum(r['clv'])/len(r['clv']):+.1%}" if r["clv"] else ""
        print(f"{s:20s} {r['hits']}/{r['bets']}  flat {r['flat_pl']:+7.0f} Kč (ROI {roi('flat'):+.0%})  kelly {r['kelly_pl']:+7.0f} Kč (ROI {roi('kelly'):+.0%}){clv}")


if __name__ == "__main__":
    a = sys.argv[1:]
    place(a[1], a[2] if len(a) > 2 else None) if a[0] == "place" else settle(a[1])
