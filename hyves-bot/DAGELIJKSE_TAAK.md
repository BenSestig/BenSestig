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
5. De IDs van de hyves staan in `config.json` (`hyve_ids`). Controleer met `groups/ID` (via `raw GET`)
   dat de naam klopt en Ben eigenaar is (`isOwner`). Klopt het niet, zoek de hyves dan op naam ("Voetbal", "Poker", "Vastgoed") waar Ben
   eigenaar van is (`python3 hyves_api.py groups`, eventueel `groups Voetbal`). Vind je ze niet
   eenduidig: post niets in die hyve en meld het.
6. Haal de recente berichten van alle drie de hyves op (`python3 hyves_api.py posts ID 50`; de tekst
   van een bericht staat in het veld `content`, de datum in `createdAt`). Gebruik deze
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
- Foto: zie stap 6c.

## 6b. Eenmalige berichten

- In `eenmalig/` staan losse berichten die Ben zelf heeft aangeleverd (bijv. een LinkedIn-post),
  als JSON: `hyve` (sleutel uit `config.json` → `hyves`), `label`, `datum`, `tekst`, `afbeeldingen`
  (paden relatief aan `hyves-bot/`).
- Plaats elk bericht waarvan `datum` vandaag of eerder is en dat nog niet in die hyve staat
  (vergelijk de eerste regel van de tekst met de recente berichten). Tekst ongewijzigd laten en
  `link` meegeven als die in het bestand staat.
- Deze berichten gelden niet voor het maximum aantal nieuwsberichten per dag.

## 6c. Foto's bij de berichten

- Geef elk bericht één **echte foto** die vrij gebruikt mag worden, via `foto.py` (Wikimedia
  Commons). Uitzonderingen: YouTube-berichten (Hyves toont zelf de video) en eenmalige berichten
  (die hebben hun eigen foto's).
- Zoek eerst een **echte, specifieke foto** van waar het bericht over gaat, op naam:
  - voetbal: de hoofdrolspeler(s) uit het bericht ("Rayane Bounida", "Tjaronn Chery"), dan de
    club in actie ("AZ Alkmaar match", "NEC Nijmegen"), dan het stadion ("De Kuip");
  - poker: de genoemde speler of het toernooi ("World Series of Poker", "European Poker Tour");
  - vastgoed: het genoemde gebouw, de straat of de stad/wijk; anders een passend type pand.
  Lukt dat niet, neem dan een algemene foto ("football stadium", "poker chips",
  "Dutch row houses").
- Let bij spelers op de **datum** (`"datum"`): liefst recent, en controleer aan titel en
  beschrijving dat het echt die persoon of dat gebouw is.
- `python3 foto.py zoek "trefwoorden"` geeft kandidaten (vrije licenties eerst). Kies er één en
  haal hem op: `python3 foto.py haal "File:..." /tmp/foto-LABEL.jpg`. **Bekijk de foto (Read)**
  voordat je hem gebruikt: hij moet passen bij het bericht, er goed uitzien, geen watermerk of
  grote logo's hebben, en geen herkenbare mensen in een vervelende context tonen.
- Wek nooit de indruk dat de foto van de besproken wedstrijd of gebeurtenis zelf is: is hij
  dat niet, zet dan "Archieffoto" voor de naamsvermelding (bijv. "Archieffoto 📷 Hans Reefman /
  Wikimedia Commons (CC BY-SA 4.0) …").
- De foto past altijd bij het **thema van de hyve**: in Poker een pokerfoto (tafel, kaarten, chips,
  toernooi), in Voetbal een voetbalfoto, in Vastgoed een gebouw/woning. Gaat een pokerbericht over
  iemand die vooral van iets anders bekend is (bijv. voetballer Neymar die een pokertoernooi wint),
  neem dan een foto van die persoon **aan de pokertafel**; is die er niet, dan een algemene pokerfoto.
  Nooit een voetbalfoto in Poker of andersom.
- Alleen **liggende of vierkante** foto's (Bens voorkeur); `foto.py` slaat staande foto's over.
- Varieer: gebruik niet dezelfde foto als in de recente berichten van die hyve.
- Geeft `haal` een `"naamsvermelding"`, zet die regel dan onderaan de tekst van het bericht
  (verplicht bij CC BY / CC BY-SA). Bij CC0 / publiek domein is dat niet nodig.
- Nooit foto's van nieuwssites, persbureaus, clubs of andere bronnen buiten `foto.py`.
- Lukt het niet om een passende foto te vinden: plaats het bericht zonder foto.

## 7. Plaatsen

1. Zet alle berichten in `/tmp/wachtrij.json` (formaat: zie bovenaan `plaats_wachtrij.py`), met
   per bericht een duidelijke `label` (bijv. `voetbal`, `youtube-afl-2`, `poker-winnaar`).
2. Controleer eerst: `python3 plaats_wachtrij.py /tmp/wachtrij.json --droog`.
3. Start daarna `python3 plaats_wachtrij.py /tmp/wachtrij.json` **op de achtergrond** (Bash met
   `run_in_background` en `timeout` 7200000), want het wacht tot de geplande tijden. Wacht tot het
   klaar is.
4. Lees `/tmp/wachtrij.json.resultaat.json` en controleer met `posts ID` dat de berichten echt in de
   hyves staan.
5. De Hyves-API geeft soms een losse HTTP 500. Bij lezen probeert `hyves_api.py` het zelf opnieuw. Bij
   plaatsen niet: kijk na een fout eerst met `posts ID 5` of het bericht er toch staat.
6. Faalt een bericht door een API-fout (bijv. HTTP 400 over het formaat): zoek uit wat de API wil
   (`hyves_api.py raw`), en plaats het bericht daarna maximaal één keer opnieuw. Nooit
   testberichten plaatsen.

## Stijl

- **De vraag of call-to-action staat altijd boven de vouw.** Hyves toont ongeveer de eerste
  250 tekens (±5 regels) en zet daarna "Lees meer". Zet de vraag of CTA daarom in de eerste
  twee regels, binnen de eerste 200 tekens. Opbouw:
  1. pakkende openingszin + de vraag/CTA (bijv. "Wat een Europese avond! Wat was jullie
     hoogtepunt? 👇" of "Afl. 2 staat online: call of fold? 🃏");
  2. witregel;
  3. de details (uitslagen, uitleg, cijfers);
  4. onderaan eventueel de naamsvermelding van de foto.
  `plaats_wachtrij.py` controleert dit: zonder "?" in de eerste 200 tekens weigert hij het bericht,
  tenzij het in de wachtrij `"geen_vraag": true` heeft (alleen voor een eenmalig bericht van Ben
  dat al een CTA bovenaan heeft, of een kale videolink).

- **Maximaal 500 tekens per bericht**, inclusief naamsvermelding en links (Hyves weigert langere
  berichten met HTTP 400; `hyves_api.py` controleert dit vooraf). Liever 300–450 tekens.
- Zet de belangrijkste link (YouTube-video, nieuwsbron, LinkedIn) in het veld `"link"` van de
  wachtrij: Hyves toont dan een voorbeeld. Zet hem dan niet ook nog in de tekst, dat kost tekens.
- Naamsvermelding van foto's kort en zonder URL: "📷 Archieffoto: Maker / Wikimedia Commons (licentie)".

- Nederlands, informeel en gezellig, alsof Ben het zelf schrijft voor zijn community.
- Varieer elke dag in woorden en opbouw; geen vaste sjablonen, geen hashtags, hooguit een paar emoji.
- Kort en to-the-point. Geen dingen verzinnen: alleen feiten die je hebt gecontroleerd.
- Nodig mensen uit om te reageren: eindig (behalve bij een kale videolink) met een vraag waar ze
  hun mening onder kwijt kunnen.

## Eindbericht van de sessie

Sluit af met een kort overzicht: welke berichten op welk tijdstip zijn geplaatst, wat bewust
is overgeslagen (en waarom), en eventuele fouten.
