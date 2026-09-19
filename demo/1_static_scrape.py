"""
PART 1 — Scraping a plain static HTML page.

quotes.toscrape.com serves fully-rendered HTML: the quotes are
already in the response the server sends back. requests + BeautifulSoup
is all we need here — no browser required.
"""

import requests
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com/"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.select(".quote")

print(f"Found {len(quotes)} quotes on the page.\n")

for q in quotes[:3]:  # just show the first 3 for the demo
    text = q.select_one(".text").get_text(strip=True)
    author = q.select_one(".author").get_text(strip=True)
    tags = [t.get_text(strip=True) for t in q.select(".tags .tag")]
    print(f'{text}\n  — {author}  {tags}\n')