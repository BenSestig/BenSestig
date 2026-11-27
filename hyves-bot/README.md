# Hyves-bot (voetbal, poker & vastgoed)

Hulpscripts voor een dagelijkse geplande Claude-taak die berichten plaatst op Hyves:

- **Voetbal-hyve**: elke dag dat er een Eredivisie- of Eerste Divisie-club speelt
  (competitie, KNVB Beker of Europees) een bericht met de wedstrijden van die dag, plus een
  terugblik op de vorige speeldag met de spraakmakendste momenten. Elk bericht eindigt met een
  vraag aan de leden.
- **Poker-hyve**:
  - een link naar de video's op het YouTube-kanaal (oude afleveringen één per week, nieuwe
    meteen; geen Shorts of home game-video's);
  - af en toe een interessante hand om over te discussiëren;
  - een bericht als een Nederlander een (live of online) toernooi wint met minimaal €250.000 prijzengeld;
  - een bericht bij grote ontwikkelingen in de pokerwereld.
- **Vastgoed-hyve** (maandag t/m vrijdag): relevant vastgoednieuws, geschreven vanuit het
  perspectief van een investeerder.

## Scripts

| Script | Wat het doet |
| --- | --- |
| `hyves_api.py` | Inloggen op Hyves en de API aanroepen (`me`, `groups`, `posts`, `post`, `raw`). |
| `voetbal.py [JJJJ-MM-DD]` | Wedstrijden van die dag met een Eredivisie- of Eerste Divisie-club (bron: ESPN), tijden in Nederlandse tijd. |
| `youtube.py KANAAL` | De nieuwste video's van een YouTube-kanaal (met Shorts gemarkeerd). |
| `kaart.py JJJJ-MM-DD uit.png` | Maakt een eigen afbeelding met de uitslagen of het programma van die dag. |
| `plaats_wachtrij.py wachtrij.json` | Plaatst berichten op willekeurige momenten tussen 11:00 en 13:00 (piek rond 12:00). |
| `eenmalig/` | Losse berichten die Ben aanlevert (tekst + foto's), geplaatst op de aangegeven datum. |
| `config.json` | Namen van de hyves, YouTube-kanaal, wat over te slaan, schema voor de oude video's. |
| `DAGELIJKSE_TAAK.md` | De instructies die de dagelijkse geplande sessie volgt. |

## Inloggegevens

`hyves_api.py` leest het e-mailadres en wachtwoord uit de omgevingsvariabelen
`HYVES_EMAIL` en `HYVES_PASSWORD`. Die staan **niet** in deze repository: je vult ze zelf in
bij de instellingen van de cloudomgeving `hyves-bot` (Omgeving → Bewerken → Omgevingsvariabelen).
Het inlogtoken wordt alleen lokaal in de sessie bewaard (`~/.cache/hyves-bot/`).

Verander je je Hyves-wachtwoord, pas dan alleen `HYVES_PASSWORD` in die omgeving aan.
