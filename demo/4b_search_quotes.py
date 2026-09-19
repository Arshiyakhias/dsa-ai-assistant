"""
PART 4b — Turn scraped data into a tiny "product".

No embeddings, no ML — just a plain keyword filter over the JSON we
scraped. The point for the demo: raw scraped data becomes something a
user can actually interact with in a few lines of code.
"""

import json

with open("quotes.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

keyword = input("Search quotes by keyword, author, or tag: ").strip().lower()

matches = [
    q for q in quotes
    if keyword in q["text"].lower()
    or keyword in q["author"].lower()
    or any(keyword in tag.lower() for tag in q["tags"])
]

print(f"\nFound {len(matches)} matching quote(s):\n")

for q in matches:
    print(f'"{q["text"]}"\n  — {q["author"]}  {q["tags"]}\n')