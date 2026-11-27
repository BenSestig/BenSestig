#!/usr/bin/env python3
"""Draws a square image card (1080x1080 PNG) with Dutch club matches of a day:
results (with scores) for a finished day, or the programme with kick-off times.
Only text and colours, no photos or club logos, so there are no rights issues.

Usage:
  python3 kaart.py JJJJ-MM-DD uit.png ["Eigen titel"]
"""
import datetime as dt
import sys

from PIL import Image, ImageDraw, ImageFont

import voetbal

W = H = 1080
BG_TOP, BG_BOTTOM = (16, 84, 52), (6, 38, 24)
WHITE, MUTED, ACCENT = (255, 255, 255), (178, 214, 192), (255, 196, 0)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DAYS = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]
MONTHS = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus",
          "september", "oktober", "november", "december"]


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def fit(draw, text, max_w, size, bold=False):
    while size > 14 and draw.textlength(text, font=font(size, bold)) > max_w:
        size -= 2
    return font(size, bold)


def render(day, matches, out, title=None):
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):  # vertical gradient
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOTTOM)))
    finished = all("score" in m for m in matches)
    title = title or ("Uitslagen" if finished else "Vandaag op het programma")
    subtitle = f"{DAYS[day.weekday()]} {day.day} {MONTHS[day.month - 1]}"
    d.text((70, 70), title, font=fit(d, title, W - 140, 64, True), fill=WHITE)
    d.text((70, 150), subtitle, font=font(36), fill=ACCENT)

    # rows grouped per competition: a small header, then one bar per match
    order = list(voetbal.COMPETITIONS.values())
    matches = sorted(matches, key=lambda m: (order.index(m["competition"]) if m["competition"] in order else 99, m["kickoff"]))
    items, last = [], None
    for m in matches:
        if m["competition"] != last:
            items.append(("kop", m["competition"]))
            last = m["competition"]
        items.append(("duel", m))
    top, bottom = 240, H - 70
    sizes = {"kop": 54, "duel": 92}
    scale = min(1.0, (bottom - top) / sum(sizes[k] for k, _ in items))
    scale = max(scale, 0.62)
    shown, used = [], 0
    for k, v in items:
        if used + sizes[k] * scale > bottom - top + 0.5:
            break
        shown.append((k, v))
        used += sizes[k] * scale
    if shown and shown[-1][0] == "kop":
        shown.pop()
    hidden = sum(1 for k, _ in items if k == "duel") - sum(1 for k, _ in shown if k == "duel")

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    o = ImageDraw.Draw(overlay)
    y = top
    for k, v in shown:
        h = sizes[k] * scale
        if k == "duel":
            o.rounded_rectangle([60, y, W - 60, y + h - 12 * scale], radius=int(18 * scale), fill=(0, 0, 0, 80))
        y += h
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)

    y = top
    for k, v in shown:
        h = sizes[k] * scale
        if k == "kop":
            d.text((72, y + h - 34 * scale), v.upper(), font=font(int(24 * scale), True), fill=MUTED)
        else:
            mid = y + (h - 12 * scale) / 2
            centre = v.get("score", v["kickoff"]).replace("-", " – ")
            cf = font(int(44 * scale), True)
            cw = d.textlength(centre, font=cf)
            d.text((W / 2, mid), centre, font=cf, fill=ACCENT if "score" in v else WHITE, anchor="mm")
            side = W / 2 - cw / 2 - 30 - 80
            hf = fit(d, v["home"], side, int(38 * scale), True)
            d.text((W / 2 - cw / 2 - 28, mid), v["home"], font=hf, fill=WHITE, anchor="rm")
            af = fit(d, v["away"], side, int(38 * scale), True)
            d.text((W / 2 + cw / 2 + 28, mid), v["away"], font=af, fill=WHITE, anchor="lm")
        y += h
    if hidden:
        d.text((72, H - 60), f"+ {hidden} andere wedstrijden", font=font(28), fill=MUTED)
    d.text((W - 60, H - 46), "Hyves Voetbal", font=font(24, True), fill=MUTED, anchor="rm")
    img.convert("RGB").save(out, "PNG", optimize=True)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    day = dt.date.fromisoformat(sys.argv[1])
    matches = voetbal.matches_on(day)
    if not matches:
        raise SystemExit("Geen wedstrijden op die dag")
    render(day, matches, sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    print(sys.argv[2])
