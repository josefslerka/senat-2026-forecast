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
