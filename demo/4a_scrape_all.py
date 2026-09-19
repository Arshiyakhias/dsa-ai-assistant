"""
PART 4a — Scrape every page and save the results.

Same static-HTML technique as Part 1, but looped across all 10 pages
of quotes.toscrape.com, with results saved to a JSON file so the next
script can turn them into something searchable.
"""

import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com/page/{}/"

all_quotes = []
page_number = 1

while True:
    response = requests.get(BASE_URL.format(page_number))
    soup = BeautifulSoup(response.text, "html.parser")
    quote_elements = soup.select(".quote")

    if not quote_elements:
        break  # no more pages

    for q in quote_elements:
        all_quotes.append({
            "text": q.select_one(".text").get_text(strip=True),
            "author": q.select_one(".author").get_text(strip=True),
            "tags": [t.get_text(strip=True) for t in q.select(".tags .tag")],
        })

    print(f"Scraped page {page_number} ({len(quote_elements)} quotes)")
    page_number += 1

with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(all_quotes, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(all_quotes)} quotes total to quotes.json")