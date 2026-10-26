"""Shared ESPN fetch with retries, so one flaky response doesn't break a script."""

import time

import httpx

BASE = "https://site.api.espn.com/apis"
ATTEMPTS = 4
# Rate limited or ESPN-side errors: worth waiting and trying again
RETRY_STATUSES = {429, 500, 502, 503, 504}


def get(path, params=None):
    for attempt in range(1, ATTEMPTS + 1):
        try:
            resp = httpx.get(BASE + path, params=params, timeout=15)
            if resp.status_code not in RETRY_STATUSES:
                resp.raise_for_status()
                return resp.json()
            reason = f"HTTP {resp.status_code}"
            retry_after = resp.headers.get("Retry-After", "")
            wait = int(retry_after) if retry_after.isdigit() else 2 ** attempt
        except httpx.TransportError as err:
            reason = type(err).__name__
            wait = 2 ** attempt

        if attempt == ATTEMPTS:
            raise RuntimeError(f"ESPN {path} failed after {ATTEMPTS} attempts ({reason})")
        print(f"ESPN {path}: {reason}, retrying in {wait}s")
        time.sleep(wait)