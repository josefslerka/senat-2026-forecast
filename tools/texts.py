# Long-form texts for the public Senát 2026 site (cs/en). HTML fragments.

INTRO = {
    "cs": dict(
        lead="Pravděpodobnostní předpověď všech 27 senátních obvodů, ve kterých se v roce 2026 volí. Zveřejňujeme ji den po dni: nejdřív bez kurzů, pak po zohlednění trhu, s každodenními updaty a nakonec s vyhodnocením.",
        body="""<p><b>Co je to za experiment.</b> Zkoušíme, jak dobrým forecasterem může být AI agent. Předpovědi vytváří vícekroková AI pipeline (Claude): upřesnění otázky, research, odhad, kontrola, že tvrzení stojí na zdrojích, a oponentura (red-team). Člověk ji řídí a kontroluje.</p>
<p><b>Proč „blind“.</b> První zveřejněné číslo vzniká <i>bez znalosti sázkových kurzů</i>. Kurzy přidáváme až v dalším kroku a zvlášť. Díky tomu půjde po volbách změřit, jestli model sám přidává informaci, nebo jen opakuje trh.</p>
<p><b>Termíny.</b> 1. kolo 9.–10. 10. 2026 (spolu s komunálními volbami), 2. kolo 16.–17. 10. 2026. Pravidla vyhodnocení jsou zveřejněná předem, viz <a href="pravidla.html">Pravidla</a>. Postup den po dni zachycuje <a href="denik.html">Deník</a>.</p>"""),
    "en": dict(
        lead="Probabilistic forecasts for all 27 Czech Senate districts up for election in 2026, published day by day: first without odds, then market-aware, with daily updates and a final evaluation.",
        body="""<p><b>What this is.</b> A test of how good a forecaster an AI agent can be. Forecasts come from a multi-stage AI pipeline (Claude): question normalization, research, forecast, a check that every claim rests on a source, and an adversarial red-team. A human runs and supervises it.</p>
<p><b>Why “blind”.</b> The first published number is made <i>without seeing betting odds</i>. Odds are added later, as a separate step. After the election this lets us measure whether the model adds information or just echoes the market.</p>
<p><b>Dates.</b> Round 1 on 9–10 Oct 2026 (together with municipal elections), runoff on 16–17 Oct 2026. Scoring rules are published in advance, see <a href="pravidla.html">Rules</a>. The <a href="denik.html">Journal</a> records the process day by day.</p>"""),
}

RULES = {
    "cs": """
<h2>Co předpovídáme</h2>
<p>V každém z 27 obvodů: kdo bude zvolen senátorem, ať už nadpoloviční většinou v 1. kole, nebo vítězstvím ve 2. kole. Každý obvod má rozdělení pravděpodobností přes hlavní kandidáty a položku „ostatní“, které dává dohromady 100 %. Rozhoduje oficiální výsledek ČSÚ (volby.cz).</p>
<h2>Fáze a zveřejňování</h2>
<ul>
<li><b>Blind:</b> odhad bez znalosti sázkových kurzů. Zveřejňuje se jako první.</li>
<li><b>Final:</b> blind odhad zkombinovaný s trhem, tedy kurzy po odečtení marže sázkové kanceláře. Zveřejňuje se zvlášť a později. Blind číslo se tím nemění.</li>
<li><b>Updaty:</b> nové verze při nových informacích, například po 1. kole. Každá verze je nový záznam, starší se nepřepisují.</li>
<li>Každý den ukládáme neměnný snapshot do <a href="archiv.html">archivu</a> a commit do gitu. Opravu chyby zveřejníme jako novou verzi s vysvětlením, nikdy tichým přepsáním.</li>
</ul>
<h2>Co se vyhodnocuje</h2>
<ul>
<li><b>Hlavní hodnocený snapshot:</b> poslední zveřejněná verze před začátkem hlasování, tedy před 9. 10. 2026 ve 14:00. Hodnotí se zvlášť blind a zvlášť final.</li>
<li><b>Updaty po 1. kole</b> se hodnotí odděleně jako sekundární. Po 1. kole je předpověď výrazně snazší, takže do hlavního skóre nevstupují.</li>
<li><b>Metriky:</b> průměr přes všech 27 obvodů:
  <ul>
  <li>multi-outcome Brier, tedy Σ(p<sub>i</sub> − o<sub>i</sub>)²; čím nižší, tím lepší;</li>
  <li>log skóre vítěze, ln p(vítěz); čím blíž nule, tím lepší;</li>
  <li>počet obvodů, kde vyhrál náš favorit.</li>
  </ul></li>
<li><b>Srovnávací měřítka:</b>
  <ul>
  <li>sázkové kurzy po odečtení marže, kde jsou dostupné;</li>
  <li>naivní pravidlo „vyhraje obhájce, a kde nekandiduje, kandidát s nejširší koaliční podporou“ (jen Brier a počet trefených favoritů);</li>
  <li>rovnoměrné rozdělení mezi hlavní kandidáty.</li>
  </ul></li>
</ul>
<h2>Důležité upozornění: korelace</h2>
<p>27 obvodů nejsou nezávislé pokusy. Celostátní nálada, například nespokojenost s vládou, posouvá všechny obvody najednou. Ve většině obvodů je favoritem opoziční kandidát, takže výsledek je do značné míry jedna velká sázka. Při vyhodnocení to uvedeme.</p>
<h2>Jak predikce vznikají</h2>
<ol>
<li>Upřesnění otázky.</li>
<li>Research: kandidáti, historické výsledky obvodu, výsledky sněmovních voleb 2025 a místní kontext.</li>
<li>Blind odhad: model podílů v 1. kole a dvojic ve 2. kole, s podmíněnou pravděpodobností výhry podle soupeře a podle toho, kdo vedl 1. kolo.</li>
<li>Kontrola, že každé tvrzení má oporu v researchi.</li>
<li>Red-team.</li>
<li>Revize a agregace.</li>
</ol>
<p>Sdílené základní poznatky (base rates):</p>
<ul>
<li>Vítěz 1. kola vyhrává 2. kolo asi v 70 % případů (ČSÚ).</li>
<li>Kandidáti ANO vyhráli v letech 2020–2024 jen asi 9 ze 44 druhých kol. V roce 2020, kdy ANO vládlo, to bylo asi 1 z 8.</li>
</ul>
<h2>Pět sérií (od 5. 10.)</h2>
<ul>
<li><b>AI</b>: čistý AI agent bez modelu a bez kurzů. Mění se jen při nových faktech (zprávy, podpory, kauzy, průzkumy). Sloupec „AI 2. 10.“ ukazuje výchozí stav.</li>
<li><b>Statistický model</b> (viz <a href="model.html">popis modelu</a>). Mění se jen při změně vstupů, například po 1. kole.</li>
<li><b>AI s modelem</b>: AI agent, který vychází z modelu a odchyluje se jen kvůli faktům, které model nevidí. Každou odchylku zapisuje. Bez kurzů.</li>
<li><b>Sázky</b>: kurzy Fortuny a Tipsportu na vítěze obvodu po odečtení marže (metoda power). Kde má Tipsport jen sázku Ano/Ne na jednoho kandidáta, průměrujeme ji s Fortunou a zbytek rozdělujeme v poměru Fortuny. Kurzy čteme až po zamčení blind sérií.</li>
<li><b>Blend</b>: mechanická kombinace „AI s modelem“ a „Sázek“ v log-odds, ρ = 0,55 (w<sub>blind</sub> = 0,31). Žádný úsudek, jen nástroj.</li>
</ul>
<p>Série AI, Model a AI s modelem jsou <b>blind</b>. Snapshoty vznikají před čtením kurzů a v gitu jsou zamčené dřív, než kurzy přibydou. Pokud by se pozdější update AI vytvářel až po zobrazení kurzů, označíme ho jako <i>post-market</i>. Hodnotí se všech pět sérií.</p>
<h2>Co nezveřejňujeme</h2>
<p>Sázková doporučení ani výši sázek. Tohle není tipovací služba. Nezveřejňujeme ani surové pracovní soubory.</p>
<h2>Známá omezení prvního běhu (2. 10.)</h2>
<ul>
<li>Během běhu došla kapacita webového vyhledávání. U většiny obvodů proto research stál jen na přímo načtených stránkách (Wikipedie, programydovoleb.cz, senat.cz). Chybí čerstvé místní zprávy a často i okresní výsledky z roku 2025. Na stránce obvodu je to označeno jako <code>research_limitation</code>.</li>
<li>Kvůli limitu souběžných agentů neběžel ve 4 obvodech (12, 21, 24, 39) red-team nezávisle. Dodatečně jsme ho proto spustili zvlášť, ještě před zveřejněním.</li>
<li>Několik odhadů bylo před zveřejněním revidováno po red-teamu. Zveřejněný stav je výchozí bod; od něj už platí jen nové verze.</li>
<li><b>Průzkumy veřejného mínění blind odhad systematicky nepoužívá.</b> Průzkumy po obvodech se dělají jen výjimečně a kvůli vyčerpanému vyhledávání jsme je ve většině obvodů nemohli ani pořádně hledat. „Bez průzkumu“ proto znamená spíš „nenašli jsme“ než „neexistuje“. Celostátní průzkumy (STEM, Median, NMS, Kantar) sloužily jen jako kontext, ne jako vstup modelu. Plán: do pondělí 5. 10. (od 6. 10. platí moratorium na zveřejňování průzkumů) cíleně dohledat průzkumy obvodů a celostátní posun od voleb 2025 zapracovat jednotně do všech obvodů jako nový update.</li>
<li>Plzeň (obvod 9) prošla krokem s trhem už dříve. Zde zveřejňujeme jen její blind číslo, final přijde spolu s ostatními.</li>
</ul>
<h2>Časová razítka</h2>
<p>Každý denní stav je commit v gitu a zároveň snapshot v archive.org, aby šlo doložit, že predikce existovala před výsledkem.</p>
""",
    "en": """
<h2>What we forecast</h2>
<p>For each of the 27 districts: who will be elected senator, either by an absolute majority in round 1 or by winning the runoff. Each district gets a probability distribution over the main candidates plus “others”, summing to 100 %. Resolution follows the official ČSÚ result (volby.cz).</p>
<h2>Stages and publishing</h2>
<ul>
<li><b>Blind:</b> a forecast made without seeing betting odds. Published first.</li>
<li><b>Final:</b> the blind forecast combined with the market (odds with the bookmaker's margin removed). Published separately and later; the blind number does not change.</li>
<li><b>Updates:</b> new versions when new information arrives (e.g. after round 1). Every version is a new record; old ones are never overwritten.</li>
<li>Every day an immutable snapshot goes to the <a href="archiv.html">archive</a> and a commit goes to git. Corrections are published as new versions with an explanation, never as silent edits.</li>
</ul>
<h2>What gets scored</h2>
<ul>
<li><b>Primary scored snapshot:</b> the last version published before voting opens, i.e. before 9 Oct 2026 14:00 CEST. Blind and final are scored separately.</li>
<li><b>Post-round-1 updates</b> are scored separately as secondary. Forecasting gets much easier after round 1, so they don't count toward the main score.</li>
<li><b>Metrics:</b> averaged over all 27 districts:
  <ul>
  <li>multi-outcome Brier score, Σ(p<sub>i</sub> − o<sub>i</sub>)²; lower is better;</li>
  <li>log score of the winner, ln p(winner); closer to 0 is better;</li>
  <li>number of districts where our favourite won.</li>
  </ul></li>
<li><b>Benchmarks:</b>
  <ul>
  <li>de-vigged betting odds, where available;</li>
  <li>a naive rule, “the incumbent wins, otherwise the candidate with the broadest coalition” (Brier and favourite count only);</li>
  <li>a uniform split across the main candidates.</li>
  </ul></li>
</ul>
<h2>Important caveat: correlation</h2>
<p>The 27 districts are not independent trials. The national mood, for example discontent with the government, moves all districts at once. In most districts the favourite is an opposition candidate, so the outcome is largely one big correlated bet. We will say so in the evaluation.</p>
<h2>How the forecasts are made</h2>
<ol>
<li>Question normalization.</li>
<li>Research: candidates, district history, 2025 Chamber results, local context.</li>
<li>Blind forecast: a model of round-1 shares and runoff pairings, with win probabilities conditional on the opponent and on who led round 1.</li>
<li>A grounding check that every claim rests on the research.</li>
<li>Red-team.</li>
<li>Revision and aggregation.</li>
</ol>
<p>Shared base rates:</p>
<ul>
<li>The round-1 leader wins the runoff about 70 % of the time (ČSÚ).</li>
<li>ANO candidates won only about 9 of 44 runoffs in 2020–2024, and about 1 of 8 in 2020, when ANO was in government.</li>
</ul>
<h2>Five series (from 5 Oct)</h2>
<ul>
<li><b>AI</b>: the pure AI agent, with no model and no odds. It changes only on new facts (news, endorsements, scandals, polls). The “AI 2 Oct” column shows the starting point.</li>
<li><b>Statistical model</b> (see <a href="model.html">model description</a>). It changes only when its inputs change, e.g. after round 1.</li>
<li><b>AI + model</b>: the AI agent starting from the model and deviating only for facts the model cannot see. Every deviation is logged. No odds.</li>
<li><b>Betting</b>: Fortuna and Tipsport seat-winner odds with the margin removed (power method). Where Tipsport only offers a yes/no on one candidate, we average it with Fortuna and split the rest in Fortuna's ratios. Odds are read only after the blind series are locked.</li>
<li><b>Blend</b>: a mechanical log-odds combination of “AI + model” and “Betting”, ρ = 0.55 (w<sub>blind</sub> = 0.31). No judgment, just a tool.</li>
</ul>
<p>AI, Model and AI + model are <b>blind</b>. Their snapshots are made before any odds are read and are locked in git before the odds are added. Any later AI update made after seeing odds will be labelled <i>post-market</i>. All five series are scored.</p>
<h2>What we don't publish</h2>
<p>Betting recommendations or stakes. This is not a tipping service. We don't publish raw working files either.</p>
<h2>Known limitations of the first run (2 Oct)</h2>
<ul>
<li>The web-search budget ran out mid-run. For most districts, research relied on directly fetched pages (Wikipedia, programydovoleb.cz, senat.cz). Fresh local news and often 2025 district-level results are missing. District pages flag this as <code>research_limitation</code>.</li>
<li>Because of a concurrency limit, the red-team in 4 districts (12, 21, 24, 39) did not run independently. We therefore ran independent red-teams separately before publication.</li>
<li>Several forecasts were revised after the red-team before publication. The published state is the starting point; from here on only new versions count.</li>
<li><b>The blind forecast does not use opinion polls systematically.</b> District-level polls are rare, and with the search budget exhausted most districts could not search for them properly. “No poll” therefore means “none found” rather than “none exists”. National polls (STEM, Median, NMS, Kantar) served only as context, not as a model input. Plan: by Monday 5 Oct (a poll-publication blackout starts on 6 Oct), search specifically for district polls and apply the national swing since the 2025 election uniformly to all districts as a new update.</li>
<li>Plzeň (district 9) had already gone through the market step. We publish only its blind number here; its final comes with the others.</li>
</ul>
<h2>Timestamps</h2>
<p>Each daily state is a git commit plus an archive.org snapshot, so it can be shown that a forecast existed before the result.</p>
""",
}

JOURNAL = [
    dict(date="2026-10-02",
         title_cs="Den 1: blind předpovědi všech 27 obvodů",
         title_en="Day 1: blind forecasts for all 27 districts",
         cs="""<p>Spustili jsme plnou pipeline pro všech 27 obvodů. Brno 60 a Kladno 30 měly starší predikce z 21. 9., ty dostaly nový blind update. <b>Žádná fáze neviděla sázkové kurzy.</b></p>
<p><b>Celkový obraz:</b> v 26 z 27 obvodů je favoritem opoziční kandidát. Jedinou výjimkou je Karviná (75), kde ANO obhajuje volné místo. ANO často postupuje do 2. kola, ale v něm dlouhodobě prohrává, zvlášť v letech, kdy vládne. Nejtěsnější jsou Pelhřimov (15), Litovel (66), Hradec Králové (45), Praha 5 (21) a Plzeň (9).</p>
<p><b>Co se pokazilo a jak jsme to chytili:</b></p>
<ul>
<li>V Plzni, České Lípě, Zlíně a Rychnově red-team našel konstrukční chybu. Tabulka dvojic pro 2. kolo neodpovídala odhadu 1. kola, například v Plzni vycházel postup obhájce na 68 % místo zhruba 90 %.</li>
<li>Sdílené zadání špatně neoznačilo rok 2022 jako rok, kdy bylo ANO v opozici. Opraveno během běhu.</li>
<li>U Kladna update nejdřív vyšel na 55 % bez nové evidence. Nezávislý red-team ho stáhl na 51 %.</li>
<li>Došla kapacita webového vyhledávání, takže většina researche stála jen na přímo načtených stránkách.</li>
</ul>
<p><b>Kontrola před zveřejněním:</b> všechny obvody jsme porovnali s oficiálními kandidátkami ČSÚ (volby.gov.cz). Na lístku nechybí žádný kandidát, se kterým model počítá, a model nevynechal nikoho podstatného. Opravili jsme ale popisky: obhájce v Chebu se jmenuje Miroslav Plevný, ne Jaroslav. Adélu Sucharda Šípovou na Kladně navrhli Piráti za koalici Zelení, STAN, Piráti, TOP 09 a SEN 21. Na webu jsou teď jména a volební strany přímo z dat ČSÚ.</p>
<h3>Reflexe: proč se to stalo a co s tím</h3>
<ol>
<li><b>Konstrukční chyby v tabulce 2. kol</b> (4 obvody plus Plzeň). <i>Příčina:</i> model ručně odhadoval pravděpodobnosti dvojic ve 2. kole odděleně od podílů v 1. kole, a ty si pak odporovaly. <i>Náprava:</i> dvojice se odvozují simulací přímo z podílů v 1. kole, takže konzistence je daná konstrukcí. Některé obvody to tak už udělaly. Příště to bude povinný deterministický skript, ne úsudek modelu.</li>
<li><b>Chybný údaj ve sdíleném zadání</b> (rok 2022 neoznačený jako rok, kdy bylo ANO v opozici). <i>Příčina:</i> jedno zadání jsme rozeslali do 24 paralelních běhů bez kontroly faktů. Chyba se tak namnožila. <i>Náprava:</i> sdílené base rates projde před rozesláním nezávislá kontrola. Obvody spuštěné před opravou při dalším updatu zkontrolujeme.</li>
<li><b>Nedostupný web.</b> Došla kapacita vyhledávání a řada zdrojů je nedostupná: volby.gov.cz je JavaScriptová aplikace, iROZHLAS vracel 403, regionální Deník je za paywallem. Research proto často stál jen na Wikipedii. <i>Příčina:</i> nástroj, který stránky načítá jako text, neumí stránky vykreslované JavaScriptem, a vyhledávání má pevný limit na celou relaci. <i>Náprava:</i> (a) data ČSÚ stáhnout jednou centrálně přes jejich JSON rozhraní do sdílené cache, ne v každém obvodu zvlášť; (b) pro nedostupné stránky použít skutečný prohlížeč; (c) navýšit limit vyhledávání a hledání rozplánovat napřed, ne vyčerpat v prvních obvodech.</li>
<li><b>Nedostatečná nezávislost kroků.</b> Kvůli limitu souběžných agentů dělal v části obvodů jeden model research, odhad i oponenturu. <i>Náprava:</i> menší vlny místo spuštění všeho najednou a red-team vždy jako samostatný agent. Ve 4 dotčených obvodech jsme red-team zopakovali nezávisle; změnil se jen jeden (Praha 5, o 3 body).</li>
<li><b>„Překalibrace“ bez nové evidence</b> (Kladno 45 → 55). <i>Příčina:</i> update přepočítal model na nepodložených předpokladech a vydával to za zpřesnění. <i>Náprava:</i> nové pravidlo, že posun větší než 3 body bez nové evidence musí projít nezávislým red-teamem. Tady ho stáhl na 51.</li>
<li><b>Zastaralé predikce.</b> Z dřívějších otázek víme, že největší chyby nevznikaly špatným modelem, ale tím, že predikce týdny nikdo neaktualizoval. <i>Náprava:</i> denní kontrola každého obvodu, i kdyby byl výsledek „beze změny“, a povinný update po 1. kole.</li>
</ol>
<p><b>Další krok:</b> trh, tedy kurzy po odečtení marže, a final čísla. Pak denní kontrola novinek až do zmrazení 9. 10. ve 14:00.</p>""",
         en="""<p>We ran the full pipeline for all 27 districts. Brno 60 and Kladno 30 had older forecasts from 21 Sep, so they got a fresh blind update. <b>No stage saw betting odds.</b></p>
<p><b>Big picture:</b> in 26 of 27 districts the favourite is an opposition candidate. The only exception is Karviná (75), where ANO defends an open seat. ANO often reaches the runoff but has a long record of losing it, especially when it is in government. The closest races are Pelhřimov (15), Litovel (66), Hradec Králové (45), Praha 5 (21) and Plzeň (9).</p>
<p><b>What went wrong and how we caught it:</b></p>
<ul>
<li>In Plzeň, Česká Lípa, Zlín and Rychnov the red-team found a construction error. The runoff-pairing table did not match the round-1 share model; in Plzeň, for example, it put the incumbent's chance of reaching the runoff at 68 % instead of about 90 %.</li>
<li>The shared brief failed to mark 2022 as a year when ANO was in opposition. Fixed mid-run.</li>
<li>The Kladno update first came out at 55 % with no new evidence; an independent red-team pulled it to 51 %.</li>
<li>The web-search budget ran out, so most research relied on directly fetched pages.</li>
</ul>
<p><b>Pre-publication check:</b> we checked all districts against the official ČSÚ candidate register (volby.gov.cz). Every candidate the model uses is on the ballot, and the model leaves out no one significant. We did fix some labels: the Cheb incumbent is Miroslav Plevný, not Jaroslav. In Kladno, Adéla Sucharda Šípová was nominated by the Pirates on behalf of a Greens/STAN/Pirates/TOP 09/SEN 21 coalition. The site now takes names and lists straight from ČSÚ data.</p>
<h3>Reflection: why it happened and what we do about it</h3>
<ol>
<li><b>Construction errors in the runoff table</b> (4 districts plus Plzeň). <i>Cause:</i> the model estimated runoff-pair probabilities by hand, separately from round-1 shares, and the two contradicted each other. <i>Fix:</i> pairings are now derived by simulation directly from round-1 shares, so consistency holds by construction. Some districts already did this. Next time it will be a mandatory deterministic script, not model judgement.</li>
<li><b>An error in the shared brief</b> (2022 not marked as an ANO-in-opposition year). <i>Cause:</i> one brief was sent to 24 parallel runs without a fact check, so the mistake was copied everywhere. <i>Fix:</i> shared base rates get an independent check before fan-out. Districts started before the fix will be checked at their next update.</li>
<li><b>Unreachable web.</b> The search budget ran out and many sources are unreachable: volby.gov.cz is a JavaScript app, iROZHLAS returned 403, regional Deník is paywalled. Research often relied on Wikipedia alone. <i>Cause:</i> the tool that fetches pages as text can't handle JS-rendered pages, and search has a hard per-session cap. <i>Fix:</i> (a) fetch ČSÚ data once, centrally, via its JSON interface into a shared cache, instead of in every district; (b) use a real browser for unreachable pages; (c) raise the search cap and plan searches up front instead of exhausting them on the first districts.</li>
<li><b>Insufficient independence between stages.</b> Because of a concurrency limit, in some districts one model did research, forecast and red-team. <i>Fix:</i> smaller waves instead of launching everything at once, with the red-team always a separate agent. We re-ran independent red-teams in the 4 affected districts; only one changed (Praha 5, by 3 points).</li>
<li><b>“Recalibration” without new evidence</b> (Kladno 45 → 55). <i>Cause:</i> the update re-ran the model on unsupported assumptions and presented it as a refinement. <i>Fix:</i> a new rule that any move of more than 3 points without new evidence must pass an independent red-team. Here it pulled the number back to 51.</li>
<li><b>Stale forecasts.</b> Earlier questions taught us that the biggest misses came not from a bad model but from forecasts nobody updated for weeks. <i>Fix:</i> a daily check of every district, even when the answer is “no change”, and a mandatory update after round 1.</li>
</ol>
<p><b>Next:</b> the market step (de-vigged odds) and final numbers, then daily news checks until the freeze on 9 Oct 14:00.</p>"""),
]


def _model_page(lang: str):
    def render(m: dict) -> str:
        v = m.get("validation") or {}
        b = (m.get("coefficients") or {}).get("beta", {})
        cyc = v.get("cycles", {})
        if lang == "cs":
            coef = "".join(f"<tr><td><code>{k}</code></td><td class='num'>{val:+.2f}</td></tr>" for k, val in b.items())
            return f"""
<p class="lead">Samostatná série: statistický model ze tří vrstev se simulací Monte Carlo. Pracuje jen s oficiálními daty ČSÚ a nevidí žádné sázkové kurzy. Od pondělí ho AI agent dostane jako vstup, takže půjde porovnat čtyři série: AI samotné (2. 10.), model samotný, AI s modelem a trh.</p>
<h2>Vrstvy</h2>
<ol>
<li><b>Stranická základna:</b> výsledek sněmovních voleb (2025 pro letošek, 2021 pro historii) po okrscích, převedený na senátní obvody podle oficiálních převodníků ČSÚ. Základna kandidáta je součet podílů stran, které ho navrhly nebo podpořily. Celostátní posun od voleb 2025 se bere z průměru průzkumů (Kantar, Median, NMS, STEM za srpen a září 2026), je pro všechny obvody společný a v simulaci se losuje.</li>
<li><b>Místní základna:</b> podíl místních a regionálních hnutí v komunálních volbách (2018 pro roky 2020 a 2022, 2022 pro roky 2024 a 2026), u subjektů, které ve sněmovních volbách nekandidují. Zavedené celostátní strany (SOCDEM, KSČM) jsou vyřazené.</li>
<li><b>Efekt kandidáta (1. kolo):</b> regrese na 582 kandidátech z let 2020–2024. Rysy: obhájce a bývalý senátor (podle historie voleb), starosta nebo hejtman a poslanec (podle povolání), vládní strana, ANO, STAN, KDU-ČSL, kandidát bez stranické základny, počet podporujících stran a počet kandidátů.</li>
<li><b>Druhé kolo:</b> model výsledku finalistů podle náskoku z 1. kola, rezervy hlasů ve stejném bloku (DEM / ANO / NAT / ostatní) a vládní příslušnosti. Fitovaný na zhruba 80 druhých kolech.</li>
<li><b>Simulace:</b> 20 000 průběhů. Společný celostátní posun, šum kandidátů, výsledek 2. kola. Nakonec kalibrace p ∝ p<sup>0,55</sup>.</li>
</ol>
<h2>Validace (vynechání jednoho volebního cyklu, 81 obvodů 2020–2024)</h2>
<table><thead><tr><th>Model / heuristika</th><th>Brier ↓</th><th>log skóre ↑</th></tr></thead><tbody>
<tr><td><b>statistický model</b></td><td class="num"><b>{v.get('brier_model', 0):.3f}</b></td><td class="num"><b>−1,40</b></td></tr>
<tr><td>pravděpodobnost úměrná stranické základně</td><td class="num">0,770</td><td class="num">−1,75</td></tr>
<tr><td>obhájce 50 %, zbytek rovnoměrně</td><td class="num">0,783</td><td class="num">−1,78</td></tr>
<tr><td>rovnoměrné rozdělení</td><td class="num">0,843</td><td class="num">−1,92</td></tr>
</tbody></table>
<p>Podle cyklů: 2020 {cyc.get('2020', {}).get('brier', 0):.3f} · 2022 {cyc.get('2022', {}).get('brier', 0):.3f} · 2024 {cyc.get('2024', {}).get('brier', 0):.3f}. Průměrná chyba odhadu podílu v 1. kole je {v.get('r1_mae', 0):.1f} procentního bodu. Favorit modelu vyhrál v {v.get('acc_model', 0)*100:.0f} % obvodů.</p>
<h2>Poctivě o slabinách</h2>
<ul>
<li><b>Signál je mírný.</b> Model jednoduchá pravidla poráží, ale senátní volby jsou málo předvídatelné.</li>
<li><b>Model bez kalibrace byl přehnaně sebejistý.</b> V pásmu 70–90 % vyhrálo jen 32 % kandidátů. Mocnina 0,55 je nastavená na stejných validačních datech, takže hodnoty po kalibraci jsou mírně optimistické.</li>
<li><b>Nevidí osobní značku</b> nezávislých kandidátů a nová hnutí, která v roce 2022 ještě neexistovala (Vosecký, Chalupský, Ošťádal). Tady má přidat hodnotu AI agent.</li>
<li><b>Vládní období ANO je v historických datech jen jedno</b> (2020). Efekt „ANO ve vládě“ je proto odhadnutý z malého vzorku.</li>
<li><b>Ve sněmovních volbách 2021 kandidovali Piráti a STAN společně</b> a jejich podíl je rozdělený napůl (předpoklad). SPOLU je rozdělené jako ODS 60 %, KDU-ČSL 22 % a TOP 09 18 % (předpoklad).</li>
</ul>
<h2>Koeficienty 1. kola (procentní body)</h2>
<div class="scroll"><table><tbody>{coef}</tbody></table></div>
<p class="muted">Kód: <code>tools/senat_model/</code>, data: <code>data/snapshots/*-model.json</code>.</p>"""
        coef = "".join(f"<tr><td><code>{k}</code></td><td class='num'>{val:+.2f}</td></tr>" for k, val in b.items())
        return f"""
<p class="lead">A separate series: a three-layer statistical model with Monte Carlo simulation. It uses only official ČSÚ data and sees no betting odds. From Monday the AI agent gets it as an input, so we can compare four series: AI alone (2 Oct), model alone, AI + model, and the market.</p>
<h2>Layers</h2>
<ol>
<li><b>Party base:</b> the Chamber election result (2025 for this year, 2021 for history) by precinct, mapped to Senate districts with ČSÚ's official mapping tables. A candidate's base is the sum of the shares of the parties that nominated or backed them. The national swing since the 2025 election comes from the poll average (Kantar, Median, NMS, STEM, Aug–Sep 2026); it is shared by all districts and drawn in the simulation.</li>
<li><b>Local base:</b> the municipal-election share (2018 for the 2020 and 2022 cycles, 2022 for 2024 and 2026) of local and regional movements that do not run in Chamber elections. Established national parties (SOCDEM, KSČM) are excluded.</li>
<li><b>Candidate effect (round 1):</b> a regression on 582 candidates from 2020–2024. Features: incumbent and former senator (from election history), mayor or governor and MP (from occupation), government party, ANO, STAN, KDU-ČSL, no party base, number of backing parties, number of candidates.</li>
<li><b>Runoff:</b> a model of the finalists' result from the round-1 margin, the same-bloc vote reservoir (DEM / ANO / NAT / other) and government affiliation. Fitted on about 80 runoffs.</li>
<li><b>Simulation:</b> 20,000 runs with a shared national swing, candidate noise and the runoff outcome. Finally, calibration p ∝ p<sup>0.55</sup>.</li>
</ol>
<h2>Validation (leave one election cycle out, 81 districts 2020–2024)</h2>
<table><thead><tr><th>Model / heuristic</th><th>Brier ↓</th><th>log score ↑</th></tr></thead><tbody>
<tr><td><b>statistical model</b></td><td class="num"><b>{v.get('brier_model', 0):.3f}</b></td><td class="num"><b>−1.40</b></td></tr>
<tr><td>probability proportional to party base</td><td class="num">0.770</td><td class="num">−1.75</td></tr>
<tr><td>incumbent 50 %, rest uniform</td><td class="num">0.783</td><td class="num">−1.78</td></tr>
<tr><td>uniform</td><td class="num">0.843</td><td class="num">−1.92</td></tr>
</tbody></table>
<p>By cycle: 2020 {cyc.get('2020', {}).get('brier', 0):.3f} · 2022 {cyc.get('2022', {}).get('brier', 0):.3f} · 2024 {cyc.get('2024', {}).get('brier', 0):.3f}. The mean absolute error of the round-1 share is {v.get('r1_mae', 0):.1f} pp. The model's favourite won in {v.get('acc_model', 0)*100:.0f} % of districts.</p>
<h2>Honest limitations</h2>
<ul>
<li><b>The signal is modest.</b> The model beats simple rules, but Senate races are hard to predict.</li>
<li><b>The raw model was overconfident.</b> In the 70–90 % bucket only 32 % won. The 0.55 exponent was fitted on the same validation data, so the calibrated numbers are slightly optimistic.</li>
<li><b>It cannot see the personal brand</b> of independents or of movements that didn't exist in 2022 (Vosecký, Chalupský, Ošťádal). This is where the AI agent should add value.</li>
<li><b>There is only one ANO-in-government cycle</b> in the historical data (2020), so the “ANO in government” effect rests on a small sample.</li>
<li><b>In the 2021 Chamber election Pirates and STAN ran on a joint list</b>, which is split 50/50 (assumption). SPOLU is split ODS 60 %, KDU-ČSL 22 %, TOP 09 18 % (assumption).</li>
</ul>
<h2>Round-1 coefficients (percentage points)</h2>
<div class="scroll"><table><tbody>{coef}</tbody></table></div>
<p class="muted">Code: <code>tools/senat_model/</code>, data: <code>data/snapshots/*-model.json</code>.</p>"""
    return render


MODEL_PAGE = {"cs": _model_page("cs"), "en": _model_page("en")}

JOURNAL.append(dict(
    date="2026-10-03",
    title_cs="Den 2: statistický model jako druhá série",
    title_en="Day 2: a statistical model as a second series",
    cs="""<p><b>Co jsme udělali:</b> postavili jsme statistický model podle návrhu „Model predikce senátních voleb 2026“ a zveřejňujeme ho jako samostatnou sérii. Popis je na stránce <a href="model.html">Model</a>. Kurzy model nevidí. Při validaci na 81 obvodech z let 2020–2024 poráží jednoduchá pravidla: Brier 0,673 proti 0,770 u nejlepší heuristiky.</p>
<p><b>Kde se model a AI agent rozcházejí:</b> Praha 5 (model Sáblík 68 %, AI Láska 46 %), Praha 1 (Padevět 70 % vs. Čižinský 54 %), Pelhřimov (Med 75 % vs. 45 %) a Karviná (Brzyszkowská 40 % vs. 65 %). Jde o obvody se silnými místními nebo nezávislými kandidáty. Po volbách se tu ukáže, jestli agent přidává informaci, nebo šum.</p>
<h3>Chyby a jejich nápravy</h3>
<ol>
<li><b>První verze trefila favorita jen ve 41 % obvodů.</b> <i>Příčina:</i> obhájce jsme poznávali podle slova „senátor“ v povolání, což často chybí. <i>Náprava:</i> obhájce se teď určuje z úplné historie voleb ČSÚ, včetně změny jména (Šípová → Sucharda Šípová).</li>
<li><b>Model v roce 2020 nadhodnotil kandidáty ANO o 10–15 bodů.</b> <i>Příčina:</i> vládní strana má v senátních volbách nižší podíl než ve sněmovních, a validace bez roku 2020 neměla jiný cyklus, kdy ANO vládlo. <i>Náprava:</i> interakce mezi základnou a vládní stranou. V datech je ale jen jeden takový cyklus, proto to uvádíme jako slabinu.</li>
<li><b>Model podceňoval kandidáty STAN a KDU-ČSL.</b> <i>Příčina:</i> jsou to strany starostů, takže v Senátu mají víc, než říká jejich sněmovní základna. <i>Náprava:</i> stranické efekty pro STAN a KDU-ČSL.</li>
<li><b>Model byl přehnaně sebejistý.</b> V pásmu 70–90 % vyhrálo jen 32 % kandidátů. <i>Náprava:</i> kalibrace na validačních datech. Je nastavená na stejných datech, takže je mírně optimistická.</li>
<li><b>Model nevidí místní hnutí</b> (Praha sobě, SLK, SEN 21, Rozvíjíme Hradec…). <i>Náprava:</i> místní základna z komunálních voleb. Brier se zlepšil z 0,693 na 0,673.</li>
<li><b>Artefakt:</b> kandidát SOCDEM v Karviné vyskočil na 43 % kvůli síle ČSSD v komunálních volbách 2022, i když se strana celostátně zhroutila. <i>Náprava:</i> zavedené celostátní strany do místní základny nepočítáme.</li>
<li><b>Tabulka průzkumů na Wikipedii nebyla k nalezení vyhledáváním</b> (anglická verze stránku pro rok 2029 nemá). <i>Náprava:</i> data jsme vzali z české Wikipedie přes její API. Výsledkem je průměr čtyř agentur místo úryvků z researche.</li>
</ol>
<p><b>Další krok (po 5. 10.):</b> průzkumy po obvodech před moratoriem, AI update s modelem jako vstupem, zamčení blind odhadu a potom trh.</p>""",
    en="""<p><b>What we did:</b> we built a statistical model following the design note “Model predikce senátních voleb 2026” and publish it as a separate series. The description is on the <a href="model.html">Model</a> page. The model sees no odds. In validation on 81 districts from 2020–2024 it beats simple rules: Brier 0.673 vs. 0.770 for the best heuristic.</p>
<p><b>Where the model and the AI agent disagree:</b> Praha 5 (model Sáblík 68 %, AI Láska 46 %), Praha 1 (Padevět 70 % vs. Čižinský 54 %), Pelhřimov (Med 75 % vs. 45 %) and Karviná (Brzyszkowská 40 % vs. 65 %). These are districts with strong local or independent candidates. After the election they will show whether the agent adds information or noise.</p>
<h3>Mistakes and their fixes</h3>
<ol>
<li><b>The first version picked the right favourite in only 41 % of districts.</b> <i>Cause:</i> incumbents were detected from the word “senator” in the occupation field, which is often missing. <i>Fix:</i> incumbency now comes from the full ČSÚ election history, including name changes (Šípová → Sucharda Šípová).</li>
<li><b>In 2020 the model overrated ANO candidates by 10–15 points.</b> <i>Cause:</i> a governing party gets a lower share in Senate elections than in Chamber elections, and validating without 2020 left no other cycle with ANO in government. <i>Fix:</i> an interaction between base and government party. There is only one such cycle in the data, so we list it as a limitation.</li>
<li><b>The model underrated STAN and KDU-ČSL candidates.</b> <i>Cause:</i> they are mayors' parties and do better in the Senate than their Chamber base suggests. <i>Fix:</i> party effects for STAN and KDU-ČSL.</li>
<li><b>The model was overconfident.</b> In the 70–90 % bucket only 32 % won. <i>Fix:</i> calibration on validation data. It is fitted on the same data, so it is slightly optimistic.</li>
<li><b>The model couldn't see local movements</b> (Praha sobě, SLK, SEN 21, Rozvíjíme Hradec…). <i>Fix:</i> a local base from municipal elections. Brier improved from 0.693 to 0.673.</li>
<li><b>Artefact:</b> the SOCDEM candidate in Karviná jumped to 43 % because of ČSSD's strength in the 2022 municipal elections, even though the party has collapsed nationally. <i>Fix:</i> established national parties don't count toward the local base.</li>
<li><b>The Wikipedia poll table couldn't be found through search</b> (the English site has no 2029 polling page). <i>Fix:</i> we took the data from Czech Wikipedia via its API. The result is an average of four pollsters instead of snippets from research.</li>
</ol>
<p><b>Next (Mon 5 Oct):</b> district polls before the blackout, an AI update with the model as input, locking the blind forecast, then the market.</p>"""))

JOURNAL.append(dict(
    date="2026-10-04",
    title_cs="Den 3: příprava na pondělí, průchod médii, čísla beze změny",
    title_en="Day 3: getting ready for Monday, media sweep, numbers unchanged",
    cs="""<p><b>Odhady jsme dnes neměnili</b>, a to záměrně: AI blind je pořád ze 2. 10., model ze 3. 10. Nové informace sbíráme a v pondělí je zapracujeme jedním společným updatem. Ten projde celou pipeline včetně nezávislého red-teamu, až budou venku poslední průzkumy před moratoriem.</p>
<h3>Co jsme udělali</h3>
<ul>
<li><b>Oprava pipeline.</b> Kombinaci blind odhadu a trhu teď počítá deterministický nástroj. Parametr ρ v něm znamená korelaci mezi blind odhadem a trhem, ne váhu blind odhadu, a průměruje se v log-odds. Tím je opravená chyba z prvního běhu (Plzeň), kdy trh dostal menší váhu, než měl.</li>
<li><b>Pravidla pro pondělní update.</b> AI agent vyjde ze statistického modelu. Odchýlit se smí jen kvůli faktu, který model nevidí (osobní značka, kauza, podpora, průzkum v obvodu), a každou odchylku zapíše i s důvodem. Nesmí znovu započítat to, co už je v modelu.</li>
<li><b>Průchod médii.</b> Nedělní diskusní pořady byly o celostátní politice (Havlíček v Poledni s Moravcem, Nedělní debata o důchodech).
  <ul>
  <li><b>Praha 5:</b> zářijový průzkum NMS (celopražský, komunální) ukazuje, že Láska je nejznámější pražský politik (34 % si na něj vzpomene spontánně), ale jeho hnutí zvažuje jen asi 10 % voličů. Nepřímo to svědčí proti velké osobní značce, se kterou počítal AI odhad.</li>
  <li><b>Přerov:</b> v sobotu tam podpořil kandidáta ANO premiér Babiš.</li>
  <li><b>Peníze na kampaně:</b> Tsoukernik (Cheb) přispěla milionem, Dvořák (Hradec) 400 tisíci. Motoristé do Senátu nikoho nenasadili.</li>
  <li><b>Průzkum přímo v senátním obvodu jsme nenašli žádný.</b></li>
  </ul></li>
</ul>
<h3>Chyby a nápravy</h3>
<ol>
<li><b>Termín moratoria jsme uvedli bez ověření</b> („pondělí 22:00“). <i>Náprava:</i> zákaz zveřejňování průzkumů začíná 3 dny před dnem voleb, tedy v úterý 6. 10. Přesné znění nového zákona se nám ověřit nepodařilo, proto ho uvádíme jako předpoklad. Průzkumy budeme hledat do pondělního večera.</li>
<li><b>Vyhledávání v nástroji agenta je vyčerpané.</b> <i>Náprava:</i> hledáme přes prohlížeč (Google s filtrem na poslední týden). Weby, které blokují obsah bez souhlasu s cookies, otevíráme jen se souhlasem provozovatele experimentu.</li>
<li><b>Mylný předpoklad o vysílání.</b> Hledali jsme Otázky Václava Moravce, ale nedělní pořad se dnes jmenuje Poledne s Moravcem. Výsledek to neovlivnilo, je to ale připomínka ověřovat i drobnosti.</li>
<li><b>Riziko ovlivnění kurzy.</b> Ve výsledcích vyhledávání se objevil článek o favoritech sázkových kanceláří. <i>Náprava:</i> neotevřeli jsme ho a zapsali jsme to. Blind odhad musí zůstat bez kurzů až do jeho zamčení.</li>
</ol>
<p><b>Pondělí 5. 10.:</b> poslední hledání průzkumů, potom AI update všech 27 obvodů se statistickým modelem jako vstupem, zamčení blind odhadu a teprve pak trh a final čísla.</p>""",
    en="""<p><b>We did not change any forecasts today</b>, on purpose: the AI blind is still from 2 Oct and the model from 3 Oct. We are collecting new information and will fold it into one joint update on Monday. That update goes through the full pipeline, including an independent red-team, once the last polls before the blackout are out.</p>
<h3>What we did</h3>
<ul>
<li><b>Pipeline fix.</b> The blind–market blend is now computed by a deterministic tool. Its ρ is the correlation between the blind forecast and the market, not the blind weight, and the pooling is in log-odds. This fixes the first-run bug (Plzeň) where the market got less weight than it should.</li>
<li><b>Rules for Monday's update.</b> The AI agent starts from the statistical model. It may deviate only for a fact the model cannot see (personal brand, scandal, endorsement, district poll) and logs every deviation with its reason. It must not re-count what the model already contains.</li>
<li><b>Media sweep.</b> Sunday's TV debates were about national politics (Havlíček on Poledne s Moravcem, Nedělní debata on pensions).
  <ul>
  <li><b>Praha 5:</b> a September NMS poll (Prague-wide, municipal) shows Láska is the best-known Prague politician (34 % unaided recall), but only about 10 % of voters consider his movement. This is indirect evidence against the large personal-brand premium the AI forecast assumed.</li>
  <li><b>Přerov:</b> PM Babiš campaigned there on Saturday for the ANO candidate.</li>
  <li><b>Campaign money:</b> Tsoukernik (Cheb) put in 1 million CZK, Dvořák (Hradec) 400k. Motoristé field no Senate candidates.</li>
  <li><b>We found no poll for any individual Senate district.</b></li>
  </ul></li>
</ul>
<h3>Mistakes and fixes</h3>
<ol>
<li><b>We stated the poll-blackout time without checking it</b> (“Monday 22:00”). <i>Fix:</i> the ban on publishing polls starts 3 days before election day, i.e. Tue 6 Oct. We could not verify the exact wording of the new law, so we state it as an assumption. We will keep searching for polls until Monday evening.</li>
<li><b>The agent's search tool is exhausted.</b> <i>Fix:</i> we search via the browser (Google with a last-week filter). Sites that block content behind a cookie consent are opened only with the operator's approval.</li>
<li><b>A wrong assumption about the TV schedule.</b> We looked for Otázky Václava Moravce, but the Sunday show is now called Poledne s Moravcem. The outcome was unaffected, but it is a reminder to verify small things too.</li>
<li><b>Risk of odds contamination.</b> A search result showed an article on bookmakers' favourites. <i>Fix:</i> we did not open it and logged it. The blind forecast must stay free of odds until it is locked.</li>
</ol>
<p><b>Monday 5 Oct:</b> a final poll search, then an AI update of all 27 districts with the statistical model as input, locking the blind forecast, and only then the market and final numbers.</p>"""))

JOURNAL.append(dict(
    date="2026-10-05",
    title_cs="Den 4: pět sérií — AI, Statistický model, AI s modelem, Sázky, Blend",
    title_en="Day 4: five series — AI, Statistical model, AI + model, Betting, Blend",
    cs="""<p><b>Dnes se poprvé objevují všechny série.</b> Pořadí bylo pevné: nejdřív AI update bez modelu (krok A), potom AI s modelem jako vstupem (krok B). Oba blind snapshoty jsme v 15:24 zamkli commitem v gitu. Kurzy jsme začali číst až potom (Fortuna od 15:35, pak Tipsport).</p>
<h3>Co se změnilo</h3>
<ul>
<li><b>AI (bez modelu):</b> od 2. 10. se změnily jen 2 obvody. V Litovli jsme posunuli 2 p.b. od Ošťádala ke Kohajdovi, protože Ošťádal prohlásil „kampaň dělat nebudu“. V Brně jsme opravili 2 p.b. kvůli vnitřní nekonzistenci předchozí verze. Ve zbylých 25 obvodech nové fakty nepřibyly a odhad zůstal (pravidlo: menší pohyb než 2 p.b. a žádná podstatná událost = beze změny).</li>
<li><b>AI s modelem:</b> ve dvou obvodech se změnil favorit: 21 (Sáblík místo Lásky) a 27 (Padevět místo Čižinského). Hodně zesílili favorité, kde model vidí silnou koaliční základnu (Kladno, Praha 9, Pelhřimov, Hradec). Oslabili tam, kde model nevidí osobní značku (Strakonice, Karviná, Česká Lípa, Uherské Hradiště).</li>
<li><b>Sázky:</b> favorit trhu se od „AI s modelem“ liší v 9 z 27 obvodů. Trh výrazně víc věří:
  <ul>
  <li>kandidátům ANO v Chebu (Tsoukernik), Pelhřimově (Kozár) a Přerově (Vrána, 82 % proti našim 24 %);</li>
  <li>osobním značkám a místním lídrům: Láska, Čižinský, Řehka, Korč, Kohajda a Paták.</li>
  </ul>
  Naše série naopak stojí víc na šíři koaliční podpory. Tohle je hlavní sázka experimentu a po volbách uvidíme, kdo měl pravdu.</li>
<li><b>Blend</b> kombinuje „AI s modelem“ a trh mechanicky (ρ = 0,55, váha AI asi 31 %).</li>
</ul>
<h3>Chyby a nápravy</h3>
<ol>
<li><b>Chyby ve vstupech statistického modelu.</b> Agenti v kroku B při kontrole vstupů našli asi tucet chyb:
  <ul>
  <li>příznak „starosta“ se chytal i na „bývalý starosta“;</li>
  <li>bývalé senátory model párová jen podle jména, takže se pletli jmenovci (dva Martinové Dvořákové);</li>
  <li>koaliční kandidátka v komunálních volbách se připisovala celá každé straně v koalici;</li>
  <li>pražská kandidátka „Praha 7 SOBĚ“ z roku 2018 nebyla namapovaná;</li>
  <li>chybějící SLK v opozičním bloku;</li>
  <li>nulová základna KSČM;</li>
  <li>kalibrace dává každému menšímu kandidátovi zhruba 2 % jako podlahu.</li>
  </ul>
  <i>Náprava:</i> model v1 dnes záměrně neměníme, aby se série Statistický model měnila jen při změně vstupů. Chyby agenti zapsali jako odchylky s důvodem a opravy půjdou do modelu v2 po 1. kole. Zveřejníme to jako novou verzi.</li>
<li><b>Dvojí započítání neformální podpory.</b> Ve Vyškově a Litovli agent spustil model znovu a „dokódoval“ neformální podporu stran, které nejsou na hlasovacím lístku. V trénovacích datech ale takhle kódovaná není, takže by se efekt počítal dvakrát. <i>Náprava:</i> doplnili jsme pravidlo (bez přepočtu modelu, jen umírněná odchylka nad typickou úroveň) a nezávislá kontrola oba obvody ještě před zamčením opravila. Vyškov zůstal kolem 76 %, v Litovli vychází Ošťádal 36,5 % a Kohajda 31 %.</li>
<li><b>Kanály, kterými mohly prosáknout kurzy.</b> Našli jsme dva:
  <ul>
  <li>v souboru se zprávami pro agenty byla naše poznámka o favoritovi modelu;</li>
  <li>automaticky načítaná paměť agenta obsahovala čísla z dřívějšího kroku s trhem pro Plzeň, Brno a Kladno.</li>
  </ul>
  <i>Náprava:</i> obojí jsme vyčistili během běhu a v dotčených obvodech to zapsali jako riziko kontaminace. Plně čisté to u nich zaručit neumíme.</li>
<li><b>Chyba v nástroji pro updaty.</b> Jako výchozí „předchozí pravděpodobnost“ nástroj kopíroval final číslo (s trhem) místo blind čísla. Agent to chytil v Plzni. <i>Náprava:</i> v updatech jsme vycházeli z blind čísla; opravu nástroje uděláme před dalším updatem.</li>
<li><b>Nejasná definice trhu.</b> U Fortuny nebylo jasné, jestli jde o vítěze 1. kola, nebo o zvolení. <i>Řešení:</i> Tipsport výslovně vypisuje „celkově“ a jeho čísla s Fortunou sedí, proto obojí bereme jako vítěze obvodu. Marže Fortuny je vysoká (11–78 %).</li>
<li><b>Omezení přístupu na Tipsportu.</b> Při rychlém procházení web dočasně zablokoval sázení. <i>Náprava:</i> pomalejší čtení s pauzami. Kurzy máme pro všech 27 obvodů z obou kanceláří.</li>
</ol>
<h3>Předem zapsaná očekávání (5. 10., před výsledky)</h3>
<p>Výsledky zatím nikdo nezná. Proto teď zapisujeme, co od jednotlivých sérií čekáme, abychom po volbách mohli ověřit i vlastní odhad slabin.</p>
<ul>
<li><b>Očekávané pořadí podle Brieru:</b> Blend ≈ Sázky &gt; AI s modelem &gt; Statistický model ≈ AI. Kombinace dvou různých zdrojů obvykle vychází nejlépe. Trh v našich dřívějších otázkách porazil náš final v 5 ze 6 případů.</li>
<li><b>AI:</b> research byl tenký (vyčerpané vyhledávání), opakovaně se objevovala chyba v konstrukci (dvojice ve 2. kole neseděly s podíly v 1. kole) a odhad se od 2. 10. téměř neměnil.</li>
<li><b>Statistický model:</b> má jen 3 volební cykly v datech, nevidí osobní značky a obsahuje známé chyby ve vstupech. Jako samostatný odhad je hrubý.</li>
<li><b>AI s modelem:</b> riziko je přílišné přimknutí k modelu a přehnaná jistota u favoritů se silnou koalicí (Kladno 80 %, Praha 9 79 %, Znojmo 84 %).</li>
<li><b>Sázky:</b> tenký trh s vysokou marží; obě kanceláře se pravděpodobně navzájem sledují.</li>
</ul>
<p><b>Hlavní hypotéza.</b> V 9 obvodech má trh jiného favorita než AI s modelem: 3 Cheb, 9 Plzeň, 15 Pelhřimov, 21 Praha 5, 27 Praha 1, 30 Kladno, 63 Přerov, 66 Litovel a 69 Frýdek-Místek. Proti sobě tu stojí dvě teorie. Podle naší rozhoduje šíře koaliční podpory a slabost ANO ve 2. kolech. Trh věří osobním značkám, místním lídrům a kandidátům ANO. Kdo v těchto 9 obvodech trefí víc vítězů, rozhodne o pořadí sérií víc než zbylých 18 obvodů dohromady.</p>
<p><b>Jak budeme hodnotit.</b> 27 obvodů je silně korelovaných, takže rozdíly v průměrném Brieru nebudou statisticky průkazné. Kromě celkového skóre proto zveřejníme párové srovnání po obvodech a zvlášť rozbor 9 sporných obvodů.</p>
<p><b>Dál:</b> od úterý 6. 10. platí moratorium na průzkumy. AI se změní jen při nových faktech, Sázky budeme číst denně. Odhady zamrazíme v pátek 9. 10. do 12:00 a hodnotit budeme poslední verzi před 14:00.</p>""",
    en="""<p><b>Today all series appear for the first time.</b> The order was fixed: first the AI update without the model (step A), then the AI with the model as input (step B). Both blind snapshots were locked with a git commit at 15:24. Only after that did we start reading odds (Fortuna from 15:35, then Tipsport).</p>
<h3>What changed</h3>
<ul>
<li><b>AI (no model):</b> only 2 districts changed since 2 Oct. In Litovel we moved 2 pp from Ošťádal to Kohajda after Ošťádal said he would not campaign. In Brno we fixed a 2 pp internal inconsistency in the previous version. The other 25 districts had no new facts and kept their forecast (rule: under 2 pp and no material event means no change).</li>
<li><b>AI + model:</b> the favourite changed in two districts: 21 (Sáblík instead of Láska) and 27 (Padevět instead of Čižinský). Favourites with a strong coalition base in the model got much stronger (Kladno, Praha 9, Pelhřimov, Hradec). Those whose personal brand the model cannot see got weaker (Strakonice, Karviná, Česká Lípa, Uherské Hradiště).</li>
<li><b>Betting:</b> the market favourite differs from “AI + model” in 9 of 27 districts. The market is much more confident in:
  <ul>
  <li>ANO candidates in Cheb (Tsoukernik), Pelhřimov (Kozár) and Přerov (Vrána, 82 % vs our 24 %);</li>
  <li>personal brands and local leaders: Láska, Čižinský, Řehka, Korč, Kohajda and Paták.</li>
  </ul>
  Our series lean more on the breadth of coalition support. This is the experiment's main bet, and the election will show who was right.</li>
<li><b>Blend</b> combines “AI + model” with the market mechanically (ρ = 0.55, AI weight about 31 %).</li>
</ul>
<h3>Mistakes and fixes</h3>
<ol>
<li><b>Bugs in the statistical model's inputs.</b> While auditing the inputs in step B, the agents found about a dozen bugs:
  <ul>
  <li>the “mayor” flag also fired on “former mayor”;</li>
  <li>former senators were matched by name only, so namesakes got mixed up (two Martin Dvořáks);</li>
  <li>a municipal coalition list was credited in full to every member party;</li>
  <li>the 2018 Prague list “Praha 7 SOBĚ” was not mapped;</li>
  <li>SLK was missing from the opposition bloc;</li>
  <li>KSČM had a zero base;</li>
  <li>calibration gives every minor candidate a floor of about 2 %.</li>
  </ul>
  <i>Fix:</i> we deliberately leave model v1 unchanged today, so that the Statistical model series changes only when its inputs do. The agents logged the bugs as deviations with reasons, and the fixes go into model v2 after round 1, published as a new version.</li>
<li><b>Double-counting informal backing.</b> In Vyškov and Litovel the agent re-ran the model with informal support “coded in” from parties not on the ballot. The training data is not coded that way, so the effect would have been counted twice. <i>Fix:</i> we added a rule (no model re-runs, only a moderate deviation above the typical level), and an independent review corrected both districts before the lock. Vyškov stayed around 76 %; Litovel is Ošťádal 36.5 % and Kohajda 31 %.</li>
<li><b>Channels through which odds could leak.</b> We found two:
  <ul>
  <li>the news file given to the agents contained our note about the model's favourite;</li>
  <li>the agent's auto-loaded memory contained numbers from an earlier market step for Plzeň, Brno and Kladno.</li>
  </ul>
  <i>Fix:</i> both were cleaned during the run, and the affected districts log it as a contamination risk. We cannot fully guarantee they are clean.</li>
<li><b>A bug in the update tool.</b> It copied the final (market-aware) number as the default “previous probability” instead of the blind one. The agent caught it in Plzeň. <i>Fix:</i> the updates started from the blind number; the tool fix comes before the next update.</li>
<li><b>An unclear market definition.</b> It was not clear whether Fortuna's market means the round-1 winner or the elected senator. <i>Resolution:</i> Tipsport explicitly says “overall”, and its numbers match Fortuna's, so we treat both as the seat winner. Fortuna's margin is high (11–78 %).</li>
<li><b>Tipsport rate limiting.</b> The site temporarily blocked betting during fast browsing. <i>Fix:</i> slower reading with pauses. We have odds for all 27 districts from both bookmakers.</li>
</ol>
<h3>Expectations recorded in advance (5 Oct, before any results)</h3>
<p>Nobody knows the results yet. So we write down now what we expect from each series, so that after the election we can also check our own read of where our weaknesses are.</p>
<ul>
<li><b>Expected ranking by Brier:</b> Blend ≈ Betting &gt; AI + model &gt; Statistical model ≈ AI. Combining two different sources usually scores best. In our earlier questions, the market beat our final in 5 of 6 cases.</li>
<li><b>AI:</b> its research was thin (search budget exhausted), it repeatedly made a construction error (runoff pairings inconsistent with round-1 shares), and it has barely changed since 2 Oct.</li>
<li><b>Statistical model:</b> only 3 election cycles of data, blind to personal brands, and known input bugs. On its own it is a rough estimate.</li>
<li><b>AI + model:</b> the risk is sticking too closely to the model, and overconfidence for favourites with a strong coalition (Kladno 80 %, Praha 9 79 %, Znojmo 84 %).</li>
<li><b>Betting:</b> a thin market with high margins; the two bookmakers likely watch each other.</li>
</ul>
<p><b>Main hypothesis.</b> In 9 districts the market has a different favourite from AI + model: 3 Cheb, 9 Plzeň, 15 Pelhřimov, 21 Praha 5, 27 Praha 1, 30 Kladno, 63 Přerov, 66 Litovel and 69 Frýdek-Místek. Two theories clash here. Ours says what matters is the breadth of coalition support and ANO's weakness in runoffs. The market trusts personal brands, local leaders and ANO candidates. Whoever calls more winners in these 9 districts will decide the series ranking more than the other 18 districts combined.</p>
<p><b>How we will score it.</b> The 27 districts are strongly correlated, so differences in mean Brier will not be statistically significant. Besides the overall score we will therefore publish a paired district-by-district comparison and a separate analysis of the 9 disputed districts.</p>
<p><b>Next:</b> the poll blackout starts Tue 6 Oct. AI changes only on new facts; Betting is read daily. Forecasts freeze Fri 9 Oct by 12:00, and the last version before 14:00 is the one scored.</p>"""))

JOURNAL.append(dict(
    date="2026-10-06",
    title_cs="Den 5: moratorium na průzkumy, AI beze změny, pohyb trhu v Kladně",
    title_en="Day 5: poll blackout, AI unchanged, market move in Kladno",
    cs="""<p><b>Dnes začalo moratorium na průzkumy.</b> Ve zprávách za poslední den jsme nenašli nic, co by změnilo situaci v některém obvodu. Proto jsme podle pravidel <b>AI ani AI s modelem neměnili</b>. Blind snapshoty jsme i tak zamkli commitem ještě před čtením kurzů. Jsou totožné s 5. 10.</p>
<h3>Co se změnilo</h3>
<ul>
<li><b>Zprávy:</b> Seznam Zprávy zveřejnily analýzu osmi „nejistých“ obvodů pro ANO (Trutnov, Příbram, Hradec Králové, Zlín, Kolín, Vyškov, Plzeň, Kladno). V Chebu kampaň Sandry Tsoukernik veřejně podporuje Michal David. Sociolog STEM upozorňuje, že ve Vyškově může Grolich vyhrát už v 1. kole. Jsou to spíš komentáře než nová fakta, odhady jsme kvůli nim neměnili.</li>
<li><b>Sázky:</b> největší pohyb je v Kladně. Fortuna zkrátila kurz na Klase z 20 na 6 a prodloužila Šípovou z 2,0 na 2,8. Šípová v konsenzu klesla o 5 p.b. na 29 %, Paták zůstává favoritem (42 %). Menší posuny: Žďár (Klement +6), Litovel (Kohajda +4), Česká Lípa (Volfová +3). Favorit trhu se nezměnil nikde.</li>
<li><b>Blend</b> se mění jen s trhem.</li>
</ul>
<h3>Externí benchmark: datový model Seznam Zpráv</h3>
<p>Seznam Zprávy 5. 10. zveřejnily <a href="https://www.seznamzpravy.cz/clanek/volby-do-senatu-datovy-model-predpovida-dva-scenare-boje-ano-o-senat-316700">datový model</a>. Ten odhaduje jen šanci kandidátů ANO na postup do 2. kola a jejich procenta v 1. kole, a to ve dvou scénářích. Viděli jsme ho 6. 10. <b>Jako vstup ho nepoužíváme</b>. Čísla jsme uložili zvlášť a do podkladů pro agenty se nedostanou. Po 1. kole jeho střední scénář porovnáme s naším statistickým modelem a s AI s modelem na 23 kandidátech ANO (Brier na postup a chyba v procentech).</p>
<p><b>Předem zapsáno:</b> Seznam Zprávy čekají 13,4 postupů ANO v nepříznivém, 17,3 ve středním a 21,2 v příznivém scénáři. Náš statistický model čeká 14,5. Podle stupnice Seznam Zpráv (16 a méně = neúspěch) tedy předpovídáme spíš neúspěch ANO v 1. kole. Největší rozdíly proti střednímu scénáři Seznam Zpráv jsou v Hradci Králové, ve Zlíně, ve Znojmě a v Praze 5 (u nás slabší ANO) a ve Vyškově (u nás silnější).</p>
<h3>Nové zdroje dne</h3>
<p>Zdroje jsme dnes jen zapsali, žádný z nich nezměnil odhady.</p>
<ul>
<li>Seznam Zprávy (6. 10.): <a href="https://www.seznamzpravy.cz/clanek/volby-do-senatu-chce-ano-triumf-v-senatu-nasli-jsme-osm-mist-kde-musi-zabrat-316682">Chce ANO triumf v Senátu? Našli jsme osm míst, kde musí zabrat</a>. Jde o nejisté obvody pro ANO, Michala Davida v Chebu a komentář STEM k Vyškovu a České Lípě.</li>
<li>Seznam Zprávy (5. 10.): <a href="https://www.seznamzpravy.cz/clanek/volby-do-senatu-datovy-model-predpovida-dva-scenare-boje-ano-o-senat-316700">Datový model předpovídá dva scénáře boje ANO o Senát</a>. Je to externí benchmark, ne vstup (viz výše).</li>
<li>Noviny Zblízka (5. 10.): <a href="https://noviny-zblizka.cz/ostatni/ivo-tresl-v-senatu-odpracoval-sest-let-ted-zkusi-znovu-ziskat-duveru-volicu-jako-lekar-dostal-podporu-i-od-kolegy-jana-pirka/">Ivo Trešl v Senátu odpracoval šest let…</a> Obhájce v Lounech (obvod 6) podpořil lékař Jan Pirek. Malá zpráva.</li>
<li>Orlický.net (5. 10.): <a href="https://www.orlicky.net/clanek.php?id_zpravy=11547167091791211887">Senátní duel na Rychnovsku a Pardubicku</a>. Odpovědi Sadovského, Grulich odpověděl později (obvod 48). Bez dopadu.</li>
<li>Prověřeno a vyřazeno: Seznam Zprávy, <a href="https://www.seznamzpravy.cz/clanek/domaci-kauzy-chirurg-podle-zalobce-zproneveril-penize-trva-na-nevine-a-kandiduje-za-ods-316751">Chirurg podle žalobce zpronevěřil peníze…</a> Jde o komunálního kandidáta na Praze 3, ne do Senátu.</li>
</ul>
<h3>Chyby a nápravy</h3>
<ol>
<li><b>Chybějící seznam trhů Tipsportu.</b> Ze včerejška jsme měli zapsaná ID trhů jen pro polovinu obvodů. <i>Náprava:</i> našli jsme stránku kategorie se všemi 27 obvody a ID jsme zapsali do postupu.</li>
<li><b>Zjednodušené čtení Tipsportu.</b> Přehledová stránka ukazuje jen kurz „Ano“. Detail jsme otevřeli jen u pěti obvodů, kde se kurz Ano změnil. U ostatních jsme kurz „Ne“ převzali z 5. 10. <i>Riziko:</i> malé, pokud se změnil jen kurz Ne. Od zítřka budeme Ne kontrolovat namátkově.</li>
<li><b>Chyba v generátoru webu.</b> Box „Co je dnes nového“ spadl při porovnání Sázek s předchozím dnem, protože snapshot trhu ukládá rozdělení v jiném tvaru. Dnes šlo o první den, kdy předchozí snapshot trhu existoval. <i>Náprava:</i> opravili jsme načítání. Snapshoty se nezměnily.</li>
</ol>
<p><b>Dál:</b> ve středu a ve čtvrtek opět zprávy a Sázky. Odhady zamrazíme v pátek 9. 10. do 12:00.</p>""",
    en="""<p><b>The poll blackout started today.</b> The last day's news contained nothing that changes the race in any district, so under our rules <b>AI and AI + model were not changed</b>. We still locked the blind snapshots with a commit before reading the odds. They are identical to 5 Oct.</p>
<h3>What changed</h3>
<ul>
<li><b>News:</b> Seznam Zprávy published an analysis of eight “uncertain” districts for ANO (Trutnov, Příbram, Hradec Králové, Zlín, Kolín, Vyškov, Plzeň, Kladno). In Cheb, singer Michal David publicly backs Sandra Tsoukernik's campaign. A STEM sociologist warns that Grolich may win Vyškov outright in round 1. This is commentary more than new facts; we did not change our forecasts.</li>
<li><b>Betting:</b> the biggest move is in Kladno. Fortuna cut Klas from 20 to 6 and lengthened Šípová from 2.0 to 2.8. Šípová fell 5 pp to 29 % in the consensus; Paták remains the favourite (42 %). Smaller moves: Žďár (Klement +6), Litovel (Kohajda +4), Česká Lípa (Volfová +3). The market favourite did not change anywhere.</li>
<li><b>Blend</b> moves only with the market.</li>
</ul>
<h3>External benchmark: the Seznam Zprávy data model</h3>
<p>On 5 Oct Seznam Zprávy published a <a href="https://www.seznamzpravy.cz/clanek/volby-do-senatu-datovy-model-predpovida-dva-scenare-boje-ano-o-senat-316700">data model</a>. It estimates only ANO candidates' chances of reaching the runoff and their round-1 shares, in two scenarios. We saw it on 6 Oct. <b>We do not use it as an input</b>: its numbers are stored separately and are kept out of the agents' materials. After round 1 we will compare its middle scenario with our statistical model and AI + model on the 23 ANO candidates (Brier on advancing and error in vote share).</p>
<p><b>Recorded in advance:</b> Seznam Zprávy expects 13.4 ANO candidates to advance in the unfavourable scenario, 17.3 in the middle and 21.2 in the favourable one. Our statistical model expects 14.5. On the Seznam Zprávy scale (16 or fewer = failure) we therefore forecast a weak round 1 for ANO. The biggest differences from the Seznam Zprávy middle scenario are Hradec Králové, Zlín, Znojmo and Praha 5 (ANO weaker in our model) and Vyškov (stronger in ours).</p>
<h3>New sources today</h3>
<p>Today's sources were only logged; none of them changed the forecasts.</p>
<ul>
<li>Seznam Zprávy (6 Oct): <a href="https://www.seznamzpravy.cz/clanek/volby-do-senatu-chce-ano-triumf-v-senatu-nasli-jsme-osm-mist-kde-musi-zabrat-316682">Chce ANO triumf v Senátu? Našli jsme osm míst, kde musí zabrat</a>. It covers uncertain districts for ANO, Michal David in Cheb, and STEM's comment on Vyškov and Česká Lípa.</li>
<li>Seznam Zprávy (5 Oct): <a href="https://www.seznamzpravy.cz/clanek/volby-do-senatu-datovy-model-predpovida-dva-scenare-boje-ano-o-senat-316700">Datový model předpovídá dva scénáře boje ANO o Senát</a>. External benchmark, not an input (see above).</li>
<li>Noviny Zblízka (5 Oct): <a href="https://noviny-zblizka.cz/ostatni/ivo-tresl-v-senatu-odpracoval-sest-let-ted-zkusi-znovu-ziskat-duveru-volicu-jako-lekar-dostal-podporu-i-od-kolegy-jana-pirka/">Ivo Trešl v Senátu odpracoval šest let…</a> The incumbent in Louny (district 6) was endorsed by physician Jan Pirek. Minor.</li>
<li>Orlický.net (5 Oct): <a href="https://www.orlicky.net/clanek.php?id_zpravy=11547167091791211887">Senátní duel na Rychnovsku a Pardubicku</a>. Sadovský's answers; Grulich answered later (district 48). No impact.</li>
<li>Checked and discarded: Seznam Zprávy, <a href="https://www.seznamzpravy.cz/clanek/domaci-kauzy-chirurg-podle-zalobce-zproneveril-penize-trva-na-nevine-a-kandiduje-za-ods-316751">Chirurg podle žalobce zpronevěřil peníze…</a> The person is a municipal candidate in Praha 3, not a Senate candidate.</li>
</ul>
<h3>Mistakes and fixes</h3>
<ol>
<li><b>Missing list of Tipsport markets.</b> Yesterday we had recorded market IDs for only half of the districts. <i>Fix:</i> we found the category page with all 27 districts and recorded the IDs in our procedure.</li>
<li><b>Simplified Tipsport reading.</b> The overview page shows only the “Yes” price. We opened the detail only for the five districts where the Yes price changed and carried the “No” price over from 5 Oct for the rest. <i>Risk:</i> small, if only the No price moved. From tomorrow we will spot-check No prices.</li>
<li><b>A bug in the site generator.</b> The “What's new today” box crashed when comparing Betting with the previous day, because the market snapshot stores its distribution in a different shape. Today was the first day a previous market snapshot existed. <i>Fix:</i> we fixed the loader. No snapshot changed.</li>
</ol>
<p><b>Next:</b> news and Betting again on Wednesday and Thursday. Forecasts freeze Fri 9 Oct by 12:00.</p>"""))

JOURNAL.append(dict(
    date="2026-10-07",
    title_cs="Den 6: AI beze změny, objevená mezera v profilech kandidátů, trh posiluje Volfovou",
    title_en="Day 6: AI unchanged, a gap in candidate profiles, the market warms to Volfová",
    cs="""<p><b>AI ani AI s modelem se dnes nemění.</b> Prošli jsme zprávy o všech 154 kandidátech za poslední dva dny. Nenašli jsme nic, co by změnilo situaci v některém obvodu. Blind snapshoty jsme zamkli commitem ve 21:42, ještě před čtením kurzů. Jsou totožné s 6. 10.</p>
<h3>Co se změnilo</h3>
<ul>
<li><b>Zprávy:</b> v České Lípě musel Babiš kvůli nemoci vynechat závěrečné mítinky. Volfovou místo něj podpořili ministři a on se připojoval z postele přes mobil. V Chebu pokračuje negativní mediální obraz Sandry Tsoukernik. Ve Vyškově se ostře pře ministryně Schillerová s Grolichem. Jde o drobnosti, odhady jsme kvůli nim neměnili.</li>
<li><b>Sázky:</b> největší posuny jsou v České Lípě (Volfová +6 p.b. na 28 %, Půta 56 %), na Kolínsku (Kašpar +6 na 71 %), v Praze 5 (Láska +6 na 59 %) a v Příbrami (Štěpánek +5). Ve Frýdku-Místku se favorit trhu otočil: Pešatová 43 %, Korč 41 %. Rozdíl je ale v mezích šumu. V Kladně se trh téměř nehnul (Paták 44, Šípová 28).</li>
<li><b>Blend</b> se mění jen s trhem.</li>
</ul>
<p>Kurzy jsme četli kolem 21:45–22:10, tedy během večerní debaty lídrů nebo těsně po ní. Pohyby proti včerejšku proto zahrnují celý den a efekt debaty od nich neumíme oddělit.</p>
<h3>Nové zdroje dne</h3>
<p>Zdroje jsme dnes jen zapsali, žádný z nich nezměnil odhady.</p>
<ul>
<li>Deník N (7. 10.): <a href="https://denikn.cz/2208353/nemocny-premier-agitoval-z-postele-na-ceskolipsku-babis-chce-sebrat-klicovy-senatni-obvod/">Nemocný premiér agitoval z postele na Českolipsku</a>. Česká Lípa (36), Babiš chybí v závěru kampaně. Malý dopad.</li>
<li>forum24 (7. 10.): <a href="https://www.forum24.cz/kde-je-17-milionu-pane-tsoukernik-olga-menzelova-vytahla-na-senatni-kandidatku-ano-dluh-jejiho-manzela">Kde je 1,7 milionu, pane Tsoukernik?</a> Cheb (3), spor o dluh manžela kandidátky. Nic nového pro výsledek.</li>
<li>Zdopravy.cz: <a href="https://zdopravy.cz/jan-klas-po-19-letech-konci-v-cele-rizeni-letoveho-provozu-racionalni-zaver-napsal-zamestnancum-295549/">Jan Klas po 19 letech končí v čele Řízení letového provozu</a>. Kladno (30), starší zpráva, viz Chyby a nápravy.</li>
<li>iROZHLAS: <a href="https://www.irozhlas.cz/zpravy-domov/budoval-si-kolem-sebe-kult-osobnosti-zastupitele-odvolali-primatora-frydku_2606101327_vaa">Zastupitelé odvolali primátora Frýdku-Místku Petra Korče</a> (červen 2026). Frýdek-Místek (69), starší zpráva, viz Chyby a nápravy.</li>
<li>CNN Prima NEWS: <a href="https://cnn.iprima.cz/anketa-kdo-ma-byt-senatorem-za-kladensko-a-litovelsko-hlasujte-pro-sveho-favorita-522624">divácká anketa po debatě 23. 9.</a> Kladno: nejvíc hlasů získal Gerloch. Jde o anketu pro přihlášené diváky bez čísel, takže váha je zanedbatelná.</li>
<li>Prověřeno a vyřazeno: Novinky, „Špičky ODS vyzvaly lídra Prahy 1 Dvořáka, aby odstoupil“. Týká se komunální kandidátky, ne Senátu.</li>
</ul>
<h3>Chyby a nápravy</h3>
<ol>
<li><b>Chybějící profily „vedlejších“ kandidátů.</b> Research z 2. 10. běžel bez webového vyhledávání (vyčerpaný limit). U kandidátů mimo hlavní dvojici proto chybí životopis. Dnes jsme narazili na dva případy. Jan Klas (Kladno, Naše Česko) byl 19 let generálním ředitelem Řízení letového provozu. U nás figuroval jako obecný minoritní kandidát. Petra Korče (Frýdek-Místek) zastupitelé v červnu odvolali z funkce primátora, náš research znal jen „funkce neobsazena“. <i>Proč jsme odhady neměnili:</i> na Klase jsme se zaměřili kvůli včerejšímu pohybu kurzů. Update vyvolaný trhem by z AI série udělal kopii Sázek a znehodnotil srovnání. Navíc odhadovaný dopad na to, kdo vyhraje, je malý (1–3 p.b.). U Korče není jasný ani směr dopadu. <i>Náprava:</i> do zadání pro příští běhy přidáváme povinný krok „životopis každého kandidáta na lístku“. Mezeru po 1. kole vyhodnotíme jako známé omezení AI série.</li>
<li><b>Kurzy zahlédnuté před zámkem.</b> Při hledání zpráv ukázal Google ve výsledcích úryvek ze sázkového webu s kurzy pro Prahu 5, 9 a 1. Bylo to asi hodinu před zamčením snapshotů. Dnes to nemělo vliv, protože AI ani AI s modelem jsme neměnili. <i>Náprava:</i> dotazy na zprávy teď vylučují sázkové weby.</li>
<li><b>Výpadek Tipsportu.</b> Po otevření 12 detailů Tipsport zablokoval přístup („nedostupnost internetového sázení“). U tří obvodů, kde se změnil kurz Ano (Žďár, Brno, Frýdek-Místek), jsme kurz Ne dopočítali tak, že jsme zachovali včerejší marži sázkové kanceláře. U deseti obvodů, kde jsme měli oba kurzy, se marže od včerejška lišila nejvýš o 0,15 %. Namátková kontrola Ne u nezměněných obvodů (Kladno, Hradec Králové) potvrdila, že se Ne nezměnilo.</li>
</ol>
<p><b>Dál:</b> ve čtvrtek naposledy zprávy a Sázky. Odhady zamrazíme v pátek 9. 10. do 12:00.</p>""",
    en="""<p><b>AI and AI + model are unchanged today.</b> We went through the last two days of news on all 154 candidates and found nothing that changes the race in any district. The blind snapshots were locked with a commit at 21:42, before reading the odds. They are identical to 6 Oct.</p>
<h3>What changed</h3>
<ul>
<li><b>News:</b> in Česká Lípa, Babiš was ill and missed the final rallies. Ministers campaigned for Volfová in his place and he joined by phone video from bed. In Cheb, negative press around Sandra Tsoukernik continues. In Vyškov, minister Schillerová and Grolich traded sharp attacks. These are minor; we did not change our forecasts.</li>
<li><b>Betting:</b> the biggest moves are in Česká Lípa (Volfová +6 pp to 28 %, Půta 56 %), Kolín (Kašpar +6 to 71 %), Praha 5 (Láska +6 to 59 %) and Příbram (Štěpánek +5). In Frýdek-Místek the market favourite flipped: Pešatová 43 %, Korč 41 %. The gap is within noise. In Kladno the market barely moved (Paták 44, Šípová 28).</li>
<li><b>Blend</b> moves only with the market.</li>
</ul>
<p>Odds were read around 21:45–22:10, during or just after the evening leaders' debate. The moves since yesterday therefore cover the whole day, and we cannot separate the effect of the debate.</p>
<h3>New sources today</h3>
<p>Today's sources were only logged; none of them changed the forecasts.</p>
<ul>
<li>Deník N (7 Oct): <a href="https://denikn.cz/2208353/nemocny-premier-agitoval-z-postele-na-ceskolipsku-babis-chce-sebrat-klicovy-senatni-obvod/">Nemocný premiér agitoval z postele na Českolipsku</a>. Česká Lípa (36): Babiš missing at the end of the campaign. Small impact.</li>
<li>forum24 (7 Oct): <a href="https://www.forum24.cz/kde-je-17-milionu-pane-tsoukernik-olga-menzelova-vytahla-na-senatni-kandidatku-ano-dluh-jejiho-manzela">Kde je 1,7 milionu, pane Tsoukernik?</a> Cheb (3): a dispute over the candidate's husband's debt. Nothing new for the outcome.</li>
<li>Zdopravy.cz: <a href="https://zdopravy.cz/jan-klas-po-19-letech-konci-v-cele-rizeni-letoveho-provozu-racionalni-zaver-napsal-zamestnancum-295549/">Jan Klas po 19 letech končí v čele Řízení letového provozu</a>. Kladno (30), older news; see Mistakes and fixes.</li>
<li>iROZHLAS: <a href="https://www.irozhlas.cz/zpravy-domov/budoval-si-kolem-sebe-kult-osobnosti-zastupitele-odvolali-primatora-frydku_2606101327_vaa">Zastupitelé odvolali primátora Frýdku-Místku Petra Korče</a> (June 2026). Frýdek-Místek (69), older news; see Mistakes and fixes.</li>
<li>CNN Prima NEWS: <a href="https://cnn.iprima.cz/anketa-kdo-ma-byt-senatorem-za-kladensko-a-litovelsko-hlasujte-pro-sveho-favorita-522624">viewer poll after the 23 Sep debate</a>. Kladno: Gerloch got the most votes. A poll for logged-in viewers with no numbers, so negligible weight.</li>
<li>Checked and discarded: Novinky, “ODS leaders asked Praha 1 list leader Dvořák to step down”. This concerns a municipal list, not the Senate.</li>
</ul>
<h3>Mistakes and fixes</h3>
<ol>
<li><b>Missing profiles of “minor” candidates.</b> The 2 Oct research ran without web search (the limit was used up), so candidates outside the main pair lack a CV. Today we found two cases. Jan Klas (Kladno, Naše Česko) ran Czech air traffic control (ŘLP) for 19 years; we treated him as a generic minor candidate. Petr Korč (Frýdek-Místek) was removed as mayor by the city council in June; our research only knew the post was vacant. <i>Why we did not change the forecasts:</i> we looked into Klas because the odds moved yesterday. A market-triggered update would turn the AI series into a copy of Betting and spoil the comparison. The estimated effect on who wins is also small (1–3 pp), and for Korč even the direction is unclear. <i>Fix:</i> future briefs get a mandatory “CV of every candidate on the ballot” step. After round 1 we will score this gap as a known limitation of the AI series.</li>
<li><b>Odds seen before the lock.</b> While searching the news, Google showed a snippet from a betting site with odds for Praha 5, 9 and 1, about an hour before the snapshots were locked. It had no effect today because AI and AI + model were not changed. <i>Fix:</i> news queries now exclude betting sites.</li>
<li><b>Tipsport outage.</b> After 12 detail pages Tipsport blocked access (“betting unavailable”). For the three districts where the Yes price changed (Žďár, Brno, Frýdek-Místek) we computed the No price by keeping yesterday's bookmaker margin. In the ten districts where we had both prices, the margin moved by at most 0.15 % since yesterday. Spot-checks of No prices in unchanged districts (Kladno, Hradec Králové) confirmed they had not moved.</li>
</ol>
<p><b>Next:</b> news and Betting for the last time on Thursday. Forecasts freeze Fri 9 Oct by 12:00.</p>"""))

JOURNAL.append(dict(
    date="2026-10-08",
    title_cs="Den 7: poslední den kampaně, AI beze změny, předregistrace benchmarku z Wikipedie",
    title_en="Day 7: last day of the campaign, AI unchanged, a Wikipedia benchmark pre-registered",
    cs="""<p><b>AI ani AI s modelem se nemění.</b> Ve zprávách z posledního dne kampaně ani v reakcích na středeční debatu lídrů jsme nenašli nic, co by změnilo situaci v některém obvodu. Snapshoty jsme zamkli v 16:47, ještě před čtením kurzů. Tyto verze AI a AI s modelem jsou s velkou pravděpodobností ty, které budeme hodnotit. Zítra do 12:00 je změníme jen tehdy, pokud se objeví zásadní fakt.</p>
<h3>Co se změnilo</h3>
<ul>
<li><b>Zprávy:</b> Přerovský deník zveřejnil profily všech čtyř kandidátů v Přerově. Oba hlavní soupeři, primátor Vrána (ANO) a radní Navařík (ODS), jsou ze stejného vedení města. V Chebu pokračují negativní články o Sandře Tsoukernik. Debata lídrů nepřinesla nic konkrétního k obvodům.</li>
<li><b>Sázky:</b> v Praze 1 se favorit trhu otočil z Jana Čižinského na Padevěta (45 %). Padevět je i favoritem AI s modelem. V Pelhřimově roste Med (+6 p.b. na 28 %), Kozár zůstává favoritem (45 %). V Praze 5 posiluje Láska (64 %), ve Žďáru Klement (73 %). Ve dvou sporných obvodech (Pelhřimov, Praha 1) se trh přiblížil našemu odhadu, ve dvou (Praha 5, Litovel) se od něj vzdálil. Celkový rozdíl mezi trhem a AI s modelem zůstává zhruba stejný.</li>
<li><b>Blend</b> se mění jen s trhem.</li>
</ul>
<h3>Předem zapsáno: benchmark z Wikipedie</h3>
<p>Spočítali jsme denní návštěvnost článků o kandidátech na české Wikipedii (1. 8.–7. 10., článek má 93 ze 154 kandidátů). Jako vstup ji <b>nepoužíváme</b>, protože pozornost táhnou hlavně kauzy a známá jména. Po volbách ji ale vyhodnotíme jako jednoduchý srovnávací benchmark: <i>vyhraje nejčtenější kandidát obvodu</i> (průměr 24. 9.–7. 10.). Předpověď tohoto pravidla:</p>
<p class="muted">3 Tsoukernik · 6 Steiner · 9 Řehka · 12 Ušatý · 15 Chalupský · 18 Štěpánek · 21 Šarapatka · 24 Pecková · 27 J. Čižinský · 30 Gerloch · 33 Linhart · 36 Půta · 39 Sobotka · 42 Sehnal · 45 Nebeská · 48 Grulich · 51 Šmarda · 54 Rédová Fajmonová · 57 Grolich · 60 Papoušek · 63 Obrtel · 66 Kohajda · 69 Lisková · 72 Šimetka · 75 Szyja · 78 Goláň · 81 Balaštíková</p>
<p>Nejčtenější kandidát je favoritem trhu ve 13 z 25 obvodů, favoritem AI s modelem v 9. Google Trends jsme zkusili taky, ale pro senátní obvody vracejí samé nuly a pletou si jmenovce, proto je nepoužíváme. Data jsou v repozitáři.</p>
<h3>Předem zapsáno: hypotéza o domácích baštách</h3>
<p>Podezíráme, že náš statistický model podceňuje kandidáty s velkou domácí baštou (viz Chyby a nápravy). Abychom si skupinu nemohli vybrat až podle výsledků, určili jsme ji mechanicky z dat ČSÚ: <i>současný starosta nebo primátor obce, kde žije aspoň 15 % voličů obvodu</i>.</p>
<ul>
<li>15 Kozár (Jindřichův Hradec, 16 % voličů), model 1. kolo 22,2 %</li>
<li>27 J. Čižinský (Praha 7, 37 %), model 22,9 %</li>
<li>36 Volfová (Česká Lípa, 25 %), model 28,8 %</li>
<li>42 Kašpar (Kolín, 21 %), model 30,3 %</li>
<li>63 Vrána (Přerov, 33 %), model 31,9 %</li>
<li>75 Brzyszkowská (Orlová, 28 %), model 36,9 %</li>
</ul>
<p><b>Metrika:</b> skutečný výsledek v 1. kole minus průměr statistického modelu. <b>Srovnávací skupina:</b> ostatní kandidáti, kterým model dává aspoň 15 %. <b>Hypotéza:</b> baštoví kandidáti překonají model v průměru alespoň o 3 p.b. víc než srovnávací skupina. <b>Vyvráceno</b>, pokud bude rozdíl nulový nebo záporný. <i>Omezení:</i> šest kandidátů je malý vzorek. Starostka Poruby Baránková Vilamová vypadla, protože data ČSÚ za Ostravu nerozlišují městské obvody.</p>
<h3>Předem zapsáno: pravidlo pro sobotní předpovědi STEM</h3>
<p>CNN Prima ohlásila, že v sobotu po sečtení zhruba 80 % hlasů zveřejní pravděpodobnosti výhry ve 2. kole od analytiků STEM. Před 1. kolem žádnou předpověď nezveřejnila. Aby naše updaty po 1. kole nebyly jejich ozvěnou, <b>uděláme a zamkneme je commitem dřív, než se na čísla STEM podíváme</b>. Ta si pak zapíšeme jako externí benchmark pro 2. kolo, podobně jako model Seznam Zpráv pro 1. kolo.</p>
<h3>Nové zdroje dne</h3>
<p>Zdroje jsme dnes jen zapsali, žádný z nich nezměnil odhady.</p>
<ul>
<li>Přerovský deník (8. 10.): <a href="https://prerovsky.denik.cz/zpravy-region/o-senat-se-na-prerovsku-utkaji-ctyri-osobnosti-tady-jsou-jejich-profily/">O Senát se na Přerovsku utkají čtyři osobnosti</a>. Přerov (63), profily kandidátů.</li>
<li>INFO.CZ a forum24 (8. 10.): další články o Sandře Tsoukernik a Rozvadově. Cheb (3), nic nového pro výsledek.</li>
<li>Odkryto a Praha na dlani (8. 10.): Láskův protikorupční tým a jeho kampaňové výdaje. Praha 5 (21), drobnost.</li>
<li>forum24 (8. 10.): dvacet uskupení nestihlo oznámit sponzory. O které jde, jsme neověřovali.</li>
<li>Neotevřeno: iDNES „Zeman jako maskot voleb“ (vyžaduje souhlas s cílenou reklamou, podle adresy jde hlavně o komunální volby) a CNN Prima „předpovědi analytiků“ (cizí předpověď, ne vstup).</li>
</ul>
<h3>Chyby a nápravy</h3>
<ol>
<li><b>Druhá mezera v researchi: geografie uvnitř obvodu.</b> Z dat ČSÚ po obcích jsme zjistili, že Vrána v roce 2020 ve 2. kole <b>vyhrál město Přerov 55:45</b> a prohrál až na venkově. Náš model zná funkci „starosta“, ale ne velikost domácí bašty ani bašty soupeřů. Podobně Šípová (Kladno) bydlí v Doksech mimo obvod, kdežto Paták je z Kladna, kde žije 45 % voličů. Historicky ale bašta automaticky nevyhrává: starostové největšího města obvodu v letech 2020–2024 postoupili do 2. kola jen ve 27 % případů. <i>Proč jsme odhady neměnili:</i> všechny nálezy jdou směrem k trhu a analýzu jsme dělali kvůli sporu s trhem. Úprava den před uzávěrkou by byla skryté dorovnání na Sázky. <i>Náprava:</i> do modelu v2 přidáváme proměnnou „podíl voličů domácí obce × funkce × strana“ a historické výsledky po obcích. Po 1. kole změříme, jestli kandidáti s baštou model systematicky překonali.</li>
<li><b>Včerejší dopočet kurzů Tipsportu se potvrdil.</b> U Brna (5,62) a Frýdku-Místku (1,67) odpovídal dopočtený kurz „Ne“ přesně skutečnému. Dnes jsme stránky otevírali pomaleji a Tipsport nás neblokoval.</li>
</ol>
<p><b>Dál:</b> v pátek dopoledne poslední rychlá kontrola zpráv a závěrečné kurzy. Odhady zamrazíme do 12:00, výsledky 1. kola budou v sobotu.</p>""",
    en="""<p><b>AI and AI + model are unchanged.</b> The news from the last day of the campaign and the reactions to Wednesday's leaders' debate contained nothing that changes the race in any district. The snapshots were locked at 16:47, before reading the odds. These versions of AI and AI + model will very likely be the ones scored. By 12:00 tomorrow we will change them only if a major fact appears.</p>
<h3>What changed</h3>
<ul>
<li><b>News:</b> Přerovský deník profiled all four Přerov candidates. Both front-runners, mayor Vrána (ANO) and councillor Navařík (ODS), sit in the same city leadership. In Cheb, negative coverage of Sandra Tsoukernik continues. The leaders' debate brought nothing district-specific.</li>
<li><b>Betting:</b> in Praha 1 the market favourite flipped from Jan Čižinský to Padevět (45 %), who is also the AI + model favourite. In Pelhřimov, Med rises (+6 pp to 28 %) while Kozár stays the favourite (45 %). Láska strengthens in Praha 5 (64 %) and Klement in Žďár (73 %). In two disputed districts (Pelhřimov, Praha 1) the market moved towards our forecast, in two (Praha 5, Litovel) away from it. The overall gap between the market and AI + model is roughly unchanged.</li>
<li><b>Blend</b> moves only with the market.</li>
</ul>
<h3>Recorded in advance: a Wikipedia benchmark</h3>
<p>We collected daily Czech Wikipedia pageviews of the candidates' articles (1 Aug–7 Oct; 93 of 154 candidates have an article). We do <b>not</b> use them as an input, because attention is driven mostly by scandals and famous names. After the election we will score them as a simple benchmark: <i>the most-viewed candidate in a district wins</i> (average 24 Sep–7 Oct). This rule predicts:</p>
<p class="muted">3 Tsoukernik · 6 Steiner · 9 Řehka · 12 Ušatý · 15 Chalupský · 18 Štěpánek · 21 Šarapatka · 24 Pecková · 27 J. Čižinský · 30 Gerloch · 33 Linhart · 36 Půta · 39 Sobotka · 42 Sehnal · 45 Nebeská · 48 Grulich · 51 Šmarda · 54 Rédová Fajmonová · 57 Grolich · 60 Papoušek · 63 Obrtel · 66 Kohajda · 69 Lisková · 72 Šimetka · 75 Szyja · 78 Goláň · 81 Balaštíková</p>
<p>The most-viewed candidate is the market favourite in 13 of 25 districts and the AI + model favourite in 9. We also tried Google Trends, but for Senate districts it returns mostly zeros and confuses namesakes, so we do not use it. The data are in the repository.</p>
<h3>Recorded in advance: the home-base hypothesis</h3>
<p>We suspect our statistical model underrates candidates with a large home base (see Mistakes and fixes). So that we cannot choose the group after seeing the results, we defined it mechanically from ČSÚ data: <i>a sitting mayor of a municipality that is home to at least 15 % of the district's voters</i>.</p>
<ul>
<li>15 Kozár (Jindřichův Hradec, 16 % of voters), model round 1 22.2 %</li>
<li>27 J. Čižinský (Praha 7, 37 %), model 22.9 %</li>
<li>36 Volfová (Česká Lípa, 25 %), model 28.8 %</li>
<li>42 Kašpar (Kolín, 21 %), model 30.3 %</li>
<li>63 Vrána (Přerov, 33 %), model 31.9 %</li>
<li>75 Brzyszkowská (Orlová, 28 %), model 36.9 %</li>
</ul>
<p><b>Metric:</b> actual round-1 share minus the statistical model's mean. <b>Comparison group:</b> all other candidates the model gives at least 15 %. <b>Hypothesis:</b> home-base candidates beat the model by at least 3 pp more on average than the comparison group. <b>Refuted</b> if the difference is zero or negative. <i>Limitations:</i> six candidates is a small sample. Poruba mayor Baránková Vilamová drops out because ČSÚ data do not split Ostrava into city districts.</p>
<h3>Recorded in advance: a rule for Saturday's STEM predictions</h3>
<p>CNN Prima announced that on Saturday, once about 80 % of the votes are counted, it will publish runoff win probabilities from STEM analysts. It published no forecast before round 1. To keep our post-round-1 updates from echoing them, <b>we will make and lock our updates with a commit before looking at the STEM numbers</b>. We will then record those as an external benchmark for round 2, just as the Seznam Zprávy model serves for round 1.</p>
<h3>New sources today</h3>
<p>Today's sources were only logged; none of them changed the forecasts.</p>
<ul>
<li>Přerovský deník (8 Oct): <a href="https://prerovsky.denik.cz/zpravy-region/o-senat-se-na-prerovsku-utkaji-ctyri-osobnosti-tady-jsou-jejich-profily/">O Senát se na Přerovsku utkají čtyři osobnosti</a>. Přerov (63), candidate profiles.</li>
<li>INFO.CZ and forum24 (8 Oct): more pieces on Sandra Tsoukernik and Rozvadov. Cheb (3), nothing new for the outcome.</li>
<li>Odkryto and Praha na dlani (8 Oct): Láska's anti-corruption team and his campaign spending. Praha 5 (21), minor.</li>
<li>forum24 (8 Oct): twenty groupings missed the deadline to disclose sponsors. We did not check which ones.</li>
<li>Not opened: iDNES “Zeman as the election mascot” (requires consent to targeted ads; per its URL mainly about municipal elections) and CNN Prima “analysts' predictions” (someone else's forecast, not an input).</li>
</ul>
<h3>Mistakes and fixes</h3>
<ol>
<li><b>A second research gap: geography within a district.</b> ČSÚ municipality-level data show that in 2020 Vrána <b>won the city of Přerov 55:45</b> in the runoff and lost only in the countryside. Our model knows the “mayor” role but not the size of a candidate's home base or the opponents' bases. Similarly, Šípová (Kladno) lives in Doksy, outside the district, while Paták is from Kladno, home to 45 % of the district's voters. Historically, however, a home base does not win automatically: mayors of a district's largest town reached the runoff only 27 % of the time in 2020–2024. <i>Why we did not change the forecasts:</i> every finding points towards the market, and we ran the analysis because of a disagreement with the market. A change the day before the freeze would be a hidden move towards Betting. <i>Fix:</i> model v2 gets a “home-town share of voters × role × party” variable and municipality-level history. After round 1 we will measure whether candidates with a home base systematically beat the model.</li>
<li><b>Yesterday's Tipsport imputation held up.</b> In Brno (5.62) and Frýdek-Místek (1.67) the imputed “No” price matched the actual one exactly. Today we opened pages more slowly and Tipsport did not block us.</li>
</ol>
<p><b>Next:</b> on Friday morning a last quick news check and the closing odds. Forecasts freeze by 12:00; round 1 results come on Saturday.</p>"""))

JOURNAL.append(dict(
    date="2026-10-09",
    title_cs="Den 8: freeze. Tyto odhady hodnotíme",
    title_en="Day 8: freeze. These are the forecasts we will score",
    cs="""<p><b>Odhady jsou zamrazené.</b> Poslední kontrola zpráv (10:25–10:35) nenašla nic, co by změnilo situaci v některém obvodu. AI a AI s modelem jsme proto zamkli v 10:35 beze změny, ještě před čtením kurzů (commit <code>ced8415</code>). <b>Hodnotit budeme snapshoty z 9. 10.</b>: AI, Statistický model (stav 3. 10.), AI s modelem, Sázky (kurzy čtené 10:36–10:42) a Blend. Volby začínají dnes ve 14:00. <i>Poznámka: tato stránka vyšla až odpoledne, po otevření volebních místností. Odhady se tím nemění. Že vznikly před 14:00, dokládají časy commitů v repozitáři (lock 10:35, build 10:42).</i></p>
<h3>Co se změnilo</h3>
<ul>
<li><b>Zprávy:</b> Babišovi lékař zakázal zbytek kampaně kvůli horečce. Jde o pokračování středeční nemoci, která ANO v posledních dnech mírně oslabuje. Jinak se objevily jen předvolební přehledy a rozhovory.</li>
<li><b>Sázky:</b> poslední den byl klidný. Favorit trhu se nezměnil v žádném obvodu, žádný kandidát se nepohnul o víc než 3 p.b. Nejvíc se změnila Plzeň (Řehka +2 na 63 %, tedy dál od nás) a Hradec Králové (Dvořák +3 na 51 %, blíž k nám). Celkový rozdíl mezi trhem a AI s modelem je stejný jako včera.</li>
<li><b>Sporné obvody při freeze:</b> trh má jiného favorita než AI s modelem v 7 obvodech: Cheb, Plzeň, Pelhřimov, Praha 5, Kladno, Přerov a Litovel. Praha 1 a Frýdek-Místek mezi ně od středy a čtvrtka nepatří, protože trh se tam přesunul k našemu favoritovi. Při vyhodnocení ale použijeme předem zapsaný seznam 9 obvodů z 5. 10. a k tomu tento.</li>
</ul>
<h3>Předem zapsáno: kurzy během voleb</h3>
<p>Fortuna sázky uzavírá dnes ve 14:00, ale <b>Tipsport bere sázky až do soboty 12:00</b>, tedy i během hlasování. Pozdější kurzy už v sobě mají dění během voleb, třeba zprávy o volební účasti. Srovnávat s nimi naše páteční odhady by nebylo férové. Proto:</p>
<ul>
<li><b>Hodnocená série Sázky</b> = dnešní snapshot (kurzy čtené 10:36–10:42). Všech pět sérií tak vychází ze stejných informací.</li>
<li><b>Jen pro srovnání</b> si zapíšeme ještě kurzy Fortuny těsně před 14:00 a kurzy Tipsportu v sobotu kolem 11:30, tedy poslední cenu před uzavřením. Ukážou, kam se trh posunul během voleb, jestli k nám, nebo od nás. Do skóre nevstupují.</li>
</ul>
<h3>Nové zdroje dne</h3>
<ul>
<li>CNN Prima NEWS (8. 10.): <a href="https://cnn.iprima.cz/skolilo-me-to-doktor-mi-zakazal-pokracovat-v-kampani-rekl-babis-priznivcum-kopl-si-do-senatu-523920">Skolilo mě to, doktor mi zakázal pokračovat v kampani, řekl Babiš příznivcům</a>. Celostátní, mírné minus pro ANO, nic nového.</li>
<li>XTV (8. 10.): rozhovor s Alešem Gerlochem. Kladno (30), nic nového. Živé Chebsko (8. 10.): programy kandidátů. Cheb (3).</li>
<li>Vyřazeno: iDNES (8. 10.) <a href="https://www.idnes.cz/volby/ostrava/komunalni-volby-zameny-ostrava-poruba-hlasovaci-listky.A261008_122233_ostrava-zpravy_jog">chybné hlasovací lístky v Porubě</a>. Podle titulku vypadal jako zpráva o senátním obvodu, po otevření jde o komunální volby.</li>
<li>Neotevřeno: iROZHLAS „Analýza senátních voleb obvod po obvodu“, Echo24 „10 nejnapínavějších soubojů“ a předpovědi analytiků CNN Prima. Jde o cizí předpovědi, ne o vstup. Přečteme je až po volbách.</li>
</ul>
<h3>Chyby a nápravy</h3>
<ol>
<li><b>Titulek není obsah.</b> Zprávu o Porubě jsme v prvním zápisu přiřadili k ostravskému senátnímu obvodu jen podle titulku. Šlo ale o komunální volby. Na odhady to vliv nemělo (krok A/B jsme stejně přeskočili). <i>Náprava:</i> zdroj, který by mohl změnit odhad, vždy otevřít, nestačí titulek.</li>
<li><b>Tipsport nepovolí načítání stránek v rámu</b>, takže jsme detaily deseti obvodů, kde se změnil kurz Ano, otevírali postupně (8 s mezi stránkami). U ostatních 17 obvodů se kurz Ano nezměnil a kurz Ne přebíráme ze 8. 10. stejně jako v předchozích dnech.</li>
</ol>
<h3>Večerní doplněk (21:15)</h3>
<p>Odhady jsou zamrazené a nic z toho je nemění. Jen zapisujeme, co se během prvního dne voleb stalo.</p>
<ul>
<li><b>Kladno (30):</b> Miloš Zeman, který volí v Lánech v tomto obvodu, u urny veřejně řekl, že volil Aleše Gerlocha (<a href="https://www.idnes.cz/volby/volby-2026-prezident-zeman-lany-petr-pavel-gerloch-senat-pro.A261008_193825_volby_sahu">iDNES</a>, 16:03). Může to ovlivnit jen voliče, kteří půjdou volit v sobotu.</li>
<li><b>Celostátně:</b> prezident Pavel se po kritice vrátil z dovolené v Maroku, odvolil a zase odletěl. Babiš za úspěch považuje obhajobu výsledku ANO.</li>
<li><b>Účast:</b> oficiální čísla nejsou, ČSÚ je zveřejní až v sobotu po 14:00. Jen útržky: podle ČTK v prvních hodinách 10–15 %, v Havířově kolem 10 % v 17:00, Přerovský deník píše o „slibné účasti“. Neověřené.</li>
<li><b>Závěrečné kurzy Fortuny (13:46, jen pro srovnání, nehodnotí se):</b> proti hodnocenému čtení z 10:38 se pohnuly jen dva obvody. V Praze 1 posílil Jan Čižinský (2,00 → 1,90), což je pohyb od nás. V Pelhřimově posílil Med (2,70 → 2,50), což je pohyb k nám. Ostatních 25 obvodů beze změny.</li>
<li><b>Tipsport večer (21:10–21:20, během voleb, jen pro srovnání):</b> favorit se nezměnil v žádném obvodu, největší pohyby jsou do 3 p.b. K nám se trh posunul v Chebu (Plevný +3), Lounech, Pelhřimově (Med +3), na Znojemsku a ve Frýdku-Místku. Od nás v Plzni (Řehka +2). Celkový rozdíl mezi trhem a AI s modelem se mírně zmenšil. U pěti obvodů jsme kurz „Ne“ dopočítali se zachováním marže, protože Tipsport měl výpadek.</li>
</ul>
<p><b>Dál:</b> v sobotu po 14:00 výsledky 1. kola z volby.gov.cz. Vyhodnotíme postupy do 2. kola pro všech pět sérií, porovnáme se Seznam Zprávami a s Wikipedií a ověříme hypotézu o domácích baštách. Pak přepočítáme model se skutečnými výsledky a uděláme updaty pro 2. kolo. Ty zamkneme dřív, než uvidíme předpovědi STEM.</p>""",
    en="""<p><b>The forecasts are frozen.</b> A final news check (10:25–10:35) found nothing that changes the race in any district. We therefore locked AI and AI + model unchanged at 10:35, before reading the odds (commit <code>ced8415</code>). <b>The 9 Oct snapshots are the ones we will score</b>: AI, Statistical model (as of 3 Oct), AI + model, Betting (odds read 10:36–10:42) and Blend. Polls open today at 14:00. <i>Note: this page went live only in the afternoon, after the polls had opened. The forecasts are unchanged; the commit times in the repository show they were made before 14:00 (lock 10:35, build 10:42).</i></p>
<h3>What changed</h3>
<ul>
<li><b>News:</b> Babiš's doctor banned him from the rest of the campaign because of a fever. This continues Wednesday's illness, which mildly weakens ANO's final days. Otherwise there were only election previews and interviews.</li>
<li><b>Betting:</b> the last day was quiet. The market favourite changed in no district and no candidate moved by more than 3 pp. The biggest moves were Plzeň (Řehka +2 to 63 %, away from us) and Hradec Králové (Dvořák +3 to 51 %, towards us). The overall gap between the market and AI + model is the same as yesterday.</li>
<li><b>Disputed districts at the freeze:</b> the market has a different favourite from AI + model in 7 districts: Cheb, Plzeň, Pelhřimov, Praha 5, Kladno, Přerov and Litovel. Praha 1 and Frýdek-Místek have dropped out since Wednesday and Thursday because the market moved to our favourite there. For scoring we will use the 9-district list pre-registered on 5 Oct, and this one as well.</li>
</ul>
<h3>Recorded in advance: odds during voting</h3>
<p>Fortuna closes its markets today at 14:00, but <b>Tipsport takes bets until Saturday 12:00</b>, i.e. during voting. Later odds already reflect events during the election, such as turnout reports. Comparing them with our Friday forecasts would be unfair. Therefore:</p>
<ul>
<li><b>The scored Betting series</b> = today's snapshot (odds read 10:36–10:42). All five series are thus based on the same information.</li>
<li><b>For reference only</b> we will also record Fortuna just before 14:00 and Tipsport on Saturday around 11:30, the last price before it closes. They will show where the market moved during voting, towards us or away from us. They do not enter the score.</li>
</ul>
<h3>New sources today</h3>
<ul>
<li>CNN Prima NEWS (8 Oct): <a href="https://cnn.iprima.cz/skolilo-me-to-doktor-mi-zakazal-pokracovat-v-kampani-rekl-babis-priznivcum-kopl-si-do-senatu-523920">Babiš: the doctor banned me from continuing the campaign</a>. National, mild minus for ANO, nothing new.</li>
<li>XTV (8 Oct): interview with Aleš Gerloch. Kladno (30), nothing new. Živé Chebsko (8 Oct): candidates' programmes. Cheb (3).</li>
<li>Excluded: iDNES (8 Oct) <a href="https://www.idnes.cz/volby/ostrava/komunalni-volby-zameny-ostrava-poruba-hlasovaci-listky.A261008_122233_ostrava-zpravy_jog">wrong ballots in Poruba</a>. Judging by the headline it looked like a Senate-district story; once opened, it is about the municipal election.</li>
<li>Not opened: iROZHLAS “district-by-district analysis”, Echo24 “10 most exciting races” and CNN Prima analysts' predictions. These are someone else's forecasts, not inputs. We will read them after the election.</li>
</ul>
<h3>Mistakes and fixes</h3>
<ol>
<li><b>A headline is not the content.</b> In the first log entry we assigned the Poruba story to the Ostrava Senate district based on the headline alone. It was about the municipal election. It had no effect on the forecasts (step A/B was skipped anyway). <i>Fix:</i> always open any source that could change a forecast; the headline is not enough.</li>
<li><b>Tipsport does not allow its pages in a frame</b>, so we opened the detail pages of the ten districts whose “Yes” price changed one by one (8 s apart). In the other 17 districts the “Yes” price did not change and the “No” price is carried from 8 Oct, as on previous days.</li>
</ol>
<h3>Evening addendum (21:15)</h3>
<p>The forecasts are frozen and none of this changes them. We only record what happened on the first day of voting.</p>
<ul>
<li><b>Kladno (30):</b> Miloš Zeman, who votes in Lány in this district, said publicly at the ballot box that he voted for Aleš Gerloch (<a href="https://www.idnes.cz/volby/volby-2026-prezident-zeman-lany-petr-pavel-gerloch-senat-pro.A261008_193825_volby_sahu">iDNES</a>, 16:03). It can only affect those who vote on Saturday.</li>
<li><b>Nationally:</b> after criticism, President Pavel flew back from his holiday in Morocco, voted and left again. Babiš says defending ANO's result would be a success.</li>
<li><b>Turnout:</b> there are no official numbers; ČSÚ publishes them only after 14:00 on Saturday. Only fragments: per ČTK 10–15 % in the first hours, Havířov about 10 % at 17:00, Přerovský deník reports “promising turnout”. Unverified.</li>
<li><b>Fortuna closing odds (13:46, reference only, not scored):</b> compared with the scored 10:38 read, only two districts moved. In Praha 1 Jan Čižinský strengthened (2.00 → 1.90), a move away from us. In Pelhřimov Med strengthened (2.70 → 2.50), a move towards us. The other 25 districts are unchanged.</li>
<li><b>Tipsport in the evening (21:10–21:20, during voting, reference only):</b> the favourite changed in no district and the biggest moves are up to 3 pp. The market moved towards us in Cheb (Plevný +3), Louny, Pelhřimov (Med +3), Znojmo and Frýdek-Místek, and away from us in Plzeň (Řehka +2). The overall gap between the market and AI + model narrowed slightly. For five districts the “No” price was imputed keeping the margin, because Tipsport had an outage.</li>
</ul>
<p><b>Next:</b> on Saturday after 14:00, round 1 results from volby.gov.cz. We will score runoff qualification for all five series, compare with Seznam Zprávy and Wikipedia, and test the home-base hypothesis. Then we re-run the model with the actual results and update for round 2. Those updates will be locked before we see the STEM predictions.</p>"""))

# "What's new today" box at the top of the overview, per date (short, hand-written; auto moves are added below it).
CHANGES = {
    "2026-10-05": dict(
        cs="""<ul>
<li><b>Nově tři série:</b> AI s modelem (AI agent, který vychází ze statistického modelu), Sázky (Fortuna a Tipsport po odečtení marže) a Blend (mechanická kombinace obou).</li>
<li><b>AI bez modelu</b> se proti 2. 10. změnila jen nepatrně: v Litovli a v Brně o 2 p.b. Jinde nepřibyly nové fakty.</li>
<li><b>AI s modelem</b> mění favorita proti AI ve dvou obvodech: v Praze 5 (Sáblík místo Lásky) a v Praze 1 (Padevět místo Čižinského).</li>
<li><b>Trh</b> má jiného favorita než AI s modelem v 9 z 27 obvodů. Výrazně víc věří kandidátům ANO (Přerov, Cheb, Pelhřimov) a osobním značkám (Láska, Čižinský, Řehka, Korč, Kohajda, Paták).</li>
</ul>""",
        en="""<ul>
<li><b>Three new series:</b> AI + model (the AI agent starting from the statistical model), Betting (Fortuna and Tipsport with the margin removed) and Blend (a mechanical combination of the two).</li>
<li><b>AI without the model</b> barely moved since 2 Oct: 2 pp in Litovel and in Brno. No new facts elsewhere.</li>
<li><b>AI + model</b> changes the favourite vs. AI in two districts: Praha 5 (Sáblík instead of Láska) and Praha 1 (Padevět instead of Čižinský).</li>
<li><b>The market</b> has a different favourite from AI + model in 9 of 27 districts. It is much more confident in ANO candidates (Přerov, Cheb, Pelhřimov) and in personal brands (Láska, Čižinský, Řehka, Korč, Kohajda, Paták).</li>
</ul>"""),
    "2026-10-06": dict(
        cs="""<ul>
<li><b>Moratorium na průzkumy:</b> nové fakty, které by změnily situaci v obvodech, nepřibyly, takže AI ani AI s modelem se nemění.</li>
<li><b>Sázky:</b> největší pohyb je v Kladně, kde Šípová klesla o 5 p.b. a Klas posílil (Fortuna 20 → 6). Paták zůstává favoritem. Favorit trhu se nezměnil v žádném obvodu.</li>
<li><b>Externí benchmark:</b> datový model Seznam Zpráv (jen postupy ANO) jsme viděli a zapsali. Nepoužíváme ho jako vstup, srovnáme ho po 1. kole. Náš model čeká 14,5 postupů ANO, Seznam Zprávy ve středním scénáři 17,3.</li>
</ul>""",
        en="""<ul>
<li><b>Poll blackout:</b> no new facts that change any race, so AI and AI + model are unchanged.</li>
<li><b>Betting:</b> the biggest move is in Kladno, where Šípová fell 5 pp and Klas strengthened (Fortuna 20 → 6). Paták remains the favourite. The market favourite did not change in any district.</li>
<li><b>External benchmark:</b> we saw and recorded the Seznam Zprávy data model (ANO runoff chances only). It is not an input and we will compare it after round 1. Our model expects 14.5 ANO candidates to advance, Seznam Zprávy's middle scenario 17.3.</li>
</ul>"""),
    "2026-10-07": dict(
        cs="""<ul>
<li><b>AI ani AI s modelem se nemění:</b> ve zprávách o 154 kandidátech jsme nenašli nic, co by změnilo situaci v některém obvodu.</li>
<li><b>Sázky:</b> trh posiluje Volfovou v České Lípě (+6 p.b.), Kašpara na Kolínsku, Lásku v Praze 5 a Štěpánka v Příbrami. Ve Frýdku-Místku se favorit otočil na Pešatovou, ale jen o 2 p.b.</li>
<li><b>Chyba dne:</b> research z 2. 10. neznal profily některých vedlejších kandidátů (Klas v Kladně, Korč ve Frýdku-Místku). Proč jsme odhady neměnili a co měníme do budoucna, píšeme v deníku.</li>
</ul>""",
        en="""<ul>
<li><b>AI and AI + model unchanged:</b> the news on all 154 candidates contained nothing that changes the race in any district.</li>
<li><b>Betting:</b> the market warms to Volfová in Česká Lípa (+6 pp), Kašpar in Kolín, Láska in Praha 5 and Štěpánek in Příbram. In Frýdek-Místek the favourite flipped to Pešatová, but only by 2 pp.</li>
<li><b>Mistake of the day:</b> the 2 Oct research lacked the profiles of some minor candidates (Klas in Kladno, Korč in Frýdek-Místek). The journal explains why we did not change the forecasts and what we are changing for the future.</li>
</ul>"""),
    "2026-10-08": dict(
        cs="""<ul>
<li><b>Poslední den kampaně:</b> AI ani AI s modelem se nemění. Zítra do 12:00 odhady zamrazíme.</li>
<li><b>Sázky:</b> v Praze 1 se favorit trhu otočil na Padevěta, stejně jako u AI s modelem. V Pelhřimově roste Med (+6 p.b.). V Praze 5 a v Litovli se naopak trh od nás vzdálil, celkový rozdíl je stejný.</li>
<li><b>Předem zapsáno:</b> benchmark „vyhraje nejčtenější kandidát na Wikipedii“, hypotéza o domácích baštách (6 starostů velkých měst) a pravidlo, že sobotní updaty zamkneme dřív, než uvidíme předpovědi STEM. Podrobnosti v deníku.</li>
</ul>""",
        en="""<ul>
<li><b>Last day of the campaign:</b> AI and AI + model are unchanged. Forecasts freeze tomorrow by 12:00.</li>
<li><b>Betting:</b> in Praha 1 the market favourite flipped to Padevět, matching AI + model. In Pelhřimov, Med rises (+6 pp). In Praha 5 and Litovel the market moved away from us; the overall gap is unchanged.</li>
<li><b>Recorded in advance:</b> a “most-viewed on Wikipedia wins” benchmark, a home-base hypothesis (6 big-town mayors) and a rule that Saturday's updates are locked before we see the STEM predictions. Details in the journal.</li>
</ul>"""),
    "2026-10-09": dict(
        cs="""<ul>
<li><b>Freeze:</b> poslední kontrola zpráv nic nezměnila. Hodnotit budeme tyto snapshoty z 9. 10. (AI a AI s modelem zamčené v 10:35, kurzy čtené 10:36–10:42).</li>
<li><b>Sázky:</b> klidný den, favorit trhu se nikde nezměnil. Trh má jiného favorita než AI s modelem v 7 obvodech (Cheb, Plzeň, Pelhřimov, Praha 5, Kladno, Přerov, Litovel).</li>
<li><b>Předem zapsáno:</b> Tipsport bere sázky i během voleb (do soboty 12:00). Hodnotíme dnešní kurzy, pozdější si zapíšeme jen pro srovnání.</li>
</ul>""",
        en="""<ul>
<li><b>Freeze:</b> the final news check changed nothing. These 9 Oct snapshots are the ones we will score (AI and AI + model locked at 10:35, odds read 10:36–10:42).</li>
<li><b>Betting:</b> a quiet day; the market favourite changed nowhere. The market has a different favourite from AI + model in 7 districts (Cheb, Plzeň, Pelhřimov, Praha 5, Kladno, Přerov, Litovel).</li>
<li><b>Recorded in advance:</b> Tipsport takes bets during voting (until Saturday 12:00). We score today's odds; later ones are recorded for reference only.</li>
</ul>"""),
}