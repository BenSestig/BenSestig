# Dagelijkse taak: Hyves voetbal & poker

Deze instructies zijn voor de geplande Claude-sessie die elke dag rond 10:40 (Nederlandse tijd)
start. Doel: de hyves **Voetbal** en **Poker** van Ben levendig houden met nuttige berichten.
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
5. Zoek de IDs van de hyves met precies de namen uit `config.json` ("Voetbal" en "Poker") waar Ben
   eigenaar van is (`python3 hyves_api.py groups`, eventueel `groups Voetbal`). Vind je ze niet
   eenduidig: post niets in die hyve en meld het.
6. Haal de recente berichten van beide hyves op (`python3 hyves_api.py posts ID 50`). Gebruik deze
   om **nooit iets dubbel te plaatsen**: video-ID's/links, toernooien en nieuwsonderwerpen die al
   gepost zijn sla je over.

## 1. Voetbal-hyve

- `python3 voetbal.py` geeft de wedstrijden van vandaag met een Eredivisie- of Eerste
  Divisie-club (competitie, KNVB Beker, Europees). Lege lijst = geen bericht.
- Staat er vandaag al een wedstrijdbericht in de hyve: geen nieuw bericht.
- Schrijf één bericht met de wedstrijden van vandaag, gegroepeerd per competitie, met aftraptijd
  ("19:00 Ajax – PSV"). Licht eruit wat de dag bijzonder maakt (topper, derby, Europese avond,
  bekerronde) als dat zo is, en sluit af met een vraag aan de leden (voorspellingen, wie wint er).
- Zet `"uiterlijk"` op 30 minuten vóór de eerste aftrap (formaat `"HH:MM"`).

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

## 5. Plaatsen

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

## Eindbericht van de sessie

Sluit af met een kort overzicht: welke berichten op welk tijdstip zijn geplaatst, wat bewust
is overgeslagen (en waarom), en eventuele fouten.
