# Senát 2026: předregistrace virtuálního sázení (14. 10. 2026)

Otázka z X: „Budete testovat i sázkařskou úspěšnost, kdyby sázel na základě pravděpodobnostního rozdílu?“
Odpověď: ano, podle pravidla níže. Pravidlo je zamčené commitem, ve kterém tento soubor vznikl. Po commitu se nemění.
Kdyby se ve skriptu našla chyba, opravu zveřejníme i s diffem a výsledky ukážeme podle obou verzí.
Jde o **papírové sázky bez peněz**, ne o tipy.

## Pravidlo
- **Série:** AI, Statistický model, AI s modelem, AI + sázky. (Sázky samy proti sobě sázet nemůžou.)
- **Kurzy:** všechny ceny ve **hodnoceném čtení kurzů** (Tipsport + Fortuna, surové kurzy včetně marže). Uzamčená nebo chybějící cena se nepočítá.
- **Pro každou nabízenou sázku:** EV = p × kurz − 1, kde p je naše pravděpodobnost daného výsledku. Rozdíl = p − férová p bookmakera (power de-vig téže knihy).
- **Sázíme, jen když platí všechno:** EV ≥ **10 %**, rozdíl ≥ **3 p.b.**, kurz ≤ **20,00**. Na „ostatní kandidáty“ (v našich sériích sloučené) se nesází.
- **Nejvýš jedna sázka na obvod a sérii:** ta s nejvyšším EV.
- **Vklad:** (a) **pevný 100 Kč**; (b) **¼ Kelly** z virtuálního bankrollu 10 000 Kč, strop 2 % (200 Kč) na sázku. Všechny vklady se počítají z výchozího bankrollu, protože sázky běží souběžně.
- **Srovnávací strategie:** 100 Kč na favorita trhu v každém obvodu za nejlepší dostupný kurz.
- **Vyhodnocení:** zisk nebo ztráta, ROI a počet trefených sázek pro obě varianty vkladu. Pro 1. kolo navíc CLV, tedy srovnání s posledním kurzem před uzávěrkou trhu. Pokud kandidát odstoupí, sázka propadá a vklad se vrací.
- **Skript:** `tools/paper_bets.py` (ve vaultu `scripts/senat_model/paper_bets.py`) (`place r1`, `place r2 <datum>`, `settle`).

## 2. kolo (hlavní test)
- Snapshoty: poslední zamčené AI a AI s modelem, Statistický model r2 a AI + sázky ze dne **hodnoceného čtení kurzů v pátek 16. 10.** (před 14:00).
- Seznam sázek se vygeneruje a commitne hned po pátečním čtení kurzů, tedy před otevřením volebních místností.
- Sázky se vyhodnotí podle vítěze 2. kola.

## 1. kolo (doplňkový test, ne zcela slepý)
- Freeze z 9. 10. (AI, AI s modelem, AI + sázky; Statistický model z 3. 10.) proti hodnocenému čtení kurzů z 9. 10. (trh „Vítěz“: Fortuna celá kniha, Tipsport Ano/Ne na jednoho kandidáta).
- Sázky na trh „Vítěz“ se vyhodnotí podle **konečného vítěze mandátu** (po 2. kole).
- **Omezení:** pravidlo jsme sepsali 14. 10., kdy už výsledky 1. kola byly známé. Seznam sázek je sice daný daty z 9. 10., ale práh, vklady a výběr sérií jsme mohli (i nevědomky) zvolit s vědomím výsledků. Proto ho ukážeme odděleně a jako slabší důkaz. Seznam: `paper-bets/r1-2026-10-09.json`.

## Co čekat
- 22 duelů je málo a nejsou na sobě nezávislé (jedna celostátní nálada pohne mnoha obvody naráz). Ani výrazný zisk, ani ztráta nedokazují schopnost.
- Dosavadní track record: trh porazil náš final v 5 ze 6 sérií. Nejpravděpodobnější výsledek je ztráta zhruba o velikosti marže.
