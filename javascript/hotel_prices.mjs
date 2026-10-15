// Hotel prices from Google Hotels with Node.js.
//   npm install apify-client
//   APIFY_TOKEN=... node hotel_prices.mjs "Tokyo"
import { ApifyClient } from 'apify-client';

const city = process.argv[2] ?? 'Tokyo';
const checkIn = new Date(Date.now() + 30 * 864e5);
const checkOut = new Date(checkIn.getTime() + 2 * 864e5);
const iso = (d) => d.toISOString().slice(0, 10);

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('zet46/google-hotels-scraper').call({
    queries: [city],
    checkIn: iso(checkIn),
    checkOut: iso(checkOut),
    currency: 'JPY',
    maxHotelsPerQuery: 15,
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const h of items) {
    console.log(`${h.name.slice(0, 40).padEnd(40)} ${String(h.pricePerNightText).padStart(8)}  rating ${h.rating}`);
}
