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
from texts import JOURNAL, RULES, INTRO  # noqa: E402

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


def snapshot(stage: str, date: str) -> dict:
    districts = []
    for d in DISTRICTS:
        path = FORECASTS / d["note"]
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
        })
    return {"experiment": "senat-2026", "date": date, "stage": stage,
            "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "districts": sorted(districts, key=lambda x: x["n"])}


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
               rl="Omezení researche", otherslist="Ostatní kandidáti na lístku", ballotsrc="Kandidáti a volební strany podle oficiálního seznamu ČSÚ (volby.gov.cz).", posthoc="dodatečný nezávislý red-team", updated="Stav k",
               foot="Predikce generuje AI pipeline (Claude) s člověkem ve smyčce. Nejde o sázkové tipy. Obsah CC BY 4.0, kód MIT."),
    "en": dict(title="Czech Senate 2026 — a public AI forecasting experiment", home="Overview", rules="Rules",
               journal="Journal", archive="Archive", other="CS", district="District", fav="Favourite",
               p="P(win)", band="Band", dist="Distribution", status="Status", cand="Candidate",
               party="Party / backing", why="Why", watch="What to watch", meta="Technical details",
               stage="Stage", blind="blind (no odds)", final="final (market-aware)",
               snapshot="Snapshot", others="Others", back="← back to overview",
               limits="Run limitations", rt="Red-team", gr="Grounding", cont="Odds contamination risk",
               rl="Research limitation", otherslist="Other candidates on the ballot", ballotsrc="Candidates and lists per the official ČSÚ register (volby.gov.cz).", posthoc="post-hoc independent red-team", updated="As of",
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
           f'<a href="denik.html">{t["journal"]}</a><a href="archiv.html">{t["archive"]}</a>'
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


def overview(lang: str, snap: dict) -> str:
    t = L[lang]
    rows = []
    for d in snap["districts"]:
        lead = next(c for c in d["candidates"] if c["key"] == d["leader"])
        b = d["leader_band"]
        band = f"{b[0]*100:.0f}–{b[1]*100:.0f} %" if b and None not in b else "—"
        rows.append(
            f'<tr><td class="num">{d["n"]}</td><td><a href="obvod-{d["n"]:02d}.html">{esc(d["name"])}</a></td>'
            f'<td>{esc(lead["name"])}<div class="muted" style="font-size:13px">{esc(lead["party"])}</div></td>'
            f'<td class="num"><b>{pct(d["leader_p"])}</b></td><td class="num hide-sm">{band}</td>'
            f'<td>{bar(d["candidates"])}</td><td class="hide-sm"><span class="pill">{esc(d["status_"+lang])}</span></td></tr>')
    intro = INTRO[lang]
    return layout(lang, "index.html", t["title"], f"""
<h1>{esc(t['title'])}</h1><p class="lead">{intro['lead']}</p>
<div class="card">{intro['body']}</div>
<h2>{t['updated']} {esc(snap['date'])} · {t['stage']}: {t[snap['stage']]}</h2>
<div class="scroll"><table><thead><tr><th>#</th><th>{t['district']}</th><th>{t['fav']}</th><th>{t['p']}</th>
<th class="hide-sm">{t['band']}</th><th>{t['dist']}</th><th class="hide-sm">{t['status']}</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>""")


def band_str(b) -> str:
    return f"{b[0] * 100:.0f}–{b[1] * 100:.0f} %" if b else "—"


def district_page(lang: str, d: dict, snap: dict) -> str:
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
<h1>{esc(title)}</h1><p class="lead"><span class="pill">{esc(d['status_'+lang])}</span>
&nbsp;{t['updated']} {esc(snap['date'])} · {t['stage']}: {t[d['stage']]} · v{esc(d['version'])}</p>
{bar(d['candidates'])}
<div class="scroll"><table style="margin-top:12px"><thead><tr><th>{t['cand']}</th><th>{t['party']}</th><th>{t['p']}</th><th>{t['band']}</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="muted" style="font-size:14px">{t['otherslist']}: {esc(', '.join(d['others_on_ballot'])) or '—'}. {t['ballotsrc']}</p>
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


def build(out: Path, date: str, stage: str) -> None:
    snap = snapshot(stage, date)
    sdir = out / "data" / "snapshots"
    sdir.mkdir(parents=True, exist_ok=True)
    target = sdir / f"{date}-{stage}.json"
    if target.exists():
        old = json.loads(target.read_text())
        if old["districts"] != snap["districts"]:
            raise SystemExit(f"{target.name} exists with different content — snapshots are append-only; use a new date/stage")
    else:
        target.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "data" / "latest.json").write_text(json.dumps(snap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for lang in ("cs", "en"):
        base = out if lang == "cs" else out / "en"
        base.mkdir(parents=True, exist_ok=True)
        (base / "index.html").write_text(overview(lang, snap), encoding="utf-8")
        for d in snap["districts"]:
            (base / f"obvod-{d['n']:02d}.html").write_text(district_page(lang, d, snap), encoding="utf-8")
        (base / "pravidla.html").write_text(simple_page(lang, "pravidla.html", L[lang]["rules"], RULES[lang]), encoding="utf-8")
        journal = "".join(f'<div class="card"><h2 style="margin-top:0">{esc(e["date"])} — {esc(e["title_"+lang])}</h2>{e[lang]}</div>'
                          for e in sorted(JOURNAL, key=lambda e: e["date"], reverse=True))
        (base / "denik.html").write_text(simple_page(lang, "denik.html", L[lang]["journal"], journal), encoding="utf-8")
        (base / "archiv.html").write_text(archive_page(lang, out), encoding="utf-8")
    (out / ".nojekyll").write_text("")
    print(f"Built {len(snap['districts'])} districts, stage={stage}, date={date} → {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--stage", default="blind", choices=["blind", "final"])
    a = ap.parse_args()
    build(Path(a.out).resolve(), a.date, a.stage)
