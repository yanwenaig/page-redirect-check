from playwright.sync_api import sync_playwright
import sys

PAGES = [
    {
        "url": "https://www.aig.sg/travel",
        "key_sections": [
            "Travel Guard",
            "Support"
        ]
    },
    {
        "url": "https://www.aig.sg/home/solutions/personal/home-insurance",
        "key_sections": [
            "Current Promotion",
            "Customer Reviews"
        ]
    },
    {
        "url": "https://www.travelguard.com.sg/global-markets",
        "key_sections": [
            "Travel Guard",
            "Important Information"
        ]
    }    
]

def check_page(page, target):
    page.goto(target["url"], wait_until="domcontentloaded")
    page.wait_for_timeout(6000)  # catch delayed JS redirects

    # 1️⃣ Redirect check
    if page.url != target["url"]:
        print(f"REDIRECT DETECTED → {target['url']} → {page.url}")
        return False

    # 2️⃣ Content check
    content = page.content()
    for text in target["key_sections"]:
        if text not in content:
            print(f"MISSING CONTENT on {target['url']} → '{text}'")
            return False

    print(f"OK → {target['url']}")
    return True

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for target in PAGES:
        if not check_page(page, target):
            browser.close()
            sys.exit(1)

    browser.close()

print("ALL PAGES OK")
