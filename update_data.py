"""Fetch QQQ daily closes and write data.json for the page to read.

Why this exists: the browser cannot fetch price data directly. Yahoo has the
data but sends no CORS header, so Safari blocks it. Alpha Vantage sends CORS
but puts full history behind a paid plan, and the free 100-day `compact`
response is short of the 250 sessions the gates need.

Running server-side sidesteps both problems at once. CORS is a browser rule and
does not apply here, so this can read Yahoo directly; the result is committed to
the repo and served same-origin, which means the page needs no API key, has no
rate limit, and nothing to configure.

Freshness is not a compromise either: the rule reads the PRIOR close by design,
so a once-daily refresh after the close is exactly the cadence it wants.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

SYMBOL = "QQQ"
KEEP = 420          # 250-day windows plus comfortable margin
URL = ("https://query1.finance.yahoo.com/v8/finance/chart/"
       f"{SYMBOL}?range=3y&interval=1d")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")


def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def main():
    d = fetch()
    res = d["chart"]["result"][0]
    stamps = res["timestamp"]
    closes = res["indicators"]["quote"][0]["close"]

    rows = [(datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%d"), c)
            for t, c in zip(stamps, closes) if c is not None]
    rows = rows[-KEEP:]
    if len(rows) < 300:
        print(f"FAIL: only {len(rows)} sessions returned, refusing to write",
              file=sys.stderr)
        return 1

    dates = [r[0] for r in rows]
    vals = [round(float(r[1]), 4) for r in rows]

    # A split shows up as an impossible one-day move in this series. Refuse
    # rather than publish data that would produce a wrong signal.
    for i in range(1, len(vals)):
        move = vals[i] / vals[i - 1] - 1
        if abs(move) > 0.25:
            print(f"FAIL: {move*100:.1f}% move on {dates[i]} looks like a split, "
                  f"not a market move; refusing to write", file=sys.stderr)
            return 1

    payload = {
        "symbol": SYMBOL,
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_close": dates[-1],
        "sessions": len(dates),
        "dates": dates,
        "closes": vals,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, separators=(",", ":"))
    print(f"wrote data.json  {len(dates)} sessions  {dates[0]} -> {dates[-1]}  "
          f"last close {vals[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
