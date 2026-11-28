#!/usr/bin/env python3
"""Places a queue of posts on Hyves at random, human-looking moments.

Every post gets its own random time inside a window (default 11:00-13:00,
Amsterdam time), drawn from a triangular distribution that peaks in the middle
of the window (12:00 for the default). Posts are at least
MIN_GAP minutes apart, never scheduled in the past, and never after the post's
optional "uiterlijk" (latest) time. The script then waits and posts each one.

Usage:
  python3 plaats_wachtrij.py wachtrij.json                       # 11:00-13:00
  python3 plaats_wachtrij.py wachtrij.json --venster 17:00-19:00  # other window
  python3 plaats_wachtrij.py wachtrij.json --venster nu-10:30     # from now
  python3 plaats_wachtrij.py wachtrij.json --droog                # show schedule only

wachtrij.json is a list of:
  {"label": "voetbal", "hyve_id": "...", "tekst": "...", "uiterlijk": "11:45",
   "afbeeldingen": ["foto.jpg"], "link": "https://..."}
("uiterlijk", "afbeeldingen" and "link" are optional). A post whose images are
refused with HTTP 400 is placed once more without them (400 = nothing created). Results are written to wachtrij.json.resultaat.json.
"""
import datetime as dt
import json
import random
import sys
import time
from zoneinfo import ZoneInfo

import hyves_api

AMS = ZoneInfo("Europe/Amsterdam")
DEFAULT_WINDOW = "11:00-13:00"
MIN_GAP = dt.timedelta(minutes=7)


def _sample(queue, lo, peak):
    planned = []
    for item in queue:
        hi = item["_hi"]
        if hi <= lo:  # window already passed: post soon
            when = lo + dt.timedelta(seconds=random.randint(0, 240))
        else:
            mode = min(max(peak, lo), hi)
            when = dt.datetime.fromtimestamp(random.triangular(lo.timestamp(), hi.timestamp(), mode.timestamp()), AMS)
        planned.append([when.replace(microsecond=0), item])
    planned.sort(key=lambda p: p[0])
    for i in range(1, len(planned)):  # keep posts apart
        if planned[i][0] - planned[i - 1][0] < MIN_GAP:
            planned[i][0] = planned[i - 1][0] + MIN_GAP + dt.timedelta(seconds=random.randint(0, 180))
    return planned


def plan(queue, now, window=DEFAULT_WINDOW):
    at = lambda t: dt.datetime.combine(now.date(), t, AMS)
    start, end = window.split("-")
    soon = now + dt.timedelta(minutes=2)
    first = soon if start == "nu" else at(dt.time.fromisoformat(start))
    end = at(dt.time.fromisoformat(end))
    lo, peak = max(first, soon), first + (end - first) / 2
    for item in queue:
        item["_hi"] = end
        if item.get("uiterlijk"):
            item["_hi"] = min(item["_hi"], at(dt.time.fromisoformat(item["uiterlijk"])))
    for _ in range(200):  # redraw until every post with a deadline makes it in time
        planned = _sample(queue, lo, peak)
        if all(when <= max(item["_hi"], lo + dt.timedelta(minutes=5)) for when, item in planned):
            return planned
    # fallback: earliest deadline first, MIN_GAP apart
    planned, when = [], lo
    for item in sorted(queue, key=lambda i: i["_hi"]):
        planned.append([when, item])
        when += MIN_GAP
    return planned


FOLD = 200  # Hyves shows about 250 characters before "Lees meer"; keep the question well above it


def check_fold(item):
    """The question / call to action must be visible without tapping "Lees meer"."""
    head = item["tekst"].encode("utf-16-le")[: FOLD * 2].decode("utf-16-le", "ignore")
    if "?" not in head and not item.get("geen_vraag"):
        raise SystemExit(f"{item.get('label', '')}: geen vraag in de eerste {FOLD} tekens. "
                         "Zet de vraag/CTA bovenaan (boven 'Lees meer').")


def main(path, dry=False, window=DEFAULT_WINDOW):
    with open(path) as f:
        queue = json.load(f)
    for item in queue:
        check_fold(item)
    planned = plan(queue, dt.datetime.now(AMS), window)
    for when, item in planned:
        print(f"{when:%H:%M:%S}  {item.get('label', '')}: {item['tekst'][:70]!r}", flush=True)
    if dry:
        return
    hyves_api.token()  # fail early if login does not work
    results = []
    for when, item in planned:
        wait = (when - dt.datetime.now(AMS)).total_seconds()
        if wait > 0:
            time.sleep(wait)
        try:
            try:
                res = hyves_api.post_to_group(item["hyve_id"], item["tekst"], item.get("afbeeldingen", ()),
                                              item.get("link"))
            except SystemExit as e:
                # HTTP 400 means nothing was created, so trying once without images is safe
                if "HTTP 400" not in str(e) or not item.get("afbeeldingen"):
                    raise
                print(f"{dt.datetime.now(AMS):%H:%M:%S}  afbeelding geweigerd, opnieuw zonder: {e}", flush=True)
                res = hyves_api.post_to_group(item["hyve_id"], item["tekst"], (), item.get("link"))
                res = {"zonder_afbeelding": True, "antwoord": res}
            results.append({"label": item.get("label"), "geplaatst": dt.datetime.now(AMS).isoformat(), "antwoord": res})
            print(f"{dt.datetime.now(AMS):%H:%M:%S}  geplaatst: {item.get('label', '')}", flush=True)
        except SystemExit as e:  # keep going with the other posts
            results.append({"label": item.get("label"), "fout": str(e)})
            print(f"{dt.datetime.now(AMS):%H:%M:%S}  MISLUKT: {item.get('label', '')}: {e}", flush=True)
        with open(path + ".resultaat.json", "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    window = sys.argv[sys.argv.index("--venster") + 1] if "--venster" in sys.argv else DEFAULT_WINDOW
    main(sys.argv[1], dry="--droog" in sys.argv, window=window)
