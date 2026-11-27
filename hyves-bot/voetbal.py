#!/usr/bin/env python3
"""Lists the matches on a given day (default: today, Amsterdam time) that involve
a team from the Eredivisie or the Eerste Divisie, in any competition: league,
KNVB Beker, or European cups. Data comes from ESPN's public scoreboard API.

Usage:
  python3 voetbal.py            # today
  python3 voetbal.py 2026-11-29 # a specific date
Prints JSON: {"date": ..., "matches": [...]}; "matches" is empty on a day
without Dutch professional football. Finished matches also get "score" and
"events" (goals and red cards with minute and player).
"""
import datetime as dt
import json
import sys
from zoneinfo import ZoneInfo

import requests

ESPN = "https://site.api.espn.com/apis/site/v2/sports/soccer/{}/"
AMS = ZoneInfo("Europe/Amsterdam")
COMPETITIONS = {
    "ned.1": "Eredivisie",
    "ned.2": "Keuken Kampioen Divisie",
    "ned.cup": "KNVB Beker",
    "uefa.champions": "Champions League",
    "uefa.europa": "Europa League",
    "uefa.europa.conf": "Conference League",
    "uefa.champions_qual": "Champions League-voorronde",
    "uefa.europa_qual": "Europa League-voorronde",
    "uefa.europa.conf_qual": "Conference League-voorronde",
}
# ESPN uses English/long club names; these are the names Dutch fans use.
NAMES = {
    "Ajax Amsterdam": "Ajax", "PSV Eindhoven": "PSV", "Feyenoord Rotterdam": "Feyenoord",
    "AZ Alkmaar": "AZ", "Helmond Spor": "Helmond Sport", "Maastricht": "MVV Maastricht",
    "Emmen": "FC Emmen", "Dordrecht": "FC Dordrecht", "Groningen": "FC Groningen",
    "Sparta Prague": "Sparta Praag", "Slavia Prague": "Slavia Praag", "Bayern Munich": "Bayern München",
    "Inter Milan": "Inter", "AC Milan": "AC Milan", "Sporting CP": "Sporting Lissabon", "Benfica": "Benfica",
}


def _get(league, path, **params):
    r = requests.get(ESPN.format(league) + path, params=params, timeout=30)
    if r.status_code != 200 or not r.text.startswith("{"):
        return {}
    return r.json()


def dutch_team_ids():
    ids = set()
    for league in ("ned.1", "ned.2"):
        data = _get(league, "teams")
        for t in data.get("sports", [{}])[0].get("leagues", [{}])[0].get("teams", []):
            ids.add(t["team"]["id"])
    return ids


def name(team):
    n = team.get("displayName") or team.get("name")
    return NAMES.get(n, n)


def matches_on(day):
    dutch = dutch_team_ids()
    out = []
    # ESPN dates are UTC; a late kick-off in Amsterdam can fall on the next UTC day and vice versa.
    for league, comp in COMPETITIONS.items():
        seen = set()
        for d in (day - dt.timedelta(days=1), day, day + dt.timedelta(days=1)):
            for e in _get(league, "scoreboard", dates=d.strftime("%Y%m%d")).get("events", []):
                if e["id"] in seen:
                    continue
                seen.add(e["id"])
                kickoff = dt.datetime.fromisoformat(e["date"].replace("Z", "+00:00")).astimezone(AMS)
                if kickoff.date() != day:
                    continue
                c = e["competitions"][0]
                teams = {t["homeAway"]: t for t in c["competitors"]}
                home, away = teams["home"]["team"], teams["away"]["team"]
                if not league.startswith("ned.") and not ({home["id"], away["id"]} & dutch):
                    continue
                match = {
                    "competition": comp,
                    "kickoff": kickoff.strftime("%H:%M"),
                    "home": name(home),
                    "away": name(away),
                    "status": e["status"]["type"]["description"],
                    "venue": c.get("venue", {}).get("fullName"),
                }
                if e["status"]["type"].get("completed"):
                    match["score"] = f'{teams["home"].get("score")}-{teams["away"].get("score")}'
                    match["events"] = [  # goals and red cards, with minute and player
                        f'{x.get("clock", {}).get("displayValue", "")} {x.get("type", {}).get("text", "")}: '
                        + ", ".join(a.get("displayName", "") for a in x.get("athletesInvolved", []))
                        for x in c.get("details", []) if "Yellow" not in x.get("type", {}).get("text", "")]
                out.append(match)
    out.sort(key=lambda m: (m["kickoff"], m["competition"]))
    return out


if __name__ == "__main__":
    day = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.datetime.now(AMS).date()
    print(json.dumps({"date": day.isoformat(), "matches": matches_on(day)}, indent=2, ensure_ascii=False))
