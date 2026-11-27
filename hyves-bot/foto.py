#!/usr/bin/env python3
"""Finds real photos that may be reused freely, on Wikimedia Commons.

Only these licences are accepted:
  - CC0 / public domain: free to use, no credit needed;
  - CC BY / CC BY-SA: free to use, but the post must credit the photo
    (the "naamsvermelding" line printed by `haal`).

Usage:
  python3 foto.py zoek "poker chips"            # candidates as JSON (best first)
  python3 foto.py zoek "poker chips" --zonder-naam  # only CC0 / public domain
  python3 foto.py haal "File:Poker chips 2.jpg" /tmp/foto.jpg
      -> saves a 1280px JPEG (metadata stripped) and prints JSON with the
         licence and, if required, the credit line to put under the post.
"""
import io
import json
import re
import sys
import time

import requests
from PIL import Image

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "hyves-community-bot/1.0 (small script that illustrates community posts)"}
FREE = ("cc0", "public domain", "pdm", "pd")
CREDIT = ("cc by", "cc-by")
BLOCK = ("nc", "nd", "fair use", "non-free")


def _get(url, **params):
    for attempt in range(5):
        r = requests.get(url, params=params or None, headers=HEADERS, timeout=30)
        if r.status_code == 200 and (not params or r.text.lstrip().startswith("{")):
            return r
        time.sleep(3 * (attempt + 1))  # Wikimedia throttles quick repeats
    r.raise_for_status()
    raise SystemExit(f"Wikimedia gaf geen geldig antwoord voor {url}")


def _clean(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html or "")).strip()


def _licence(meta):
    name = _clean(meta.get("LicenseShortName", {}).get("value"))
    low = name.lower()
    if not name or any(b in low.replace("-", " ").split() for b in BLOCK) or "non-free" in low:
        return name, None
    if any(low.startswith(f) for f in FREE) or "public domain" in low:
        return name, False
    if any(low.startswith(c) for c in CREDIT):
        return name, True
    return name, None


def _info(titles=None, search=None, limit=20):
    params = dict(action="query", format="json", prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=1280)
    if search:
        params.update(generator="search", gsrsearch=f"{search} filetype:bitmap", gsrnamespace=6, gsrlimit=limit)
    else:
        params["titles"] = titles
    pages = _get(API, **params).json().get("query", {}).get("pages", {})
    return sorted(pages.values(), key=lambda p: p.get("index", 0))


def _describe(p):
    ii = p["imageinfo"][0]
    meta = ii.get("extmetadata", {})
    name, credit = _licence(meta)
    return {
        "titel": p["title"],
        "licentie": name,
        "naamsvermelding_nodig": credit,
        "maker": _clean(meta.get("Artist", {}).get("value"))[:80],
        "beschrijving": _clean(meta.get("ImageDescription", {}).get("value"))[:160],
        "breedte": ii["width"], "hoogte": ii["height"],
        "pagina": ii.get("descriptionurl"),
        "url": ii.get("thumburl") or ii.get("url"),
    }


def zoek(query, only_free=False):
    out = []
    for p in _info(search=query):
        d = _describe(p)
        if d["naamsvermelding_nodig"] is None:  # unknown or not free: skip
            continue
        if only_free and d["naamsvermelding_nodig"]:
            continue
        if d["breedte"] < 1000 or d["hoogte"] < 600:
            continue
        out.append(d)
    out.sort(key=lambda d: d["naamsvermelding_nodig"])  # free-without-credit first
    return out


def haal(title, dest):
    pages = _info(titles=title)
    if not pages or "imageinfo" not in pages[0]:
        raise SystemExit(f"Foto niet gevonden: {title}")
    d = _describe(pages[0])
    if d["naamsvermelding_nodig"] is None:
        raise SystemExit(f"Licentie niet vrij bruikbaar: {d['licentie']}")
    img = Image.open(io.BytesIO(_get(d["url"]).content)).convert("RGB")
    img.thumbnail((1280, 1280))
    clean = Image.new("RGB", img.size)
    clean.paste(img)  # drops EXIF and other metadata
    clean.save(dest, "JPEG", quality=88, optimize=True)
    if d["naamsvermelding_nodig"]:
        d["naamsvermelding"] = f"Foto: {d['maker'] or 'onbekend'} / Wikimedia Commons ({d['licentie']}) {d['pagina']}"
    d["bestand"] = dest
    return d


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("zoek", "haal"):
        raise SystemExit(__doc__)
    if sys.argv[1] == "zoek":
        res = zoek(sys.argv[2], only_free="--zonder-naam" in sys.argv)
    else:
        res = haal(sys.argv[2], sys.argv[3])
    print(json.dumps(res, indent=2, ensure_ascii=False))
