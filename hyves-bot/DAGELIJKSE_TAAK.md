# Dagelijkse taak: Hyves voetbal, poker & vastgoed

Deze instructies zijn voor de geplande Claude-sessie die elke dag rond 10:40 (Nederlandse tijd)
start. Doel: de hyves **Voetbal**, **Poker** en **Vastgoed** van Ben levendig houden met nuttige
berichten.
De berichten worden tussen 11:00 en 13:00 op willekeurige momenten geplaatst (meestal rond 12:00)
door `plaats_wachtrij.py`.

## 0. Voorbereiden

1. Ga naar de repository `BenSestig/BenSestig` (clone hem als hij er niet is). Gebruik de map
   `hyves-bot/` van de standaardbranch; staat die map daar nog niet, check dan branch
   `claude/hyves-voetbal-poker-posts-bkodzr` uit.
2. `pip install requests` als `import requests` faalt.
3. Controleer de login: `python3 hyves_api.py me`. Faalt dit omdat `HYVES_EMAIL`/`HYVES_PASSWORD`
   ontbreken of het wachtwoord fout is: stop en meld dat in je eindbericht. Probeer niets anders.
4. Lees `config.json`.
5. Zoek de IDs van de hyves met precies de namen uit `config.json` ("Voetbal", "Poker", "Vastgoed") waar Ben
   eigenaar van is (`python3 hyves_api.py groups`, eventueel `groups Voetbal`). Vind je ze niet
   eenduidig: post niets in die hyve en meld het.
6. Haal de recente berichten van alle drie de hyves op (`python3 hyves_api.py posts ID 50`). Gebruik deze
   om **nooit iets dubbel te plaatsen**: video-ID's/links, toernooien en nieuwsonderwerpen die al
   gepost zijn sla je over.

## 1. Voetbal-hyve: vooruitkijken én terugblikken

Gegevens: `python3 voetbal.py` (vandaag) en `python3 voetbal.py JJJJ-MM-DD` (eerdere dag, met
uitslagen, doelpunten en rode kaarten). Alleen clubs uit de Eredivisie en Eerste Divisie tellen
(competitie, KNVB Beker, Europees).

Terugblik en vooruitblik zijn **twee aparte berichten**.

- **Terugblik** (ochtendronde, venster 11:00–13:00): als er gisteren gespeeld is. Inhoud:
  uitslagen (bij veel wedstrijden alleen de opvallendste) en vooral de
  **spraakmakendste momenten**: VAR-beslissingen, rode kaarten, wereldgoals, blunders, late
  winnaars, uitspraken van trainers/spelers, onrust bij een club. Zoek dat op het web (WebSearch,
  bijv. NOS, VI, Voetbalzone, ESPN NL) en neem alleen op wat meerdere bronnen bevestigen.
- **Vooruitblik** op de wedstrijden van vandaag: per competitie, met aftraptijd
  ("19:00 Ajax – PSV"), en wat de dag bijzonder maakt (topper, derby, Europese avond, bekerronde,
  degradatie-/titelstrijd). Zet `"uiterlijk"` op 30 minuten vóór de eerste aftrap (`"HH:MM"`).
  - Eerste aftrap **vóór 18:00**: in de ochtendronde (venster 11:00–13:00).
  - Eerste aftrap **om 18:00 of later**: niet in de ochtendronde, maar in de **avondronde**
    (aparte geplande sessie rond 16:40, venster 17:00–19:00). De avondronde doet alleen dit:
    vooruitblik maken en plaatsen met `plaats_wachtrij.py ... --venster 17:00-19:00`, verder niets.
- Voeg aan elk voetbalbericht een eigen kaart toe als afbeelding: `python3 kaart.py JJJJ-MM-DD
  /tmp/kaart.png ["Titel"]` (uitslagen van gisteren bij de terugblik, programma van vandaag bij
  de vooruitblik; titel bijv. "Europese donderdag" of "Vanavond op het programma"). Bekijk de kaart
  even (Read) voordat je hem gebruikt, en zet het pad in `"afbeeldingen"` in de wachtrij.
- Gebruik **nooit** persfoto's, clublogo's of andere afbeeldingen van internet: daar rust
  auteursrecht op. Alleen zelfgemaakte afbeeldingen zoals de kaart.
- Sluit **elk** voetbalbericht af met een prikkelende vraag waar mensen hun mening onder kwijt
  kunnen ("Terechte rode kaart of niet?", "Wie wordt kampioen?", "Jullie voorspelling voor de
  Klassieker?").
- Staat het bericht van vandaag al in de hyve: geen nieuw bericht.

## 2. Poker-hyve: YouTube-video's van Ben

Kanaal en regels staan in `config.json`. Haal de video's op met `python3 youtube.py KANAAL`.

- **Nooit** posten: Shorts (`"short": true`) en video's waarvan de titel "home game" bevat
  (hoofdletterongevoelig, bijv. "Friends' Home Game").
- **Oude video's**: in `oude_videos_wekelijks` staat per video de datum waarop hij gepost moet
  worden (één per week). Post vandaag de video met de datum van vandaag. Staat er een eerdere
  datum die nog niet gepost is (bijv. omdat een run mislukte), post die dan ook.
- **Nieuwe video's**: elke andere video (geen Short, geen home game, niet in de lijst met oude
  video's) die op of na `nieuw_vanaf` verschenen is en nog niet in de hyve staat: post hem.
- Eén bericht per video: korte, enthousiaste teaser in Bens stem (het is zijn eigen kanaal) +
  de link `https://www.youtube.com/watch?v=ID`.

## 3. Poker-hyve: Nederlandse winnaars (≥ €250.000)

- Zoek op het web (WebSearch) naar Nederlanders die de afgelopen dagen een pokertoernooi hebben
  gewonnen met een prijs van minimaal €250.000 (andere valuta omrekenen tegen de actuele koers),
  live én online (bijv. WSOP, EPT, WPT, Triton, PokerStars/GGPoker-series, Holland Casino).
- Alleen posten als het zeker is: winnaar is Nederlands, het is een **winst** (geen tweede plaats),
  prijs ≥ €250.000, en het staat bij een betrouwbare bron (PokerNews, The Hendon Mob,
  organisator). Twijfel = niet posten.
- Bericht: wie, welk toernooi, hoeveel, kort iets over de finale; bronlink erbij.

## 4. Poker-hyve: grote ontwikkelingen

- Alleen echt groot nieuws: bijv. grote veranderingen bij WSOP/EPT, nieuwe regels voor online poker
  in Nederland (KSA, Wet koa), grote overnames of sluitingen van pokerrooms, records, opvallend
  nieuws over bekende spelers. Gewoon toernooinieuws of kleine updates niet.
- Maximaal één zo'n bericht per dag; op de meeste dagen is er niets en dat is prima.
- Bericht: wat er gebeurd is en waarom het ertoe doet, met bronlink.

## 5. Poker-hyve: interessante handen

- Zoek een **super interessante hand** van de afgelopen dagen: een gekke fold, een hero call, een
  enorme bluff, een cooler, een discutabele beslissing in een grote live- of onlinetoernooi of een
  high-stakes cashgame (bijv. PokerNews-handanalyses, Triton/EPT/WSOP-streams, Hustler Casino Live,
  virale handen). Een opvallende hand uit Bens eigen video's mag ook.
- Beschrijf de hand zodat mensen mee kunnen denken: toernooi/game, blinds, stacks, posities,
  de kaarten en de actie per straat, en wat er uiteindelijk gebeurde. Link naar de bron/video.
- Sluit af met een vraag: "Wat had jij gedaan?", "Call of fold?", "Bluff of value?".
- Maximaal één hand per dag, gemiddeld een paar keer per week; alleen als de hand echt de moeite
  waard is én je de details uit een bron hebt (niets verzinnen).

## 6. Vastgoed-hyve: nieuws voor beleggers (alleen maandag t/m vrijdag)

- Op zaterdag en zondag niets in de Vastgoed-hyve.
- Zoek op het web (WebSearch) naar vastgoednieuws van de afgelopen 1–3 dagen dat er echt toe doet
  voor **vastgoedbeleggers in Nederland**, bijvoorbeeld:
  - fiscaal: box 3 / werkelijk rendement, overdrachtsbelasting, WOZ, verhuurderheffing;
  - huur: Wet betaalbare huur, WWS-punten, maximale huurverhoging, opkoopbescherming,
    vergunningen voor splitsen/kamerverhuur;
  - financiering: hypotheek- en ECB-rente, financiering van beleggingspanden, banken;
  - markt: prijzen (CBS/Kadaster/NVM), transactievolumes, beleggers die uitponden of instappen,
    rendementen (BAR/NAR), grote transacties, commercieel vastgoed (kantoren, winkels, logistiek);
  - regels: energielabels en verduurzamingseisen, transformatie, bouwproductie, stikstof/netcongestie.
  Goede bronnen: NOS, FD, Vastgoedmarkt, Vastgoed Actueel, PropertyNL, CBS, Kadaster, DNB,
  Rijksoverheid. Neem alleen feiten op die je in een betrouwbare bron hebt gelezen.
- Schrijf **vanuit het perspectief van een investeerder**: wat betekent dit voor rendement,
  cashflow, waarde, financiering en risico? Maak het concreet (rekenvoorbeeld als dat kan, bijv.
  "bij een pand van €400.000 betekent dit…"), noem wie er wint en wie verliest, en wat een
  belegger nu zou kunnen doen of moet afwachten. Zakelijk maar toegankelijk; geen financieel
  advies beloven.
- Sluit af met een vraag aan de leden ("Gaan jullie uitponden of juist bijkopen?", "Wat doet dit
  met jullie rendement?") en zet de bronlink erbij.
- Maximaal twee berichten per dag (zie `config.json`); is er niets relevants, dan niets plaatsen.
  Nooit hetzelfde nieuws twee keer.
- Geen afbeeldingen van nieuwssites gebruiken (auteursrecht).

## 7. Plaatsen

1. Zet alle berichten in `/tmp/wachtrij.json` (formaat: zie bovenaan `plaats_wachtrij.py`), met
   per bericht een duidelijke `label` (bijv. `voetbal`, `youtube-afl-2`, `poker-winnaar`).
2. Controleer eerst: `python3 plaats_wachtrij.py /tmp/wachtrij.json --droog`.
3. Start daarna `python3 plaats_wachtrij.py /tmp/wachtrij.json` **op de achtergrond** (Bash met
   `run_in_background` en `timeout` 7200000), want het wacht tot de geplande tijden. Wacht tot het
   klaar is.
4. Lees `/tmp/wachtrij.json.resultaat.json` en controleer met `posts ID` dat de berichten echt in de
   hyves staan.
5. Faalt een bericht door een API-fout (bijv. HTTP 400 over het formaat): zoek uit wat de API wil
   (`hyves_api.py raw`), en plaats het bericht daarna maximaal één keer opnieuw. Nooit
   testberichten plaatsen.

## Stijl

- Nederlands, informeel en gezellig, alsof Ben het zelf schrijft voor zijn community.
- Varieer elke dag in woorden en opbouw; geen vaste sjablonen, geen hashtags, hooguit een paar emoji.
- Kort en to-the-point. Geen dingen verzinnen: alleen feiten die je hebt gecontroleerd.
- Nodig mensen uit om te reageren: eindig (behalve bij een kale videolink) met een vraag waar ze
  hun mening onder kwijt kunnen.

## Eindbericht van de sessie

Sluit af met een kort overzicht: welke berichten op welk tijdstip zijn geplaatst, wat bewust
is overgeslagen (en waarom), en eventuele fouten.
