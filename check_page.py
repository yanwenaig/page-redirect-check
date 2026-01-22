from playwright.sync_api import sync_playwright

PAGES = [
    {
        "url": "https://www.aig.sg/travel",
        "expect_redirect": False,   # expected redirect (test case)
        "key_sections": [
            "Travel Guard",
            "Support"
        ]
    },
    {
        "url": "https://www.aig.sg/home/solutions/personal/home-insurance",
        "expect_redirect": False,
        "key_sections": [
            "Current Promotion",
            "Customer Reviews"
        ]
    },
    {
        "url": "https://www.travelguard.com.sg/global-markets",
        "expect_redirect": False,
        "key_sections": [
            "Travel Guard",
            "Important Information"
        ]
    }
]

def check_page(page, target):
    issues = []

    # Load page and allow JS to run
    page.goto(target["url"], wait_until="domcontentloaded")
    page.wait_for_timeout(6000)  # catch delayed JS redirects

    redirected = page.url != target["url"]

    # Redirect detection
    if redirected:
        print(f"REDIRECT DETECTED → {target['url']} → {page.url}")

        if not target.get("expect_redirect", False):
            issues.append(
                f"UNEXPECTED REDIRECT → {target['url']} → {page.url}"
            )
    else:
        if target.get("expect_redirect", False):
            issues.append(
                f"EXPECTED REDIRECT DID NOT OCCUR → {target['url']}"
            )

    # Content check (case-insensitive)
    content = page.content().lower()

    for text in target["key_sections"]:
        if text.lower() not in content:
            issues.append(
                f"MISSING CONTENT → '{text}'"
            )

    return issues


all_issues = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for target in PAGES:
        issues = check_page(page, target)
        if issues:
            all_issues[target["url"]] = issues
        else:
            print(f"OK → {target['url']}")

    browser.close()

# Final summary + alert trigger
if all_issues:
    print("\n=== ISSUES DETECTED ===")
    for url, issues in all_issues.items():
        print(f"\n{url}")
        for issue in issues:
            print(f"  - {issue}")

    raise SystemExit(1)

print("\nALL PAGES OK")
