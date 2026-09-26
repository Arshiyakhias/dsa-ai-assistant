"""
PART 3 — Scraping the JS-rendered page properly, with Playwright.

Playwright drives a real browser, so JavaScript actually runs and the
quotes get injected into the page before we read it. This is the fix
for what broke in Part 2.
"""

from playwright.sync_api import sync_playwright

URL = "http://quotes.toscrape.com/js/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")  # wait for the JS to finish

    quote_elements = page.locator(".quote")
    count = quote_elements.count()
    print(f"Found {count} quotes on the page.\n")

    for i in range(min(3, count)):  # just show the first 3 for the demo
        el = quote_elements.nth(i)
        text = el.locator(".text").inner_text()
        author = el.locator(".author").inner_text()
        tags = el.locator(".tags .tag").all_inner_texts()
        print(f"{text}\n  — {author}  {tags}\n")

    browser.close()
    