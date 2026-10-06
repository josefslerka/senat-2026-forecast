#!/usr/bin/env python3
"""Build the public Senát 2026 forecasting experiment site.

Reads blind forecasts from the vault notes (single source of truth), writes an
append-only daily snapshot JSON and a static bilingual (cs/en) HTML site.

Only public-safe fields are exported: candidate distributions, bands and short
texts from meta.py. No odds, no market fields, no bets, no raw run artifacts.

Usage: python3 site/senat2026/build.py --out ../senat-2026-forecast --date 2026-10-02 --stage blind
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[1]
sys.path.insert(0, str(VAULT / "scripts"))
sys.path.insert(0, str(HERE))

from forecast_math import read_distributions, read_frontmatter  # noqa: E402
from meta import DISTRICTS  # noqa: E402
# Display status from current meta (snapshots are immutable; wording fixes apply at render time).
STATUS = {m["n"]: m for m in DISTRICTS}


def status(d: dict, lang: str) -> str:
    return STATUS.get(d["n"], d)["status_" + lang]
from texts import JOURNAL, RULES, INTRO, MODEL_PAGE, CHANGES  # noqa: E402

FORECASTS = VAULT / "forecasts"


CSU = VAULT / "data" / "csu-senat-2026"
TITLE_TOKENS = {"MBA", "MHA", "MPH", "DBA", "PhD", "et", "CSc", "DSc"}


def fold(s: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower().replace(" ", "").replace("_", "").replace("-", "")


def is_title(tok: str) -> bool:
    return "." in tok or "," in tok or tok in TITLE_TOKENS


def official_ballot(n: int) -> list[dict]:
    """Official ČSÚ candidate list (jmsez) with parsed names and party codes."""
    cvs = {x[0]: x for x in json.loads((CSU / "cvs.json").read_text())["strany"]}
    out = []
    for e in json.loads((CSU / f"jmsez-{n}.json").read_text())["platni"]:
        toks = [t for t in e[3].split() if t]
        names = [t for t in toks if not is_title(t)]
        out.append({"raw": e[3], "tokens": names, "ballot_no": e[2], "age": e[4],
                    "list": e[5], "nominated_by": cvs.get(e[17], [None, e[6]])[1],
                    "member": cvs.get(e[18], [None, e[7]])[1], "occupation": e[8]})
    return out


def match_key(key: str, ballot: list[dict]) -> dict | None:
    kf = fold(key)
    initial = None
    if "_" in key and len(key.split("_")[0]) == 1:
        initial, kf = key[0].lower(), fold(key.split("_", 1)[1])
    for b in ballot:
        t = b["tokens"]
        for k in (2, 1):
            if len(t) <= k:
                continue
            sur = t[:k]
            if fold("".join(sur)) == kf or (k == 2 and fold(sur[1]) == kf):
                given = t[k:]
                if initial and not fold(given[0]).startswith(initial):
                    continue
                return {**b, "display": " ".join(given + sur)}
    return None


def read_bands(path: Path, key: str) -> dict[str, tuple[float, float]]:
    text = path.read_text(encoding="utf-8")
    fm = text[4 : text.find("\n---", 4)]
    out: dict[str, tuple[float, float]] = {}
    inside = False
    for line in fm.splitlines():
        if not line[:1].isspace():
            inside = line.startswith(f"{key}:")
            continue
        if inside:
            m = re.match(r"\s+([^:]+):\s*\{\s*low:\s*([\d.]+),\s*high:\s*([\d.]+)\s*\}", line)
            if m:
                out[m.group(1).strip().strip("\"'")] = (float(m.group(2)), float(m.group(3)))
    return out


def series_note(d: dict, kind: str = "ai", max_date: str | None = None) -> Path:
    """Latest note of the district's AI series (kind='ai') or AI-with-model series (kind='aimodel')."""
    base = read_frontmatter(FORECASTS / d["note"]).get("forecast_series_id")
    want = base if kind == "ai" else f"{base}-aimodel"
    best = None
    for p in FORECASTS.glob("*.md"):
        if max_date and p.name[:10] > max_date:
            continue
        fm = read_frontmatter(p)
        if fm.get("forecast_series_id") == want:
            key = (int(fm.get("forecast_version") or 1), p.name)
            if best is None or key > best[0]:
                best = (key, p)
    if best is None:
        if kind == "ai":
            return FORECASTS / d["note"]
        raise SystemExit(f"no {kind} note for series {want}")
    return best[1]


def snapshot(stage: str, date: str, kind: str = "ai", max_date: str | None = None) -> dict:
    districts = []
    for d in DISTRICTS:
        path = FORECASTS / d["note"] if kind == "day1" else series_note(d, kind, max_date)
        fm = read_frontmatter(path)
        dists = read_distributions(path)
        dist = dists[f"{stage}_distribution"]
        bands = read_bands(path, f"{stage}_distribution_bands")
        total = sum(dist.values())
        if abs(total - 1) > 0.005:
            raise SystemExit(f"{path.name}: {stage} distribution sums to {total}")
        ballot = official_ballot(d["n"])
        rows, matched = [], set()
        for key, p in sorted(dist.items(), key=lambda kv: (kv[0] == "Someone_else", -kv[1])):
            if key == "Someone_else":
                disp, party = "Ostatní", ""
            else:
                b = match_key(key, ballot)
                if b is None:
                    raise SystemExit(f"{d['n']}: key {key} not found on official ČSÚ ballot")
                matched.add(b["raw"])
                disp = b["display"]
                party = b["list"] if b["list"] == b["nominated_by"] else f"{b['list']} (navrhl/a {b['nominated_by']})"
            rows.append({"key": key, "name": disp, "party": party, "p": round(p, 4),
                         "band": list(bands[key]) if key in bands else None})
        others = [" ".join(b["tokens"][1:] + b["tokens"][:1]) + f" ({b['list']})" for b in ballot if b["raw"] not in matched]
        leader = max(rows, key=lambda r: r["p"])
        lo, hi = fm.get(f"{stage}_band_low") or fm.get("blind_band_low"), fm.get(f"{stage}_band_high") or fm.get("blind_band_high")
        districts.append({
            "n": d["n"], "name": d["name"], "series": fm.get("forecast_series_id") or fm.get("slug"),
            "version": fm.get("forecast_version", 1), "stage": stage,
            "leader": leader["key"], "leader_p": leader["p"],
            "leader_band": [lo, hi] if lo is not None else leader["band"],
            "candidates": rows, "others_on_ballot": others, "ballot_size": len(ballot),
            "status_cs": d["status_cs"], "status_en": d["status_en"],
            "why_cs": d["why_cs"], "why_en": d["why_en"],
            "watch_cs": d["watch_cs"], "watch_en": d["watch_en"],
            "redteam": fm.get("reconciliation_mode"),
            "grounding": fm.get("grounding_check_status"),
            "contamination_risk": fm.get("contamination_risk") or "none",
            "research_limitation": fm.get("research_limitation"),
            "independent_redteam_posthoc": bool(fm.get("independent_redteam_posthoc")),
            "note": path.name, "created": str(fm.get("created")),
        })
    return {"experiment": "senat-2026", "date": date, "stage": stage, "series": kind,
            "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "districts": sorted(districts, key=lambda x: x["n"])}


MODEL_JSON = VAULT / "data" / "senat-model" / "model_2026.json"


def model_snapshot(date: str) -> dict:
    m = json.loads(MODEL_JSON.read_text())
    out = []
    for d in m["prediction"]:
        ballot = {" ".join(b["tokens"][1:] + b["tokens"][:1]): b for b in official_ballot(d["obvod"])}
        cands = []
        for c in sorted(d["candidates"], key=lambda c: -c["p_win"]):
            cands.append(dict(name=c["name"], list=c["list"], p=c["p_win"], r1_mean=c["r1_mean"],
                              r1_p10=c["r1_p10"], r1_p90=c["r1_p90"], p_advance=c["p_advance"],
                              base=c["base"], local=c["local_extra"]))
        out.append(dict(n=d["obvod"], leader=cands[0]["name"], leader_p=cands[0]["p"], candidates=cands))
    return {"experiment": "senat-2026", "series": "statistical-model", "date": date,
            "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "validation": m.get("validation"), "coefficients": m.get("coefficients"),
            "districts": sorted(out, key=lambda x: x["n"])}


def write_snapshot(out: Path, name: str, snap: dict) -> dict:
    sdir = out / "data" / "snapshots"
    sdir.mkdir(parents=True, exist_ok=True)
    target = sdir / name
    if target.exists():
        old = json.loads(target.read_text())
        if old["districts"] != snap["districts"]:
            raise SystemExit(f"{name} exists with different content — snapshots are append-only")
        return old
    target.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return snap


# ── HTML ────────────────────────────────────────────────────────────────────

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1d1b;--muted:#6b6a64;--line:#e4e1d8;--card:#fff;--accent:#2f5d8a;--bar:#2f5d8a;--bar2:#c9d6e3;--warn:#9a5b00}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#151514;--fg:#ecebe6;--muted:#a3a19a;--line:#2e2d2a;--card:#1d1d1b;--accent:#8fb4dc;--bar:#8fb4dc;--bar2:#33424f;--warn:#e0a24a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:24px 16px 64px}
header{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:24px}
header a.brand{font-weight:700;color:var(--fg);text-decoration:none;font-size:18px}
nav a{margin-left:14px;color:var(--accent);text-decoration:none;font-size:15px}nav a.lang{border:1px solid var(--line);padding:2px 8px;border-radius:6px}
h1{font-size:28px;line-height:1.2;margin:8px 0 8px}h2{font-size:20px;margin:32px 0 10px}
p.lead{color:var(--muted);margin-top:0}a{color:var(--accent)}
table{width:100%;border-collapse:collapse;font-size:15px}th,td{text-align:left;padding:8px 6px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;color:var(--muted);font-size:13px;text-transform:uppercase;letter-spacing:.03em}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.bar{display:flex;height:10px;border-radius:5px;overflow:hidden;background:var(--bar2);min-width:120px}
.bar span{display:block;height:100%}
.pill{display:inline-block;font-size:12px;padding:1px 7px;border-radius:10px;border:1px solid var(--line);color:var(--muted);white-space:nowrap}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:16px 0}
.muted{color:var(--muted)}.warn{color:var(--warn)}
.scroll{overflow-x:auto}
footer{margin-top:48px;padding-top:12px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
@media (max-width:640px){.hide-sm{display:none}h1{font-size:23px}}
@media (max-width:640px){table.cards thead{display:none}table.cards,table.cards tbody,table.cards tr,table.cards td{display:block;width:auto}
table.cards tr{border:1px solid var(--line);border-radius:10px;padding:8px 12px;margin:10px 0;background:var(--card)}
table.cards td{border:0;padding:3px 0;display:flex;justify-content:space-between;gap:12px;text-align:right}
table.cards td::before{content:attr(data-label);color:var(--muted);text-align:left}
table.cards td.head{font-weight:600;font-size:17px}table.cards td.head::before{content:none}
table.cards td.nolabel{display:none}.sm-only{display:inline!important}}
.sm-only{display:none}
table.cards td b{white-space:nowrap}table.cards .pill{white-space:normal}
"""

PALETTE = ["#2f5d8a", "#c0703a", "#5b8a3c", "#8a4f7d", "#a8a39a", "#6a8fb0", "#b79b4e"]

L = {
    "cs": dict(title="Senát 2026 — veřejný experiment s AI forecastingem", home="Přehled", rules="Pravidla",
               journal="Deník", archive="Archiv", other="EN", district="Obvod", fav="Favorit",
               p="P(výhra)", band="Pásmo", dist="Rozdělení", status="Stav", cand="Kandidát",
               party="Strana / podpora", why="Proč", watch="Na co se dívat", meta="Technické údaje",
               stage="Fáze", blind="blind (bez kurzů)", final="final (po zohlednění trhu)",
               snapshot="Snapshot", others="Ostatní", back="← zpět na přehled",
               limits="Omezení běhu", rt="Red-team", gr="Grounding", cont="Riziko kontaminace kurzy",
               rl="Omezení researche", model="Model", ai="AI agent (blind)", stat="Statistický model", r1="Podíl v 1. kole (model, 80% interval)", adv="P(postup / výhra v 1. kole)", inothers="v „ostatních“", modelnote="Model nezná kandidáty bez stranické i komunální základny (nová hnutí, osobní značka) — tam ho podceňuje.", otherslist="Ostatní kandidáti na lístku", ballotsrc="Kandidáti a volební strany podle oficiálního seznamu ČSÚ (volby.gov.cz).", posthoc="dodatečný nezávislý red-team", updated="Stav k",
               foot="Predikce generuje AI pipeline (Claude) s člověkem ve smyčce. Nejde o sázkové tipy. Obsah CC BY 4.0, kód MIT."),
    "en": dict(title="Czech Senate 2026 — a public AI forecasting experiment", home="Overview", rules="Rules",
               journal="Journal", archive="Archive", other="CS", district="District", fav="Favourite",
               p="P(win)", band="Band", dist="Distribution", status="Status", cand="Candidate",
               party="Party / backing", why="Why", watch="What to watch", meta="Technical details",
               stage="Stage", blind="blind (no odds)", final="final (market-aware)",
               snapshot="Snapshot", others="Others", back="← back to overview",
               limits="Run limitations", rt="Red-team", gr="Grounding", cont="Odds contamination risk",
               rl="Research limitation", model="Model", ai="AI agent (blind)", stat="Statistical model", r1="Round-1 share (model, 80% interval)", adv="P(advance / win round 1)", inothers="in “others”", modelnote="The model cannot see candidates with neither party nor municipal base (new movements, personal brand) — it underrates them.", otherslist="Other candidates on the ballot", ballotsrc="Candidates and lists per the official ČSÚ register (volby.gov.cz).", posthoc="post-hoc independent red-team", updated="As of",
               foot="Forecasts are produced by an AI pipeline (Claude) with a human in the loop. Not betting tips. Content CC BY 4.0, code MIT."),
}


def esc(s) -> str:
    return html.escape(str(s)) if s is not None else ""


def pct(p: float) -> str:
    v = p * 100
    return f"{v:.0f} %" if v >= 1 or v == 0 else f"{v:.1f} %"


def path_for(lang: str, page: str) -> str:
    return page if lang == "cs" else f"en/{page}"


def rel(lang: str, page: str) -> str:
    # pages live at root (cs) or en/ (en); links are relative to the current page's dir
    return page


def other_lang_link(lang: str, page: str) -> str:
    return f"en/{page}" if lang == "cs" else f"../{page}"


def layout(lang: str, page: str, title: str, body: str) -> str:
    t = L[lang]
    prefix = "" if lang == "cs" else ""
    nav = (f'<a href="index.html">{t["home"]}</a><a href="pravidla.html">{t["rules"]}</a>'
           f'<a href="model.html">{t["model"]}</a><a href="denik.html">{t["journal"]}</a><a href="archiv.html">{t["archive"]}</a>'
           f'<a class="lang" href="{other_lang_link(lang, page)}">{t["other"]}</a>')
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(L[lang]['title'])}">
<style>{CSS}</style></head><body><div class="wrap">
<header><a class="brand" href="index.html">Senát 2026 · forecast</a><nav>{prefix}{nav}</nav></header>
{body}
<footer>{esc(t['foot'])} · <a href="https://github.com/josefslerka/senat-2026-forecast">GitHub</a></footer>
</div></body></html>"""


def bar(cands: list[dict]) -> str:
    segs = "".join(
        f'<span title="{esc(c["name"])} {pct(c["p"])}" style="width:{c["p"]*100:.2f}%;background:{PALETTE[i % len(PALETTE)]}"></span>'
        for i, c in enumerate(cands))
    return f'<div class="bar">{segs}</div>'


def overview(lang: str, snap: dict, msnap: dict | None = None) -> str:
    t = L[lang]
    rows = []
    mby = {d["n"]: d for d in (msnap or {}).get("districts", [])}
    for d in snap["districts"]:
        md = mby.get(d["n"])
        mcell = (f'<td>{esc(md["leader"])}</td><td class="num"><b>{pct(md["leader_p"])}</b></td>') if md else '<td>—</td><td>—</td>'
        lead = next(c for c in d["candidates"] if c["key"] == d["leader"])
        b = d["leader_band"]
        band = f"{b[0]*100:.0f}–{b[1]*100:.0f} %" if b and None not in b else "—"
        rows.append(
            f'<tr><td class="num">{d["n"]}</td><td><a href="obvod-{d["n"]:02d}.html">{esc(d["name"])}</a></td>'
            f'<td>{esc(lead["name"])}<div class="muted" style="font-size:13px">{esc(lead["party"])}</div></td>'
            f'<td class="num"><b>{pct(d["leader_p"])}</b></td><td class="num hide-sm">{band}</td>'
            f'<td class="hide-sm">{bar(d["candidates"])}</td>' + mcell + f'<td class="hide-sm"><span class="pill">{esc(status(d, lang))}</span></td></tr>')
    intro = INTRO[lang]
    return layout(lang, "index.html", t["title"], f"""
<h1>{esc(t['title'])}</h1><p class="lead">{intro['lead']}</p>
<div class="card">{intro['body']}</div>
<h2>{t['ai']}: {esc(snap['date'])} · {t['stat']}: {esc((msnap or {}).get('date', '—'))}</h2>
<div class="scroll"><table><thead><tr><th>#</th><th>{t['district']}</th><th>{t['fav']} · {t['ai']}</th><th>{t['p']}</th>
<th class="hide-sm">{t['band']}</th><th class="hide-sm">{t['dist']}</th><th>{t['fav']} · {t['stat']}</th><th>{t['p']}</th><th class="hide-sm">{t['status']}</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>""")


def band_str(b) -> str:
    return f"{b[0] * 100:.0f}–{b[1] * 100:.0f} %" if b else "—"


def model_table(lang: str, d: dict, md: dict | None) -> str:
    if not md:
        return ""
    t = L[lang]
    ai = {c["name"]: c["p"] for c in d["candidates"] if c["key"] != "Someone_else"}
    ai_other = next((c["p"] for c in d["candidates"] if c["key"] == "Someone_else"), 0.0)
    rows = "".join(
        f'<tr><td>{esc(c["name"])}</td><td class="muted">{esc(c["list"])}</td>'
        f'<td class="num">{pct(ai[c["name"]]) if c["name"] in ai else t["inothers"]}</td>'
        f'<td class="num"><b>{pct(c["p"])}</b></td><td class="num">{c["r1_mean"]:.0f} % ({c["r1_p10"]:.0f}–{c["r1_p90"]:.0f})</td>'
        f'<td class="num">{pct(c["p_advance"])}</td></tr>' for c in md["candidates"])
    return f"""<h2>{t['ai']} vs. {t['stat']}</h2>
<div class="scroll"><table><thead><tr><th>{t['cand']}</th><th>{t['party']}</th><th>{t['ai']}</th><th>{t['stat']}</th><th>{t['r1']}</th><th>{t['adv']}</th></tr></thead>
<tbody>{rows}</tbody></table></div><p class="muted" style="font-size:14px">{t['ai']} — {t['others']}: {pct(ai_other)}. {t['modelnote']} <a href="model.html">{t['model']} →</a></p>"""


def district_page(lang: str, d: dict, snap: dict, md: dict | None = None) -> str:
    t = L[lang]
    rows = "".join(
        f'<tr><td>{esc(c["name"] if c["key"] != "Someone_else" else t["others"])}</td><td class="muted">{esc(c["party"])}</td>'
        f'<td class="num"><b>{pct(c["p"])}</b></td><td class="num">{band_str(c["band"])}</td></tr>'
        for c in d["candidates"])
    lim = []
    if d["research_limitation"]:
        lim.append(f'<li>{t["rl"]}: <code>{esc(d["research_limitation"])}</code></li>')
    lim.append(f'<li>{t["cont"]}: <code>{esc(d["contamination_risk"])}</code></li>')
    lim.append(f'<li>{t["rt"]}: <code>{esc(d["redteam"])}</code>{" · " + t["posthoc"] if d["independent_redteam_posthoc"] else ""}</li>')
    lim.append(f'<li>{t["gr"]}: <code>{esc(d["grounding"])}</code></li>')
    title = f"{t['district']} {d['n']} — {d['name']}"
    return layout(lang, f"obvod-{d['n']:02d}.html", title, f"""
<p><a href="index.html">{t['back']}</a></p>
<h1>{esc(title)}</h1><p class="lead"><span class="pill">{esc(status(d, lang))}</span>
&nbsp;{t['updated']} {esc(snap['date'])} · {t['stage']}: {t[d['stage']]} · v{esc(d['version'])}</p>
{bar(d['candidates'])}
<div class="scroll"><table style="margin-top:12px"><thead><tr><th>{t['cand']}</th><th>{t['party']}</th><th>{t['p']}</th><th>{t['band']}</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="muted" style="font-size:14px">{t['otherslist']}: {esc(', '.join(d['others_on_ballot'])) or '—'}. {t['ballotsrc']}</p>
{model_table(lang, d, md)}
<h2>{t['why']}</h2><p>{esc(d['why_'+lang])}</p>
<h2>{t['watch']}</h2><p>{esc(d['watch_'+lang])}</p>
<h2>{t['limits']}</h2><ul class="muted">{''.join(lim)}</ul>""")


def simple_page(lang: str, page: str, title: str, html_body: str) -> str:
    return layout(lang, page, title, f"<h1>{esc(title)}</h1>{html_body}")


def archive_page(lang: str, out: Path) -> str:
    t = L[lang]
    snaps = sorted((out / "data" / "snapshots").glob("*.json"))
    items = "".join(
        f'<li><a href="{"" if lang=="cs" else "../"}data/snapshots/{s.name}"><code>{s.name}</code></a></li>' for s in snaps)
    txt = ("Každý den se ukládá neměnný snapshot všech predikcí ve formátu JSON. Starší snapshoty se nikdy nepřepisují; "
           "úplnou historii změn ukazuje i git historie repozitáře.") if lang == "cs" else (
           "Every day an immutable JSON snapshot of all forecasts is stored. Older snapshots are never overwritten; "
           "the repository's git history shows every change.")
    return simple_page(lang, "archiv.html", t["archive"], f"<p>{txt}</p><ul>{items}</ul>")


def build(out: Path, date: str, stage: str, model_date: str | None = None) -> None:
    existing = out / "data" / "snapshots" / f"{date}-{stage}.json"
    snap = json.loads(existing.read_text()) if existing.exists() else write_snapshot(out, f"{date}-{stage}.json", snapshot(stage, date))
    msnap = write_snapshot(out, f"{model_date}-model.json", model_snapshot(model_date)) if model_date else None
    latest = {"ai": snap, "model": msnap}
    (out / "data" / "latest.json").write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mby = {d["n"]: d for d in (msnap or {}).get("districts", [])}
    for lang in ("cs", "en"):
        base = out if lang == "cs" else out / "en"
        base.mkdir(parents=True, exist_ok=True)
        (base / "index.html").write_text(overview(lang, snap, msnap), encoding="utf-8")
        for d in snap["districts"]:
            (base / f"obvod-{d['n']:02d}.html").write_text(district_page(lang, d, snap, mby.get(d["n"])), encoding="utf-8")
        (base / "pravidla.html").write_text(simple_page(lang, "pravidla.html", L[lang]["rules"], RULES[lang]), encoding="utf-8")
        if msnap:
            (base / "model.html").write_text(simple_page(lang, "model.html", L[lang]["stat"], MODEL_PAGE[lang](msnap)), encoding="utf-8")
        journal = "".join(f'<div class="card"><h2 style="margin-top:0">{esc(e["date"])} — {esc(e["title_"+lang])}</h2>{e[lang]}</div>'
                          for e in sorted(JOURNAL, key=lambda e: e["date"], reverse=True))
        (base / "denik.html").write_text(simple_page(lang, "denik.html", L[lang]["journal"], journal), encoding="utf-8")
        (base / "archiv.html").write_text(archive_page(lang, out), encoding="utf-8")
    (out / ".nojekyll").write_text("")
    print(f"Built {len(snap['districts'])} districts, AI {stage} {date}, model {model_date} → {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--stage", default="blind", choices=["blind", "final"])
    ap.add_argument("--model-date")
    a = ap.parse_args()
    build(Path(a.out).resolve(), a.date, a.stage, a.model_date)


# ── Five-series build (from 2026-10-05): AI · Model · AI s modelem · Sázky · Blend ───────────
SERIES_LABELS = {
    "cs": dict(ai="AI", model="Statistický model", aimodel="AI s modelem", market="Sázky", blend="Blend", ai0="AI 2. 10."),
    "en": dict(ai="AI", model="Statistical model", aimodel="AI + model", market="Betting", blend="Blend", ai0="AI 2 Oct"),
}
MARKET_DIR = VAULT / "data" / "senat-market"


def keyed_model(md: dict, keys: list[str], names: dict[str, str]) -> dict[str, float]:
    """Map model candidates (by display name) onto AI ASCII keys; the rest -> Someone_else."""
    out = {k: 0.0 for k in keys}
    inv = {v: k for k, v in names.items()}
    for c in md["candidates"]:
        k = inv.get(c["name"], "Someone_else")
        out[k if k in out else "Someone_else"] = out.get(k if k in out else "Someone_else", 0.0) + c["p"]
    return out


def dist_of(snap_d: dict) -> dict[str, float]:
    if "candidates" not in snap_d:  # market snapshots store the de-vigged consensus as a dict
        return dict(snap_d.get("consensus") or {})
    return {c["key"]: c["p"] for c in snap_d["candidates"]}


def leader_cell(dist: dict[str, float] | None, names: dict[str, str], hide: bool = False, label: str = "") -> str:
    cls = (' class="hide-sm"' if hide else "") + (f' data-label="{esc(label)}"' if label else "")
    if not dist:
        return f"<td{cls}>—</td>"
    k = max(dist, key=dist.get)
    nm = names.get(k, k)
    return f'<td{cls}><span>{esc(nm.split()[-1] if k != "Someone_else" else "Ostatní")} <b>{pct(dist[k])}</b></span></td>'


def prev_snapshot(snaps: Path, series: str, date: str) -> dict | None:
    """Latest snapshot of the same series strictly before `date` (AI falls back to the 2. 10. blind)."""
    pats = [f"*-{series}.json"] + (["*-blind.json"] if series == "ai" else [])
    files = sorted(f for pat in pats for f in snaps.glob(pat) if f.name[:10] < date)
    return json.loads(files[-1].read_text()) if files else None


def changes_html(lang: str, cur: dict[str, dict | None], prev: dict[str, dict | None],
                 names_by_n: dict[int, dict[str, str]], labels: dict[str, str], min_pp: float = 5.0,
                 kept: dict[str, str] | None = None) -> str:
    """Per series: districts where the favourite flipped or any candidate moved >= min_pp."""
    items = []
    for key, snap in cur.items():
        if not snap:
            continue
        if kept and key in kept:  # series not re-run today
            items.append(f"<li><b>{esc(labels[key])}</b>: " + (f"beze změny (stav k {kept[key]})" if lang == "cs"
                         else f"unchanged (as of {kept[key]})") + "</li>")
            continue
        old = prev.get(key)
        if not old:
            items.append(f"<li><b>{esc(labels[key])}</b>: " + ("nová série" if lang == "cs" else "new series") + "</li>")
            continue
        P = {d["n"]: dist_of(d) for d in old["districts"]}
        moves = []
        for d in snap["districts"]:
            n, a = d["n"], dist_of(d)
            b = P.get(n)
            if not a or not b:
                continue
            nm = lambda k: (names_by_n.get(n, {}).get(k, k).split()[-1] if k != "Someone_else" else ("ostatní" if lang == "cs" else "others"))  # noqa: E731
            la, lb = max(a, key=a.get), max(b, key=b.get)
            big = max(a, key=lambda k: abs(a[k] - b.get(k, 0)))
            dpp = (a[big] - b.get(big, 0)) * 100
            if la != lb:
                moves.append(f"{n}: {esc(nm(lb))} → <b>{esc(nm(la))}</b> {pct(a[la])}")
            elif abs(dpp) >= min_pp:
                moves.append(f"{n}: {esc(nm(big))} {pct(b.get(big, 0))} → {pct(a[big])}")
        none = "beze změny nad 5 p.b." if lang == "cs" else "no change above 5 pp"
        items.append(f"<li><b>{esc(labels[key])}</b>: " + ("; ".join(moves) if moves else none) + "</li>")
    return "<ul>" + "".join(items) + "</ul>"


def build_five(out: Path, date: str, model_date: str, ai0_date: str = "2026-10-02",
               market_date: str | None = None, rho: float = 0.55) -> None:
    sys.path.insert(0, str(VAULT / "scripts"))
    from forecast_math import blend_dist  # noqa: E402
    snaps = out / "data" / "snapshots"
    ai0 = json.loads((snaps / f"{ai0_date}-blind.json").read_text())
    msnap = json.loads((snaps / f"{model_date}-model.json").read_text())
    def locked(name: str, make):  # existing snapshots are immutable: load, never regenerate
        f = snaps / name
        return json.loads(f.read_text()) if f.exists() else write_snapshot(out, name, make())
    ai = locked(f"{date}-ai.json", lambda: snapshot("blind", date, "ai", max_date=date))
    aim = locked(f"{date}-aimodel.json", lambda: snapshot("blind", date, "aimodel", max_date=date))
    market = blend = None
    if market_date:
        mk = json.loads((MARKET_DIR / f"{market_date}.json").read_text())
        market = write_snapshot(out, f"{market_date}-market.json", mk)
        bl = {"experiment": "senat-2026", "series": "blend", "date": market_date, "rho": rho,
              "method": "log-odds pool of AI s modelem and de-vigged market, w_blind=(1-rho)/(2-rho)", "districts": []}
        mby = {d["n"]: d for d in mk["districts"]}
        for d in aim["districts"]:
            m = mby.get(d["n"])
            if not m or not m.get("consensus"):
                continue
            fin = blend_dist(dist_of(d), m["consensus"], rho)
            bl["districts"].append({"n": d["n"], "candidates": [{"key": k, "p": round(v, 4)} for k, v in fin.items()]})
        blend = write_snapshot(out, f"{market_date}-blend.json", bl)
    latest = {"ai": ai, "model": msnap, "aimodel": aim, "market": market, "blend": blend, "ai_2026-10-02": ai0}
    (out / "data" / "latest.json").write_text(json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    by = lambda snap: {d["n"]: d for d in (snap or {}).get("districts", [])}  # noqa: E731
    AI0, AI, AIM, MD, MK, BL = by(ai0), by(ai), by(aim), by(msnap), by(market), by(blend)

    cur_series = {"ai": ai, "model": msnap, "aimodel": aim, "market": market, "blend": blend}
    prev_series = {"ai": prev_snapshot(snaps, "ai", date), "model": prev_snapshot(snaps, "model", model_date),
                   "aimodel": prev_snapshot(snaps, "aimodel", date),
                   "market": prev_snapshot(snaps, "market", market_date or date),
                   "blend": prev_snapshot(snaps, "blend", market_date or date)}
    names_by_n = {d["n"]: {c["key"]: c["name"] for c in d["candidates"]} for d in ai["districts"]}
    for lang in ("cs", "en"):
        t, S = L[lang], SERIES_LABELS[lang]
        base = out if lang == "cs" else out / "en"
        rows = []
        for d in ai["districts"]:
            n = d["n"]
            names = {c["key"]: c["name"] for c in d["candidates"]}
            keys = list(names)
            md = keyed_model(MD[n], keys, names) if n in MD else None
            mk = (MK.get(n) or {}).get("consensus")
            rows.append(f'<tr><td class="num nolabel">{n}</td><td class="head"><a href="obvod-{n:02d}.html"><span class="sm-only">{n} · </span>{esc(d["name"])}</a></td>'
                        + leader_cell(dist_of(d), names, label=S["ai"]) + leader_cell(md, names, label=S["model"])
                        + leader_cell(dist_of(AIM[n]) if n in AIM else None, names, label=S["aimodel"])
                        + leader_cell(mk, names, label=S["market"]) + leader_cell(dist_of(BL[n]) if n in BL else None, names, label=S["blend"])
                        + f'<td data-label="{esc(t["status"])}"><span class="pill">{esc(status(d, lang))}</span></td></tr>')
            # district page
            def col(dist):  # noqa: E306
                return lambda k: (pct(dist[k]) if dist and dist.get(k) is not None else "—")
            cols = [(S["ai0"], col(dist_of(AI0[n]) if n in AI0 else None)), (S["ai"], col(dist_of(d))),
                    (S["model"], col(md)), (S["aimodel"], col(dist_of(AIM[n]) if n in AIM else None)),
                    (S["market"], col(mk)), (S["blend"], col(dist_of(BL[n]) if n in BL else None))]
            head = "".join(f"<th>{esc(h)}</th>" for h, _ in cols)
            body = "".join(f'<tr><td>{esc(names[k] if k != "Someone_else" else t["others"])}</td>'
                           + "".join(f'<td class="num">{f(k)}</td>' for _, f in cols) + "</tr>" for k in keys)
            comp = (f'<h2>{esc(S["ai"])} · {esc(S["model"])} · {esc(S["aimodel"])} · {esc(S["market"])} · {esc(S["blend"])}</h2>'
                    f'<div class="scroll"><table><thead><tr><th>{t["cand"]}</th>{head}</tr></thead><tbody>{body}</tbody></table></div>')
            mnote = (MK.get(n) or {}).get("note_" + lang) or (MK.get(n) or {}).get("note", "")
            if mnote:
                comp += f'<p class="muted" style="font-size:14px">{esc(S["market"])}: {esc(mnote)}</p>'
            page = district_page(lang, d, ai, MD.get(n))
            page = page.replace(f"<h2>{t['why']}</h2>", comp + f"<h2>{t['why']}</h2>", 1)
            (base / f"obvod-{n:02d}.html").write_text(page, encoding="utf-8")
        intro = INTRO[lang]
        ov = layout(lang, "index.html", t["title"], f"""
<h1>{esc(t['title'])}</h1><p class="lead">{intro['lead']}</p>
<div class="card" style="border-left:4px solid var(--accent, #3b5b8c)"><h2 style="margin-top:0">{"Co je dnes nového" if lang == "cs" else "What's new today"} ({esc(date)})</h2>
{CHANGES.get(date, {}).get(lang, "")}
<p class="muted" style="font-size:14px;margin-bottom:0">{"Posuny oproti předchozímu snapshotu každé série (změna favorita nebo ≥ 5 p.b.):" if lang == "cs" else "Moves vs. each series' previous snapshot (favourite change or ≥ 5 pp):"}</p>
{changes_html(lang, cur_series, prev_series, names_by_n, S, kept={'model': model_date} if model_date < date else None)}
<p style="margin-bottom:0"><a href="denik.html">{"Podrobně v deníku →" if lang == "cs" else "Details in the journal →"}</a></p></div>
<div class="card">{intro['body']}</div>
<h2>{t['updated']} {esc(date)}</h2>
<div class="scroll"><table class="cards"><thead><tr><th>#</th><th>{t['district']}</th><th>{S['ai']}</th><th>{S['model']}</th>
<th>{S['aimodel']}</th><th>{S['market']}</th><th>{S['blend']}</th><th>{t['status']}</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>""")
        (base / "index.html").write_text(ov, encoding="utf-8")
        (base / "pravidla.html").write_text(simple_page(lang, "pravidla.html", L[lang]["rules"], RULES[lang]), encoding="utf-8")
        (base / "model.html").write_text(simple_page(lang, "model.html", L[lang]["stat"], MODEL_PAGE[lang](msnap)), encoding="utf-8")
        journal = "".join(f'<div class="card"><h2 style="margin-top:0">{esc(e["date"])} — {esc(e["title_"+lang])}</h2>{e[lang]}</div>'
                          for e in sorted(JOURNAL, key=lambda e: e["date"], reverse=True))
        (base / "denik.html").write_text(simple_page(lang, "denik.html", L[lang]["journal"], journal), encoding="utf-8")
        (base / "archiv.html").write_text(archive_page(lang, out), encoding="utf-8")
    print(f"Built five-series site for {date} (market: {market_date}) → {out}")
