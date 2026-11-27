#!/usr/bin/env python3
"""Small client for the Hyves API (https://api.hyves.nl/v1/).

Login uses the same OAuth2 flow as the Hyves web app (authorization code +
PKCE through the hosted login form at auth.hyves.nl). Credentials are read
from the environment variables HYVES_EMAIL and HYVES_PASSWORD; they are never
written to disk. The resulting tokens are cached in ~/.cache/hyves-bot/.

Usage:
  python3 hyves_api.py login                  # log in and cache the token
  python3 hyves_api.py me                     # show the logged-in account
  python3 hyves_api.py groups [ZOEKTERM]      # list/search hyves (groups)
  python3 hyves_api.py posts GROUP_ID [N]     # latest N posts in a hyve
  python3 hyves_api.py post GROUP_ID FILE [AFBEELDING ...]  # post text in FILE (+ images)
  python3 hyves_api.py raw METHOD PATH [JSON] # any API call, for debugging
"""
import base64
import hashlib
import html
import json
import os
import re
import secrets
import sys
import time
import urllib.parse

import requests

CLIENT_ID = "38e5b2e0-67de-4150-b71c-0e744b0ac489"  # public client id of the Hyves web app
REDIRECT_URI = "https://hyves.nl/auth"
AUTH = "https://auth.hyves.nl"
API = "https://api.hyves.nl/v1/"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
CACHE = os.path.expanduser("~/.cache/hyves-bot/token.json")


def _save(tok):
    tok["obtained_at"] = int(time.time())
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w") as f:
        json.dump(tok, f)
    os.chmod(CACHE, 0o600)
    return tok


def _hidden_fields(page):
    form = {}
    for tag in re.findall(r'<input[^>]*type="hidden"[^>]*>', page):
        name = re.search(r'name="([^"]+)"', tag)
        value = re.search(r'value="([^"]*)"', tag)
        if name:
            form[name.group(1)] = html.unescape(value.group(1)) if value else ""
    return form


def _page_text(page):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", "", page, flags=re.S)
    return " ".join(re.sub(r"<[^>]+>", " ", text).split())


def _auto_submit(s, r):
    """The 'complete registration' page: a browser submits it automatically when
    there is nothing to fill in. Do the same, but stop when the page asks for
    real input (personal details, accepting terms) - that is for Ben to do."""
    visible = []
    for tag in re.findall(r"<(?:input|select|textarea)[^>]*>", r.text):
        typ = (re.search(r'type="([^"]+)"', tag) or [None, "text"])[1]
        name = (re.search(r'name="([^"]+)"', tag) or [None, ""])[1]
        if typ not in ("hidden", "submit", "button") and name:
            visible.append(name)
    if visible:
        raise SystemExit("Hyves vraagt om de registratie af te ronden met deze velden: "
                         f"{', '.join(visible)}. Ben moet dit zelf eenmalig doen. Pagina: {_page_text(r.text)[:300]}")
    action = re.search(r'<form[^>]*action="([^"]*)"', r.text)
    url = urllib.parse.urljoin(r.url, html.unescape(action.group(1)) if action else r.url)
    r = s.post(url, data=_hidden_fields(r.text), allow_redirects=False, timeout=30)
    return r, r.headers.get("Location", "")


def login():
    user, password = os.environ.get("HYVES_EMAIL"), os.environ.get("HYVES_PASSWORD")
    if not user or not password:
        raise SystemExit("HYVES_EMAIL en HYVES_PASSWORD zijn niet gezet in deze omgeving.")
    s = requests.Session()
    s.headers["User-Agent"] = UA
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(40)).rstrip(b"=").decode()
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16)
    r = s.get(f"{AUTH}/oauth2/authorize", timeout=30, params=dict(
        client_id=CLIENT_ID, response_type="code", scope="openid offline_access",
        redirect_uri=REDIRECT_URI, code_challenge=challenge, code_challenge_method="S256", state=state))
    r.raise_for_status()
    form = _hidden_fields(r.text)
    # what the login page's own JavaScript fills in a browser
    form.update(timezone="Europe/Amsterdam", **{"metaData.device.name": "hyves-bot",
                                                 "metaData.device.type": "BROWSER"})
    form.update(loginId=user, password=password)
    r = s.post(f"{AUTH}/oauth2/authorize", data=form, allow_redirects=False, timeout=30)
    loc = r.headers.get("Location", "")
    for _ in range(5):  # follow intermediate pages the way a browser would
        if r.status_code in (302, 303) and "code=" in loc:
            break
        if r.status_code in (302, 303) and loc:
            r = s.get(urllib.parse.urljoin(AUTH, loc), allow_redirects=False, timeout=30)
            loc = r.headers.get("Location", "")
            continue
        if r.status_code == 200 and "<form" in r.text and "complete-registration" in r.url:
            r, loc = _auto_submit(s, r)
            continue
        break
    if r.status_code not in (302, 303) or "code=" not in loc:
        raise SystemExit(f"Inloggen mislukt (HTTP {r.status_code}, {r.url if r.status_code == 200 else loc[:150]}): "
                         f"{_page_text(r.text)[:400]}")
    q = urllib.parse.parse_qs(urllib.parse.urlparse(loc).query)
    if q.get("state", [""])[0] != state:
        raise SystemExit("Inloggen mislukt: state klopt niet")
    r = s.post(f"{AUTH}/oauth2/token", timeout=30, data=dict(
        grant_type="authorization_code", client_id=CLIENT_ID, code=q["code"][0],
        redirect_uri=REDIRECT_URI, code_verifier=verifier))
    r.raise_for_status()
    return _save(r.json())


def _refresh(tok):
    r = requests.post(f"{AUTH}/oauth2/token", timeout=30, headers={"User-Agent": UA}, data=dict(
        grant_type="refresh_token", client_id=CLIENT_ID, refresh_token=tok["refresh_token"]))
    if r.status_code != 200:
        return None
    new = r.json()
    new.setdefault("refresh_token", tok["refresh_token"])
    return _save(new)


def token():
    try:
        with open(CACHE) as f:
            tok = json.load(f)
    except (OSError, ValueError):
        return login()
    if time.time() < tok.get("obtained_at", 0) + tok.get("expires_in", 0) - 120:
        return tok
    return (tok.get("refresh_token") and _refresh(tok)) or login()


def call(method, path, body=None, params=None):
    for attempt in (1, 2):
        tok = token()
        r = requests.request(method, urllib.parse.urljoin(API, path.lstrip("/")), json=body, params=params,
                             timeout=30, headers={"Authorization": f"Bearer {tok['access_token']}",
                                                  "Accept": "application/json", "User-Agent": UA})
        if r.status_code == 401 and attempt == 1:
            os.remove(CACHE)  # token rejected: log in again once
            continue
        break
    if r.status_code >= 400:
        raise SystemExit(f"{method} {path} -> HTTP {r.status_code}: {r.text[:500]}")
    return r.json() if r.content else None


def post_to_group(group_id, text, images=()):
    """Places a post in a hyve, optionally with images (paths to PNG/JPEG files).
    Request shape taken from the web app: CreatePostDto with ImageAttachmentDto(base64Data, filename)."""
    body = {"text": text}
    if images:
        body["images"] = []
        for path in images:
            with open(path, "rb") as f:
                body["images"].append({"base64Data": base64.b64encode(f.read()).decode(),
                                       "filename": os.path.basename(path)})
    return call("POST", f"groups/{group_id}/posts", body=body)


def _print(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    cmd, args = argv[0], argv[1:]
    if cmd == "login":
        tok = login()
        print("Ingelogd. Token geldig voor", tok.get("expires_in"), "seconden; refresh token:", "ja" if tok.get("refresh_token") else "nee")
    elif cmd == "me":
        _print(call("GET", "account/me"))
    elif cmd == "groups":
        _print(call("GET", "groups", params={"query": args[0]} if args else None))
    elif cmd == "posts":
        _print(call("GET", f"groups/{args[0]}/posts", params={"limit": args[1] if len(args) > 1 else 20}))
    elif cmd == "post":
        with open(args[1]) as f:
            text = f.read().strip()
        _print(post_to_group(args[0], text, args[2:]))
    elif cmd == "raw":
        _print(call(args[0].upper(), args[1], body=json.loads(args[2]) if len(args) > 2 else None))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
