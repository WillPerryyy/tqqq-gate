# TQQQ Gate

A single-page reading of the three-gate TQQQ/T-bill rule, computed in the browser
from live QQQ daily closes.

- **Gate 1** — 20-day realised volatility, annualised, below 35%
- **Gate 2** — 20-day vol divided by 250-day vol, below 1.10
- **Gate 3** — drawdown from the 250-day high better than −20%, re-entry above −10%

All three must pass, holding two consecutive sessions, to read HOLD TQQQ.

Verified at 99.98% signal agreement with the tested Python rule
(`tqqq-strategy/spec.py`) across 6,646 sessions, 2000–2026.

Needs a free [Alpha Vantage](https://www.alphavantage.co/support/#api-key) key —
the only price API that sends the CORS headers a browser requires. The key is
entered on your device and stored only in that device's localStorage. It is never
in this repository.

Reads the prior close; act at today's close. Not investment advice.
