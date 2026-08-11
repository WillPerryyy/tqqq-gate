# TQQQ Gate

A single-page reading of the three-gate TQQQ/T-bill rule, computed in the browser
from live QQQ daily closes.

- **Gate 1** — 20-day realised volatility, annualised, below 35%
- **Gate 2** — 20-day vol divided by 250-day vol, below 1.10
- **Gate 3** — drawdown from the 250-day high better than −20%, re-entry above −10%

All three must pass, holding two consecutive sessions, to read HOLD TQQQ.

Verified at 99.98% signal agreement with the tested Python rule
(`tqqq-strategy/spec.py`) across 6,646 sessions, 2000–2026.

No API key and nothing to configure. `update_data.py` runs on a weekday schedule
via GitHub Actions, pulls QQQ closes server-side (where CORS does not apply) and
commits `data.json`; the page reads that file same-origin.

That design exists because neither browser route works: Yahoo has the data but
sends no CORS header, and Alpha Vantage sends CORS but puts history beyond 100
days behind a paid plan — short of the 250 sessions the gates need.

Reads the prior close; act at today's close. Not investment advice.
