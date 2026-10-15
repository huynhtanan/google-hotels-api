"""Hotel prices from Google Hotels for any city and dates.

    pip install "apify-client>=3"
    export APIFY_TOKEN=...   # free account at https://apify.com, token under Settings > API & Integrations
    python hotel_prices.py "Lisbon"
"""
import os
import sys
from datetime import date, timedelta

from apify_client import ApifyClient

city = sys.argv[1] if len(sys.argv) > 1 else "Lisbon"
check_in = date.today() + timedelta(days=30)
check_out = check_in + timedelta(days=2)

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("zet46/google-hotels-scraper").call(run_input={
    "queries": [city],
    "checkIn": check_in.isoformat(),
    "checkOut": check_out.isoformat(),
    "currency": "EUR",
    "maxHotelsPerQuery": 20,
    "maxPricePerNight": 200,
})

print(f"Hotels in {city}, {check_in} -> {check_out}, under 200 EUR/night")
for h in client.dataset(run.default_dataset_id).iterate_items():
    stars = f'{h["hotelClass"]}*' if h.get("hotelClass") else "  "
    print(f'{h["name"][:42]:42} {stars} {h["pricePerNightText"]:>6}/night  '
          f'total {h["totalPrice"]:>8.2f}  rating {h["rating"]} ({h["reviewsCount"]})')
