"""
fetch_schemes.py — Fetches ALL schemes from myscheme.gov.in
API Key discovered from browser headers: x-api-key
Run: python fetch_schemes.py
"""

import requests
import json
import time
import os

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "schemes_full.json")

BASE_URL = "https://api.myscheme.gov.in/search/v6/schemes"

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://www.myscheme.gov.in",
    "referer": "https://www.myscheme.gov.in/",
    "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "x-api-key": "tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc",
}

KEYWORDS = [
    "", "farmer", "student", "scholarship", "health", "housing", "women",
    "labour", "business", "loan", "skill", "pension", "disability",
    "sc", "st", "obc", "minority", "rural", "urban", "education",
    "employment", "startup", "artisan", "fisherman", "tribal", "solar",
    "insurance", "maternity", "child", "elderly", "food", "ration",
    "agriculture", "dairy", "crop", "girl", "widow", "weaver",
    "carpenter", "vendor", "entrepreneur", "construction", "backward",
    "fisheries", "horticulture", "irrigation", "training", "vocational",
    "mudra", "ayushman", "ujjwala", "pmkisan", "swachh", "bpl",
    "differently abled", "divyang", "senior citizen", "youth", "sports",
    "culture", "tourism", "transport", "sanitation", "water", "digital",
]


def fetch_batch(keyword="", from_=0, size=50):
    params = {
        "lang": "en",
        "q": "[]",
        "keyword": keyword,
        "sort": "",
        "from": from_,
        "size": size,
    }
    try:
        r = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=20)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"    HTTP {r.status_code}: {r.text[:100]}")
            return None
    except Exception as e:
        print(f"    Error: {e}")
        return None


def normalize(item: dict) -> dict:
    fields = item.get("fields", item)
    cat_raw = fields.get("schemeCategory", ["general"])
    category = cat_raw[0] if isinstance(cat_raw, list) and cat_raw else str(cat_raw)
    state_raw = fields.get("beneficiaryState", ["Central"])
    state = ", ".join(state_raw) if isinstance(state_raw, list) else str(state_raw)
    tags = fields.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    slug = fields.get("slug", "")
    apply_link = f"https://www.myscheme.gov.in/schemes/{slug}" if slug else "https://www.myscheme.gov.in"
    return {
        "id": str(item.get("id", "")),
        "name": fields.get("schemeName", "Unknown"),
        "category": category,
        "ministry": str(fields.get("nodalMinistryName", fields.get("ministry", ""))),
        "description": fields.get("briefDescription", ""),
        "benefits": fields.get("briefDescription", ""),
        "eligibility_text": [],
        "documents": [],
        "tags": tags[:15] if isinstance(tags, list) else [],
        "state": state or "Central",
        "level": fields.get("level", ""),
        "apply_link": apply_link,
        "source": "myscheme.gov.in",
    }


def main():
    print("🇮🇳 Fetching ALL schemes from myscheme.gov.in")
    print("=" * 55)

    # Quick test
    print("Testing API with x-api-key...")
    test = fetch_batch(keyword="farmer", from_=0, size=5)
    if not test:
        print("❌ API call failed.")
        return

    try:
        test_items = test["data"]["hits"]["items"]
        test_total = test["data"]["hits"]["page"]["total"]
        print(f"✅ API works! {test_total} schemes found for 'farmer'")
        print(f"   Sample: {test_items[0]['fields']['schemeName']}")
    except Exception as e:
        print(f"❌ Unexpected response structure: {e}")
        with open("debug.json", "w") as f:
            json.dump(test, f, indent=2)
        print("Saved debug.json")
        return

    print(f"\nSweeping {len(KEYWORDS)} keywords to collect all schemes...\n")

    all_schemes = {}

    for i, keyword in enumerate(KEYWORDS):
        from_ = 0
        kw_new = 0

        while True:
            data = fetch_batch(keyword=keyword, from_=from_, size=50)
            if not data:
                break

            try:
                items = data["data"]["hits"]["items"]
                total = data["data"]["hits"]["page"]["total"]
            except (KeyError, TypeError):
                break

            if not items:
                break

            for item in items:
                norm = normalize(item)
                sid = norm["id"] or norm["name"]
                if sid and sid not in all_schemes:
                    all_schemes[sid] = norm
                    kw_new += 1

            from_ += len(items)
            if from_ >= total or len(items) < 50:
                break

            time.sleep(0.25)

        if kw_new > 0:
            kw_label = f"'{keyword}'" if keyword else "'all'"
            print(f"  [{i+1}/{len(KEYWORDS)}] {kw_label}: +{kw_new} new → total {len(all_schemes)}")

    final = list(all_schemes.values())

    if not final:
        print("❌ No schemes fetched.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"\n{'='*55}")
    print(f"✅ Done! Saved {len(final)} unique schemes")
    print(f"   File: schemes_full.json ({size_kb:.0f} KB)")
    print(f"\nSamples:")
    for s in final[:5]:
        print(f"  • {s['name'][:55]} [{s['state'][:25]}]")
    print(f"\n▶  Restart uvicorn to load all {len(final)} schemes!")


if __name__ == "__main__":
    main()