from playwright.sync_api import sync_playwright
import sys

URL = "https://example.com/your-link"

KEY_SECTIONS = [
    "Welcome to Our Page",
    "Pricing",
    "Contact Us"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(4000)  # catch delayed JS redirects

    final_url = page.url
    content = page.content()

    browser.close()

if final_url != URL:
    print(f"REDIRECT DETECTED → {final_url}")
    sys.exit(1)

for text in KEY_SECTIONS:
    if text not in content:
        print(f"MISSING CONTENT → '{text}'")
        sys.exit(1)

print("OK — no redirect, key content intact")
