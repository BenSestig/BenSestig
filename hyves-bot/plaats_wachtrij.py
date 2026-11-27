#!/usr/bin/env python3
"""Places a queue of posts on Hyves at random, human-looking moments.

Every post gets its own random time between 11:00 and 13:00 (Amsterdam time),
drawn from a triangular distribution that peaks at 12:00. Posts are at least
MIN_GAP minutes apart, never scheduled in the past, and never after the post's
optional "uiterlijk" (latest) time. The script then waits and posts each one.

Usage:
  python3 plaats_wachtrij.py wachtrij.json          # schedule and post
  python3 plaats_wachtrij.py wachtrij.json --droog  # only show the schedule

wachtrij.json is a list of:
  {"label": "voetbal", "hyve_id": "...", "tekst": "...", "uiterlijk": "11:45"}
("uiterlijk" is optional). Results are written to wachtrij.json.resultaat.json.
"""
import datetime as dt
import json
import random
import sys
import time
from zoneinfo import ZoneInfo

import hyves_api

AMS = ZoneInfo("Europe/Amsterdam")
START, PEAK, END = dt.time(11, 0), dt.time(12, 0), dt.time(13, 0)
MIN_GAP = dt.timedelta(minutes=7)


def _sample(queue, lo, at):
    planned = []
    for item in queue:
        hi = item["_hi"]
        if hi <= lo:  # window already passed: post soon
            when = lo + dt.timedelta(seconds=random.randint(0, 240))
        else:
            mode = min(max(at(PEAK), lo), hi)
            when = dt.datetime.fromtimestamp(random.triangular(lo.timestamp(), hi.timestamp(), mode.timestamp()), AMS)
        planned.append([when.replace(microsecond=0), item])
    planned.sort(key=lambda p: p[0])
    for i in range(1, len(planned)):  # keep posts apart
        if planned[i][0] - planned[i - 1][0] < MIN_GAP:
            planned[i][0] = planned[i - 1][0] + MIN_GAP + dt.timedelta(seconds=random.randint(0, 180))
    return planned


def plan(queue, now):
    at = lambda t: dt.datetime.combine(now.date(), t, AMS)
    lo = max(at(START), now + dt.timedelta(minutes=2))
    for item in queue:
        item["_hi"] = at(END)
        if item.get("uiterlijk"):
            item["_hi"] = min(item["_hi"], at(dt.time.fromisoformat(item["uiterlijk"])))
    for _ in range(200):  # redraw until every post with a deadline makes it in time
        planned = _sample(queue, lo, at)
        if all(when <= max(item["_hi"], lo + dt.timedelta(minutes=5)) for when, item in planned):
            return planned
    # fallback: earliest deadline first, MIN_GAP apart
    planned, when = [], lo
    for item in sorted(queue, key=lambda i: i["_hi"]):
        planned.append([when, item])
        when += MIN_GAP
    return planned


def main(path, dry=False):
    with open(path) as f:
        queue = json.load(f)
    planned = plan(queue, dt.datetime.now(AMS))
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
            res = hyves_api.post_to_group(item["hyve_id"], item["tekst"])
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
    main(sys.argv[1], dry="--droog" in sys.argv)
