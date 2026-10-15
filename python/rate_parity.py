"""Which booking site is cheapest for each hotel? Compares Booking.com, Expedia, Agoda, the official site...

    python rate_parity.py "Paris"
"""
import os
import sys
from datetime import date, timedelta

from apify_client import ApifyClient

city = sys.argv[1] if len(sys.argv) > 1 else "Paris"
check_in = date.today() + timedelta(days=21)

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("zet46/google-hotels-scraper").call(run_input={
    "queries": [city],
    "checkIn": check_in.isoformat(),
    "checkOut": (check_in + timedelta(days=1)).isoformat(),
    "currency": "USD",
    "maxHotelsPerQuery": 10,
    "includeProviderPrices": True,
})

for h in client.dataset(run.default_dataset_id).iterate_items():
    providers = h.get("providers") or []
    if not providers:
        continue
    cheapest, priciest = providers[0], providers[-1]
    spread = (priciest["pricePerNight"] - cheapest["pricePerNight"]) / cheapest["pricePerNight"] * 100
    print(f'\n{h["name"]}  ({len(providers)} booking sites, {spread:.0f}% spread)')
    for p in providers[:5]:
        print(f'   {p["provider"][:28]:28} {p["pricePerNightText"]:>6}')
