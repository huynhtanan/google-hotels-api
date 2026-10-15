"""Price of one hotel for every date in the next 30 days, and the cheapest nights to book.

    python cheapest_dates.py "Hilton Paris Opera"
"""
import os
import sys

from apify_client import ApifyClient

hotel = sys.argv[1] if len(sys.argv) > 1 else "Hilton Paris Opera"
client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("zet46/google-hotels-price-calendar").call(run_input={
    "hotels": [hotel],
    "numberOfDates": 30,
    "nights": 1,
    "currency": "USD",
})

rows = [r for r in client.dataset(run.default_dataset_id).iterate_items() if r["lowestPricePerNight"]]
rows.sort(key=lambda r: r["lowestPricePerNight"])
print(f"{rows[0]['hotel']}: 5 cheapest nights in the next 30 days")
for r in rows[:5]:
    print(f'  {r["checkIn"]} ({r["dayOfWeek"][:3]})  ${r["lowestPricePerNight"]:.0f} on {r["cheapestProvider"]}')

summary = client.key_value_store(run.default_key_value_store_id).get_record("SUMMARY")["value"]
print("Average:", summary[0]["averagePricePerNight"], "| most expensive:", summary[0]["mostExpensiveDate"])
