"""
PART 2 — The same technique against a JavaScript-rendered page.

quotes.toscrape.com/js looks identical in the browser, but the quotes
are injected by a script AFTER the page loads. requests only ever sees
the initial HTML the server sends — before that script runs — so this
will find zero quotes. 
"""

import requests
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com/js/"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.select(".quote")

print(f"Found {len(quotes)} quotes on the page.")
print("(The HTML requests sees is missing the JS-rendered content —")
print(" open view-source: on this URL and search for 'quote' to see why.)")