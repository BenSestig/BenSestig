#!/usr/bin/env python3
"""Lists the latest videos of a YouTube channel (about 30, newest first).

Tries the channel's RSS feed first; when YouTube refuses it (it often answers
503 to servers), it reads the channel's public "Videos" page instead.

Usage:
  python3 youtube.py CHANNEL    # CHANNEL = channel URL, @handle or UC... channel id
Prints JSON list: [{"id", "title", "url", "published"}]. "published" is an ISO
date from RSS, or YouTube's relative text (e.g. "3 dgn geleden") from the page.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET

import requests

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36",
      "Accept-Language": "nl-NL,nl;q=0.9"}
COOKIES = {"CONSENT": "YES+1"}
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}


def channel_id(channel):
    m = re.search(r"(UC[\w-]{22})", channel)
    if m:
        return m.group(1)
    if not channel.startswith("http"):
        channel = "https://www.youtube.com/" + (channel if channel.startswith("@") else "@" + channel)
    r = requests.get(channel, headers=UA, cookies=COOKIES, timeout=30)
    m = re.search(r'"(?:channelId|externalId)":"(UC[\w-]{22})"', r.text) or re.search(r"channel/(UC[\w-]{22})", r.text)
    if r.status_code != 200 or not m:
        raise SystemExit(f"Kan geen YouTube-kanaal vinden voor {channel} (HTTP {r.status_code})")
    return m.group(1)


def _url(vid):
    return f"https://www.youtube.com/watch?v={vid}"


def from_rss(cid):
    r = requests.get("https://www.youtube.com/feeds/videos.xml", params={"channel_id": cid}, headers=UA, timeout=30)
    if r.status_code != 200:
        return None
    root = ET.fromstring(r.content)
    return [{"id": (vid := e.findtext("yt:videoId", namespaces=NS)), "title": e.findtext("a:title", namespaces=NS),
             "url": _url(vid), "published": e.findtext("a:published", namespaces=NS)}
            for e in root.findall("a:entry", NS)]


def from_page(cid):
    r = requests.get(f"https://www.youtube.com/channel/{cid}/videos", headers=UA, cookies=COOKIES, timeout=30)
    r.raise_for_status()
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", r.text, re.S)
    if not m:
        raise SystemExit("YouTube-pagina heeft een onbekend formaat")
    out = []

    def walk(o):
        if isinstance(o, dict):
            v = o.get("lockupViewModel")
            if v and v.get("contentType") == "LOCKUP_CONTENT_TYPE_VIDEO":
                md = v.get("metadata", {}).get("lockupMetadataViewModel", {})
                rows = md.get("metadata", {}).get("contentMetadataViewModel", {}).get("metadataRows", [])
                parts = [p.get("text", {}).get("content", "") for row in rows for p in row.get("metadataParts", [])]
                out.append({"id": v["contentId"], "title": md.get("title", {}).get("content"),
                            "url": _url(v["contentId"]), "published": next((p for p in parts if "geleden" in p or "ago" in p), None)})
            v = o.get("videoRenderer")  # older page layout
            if v:
                out.append({"id": v["videoId"], "title": v["title"]["runs"][0]["text"], "url": _url(v["videoId"]),
                            "published": v.get("publishedTimeText", {}).get("simpleText")})
            for x in o.values():
                walk(x)
        elif isinstance(o, list):
            for x in o:
                walk(x)

    walk(json.loads(m.group(1)))
    return out


def videos(channel):
    cid = channel_id(channel)
    return from_rss(cid) or from_page(cid)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    print(json.dumps(videos(sys.argv[1]), indent=2, ensure_ascii=False))
