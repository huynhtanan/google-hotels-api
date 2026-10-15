"""Track Google Hotels prices for a list of competitor hotels, every day.

Set APIFY_TOKEN and run this file daily (cron, Task Scheduler, or Apify Scheduler calling a webhook).
Each run appends to a local SQLite database and prints how prices moved versus the previous observation.

    pip install "apify-client>=3"
    export APIFY_TOKEN=...
    python track_prices.py
"""
import os
import sqlite3
from datetime import date, timedelta
from pathlib import Path

from apify_client import ApifyClient

HOTELS = [
    # Any Google Hotels search term works. One hotel is kept per entry.
    "Hilton Paris Opera",
    "Pullman Paris Tour Eiffel",
    "Le Meurice Paris",
]
CHECK_IN = date.today() + timedelta(days=30)
CHECK_OUT = CHECK_IN + timedelta(days=1)
CURRENCY = "EUR"

DB = Path(__file__).with_name("prices.sqlite3")


def _attr(obj, snake, camel):
    if isinstance(obj, dict):
        return obj.get(camel) or obj.get(snake)
    return getattr(obj, snake, None) or getattr(obj, camel, None)


def fetch():
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor("zet46/google-hotels-scraper").call(run_input={
        "queries": HOTELS,
        "maxHotelsPerQuery": 1,
        "checkIn": CHECK_IN.isoformat(),
        "checkOut": CHECK_OUT.isoformat(),
        "currency": CURRENCY,
    })
    dataset_id = _attr(run, "default_dataset_id", "defaultDatasetId")
    started_at = _attr(run, "started_at", "startedAt")
    items = list(client.dataset(dataset_id).iterate_items())
    return str(started_at), items


def store(con, run_at, items):
    con.execute("""CREATE TABLE IF NOT EXISTS prices (
        run_at   TEXT NOT NULL,
        hotel    TEXT NOT NULL,
        check_in TEXT NOT NULL,
        nightly  REAL,
        total    REAL,
        currency TEXT,
        PRIMARY KEY (run_at, hotel, check_in))""")
    for h in items:
        con.execute("INSERT OR REPLACE INTO prices VALUES (?,?,?,?,?,?)",
                    (run_at, h["name"], CHECK_IN.isoformat(),
                     h.get("pricePerNight"), h.get("totalPrice"),
                     h.get("currency") or CURRENCY))
    con.commit()


def report(con, run_at):
    print(f"\nPrices on {run_at[:10]} for check-in {CHECK_IN} ({CURRENCY}):\n")
    today = con.execute(
        "SELECT hotel, nightly FROM prices WHERE run_at = ? ORDER BY hotel",
        (run_at,),
    ).fetchall()
    for hotel, nightly in today:
        prev = con.execute(
            """SELECT nightly, run_at FROM prices
               WHERE hotel = ? AND run_at < ? AND check_in = ? AND nightly IS NOT NULL
               ORDER BY run_at DESC LIMIT 1""",
            (hotel, run_at, CHECK_IN.isoformat()),
        ).fetchone()
        if nightly is None:
            print(f"  {hotel[:46]:46}       --   (sold out or missing)")
            continue
        if prev:
            diff = (nightly - prev[0]) / prev[0] * 100
            arrow = "DOWN" if diff < -0.5 else "UP" if diff > 0.5 else "flat"
            print(f"  {hotel[:46]:46}  {nightly:>7.2f}   {arrow:>4} {abs(diff):4.1f}%  "
                  f"(was {prev[0]:.2f} on {prev[1][:10]})")
        else:
            print(f"  {hotel[:46]:46}  {nightly:>7.2f}   (first observation)")


if __name__ == "__main__":
    run_at, items = fetch()
    with sqlite3.connect(DB) as con:
        store(con, run_at, items)
        report(con, run_at)
