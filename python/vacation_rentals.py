"""Vacation rentals (apartments, villas, houses) for your dates, filtered by bedrooms and price.

    python vacation_rentals.py "Lisbon"
"""
import os
import sys
from datetime import date, timedelta

from apify_client import ApifyClient

place = sys.argv[1] if len(sys.argv) > 1 else "Lisbon"
check_in = date.today() + timedelta(days=45)

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("zet46/google-vacation-rentals-scraper").call(run_input={
    "queries": [place],
    "checkIn": check_in.isoformat(),
    "checkOut": (check_in + timedelta(days=3)).isoformat(),
    "currency": "USD",
    "maxHotelsPerQuery": 15,
    "minBedrooms": 2,
    "maxPricePerNight": 250,
})

for r in client.dataset(run.default_dataset_id).iterate_items():
    print(f'{r["name"][:45]:45} {r["propertyType"] or "":18} sleeps {r["sleeps"]}, '
          f'{r["bedrooms"]} bd  {r["pricePerNightText"]:>5}/night  rating {r["rating"]}')
