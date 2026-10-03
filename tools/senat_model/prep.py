#!/usr/bin/env python3
"""Senate model, step 1: data preparation from ČSÚ open data.

Outputs (data/senat-model/):
  party_shares.csv  – Chamber-election party shares per Senate district, for each Senate year's boundaries
  candidates.csv    – Senate candidates 2020/2022/2024/2026 with support sets, party base and features

Chamber election used as the party base for each Senate year:
  2020, 2022, 2024 -> Chamber 2021;  2026 -> Chamber 2025.
Precinct -> district mapping uses that Senate year's official secoco table (obec + precinct ranges).
Multi-party Chamber lists are split across member parties with fixed weights (ASSUMPTION, documented).
"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "senat-model" / "raw"
OUT = ROOT / "data" / "senat-model"

SENATE = {
    2020: dict(secoco="se2020/SE2020ciselnik20200918_csv/secoco.csv", serk="se2020/SE2020reg20201010_csv/serk.csv",
               slozeni=None, cvs="se2020/SE2020ciselnik20200918_csv/cvs.csv", data="se2020/SENAT2020_data_20201010_k2_csv/set5.csv", chamber=2021),
    2022: dict(secoco="se2022/SE2022ciselniky20220916_csv/csv_od/secoco.csv", serk="se2022/SE2022reg20221001_csv/csv_od/serk.csv",
               slozeni="se2022/SE2022ciselniky20220916_csv/csv_od/cvs_slozeni.csv", cvs="se2022/SE2022ciselniky20220916_csv/csv_od/cvs.csv",
               data="se2022/SE2022_data_20221001_k2_csv/csv_od/set5.csv", chamber=2021),
    2024: dict(secoco="se2024/SE2024ciselniky20240928_csv/csv_od/secoco.csv", serk="se2024/SE2024reg20240928_csv/csv_od/serk.csv",
               slozeni="se2024/SE2024ciselniky20240928_csv/csv_od/cvs_slozeni.csv", cvs="se2024/SE2024ciselniky20240928_csv/csv_od/cvs.csv",
               data="se2024/SE2024data20240928_csv/csv_od/set5.csv", chamber=2021),
    2026: dict(secoco="se2026/SE2026ciselniky20260915_csv/csv_od/secoco.csv", serk="se2026/SE2026reg20260915_csv/csv_od/serk.csv",
               slozeni="se2026/SE2026ciselniky20260915_csv/csv_od/cvs_slozeni.csv", cvs="se2026/SE2026ciselniky20260915_csv/csv_od/cvs.csv",
               data=None, chamber=2025),
}
CHAMBER = {
    2021: dict(votes="ps2021/PS2021_data_20211010_csv/csv_od/pst4p.csv", slozeni="ps2021/PS2021reg20211010_csv/csv_od/psrkl_slozeni.csv"),
    2025: dict(votes="ps2025/PS2025data20251005_csv/csv_od/pst4p.csv", slozeni="ps2025/PS2025reg20251005_csv/csv_od/psrkl_slozeni.csv"),
}
# ASSUMPTION: split of joint Chamber lists among member parties (vote weights).
LIST_SPLIT = {
    frozenset({1, 53, 721}): {53: 0.60, 1: 0.22, 721: 0.18},   # SPOLU (KDU-ČSL, ODS, TOP 09)
    frozenset({720, 166}): {720: 0.50, 166: 0.50},             # Piráti + STAN (2021)
}
GOV = {2020: {768, 7}, 2022: {53, 1, 721, 166, 720}, 2024: {53, 1, 721, 166, 720}, 2026: {768, 1114, 1178}}
ANO = 768


def read(rel: str) -> list[dict]:
    p = RAW / rel
    raw = p.read_bytes()
    for enc in ("utf-8-sig", "cp1250"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    delim = ";" if text.split("\n", 1)[0].count(";") > text.split("\n", 1)[0].count(",") else ","
    return list(csv.DictReader(text.splitlines(), delimiter=delim))


def num(x) -> float:
    try:
        return float(str(x).replace(",", "."))
    except ValueError:
        return 0.0


def precinct_mapper(year: int):
    rows = read(SENATE[year]["secoco"])
    by_obec: dict[int, list] = defaultdict(list)
    for r in rows:
        ranges = []
        for k in range(1, 11):
            lo = r.get(f"MINOKRSEK{k}") or r.get(f"MINOKRSE{k}")
            hi = r.get(f"MAXOKRSEK{k}") or r.get(f"MAXOKRSE{k}")
            if lo and hi and int(lo) > 0:
                ranges.append((int(lo), int(hi)))
        by_obec[int(r["OBEC"])].append((int(r["OBVOD"]), ranges))

    def obvod(obec: int, okrsek: int) -> int | None:
        opts = by_obec.get(obec)
        if not opts:
            return None
        if len(opts) == 1:
            return opts[0][0]
        for ob, ranges in opts:
            if any(lo <= okrsek <= hi for lo, hi in ranges):
                return ob
        return None
    return obvod


def chamber_party_shares(chamber: int, senate_year: int) -> pd.DataFrame:
    members: dict[int, list[int]] = defaultdict(list)
    for r in read(CHAMBER[chamber]["slozeni"]):
        members[int(r["KSTRANA"])].append(int(r["NSTRANA"]))
    mapper = precinct_mapper(senate_year)
    votes: dict[tuple[int, int], float] = defaultdict(float)
    total: dict[int, float] = defaultdict(float)
    unmapped = 0
    for r in read(CHAMBER[chamber]["votes"]):
        ob = mapper(int(r["OBEC"]), int(r["OKRSEK"]))
        v = num(r["POC_HLASU"])
        if ob is None:
            unmapped += v
            continue
        mem = members.get(int(r["KSTRANA"]), [int(r["KSTRANA"]) * -1])
        split = LIST_SPLIT.get(frozenset(mem)) or {p: 1 / len(mem) for p in mem}
        for p, w in split.items():
            votes[(ob, p)] += v * w
        total[ob] += v
    rows = [dict(senate_year=senate_year, chamber=chamber, obvod=ob, party=p, share=v / total[ob])
            for (ob, p), v in votes.items()]
    print(f"  chamber {chamber} on {senate_year} boundaries: {len(total)} districts, unmapped votes {unmapped:.0f}")
    return pd.DataFrame(rows)


def senate_results(year: int) -> dict[tuple[int, int, int], float]:
    """(obvod, ckand, kolo) -> votes, from precinct data."""
    if not SENATE[year]["data"]:
        return {}
    out: dict[tuple[int, int, int], float] = defaultdict(float)
    for r in read(SENATE[year]["data"]):
        ob, kolo = int(r["OBVOD"]), int(r["KOLO"])
        for k in range(1, 23):
            v = num(r.get(f"HLASY_{k:02d}", 0))
            if v:
                out[(ob, k, kolo)] += v
    return out


def candidates(year: int, shares: pd.DataFrame, local: dict | None = None) -> pd.DataFrame:
    slozeni: dict[int, set[int]] = defaultdict(set)
    if SENATE[year]["slozeni"]:
        for r in read(SENATE[year]["slozeni"]):
            slozeni[int(r["VSTRANA"])].add(int(r["NSTRANA"]))
    else:  # 2020: composition is encoded in cvs.SLOZENI as a comma/space separated list
        for r in read(SENATE[year]["cvs"]):
            parts = [int(x) for x in re.findall(r"\d+", r.get("SLOZENI", ""))]
            slozeni[int(r["VSTRANA"])] = set(parts) or {int(r["VSTRANA"])}
    cvs = {int(r["VSTRANA"]): r.get("ZKRATKAV8") or r.get("ZKRATKAV30") or "" for r in read(SENATE[year]["cvs"])}
    sh = {(int(o), int(p)): s for o, p, s in shares[["obvod", "party", "share"]].itertuples(index=False)}
    res = senate_results(year)
    rows = []
    for r in read(SENATE[year]["serk"]):
        if r.get("PLATNOST", "A") not in ("A", ""):
            continue
        ob, ck, vs = int(r["OBVOD"]), int(r["CKAND"]), int(r["VSTRANA"])
        support = set(slozeni.get(vs, {vs}))
        ns = int(r["NSTRANA"] or 0)
        if ns and ns != 99:
            support.add(ns)
        base = sum(sh.get((ob, p), 0.0) for p in support)
        local = local or {}
        # local share of supporting subjects that have NO Chamber presence in the district (local/regional movements)
        local_extra = sum(local.get((ob, p), 0.0) for p in support
                          if sh.get((ob, p), 0.0) == 0.0 and p not in NATIONAL_PARTIES)
        local_all = sum(local.get((ob, p), 0.0) for p in support)
        pov = (r.get("POVOLANI") or "").lower()
        rows.append(dict(
            year=year, obvod=ob, ckand=ck, name=f"{r['JMENO']} {r['PRIJMENI']}", vstrana=vs, list=cvs.get(vs, ""),
            nstrana=ns, pstrana=int(r["PSTRANA"] or 0), support=" ".join(map(str, sorted(support))),
            n_support=len(support), base=base, local_extra=local_extra, local_all=local_all,
            incumbent=int(bool(re.search(r"\bsenátor", pov)) and "bývalý" not in pov),
            local_exec=int(bool(re.search(r"starost|primátor|hejtman", pov))),
            mp=int(bool(re.search(r"poslan", pov))),
            gov=int(bool(support & GOV[year])), ano=int(ANO in support),
            age=int(r["VEK"] or 0), povolani=r.get("POVOLANI", ""),
            votes_k1=res.get((ob, ck, 1), 0.0), votes_k2=res.get((ob, ck, 2), 0.0),
        ))
    df = pd.DataFrame(rows)
    if len(df) and res:
        df["share_k1"] = df["votes_k1"] / df.groupby("obvod")["votes_k1"].transform("sum") * 100
        k2 = df.groupby("obvod")["votes_k2"].transform("sum")
        df["share_k2"] = (df["votes_k2"] / k2.where(k2 > 0) * 100).fillna(0)
    df["n_cands"] = df.groupby("obvod")["ckand"].transform("count")
    return df


# Municipal elections as a second, local base (catches local/regional movements absent from Chamber elections).
# No look-ahead: Senate 2020/2022 -> KV2018, Senate 2024/2026 -> KV2022.
MUNICIPAL = {
    2018: dict(t3="kv2018/KV2018_data_20230224_csv/csv_od/kvt3.csv", hl="kv2018/KV2018_data_20230224_csv/csv_od/kvhl.csv",
               ros="kv2018/KV2018_reg_20230224_csv/csv_od/kvros.csv", slozeni="kv2018/KV2018_cisel_20230224_csv/csv_od/cvs_slozeni.csv"),
    2022: dict(t3="kv2022/KV2022_data_20260328_csv/csv_od/kvt3.csv", hl="kv2022/KV2022_data_20260328_csv/csv_od/kvhl.csv",
               ros="kv2022/KV2022reg20260328_csv/csv_od/kvros.csv", slozeni="kv2022/KV2022ciselniky20260328_csv/csv_od/cvs_slozeni.csv"),
}
MUNI_FOR = {2020: 2018, 2022: 2018, 2024: 2022, 2026: 2022}
# Established national parties whose municipal strength must not count as "local movement" strength
# (e.g. ČSSD/SOCDEM 2022 municipal results vs. its 2025 national collapse; KSČM ran inside Stačilo! in 2025).
NATIONAL_PARTIES = {7, 47}
GENERIC_LOCAL = {80, 90, 99}   # NK / SNK / BEZPP: generic independents, not matchable to Senate nominators


def municipal_shares(kv: int, senate_year: int) -> dict[tuple[int, int], float]:
    """(obvod, party) -> ballot-weighted municipal vote share (lowest council level: MČ if present)."""
    cfg = MUNICIPAL[kv]
    members: dict[int, set[int]] = defaultdict(set)
    for r in read(cfg["slozeni"]):
        members[int(r["VSTRANA"])].add(int(r["NSTRANA"]))
    lists: dict[tuple[str, str, str], int] = {}
    for r in read(cfg["ros"]):
        lists[(r["KODZASTUP"], r["COBVODU"], r["POR_STR_HL"])] = int(r["VSTRANA"])
    t3 = {(r["ID_OKRSKY"], r["TYPZASTUP"]): r for r in read(cfg["t3"])}
    # prefer the borough council (TYPZASTUP 2) over the city council where both exist
    has_mc = {(r["OBEC"], r["OKRSEK"]) for r in t3.values() if r["TYPZASTUP"] == "2"}
    mapper = precinct_mapper(senate_year)
    num_ = defaultdict(float)
    den_ = defaultdict(float)
    for (idk, typ), tr in t3.items():
        if typ == "1" and (tr["OBEC"], tr["OKRSEK"]) in has_mc:
            continue
        ob = mapper(int(tr["OBEC"]), int(tr["OKRSEK"]))
        if ob is not None and num(tr["PL_HL_CELK"]) > 0:
            den_[ob] += num(tr["ODEVZ_OBAL"])
    for r in read(cfg["hl"]):
        tr = t3.get((r["ID_OKRSKY"], r["TYPZASTUP"]))
        if tr is None or (r["TYPZASTUP"] == "1" and (tr["OBEC"], tr["OKRSEK"]) in has_mc):
            continue
        ob = mapper(int(tr["OBEC"]), int(tr["OKRSEK"]))
        total = num(tr["PL_HL_CELK"])
        if ob is None or total <= 0:
            continue
        vs = lists.get((tr["KODZASTUP"], tr["COBVODU"], r["POR_STR_HL"]))
        if vs is None or vs in GENERIC_LOCAL:
            continue
        share = num(r["POC_HLASU"]) / total
        for p in (members.get(vs, set()) | {vs}) - GENERIC_LOCAL:
            num_[(ob, p)] += share * num(tr["ODEVZ_OBAL"])
    return {k: v / den_[k[0]] for k, v in num_.items() if den_[k[0]] > 0}


ELECTION_DATE = {2020: 20201002, 2022: 20220923, 2024: 20240920, 2026: 20261009}


def fold(x: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", x) if not unicodedata.combining(c)).lower().strip()


def key(first: str, surname: str) -> str:
    # first name + last surname word: survives name changes like "Šípová" -> "Sucharda Šípová"
    return fold(first) + "|" + fold(surname.split()[-1] if surname.split() else surname)


def senate_history() -> list[dict]:
    """All Senate elections incl. by-elections (ČSÚ senat_vse register)."""
    return read("vse/reg/csv_od/serk.csv")


def add_incumbency(df: pd.DataFrame, hist: list[dict]) -> pd.DataFrame:
    winners = []
    for r in hist:
        if str(r.get("ZVOLEN_K1")) in ("1",) or str(r.get("ZVOLEN_K2")) in ("1",):
            winners.append((int(r["DATUMVOLEB"]), int(r["OBVOD"]), key(r["JMENO"], r["PRIJMENI"])))
    inc, former = [], []
    for row in df.itertuples():
        first, *rest = row.name.split(" ")
        date, name = ELECTION_DATE[row.year], key(first, " ".join(rest))
        prev = [w for w in winners if w[1] == row.obvod and w[0] < date]
        last = max(prev)[2] if prev else None
        inc.append(int(last == name))
        former.append(int(any(w[2] == name and w[0] < date for w in winners) and last != name))
    df = df.copy()
    df["incumbent_text"] = df["incumbent"]
    df["incumbent"] = inc
    df["former_senator"] = former
    return df


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    all_shares, all_cands = [], []
    for year, cfg in SENATE.items():
        print(f"Senate {year}")
        sh = chamber_party_shares(cfg["chamber"], year)
        all_shares.append(sh)
        loc = municipal_shares(MUNI_FOR[year], year)
        c = add_incumbency(candidates(year, sh, loc), senate_history())
        up = sorted(c["obvod"].unique())
        print(f"  candidates {len(c)} in {len(up)} districts; base mean {c['base'].mean():.3f}; incumbents {c['incumbent'].sum()} (text {c['incumbent_text'].sum()}), former {c['former_senator'].sum()}; local_extra>0: {(c['local_extra']>0).sum()}")
        all_cands.append(c)
    pd.concat(all_shares).to_csv(OUT / "party_shares.csv", index=False)
    pd.concat(all_cands).to_csv(OUT / "candidates.csv", index=False)
    print("written", OUT)


if __name__ == "__main__":
    main()
