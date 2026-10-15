# Google Hotels API examples (Python & Node.js)

Get **hotel prices from Google Hotels for any city and any dates**, in any currency, from Python or Node.js. You get:

- the nightly price and the **total stay price with taxes**
- **the price on every booking site** (Booking.com, Expedia, Agoda, Hotels.com, the hotel's own website...)
- ratings, reviews and what guests praise or complain about
- **the cheapest dates** for a specific hotel
- **vacation rentals** with bedrooms and guests

There is no official Google Hotels API. These examples call three ready-made scrapers on Apify
(pay-per-result, from $1.50 per 1,000 results, with free monthly credit for new accounts):

| Scraper | What it returns |
|---|---|
| [Google Hotels Scraper](https://apify.com/zet46/google-hotels-scraper) | Hotels for a city or area: prices, ratings, review topics, location, and booking-site prices |
| [Google Hotels Price Calendar](https://apify.com/zet46/google-hotels-price-calendar) | One hotel's price for every date in a range: cheapest dates, rate parity over time |
| [Google Vacation Rentals Scraper](https://apify.com/zet46/google-vacation-rentals-scraper) | Apartments, villas and houses: bedrooms, guests, amenities, prices |

## Setup

```bash
pip install "apify-client>=3"
export APIFY_TOKEN=...   # https://console.apify.com/settings/integrations (free account)
```

## 1. Hotels in a city under a budget ([python/hotel_prices.py](python/hotel_prices.py))

```bash
python python/hotel_prices.py "Lisbon"
```
```
Hotels in Lisbon, 2026-11-14 -> 2026-11-16, under 200 EUR/night
Brown's | Avenue Hotel                     5*   €171/night  total   378.16  rating 4.6 (282)
Dos Reis by The Beautique Hotels           4*   €104/night  total   235.54  rating 4.4 (423)
20-2 Lisbon Castle view apartment with Fre       €70/night  total   139.93  rating 5 (16)
Hotel Portugal - Portugal Boutique Hotel   4*   €128/night  total   285.90  rating 4.7 (1259)
Boutique Chiado Apartments & Suites        4*   €110/night  total   230.69  rating 4.6 (427)
Hotel Marquês de Pombal                    4*    €81/night  total   179.37  rating 4.4 (2460)
1908 Lisboa Hotel                          4*   €125/night  total   280.63  rating 4.7 (683)
Lisbon Wine House - Rooms & Suites         3*    €51/night  total   125.07  rating 3.7 (125)
```

## 2. Which booking site is cheapest? ([python/rate_parity.py](python/rate_parity.py))

```bash
python python/rate_parity.py "Paris"
```
```
Hôtel CHEVALLIER  (20 booking sites, 38% spread)
   Hotels.com                      $64
   Expedia.com                     $66
   Travelocity.com                 $66
   Orbitz.com                      $66
   CheapTickets.com                $66
Hôtel Madame Rêve  (33 booking sites, 45% spread)
   Traveluro                      $536
   trivago DEALS                  $541
   Evendo                         $559
   Super.com                      $577
   Clicktrip.com                  $592
Glint Paris  (16 booking sites, 58% spread)
   Booking.com                     $81
```

## 3. Cheapest nights to book a specific hotel ([python/cheapest_dates.py](python/cheapest_dates.py))

```bash
python python/cheapest_dates.py "Hilton Paris Opera"
```
```
Hilton Paris Opera: 5 cheapest nights in the next 30 days
  2026-11-01 (Sun)  $314 on KAYAK.com
  2026-11-08 (Sun)  $314 on KAYAK.com
  2026-11-14 (Sat)  $314 on KAYAK.com
  2026-10-26 (Mon)  $315 on Expedia.com
  2026-11-02 (Mon)  $327 on KAYAK.com
Average: 477.89 | most expensive: 2026-10-24
```

## 4. Vacation rentals with 2+ bedrooms ([python/vacation_rentals.py](python/vacation_rentals.py))

```bash
python python/vacation_rentals.py "Lisbon"
```
```
LOVELY FLAT. GREAT LOCATION, CASTLE VIEWS AND Entire apartment   sleeps 4, 2 bd   $193/night  rating 4.82
Alfama River View | Balcony | Families | Fast Entire apartment   sleeps 4, 2 bd   $123/night  rating 4.78
WHome City View Penthouse Luxurious Living in Entire apartment   sleeps 8, 3 bd   $224/night  rating 4.75
Alecrim 3 Luxury Tailor Made Flat With a View Entire apartment   sleeps 4, 2 bd   $243/night  rating 4.79
2 Bedroom Apartment with Great Transport Link Entire apartment   sleeps 4, 2 bd    $65/night  rating 4
Classy, elegant, comfortable, at the entrance Entire apartment   sleeps 4, 2 bd   $146/night  rating 4.91
```

## 5. Daily price tracking for competitor hotels ([python/track_prices.py](python/track_prices.py))

Run the script every day (cron, Windows Task Scheduler, or an Apify Scheduler that calls your own webhook).
Each run appends to a local SQLite file and prints how each hotel's nightly price moved since the previous observation:

```
Prices on 2026-10-15 for check-in 2026-11-14 (EUR):

  Hilton Paris Opera                               280.00   (first observation)
  Le Meurice                                      1535.00   (first observation)
  Pullman Paris Tour Eiffel                        320.00   (first observation)
```

On the next day you'll see something like:

```
  Hilton Paris Opera                               265.00   DOWN  5.4%  (was 280.00 on 2026-10-15)
  Le Meurice                                      1535.00   flat  0.0%  (was 1535.00 on 2026-10-15)
  Pullman Paris Tour Eiffel                        340.00     UP  6.3%  (was 320.00 on 2026-10-15)
```

The SQLite table has one row per `(run_at, hotel, check_in)`, so you can query the whole history with any SQL client,
plot it, or send yourself an alert when a competitor cuts prices by more than X%.
Full walkthrough: [Daily price tracking for competitor hotels on dev.to](https://dev.to/huynhtanan/daily-price-tracking-for-competitor-hotels-with-python-and-sqlite-2nda).

## Node.js ([javascript/hotel_prices.mjs](javascript/hotel_prices.mjs))

```bash
npm install apify-client
APIFY_TOKEN=... node javascript/hotel_prices.mjs "Tokyo"
```

## Use it from AI agents (MCP)

Give Claude, Cursor or any MCP client live hotel prices:

```json
{"mcpServers": {"apify": {"url": "https://mcp.apify.com?tools=zet46/google-hotels-scraper,zet46/google-hotels-price-calendar,zet46/google-vacation-rentals-scraper"}}}
```

Then ask things like *"Find 4-star hotels in Lisbon under 150 EUR for 12-14 December"*.

## No-code

Every scraper can also be run from the Apify web console. You can schedule it daily, export to CSV or Excel, or send results to Google Sheets, Slack, Zapier, Make or n8n.

---
Output above is from real runs (prices change constantly). MIT licensed.


## Tutorials

Deep-dive write-ups on dev.to:

- [How to get Google Hotels prices for any dates with Python](https://dev.to/huynhtanan/how-to-get-google-hotels-prices-for-any-dates-with-python-and-the-apify-api-2n7a)
- [Daily price tracking for competitor hotels, with Python and SQLite](https://dev.to/huynhtanan/daily-price-tracking-for-competitor-hotels-with-python-and-sqlite-5bfp)

Full series (all four actors): [Apify + Python: scrapers, trackers, and Claude Desktop](https://dev.to/huynhtanan/series/45271).

## See also

More repos from this account:

- [amazon-bestsellers-tracker](https://github.com/huynhtanan/amazon-bestsellers-tracker) - Daily Amazon Best Sellers rank, price and ASIN tracking in 17 country stores
- [walmart-deals-tracker](https://github.com/huynhtanan/walmart-deals-tracker) - Daily Walmart Rollback deal tracking with Python and SQLite
- [google-hotels-mcp](https://github.com/huynhtanan/google-hotels-mcp) - MCP server for Claude Desktop: Google Hotels search, price calendar, and vacation rentals
