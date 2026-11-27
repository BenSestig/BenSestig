# Hyves-bot (voetbal & poker)

Hulpscripts voor een dagelijkse geplande Claude-taak die berichten plaatst op Hyves:

- **Voetbal-hyve**: elke dag dat er een Eredivisie- of Eerste Divisie-club speelt
  (competitie, KNVB Beker of Europees) een bericht met de wedstrijden van die dag.
- **Poker-hyve**:
  - een link naar elke nieuwe video op het YouTube-kanaal;
  - een bericht als een Nederlander een (live of online) toernooi wint met minimaal €250.000 prijzengeld;
  - een bericht bij grote ontwikkelingen in de pokerwereld.

## Scripts

| Script | Wat het doet |
| --- | --- |
| `hyves_api.py` | Inloggen op Hyves en de API aanroepen (`me`, `groups`, `posts`, `post`, `raw`). |
| `voetbal.py [JJJJ-MM-DD]` | Wedstrijden van die dag met een Eredivisie- of Eerste Divisie-club (bron: ESPN), tijden in Nederlandse tijd. |
| `youtube.py KANAAL` | De nieuwste video's van een YouTube-kanaal. |

## Inloggegevens

`hyves_api.py` leest het e-mailadres en wachtwoord uit de omgevingsvariabelen
`HYVES_EMAIL` en `HYVES_PASSWORD`. Die staan **niet** in deze repository: je vult ze zelf in
bij de instellingen van de cloudomgeving `hyves-bot` (Omgeving → Bewerken → Omgevingsvariabelen).
Het inlogtoken wordt alleen lokaal in de sessie bewaard (`~/.cache/hyves-bot/`).

Verander je je Hyves-wachtwoord, pas dan alleen `HYVES_PASSWORD` in die omgeving aan.
