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
  python3 hyves_api.py post GROUP_ID FILE     # post the text in FILE to a hyve
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
    form = {}
    for tag in re.findall(r'<input[^>]*type="hidden"[^>]*>', r.text):
        name = re.search(r'name="([^"]+)"', tag)
        value = re.search(r'value="([^"]*)"', tag)
        if name:
            form[name.group(1)] = html.unescape(value.group(1)) if value else ""
    form.update(loginId=user, password=password)
    r = s.post(f"{AUTH}/oauth2/authorize", data=form, allow_redirects=False, timeout=30)
    loc = r.headers.get("Location", "")
    if r.status_code not in (302, 303) or "code=" not in loc:
        text = re.sub(r"<script.*?</script>|<style.*?</style>", "", r.text, flags=re.S)
        text = " ".join(re.sub(r"<[^>]+>", " ", text).split())
        raise SystemExit(f"Inloggen mislukt (HTTP {r.status_code}): {text[:300]}")
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
        _print(call("POST", f"groups/{args[0]}/posts", body={"text": text}))
    elif cmd == "raw":
        _print(call(args[0].upper(), args[1], body=json.loads(args[2]) if len(args) > 2 else None))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
