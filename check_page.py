from playwright.sync_api import sync_playwright

PAGES = [
    {
        "url": "https://www.aig.sg/travel",
        "expect_redirect": False,
        "key_sections": ["Travel Guard", "Support"]
    },
    {
        "url": "https://www.aig.sg/home/solutions/personal/home-insurance",
        "expect_redirect": False,
        "key_sections": ["Current Promotion", "Customer Reviews"]
    },
    {
        "url": "https://www.zurich.com.hk/zh-hk/products/travel/aig-redirect?utm_source=aig&utm_medium=referral&utm_campaign=travelredirect",
        "expect_redirect": False
    },
    {
        "url": "https://www.travelguard.com.sg/global-markets",
        "expect_redirect": False,
        "key_sections": ["Travel Guard", "Important Information"]
    }
]

def check_page(page, target):
    issues = []

    page.goto(target["url"], wait_until="domcontentloaded")
    page.wait_for_timeout(6000)

    redirected = page.url != target["url"]

    if redirected:
        print(f"REDIRECT DETECTED → {target['url']} → {page.url}")
        if not target["expect_redirect"]:
            issues.append(
                f"UNEXPECTED REDIRECT → {target['url']} → {page.url}"
            )
    else:
        if target["expect_redirect"]:
            issues.append(
                f"EXPECTED REDIRECT DID NOT OCCUR → {target['url']}"
            )

    content = page.content().lower()

    for text in target.get("key_sections", []):
        if text.lower() not in content:
            issues.append(f"MISSING CONTENT → '{text}'")

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

if all_issues:
    print("\n=== ISSUES DETECTED ===")
    for url, issues in all_issues.items():
        print(f"\n{url}")
        for issue in issues:
            print(f"  - {issue}")
else:
    print("\nALL PAGES OK")
