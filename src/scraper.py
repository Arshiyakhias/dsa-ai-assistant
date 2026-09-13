from playwright.sync_api import sync_playwright
import json
import os

BOOK_URL = "https://pressbooks.palni.org/anopenguidetodatastructuresandalgorithms/"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Open the main textbook page
    page.goto(BOOK_URL, wait_until="networkidle")

    print("Book title:", page.title())

    # Find all links
    links = page.locator("a")

    chapters = []

    for i in range(links.count()):

        link = links.nth(i)

        text = link.inner_text().strip()
        href = link.get_attribute("href")

        # Keep only chapter links
        if text and href and "/chapter/" in href:

            chapters.append({
                "title": text,
                "url": href
            })

    print(f"Found {len(chapters)} chapters.")

    book_data = []

    # Scrape every chapter
    for number, chapter in enumerate(chapters, start=1):

        print(f"\nScraping Chapter {number}: {chapter['title']}")

        page.goto(chapter["url"], wait_until="networkidle")

        # Get only the main content
        content = page.locator("main").inner_text()

        # Remove website navigation at the bottom
        if "Previous/next navigation" in content:
            content = content.split("Previous/next navigation")[0]

        # Remove unnecessary whitespace
        content = content.strip()

        book_data.append({
            "chapter_number": number,
            "title": chapter["title"],
            "url": chapter["url"],
            "content": content
        })

        print(f"Finished Chapter {number}")

    browser.close()


# Create data folder if necessary
os.makedirs("data", exist_ok=True)

# Save scraped textbook
with open("data/book.json", "w", encoding="utf-8") as file:

    json.dump(
        book_data,
        file,
        indent=2,
        ensure_ascii=False
    )

print("\nAll chapters scraped successfully!")
print("Saved to: data/book.json")