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
}
