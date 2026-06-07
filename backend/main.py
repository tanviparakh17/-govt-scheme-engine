from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import requests
import json
import os

app = FastAPI(
    title="Government Scheme Eligibility Engine",
    description="NLP + RAG powered engine to find eligible government schemes",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── MyScheme API config ───────────────────────────────────────────────────────
MYSCHEME_URL = "https://api.myscheme.gov.in/search/v6/schemes"
MYSCHEME_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://www.myscheme.gov.in",
    "referer": "https://www.myscheme.gov.in/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/148.0.0.0 Safari/537.36",
    "x-api-key": "tYTy5eEhlu9rFjyxuCr7ra7ACp4dv1RH8gWuHTDc",
}

# Occupation → myscheme filter values
OCCUPATION_FILTER_MAP = {
    "farmer":              "Farmer",
    "labour":              "Labour",
    "entrepreneur":        "Entrepreneur",
    "self-employed":       "Self Employed",
    "artisan":             "Artisans, Spinners & Weavers",
    "street vendor":       "Street Vendor",
    "domestic worker":     "Domestic Worker",
    "construction worker": "Construction Worker",
    "small business":      "Small and Marginal Farmers",
    "daily wage":          "Daily Wage Worker",
    "student":             None,   # handled via isStudent filter
    "government employee": "Government Employee",
    "private employee":    "Salaried Employee",
}

# State → myscheme beneficiaryState values
STATE_FILTER_MAP = {
    "Maharashtra": "Maharashtra",
    "Delhi": "Delhi",
    "Karnataka": "Karnataka",
    "Tamil Nadu": "Tamil Nadu",
    "Uttar Pradesh": "Uttar Pradesh",
    "Gujarat": "Gujarat",
    "Rajasthan": "Rajasthan",
    "West Bengal": "West Bengal",
    "Madhya Pradesh": "Madhya Pradesh",
    "Andhra Pradesh": "Andhra Pradesh",
    "Telangana": "Telangana",
    "Kerala": "Kerala",
    "Punjab": "Punjab",
    "Haryana": "Haryana",
    "Bihar": "Bihar",
    "Odisha": "Odisha",
    "Jharkhand": "Jharkhand",
    "Assam": "Assam",
    "Uttarakhand": "Uttarakhand",
    "Himachal Pradesh": "Himachal Pradesh",
}


def build_filters(occupation: str, state: str, age: int = None, income: int = None) -> list:
    filters = []

    # State filter — include both the specific state AND "All"
    state_val = STATE_FILTER_MAP.get(state)
    if state_val:
        filters.append({
            "identifier": "beneficiaryState",
            "value": state_val
        })

    # Occupation filter
    if occupation == "student":
        filters.append({"identifier": "isStudent", "value": "true"})
    else:
        occ_val = OCCUPATION_FILTER_MAP.get(occupation.lower())
        if occ_val:
            filters.append({"identifier": "occupation", "value": occ_val})

    return filters


def fetch_from_myscheme(keyword: str, filters: list, size: int = 10) -> list:
    """Hit the real myscheme API with proper filters."""
    params = {
        "lang": "en",
        "q": json.dumps(filters),
        "keyword": keyword,
        "sort": "",
        "from": 0,
        "size": size,
    }
    try:
        r = requests.get(MYSCHEME_URL, headers=MYSCHEME_HEADERS, params=params, timeout=15)
        if r.status_code != 200:
            return []
        data = r.json()
        items = data["data"]["hits"]["items"]
        return [normalize_item(item) for item in items]
    except Exception as e:
        print(f"MyScheme API error: {e}")
        return []


def normalize_item(item: dict) -> dict:
    fields = item.get("fields", {})
    cat_raw = fields.get("schemeCategory", ["general"])
    category = cat_raw[0] if isinstance(cat_raw, list) and cat_raw else str(cat_raw)
    state_raw = fields.get("beneficiaryState", ["Central"])
    state = ", ".join(state_raw) if isinstance(state_raw, list) else str(state_raw)
    tags = fields.get("tags", [])
    slug = fields.get("slug", "")
    return {
        "id": item.get("id", ""),
        "name": fields.get("schemeName", "Unknown"),
        "category": category,
        "ministry": str(fields.get("nodalMinistryName", "")),
        "description": fields.get("briefDescription", ""),
        "benefits": fields.get("briefDescription", ""),
        "eligibility_text": [],
        "documents": [],
        "tags": tags[:10] if isinstance(tags, list) else [],
        "state": state,
        "level": fields.get("level", ""),
        "apply_link": f"https://www.myscheme.gov.in/schemes/{slug}" if slug else "https://www.myscheme.gov.in",
        "source": "myscheme.gov.in",
    }


# ── NLP intent extraction (kept for NLP mode) ─────────────────────────────────
import re

OCCUPATION_NLP = {
    "farmer": ["farmer", "kisan", "agriculture", "farming", "crop", "cultivat"],
    "student": ["student", "college", "university", "school", "scholarship", "degree"],
    "labour": ["labour", "worker", "labourer", "daily wage", "mazdoor"],
    "entrepreneur": ["startup", "entrepreneur", "business owner", "founder"],
    "artisan": ["artisan", "craftsman", "weaver", "potter", "carpenter", "tailor"],
    "street vendor": ["vendor", "hawker", "rehdi", "thela"],
    "small business": ["small business", "msme", "shop", "trader"],
    "women": ["woman", "women", "female", "widow", "housewife"],
    "disabled": ["disabled", "divyang", "handicapped", "pwd"],
}

STATE_NLP = {
    "Maharashtra": ["maharashtra", "mumbai", "pune", "nagpur", "nashik"],
    "Delhi": ["delhi", "new delhi"],
    "Karnataka": ["karnataka", "bangalore", "bengaluru"],
    "Tamil Nadu": ["tamil nadu", "tamilnadu", "chennai"],
    "Uttar Pradesh": ["uttar pradesh", "lucknow", "varanasi"],
    "Gujarat": ["gujarat", "ahmedabad", "surat"],
    "Rajasthan": ["rajasthan", "jaipur"],
    "West Bengal": ["west bengal", "kolkata"],
    "Madhya Pradesh": ["madhya pradesh", "bhopal", "indore"],
    "Andhra Pradesh": ["andhra pradesh", "vijayawada"],
    "Telangana": ["telangana", "hyderabad"],
    "Kerala": ["kerala", "kochi"],
    "Punjab": ["punjab", "amritsar"],
    "Haryana": ["haryana", "gurugram"],
    "Bihar": ["bihar", "patna"],
    "Odisha": ["odisha", "bhubaneswar"],
    "Jharkhand": ["jharkhand", "ranchi"],
    "Assam": ["assam", "guwahati"],
    "Uttarakhand": ["uttarakhand", "dehradun"],
    "Himachal Pradesh": ["himachal", "shimla"],
}

def extract_intent(query: str) -> dict:
    q = query.lower()
    intent = {"occupations": [], "state": None, "keyword": "", "categories": [],
               "age": None, "income": None, "caste": None, "raw_keywords": []}

    for occ, kws in OCCUPATION_NLP.items():
        if any(kw in q for kw in kws):
            intent["occupations"].append(occ)

    for state, kws in STATE_NLP.items():
        if any(kw in q for kw in kws):
            intent["state"] = state
            break

    age_match = re.search(r'\b(\d{1,2})\s*(?:years?\s*old|yr)|\bage\s*(\d{1,2})', q)
    if age_match:
        intent["age"] = int(age_match.group(1) or age_match.group(2))

    stop = {"what", "which", "where", "when", "that", "this", "from", "with", "have",
            "want", "need", "like", "some", "tell", "about", "also", "apply", "schemes",
            "scheme", "government", "india", "does", "will", "would", "could", "should"}
    words = [w for w in re.findall(r'\b[a-z]{4,}\b', q) if w not in stop]
    intent["raw_keywords"] = words
    # Best keyword = first meaningful word not a state/occupation
    occ_words = {w for kws in OCCUPATION_NLP.values() for w in kws}
    state_words = {w for kws in STATE_NLP.values() for w in kws}
    content_words = [w for w in words if w not in occ_words and w not in state_words]
    intent["keyword"] = content_words[0] if content_words else (words[0] if words else "")
    return intent


# ── Pydantic Models ───────────────────────────────────────────────────────────
class FormQuery(BaseModel):
    age: int = Field(..., ge=0, le=120)
    income: int = Field(..., ge=0)
    occupation: str
    state: str

class NLPQuery(BaseModel):
    query: str = Field(..., min_length=5)


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Government Scheme Eligibility Engine v2 running!"}


@app.post("/schemes/form")
def get_schemes_form(data: FormQuery):
    """
    Calls myscheme.gov.in API with real occupation + state filters.
    Returns schemes that actually match the user's profile.
    """
    filters = build_filters(data.occupation, data.state, data.age, data.income)

    # Use occupation as keyword too for better results
    occ_keyword = data.occupation.replace("-", " ").replace("_", " ")

    schemes = fetch_from_myscheme(keyword=occ_keyword, filters=filters, size=10)

    # If filtered results are few, fetch with just state filter
    if len(schemes) < 5:
        state_only_filters = [f for f in filters if f["identifier"] == "beneficiaryState"]
        more = fetch_from_myscheme(keyword=occ_keyword, filters=state_only_filters, size=10)
        seen_ids = {s["id"] for s in schemes}
        for s in more:
            if s["id"] not in seen_ids:
                schemes.append(s)
                seen_ids.add(s["id"])

    return {
        "count": len(schemes),
        "mode": "form",
        "input": data.dict(),
        "filters_applied": filters,
        "schemes": schemes[:10]
    }


@app.post("/schemes/nlp")
def get_schemes_nlp(data: NLPQuery):
    """
    Extracts intent from natural language, then calls real myscheme API.
    """
    intent = extract_intent(data.query)

    # Build filters from intent
    filters = []
    if intent["state"]:
        state_val = STATE_FILTER_MAP.get(intent["state"])
        if state_val:
            filters.append({"identifier": "beneficiaryState", "value": state_val})

    if intent["occupations"]:
        occ = intent["occupations"][0]
        if occ == "student":
            filters.append({"identifier": "isStudent", "value": "true"})
        else:
            occ_val = OCCUPATION_FILTER_MAP.get(occ)
            if occ_val:
                filters.append({"identifier": "occupation", "value": occ_val})

    keyword = intent["keyword"] or (intent["occupations"][0] if intent["occupations"] else "")
    schemes = fetch_from_myscheme(keyword=keyword, filters=filters, size=8)

    return {
        "count": len(schemes),
        "mode": "nlp",
        "query": data.query,
        "extracted_intent": intent,
        "schemes": schemes
    }


@app.get("/schemes/info")
def dataset_info():
    full_json = os.path.join(os.path.dirname(__file__), "schemes_full.json")
    count = 0
    if os.path.exists(full_json):
        with open(full_json) as f:
            count = len(json.load(f))
    return {"total_local_schemes": count, "source": "myscheme.gov.in live API", "api_version": "v6"}