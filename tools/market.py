#!/usr/bin/env python3
"""Build the de-vigged market consensus per district (Sázky series) from raw bookmaker files.

Fortuna: full seat-winner book -> power de-vig. Tipsport: binary Ano/Ne on one candidate ("celkově") -> power de-vig.
Consensus: the Tipsport candidate's probability = 0.5*Fortuna + 0.5*Tipsport (Tipsport has a much lower margin but
covers one candidate only); the remaining mass is split across the other candidates in Fortuna's de-vigged ratios.
Probabilities are mapped onto the AI series' ASCII keys; unmatched candidates -> Someone_else.
"""
from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from forecast_math import power_fair  # noqa: E402

MK = ROOT / "data" / "senat-market"
SNAP = ROOT.parent / "senat-2026-forecast" / "data" / "snapshots"


def fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


def parse(path: Path, kind: str) -> dict[int, list]:
    out = {}
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        n, rest = line.split(":", 1)
        toks = rest.split()
        if kind == "fortuna":
            out[int(n)] = [(toks[i], float(toks[i + 1])) for i in range(0, len(toks), 2)]
        else:
            out[int(n)] = (toks[0], float(toks[2]), float(toks[4]))
    return out


def surname_key(token: str) -> str:
    parts = [p for p in token.replace("_", " ").split() if not p.endswith(".") and len(p) > 1]
    return fold(" ".join(parts))


def main(date: str) -> None:
    fort = parse(MK / f"raw-fortuna-{date}.txt", "fortuna")
    tip = parse(MK / f"raw-tipsport-{date}.txt", "tipsport") if (MK / f"raw-tipsport-{date}.txt").exists() else {}
    aim = json.loads((SNAP / f"{date}-aimodel.json").read_text())
    res = {"experiment": "senat-2026", "series": "market", "date": date,
           "method": "Fortuna power de-vig (full book) + Tipsport power de-vig (binary on one candidate), 50/50 on the "
                     "Tipsport candidate, rest in Fortuna ratios; mapped to AI keys", "districts": []}
    for d in aim["districts"]:
        n = d["n"]
        keys = {c["key"]: c["name"] for c in d["candidates"]}
        def to_key(tok: str) -> str:
            sk = surname_key(tok)
            for k, name in keys.items():
                if k == "Someone_else":
                    continue
                fn = fold(name)
                if sk and (sk in fn or fn.split()[-1] in sk):
                    # disambiguate same surname (Čižinský J./P.)
                    init = re.search(r"_([A-ZÁ-Ž])\.", tok)
                    if init and fold(init.group(1)) != fold(name.split()[0][0]):
                        continue
                    return k
            return "Someone_else"
        fb = fort.get(n)
        if not fb:
            continue
        odds = {f"c{i}": o for i, (_, o) in enumerate(fb)}
        fair = power_fair(odds)
        fmap: dict[str, float] = {}
        for i, (tok, _) in enumerate(fb):
            k = to_key(tok)
            fmap[k] = fmap.get(k, 0.0) + fair[f"c{i}"]
        margin = sum(1 / o for o in odds.values()) - 1
        cons = dict(fmap)
        note = f"Fortuna margin {margin*100:.0f} %"
        if n in tip:
            tok, ano, ne = tip[n]
            tk = to_key(tok)
            tp = power_fair({"Y": ano, "N": ne})["Y"]
            target = 0.5 * fmap.get(tk, 0.0) + 0.5 * tp
            rest = 1 - fmap.get(tk, 0.0)
            cons = {k: (target if k == tk else v * (1 - target) / rest if rest > 0 else 0.0) for k, v in fmap.items()}
            note += f"; Tipsport {keys.get(tk, tk)} fair {tp*100:.0f} % (margin {(1/ano+1/ne-1)*100:.0f} %)"
        for k in keys:
            cons.setdefault(k, 0.0)
        res["districts"].append({"n": n, "fortuna": {k: round(v, 4) for k, v in fmap.items()},
                                 "tipsport": (dict(zip(["candidate", "ano", "ne"], tip[n])) if n in tip else None),
                                 "consensus": {k: round(v, 4) for k, v in cons.items()},
                                 "note": note, "note_cs": note.replace("margin", "marže")})
    (MK / f"{date}.json").write_text(json.dumps(res, ensure_ascii=False, indent=2))
    for d in res["districts"]:
        top = sorted(d["consensus"].items(), key=lambda kv: -kv[1])[:3]
        print(d["n"], " | ".join(f"{k} {v*100:.0f}" for k, v in top), "·", d["note"])


def parse_h2h(path: Path) -> dict[int, list]:
    """Round-2 head-to-head lines: `N: A 1.40 x B 2.68` (Tipsport) or `N: A 1.40 B 2.68` (Fortuna); `zamč.` = locked."""
    out = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        n, rest = line.split(":", 1)
        toks = [t for t in rest.split() if t != "x"]
        out[int(n)] = [(toks[0], None if toks[1].startswith("zam") else float(toks[1])),
                       (toks[2], None if toks[3].startswith("zam") else float(toks[3]))]
    return out


def main_r2(date: str) -> None:
    """Round 2 (pre-registered 11. 10.): power de-vig of each two-way book; odds 1.01 kept as the floor; a book with a
    locked price is skipped for that district; consensus = mean of the available books; no book -> no Sázky/Blend."""
    books = {"fortuna": parse_h2h(MK / f"raw-fortuna-{date}-r2.txt"), "tipsport": parse_h2h(MK / f"raw-tipsport-{date}-r2.txt")}
    aim = json.loads((SNAP / f"{date}-aimodel.json").read_text())
    res = {"experiment": "senat-2026", "series": "market", "date": date, "round": 2,
           "method": "Round 2: Fortuna + Tipsport head-to-head ('who gets more votes'), power de-vig per book, "
                     "1.01 kept as floor, locked book skipped, consensus = mean of available books; mapped to AI keys",
           "districts": []}
    for d in aim["districts"]:
        n = d["n"]
        keys = {c["key"]: c["name"] for c in d["candidates"]}
        def to_key(tok: str) -> str:
            sk = surname_key(tok)
            for k, name in keys.items():
                fn = fold(name)
                if k != "Someone_else" and sk and (sk in fn or fn.split()[-1] in sk):
                    return k
            raise SystemExit(f"{n}: {tok} not matched to {list(keys)}")
        fair_by, notes = {}, []
        for bk, data in books.items():
            row = data.get(n)
            if not row:
                continue
            if any(o is None for _, o in row):
                notes.append(f"{bk.capitalize()} locked (skipped)")
                continue
            fair = power_fair({tok: o for tok, o in row})
            fair_by[bk] = {to_key(tok): p for tok, p in fair.items()}
            notes.append(f"{bk.capitalize()} margin {(sum(1 / o for _, o in row) - 1) * 100:.0f} %")
        if not fair_by:
            if notes:
                res["districts"].append({"n": n, "consensus": None, "note": "; ".join(notes),
                                         "note_cs": "; ".join(notes).replace("locked (skipped)", "uzamčeno (vynecháno)").replace("margin", "marže")})
            continue
        fin = set().union(*fair_by.values())
        cons = {k: sum(fb.get(k, 0.0) for fb in fair_by.values()) / len(fair_by) for k in fin}
        for k in keys:
            cons.setdefault(k, 0.0)
        note = "; ".join(notes)
        res["districts"].append({"n": n, **{bk: {k: round(v, 4) for k, v in fb.items()} for bk, fb in fair_by.items()},
                                 "consensus": {k: round(v, 4) for k, v in cons.items()},
                                 "note": note, "note_cs": note.replace("locked (skipped)", "uzamčeno (vynecháno)").replace("margin", "marže")})
    (MK / f"{date}.json").write_text(json.dumps(res, ensure_ascii=False, indent=2))
    for d in res["districts"]:
        top = sorted((d["consensus"] or {}).items(), key=lambda kv: -kv[1])[:2]
        print(d["n"], " | ".join(f"{k} {v*100:.1f}" for k, v in top) or "—", "·", d["note"])


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--r2"]
    (main_r2 if "--r2" in sys.argv else main)(args[0] if args else "2026-10-05")
