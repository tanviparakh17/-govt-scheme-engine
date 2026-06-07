"""
rag_engine.py — Fixed scoring for 4700 real schemes from myscheme.gov.in
"""

import re
import json
import os

FULL_JSON = os.path.join(os.path.dirname(__file__), "schemes_full.json")

def load_schemes():
    if os.path.exists(FULL_JSON):
        with open(FULL_JSON, "r", encoding="utf-8") as f:
            schemes = json.load(f)
        print(f"✅ Loaded {len(schemes)} schemes from schemes_full.json")
        return schemes, "full"
    else:
        from schemes_data import SCHEMES
        print(f"⚠️  Using {len(SCHEMES)} hardcoded schemes.")
        return SCHEMES, "local"

SCHEMES, DATA_SOURCE = load_schemes()

# ── Occupation keyword map ────────────────────────────────────────────────────
OCCUPATION_MAP = {
    "student":             ["student", "scholar", "pupil", "college", "university", "school", "education", "learning", "degree", "diploma", "academic"],
    "farmer":              ["farmer", "kisan", "agriculture", "farming", "crop", "cultivat", "horticulture", "dairy", "livestock", "irrigation", "fisherm"],
    "labour":              ["labour", "worker", "labourer", "mazdoor", "wage", "unorganised", "unorganized", "migrant", "construction", "building"],
    "entrepreneur":        ["entrepreneur", "startup", "venture", "founder", "innovator", "business owner"],
    "self-employed":       ["self-employed", "self employed", "freelancer", "proprietor"],
    "artisan":             ["artisan", "craftsman", "weaver", "potter", "carpenter", "blacksmith", "tailor", "cobbler", "handloom", "handicraft", "vishwakarma"],
    "street vendor":       ["vendor", "hawker", "rehdi", "thela", "street seller", "vending"],
    "domestic worker":     ["domestic", "maid", "househelp", "household worker"],
    "construction worker": ["construction", "mason", "plumber", "electrician", "building worker"],
    "small business":      ["small business", "msme", "shop", "trader", "merchant", "retailer"],
    "daily wage":          ["daily wage", "casual worker", "contract worker"],
    "government employee": ["government employee", "govt employee", "civil servant", "sarkari"],
    "private employee":    ["private employee", "salaried", "corporate", "it professional"],
}

STATE_MAP = {
    "Maharashtra":      ["maharashtra", "mumbai", "pune", "nagpur", "nashik"],
    "Delhi":            ["delhi", "new delhi"],
    "Karnataka":        ["karnataka", "bangalore", "bengaluru", "mysore"],
    "Tamil Nadu":       ["tamil nadu", "tamilnadu", "chennai"],
    "Uttar Pradesh":    ["uttar pradesh", " up ", "lucknow", "kanpur", "varanasi"],
    "Gujarat":          ["gujarat", "ahmedabad", "surat", "vadodara"],
    "Rajasthan":        ["rajasthan", "jaipur", "jodhpur"],
    "West Bengal":      ["west bengal", "kolkata", "bengal"],
    "Madhya Pradesh":   ["madhya pradesh", "bhopal", "indore"],
    "Andhra Pradesh":   ["andhra pradesh", "vijayawada", "visakhapatnam"],
    "Telangana":        ["telangana", "hyderabad"],
    "Kerala":           ["kerala", "kochi", "thiruvananthapuram"],
    "Punjab":           ["punjab", "amritsar", "ludhiana"],
    "Haryana":          ["haryana", "gurugram", "faridabad"],
    "Bihar":            ["bihar", "patna"],
    "Odisha":           ["odisha", "bhubaneswar"],
    "Jharkhand":        ["jharkhand", "ranchi"],
    "Assam":            ["assam", "guwahati"],
    "Uttarakhand":      ["uttarakhand", "dehradun"],
    "Himachal Pradesh": ["himachal", "shimla"],
}

CATEGORY_MAP = {
    "education":       ["study", "scholarship", "school", "college", "university", "education", "degree", "diploma", "hostel", "fees", "book", "learning", "student"],
    "health":          ["health", "medical", "hospital", "treatment", "disease", "insurance", "surgery", "medicine", "doctor", "maternity", "wellness"],
    "agriculture":     ["farm", "crop", "kisan", "agriculture", "irrigation", "seed", "fertilizer", "harvest", "livestock", "dairy", "horticulture"],
    "business":        ["loan", "business", "credit", "finance", "mudra", "capital", "msme", "trade", "commerce"],
    "housing":         ["house", "home", "shelter", "accommodation", "flat", "awas", "construction", "dwelling"],
    "employment":      ["job", "employment", "work", "wage", "nrega", "skill", "training", "placement", "career"],
    "welfare":         ["bpl", "poor", "ration", "food", "lpg", "gas", "subsidy", "relief", "assistance"],
    "pension":         ["pension", "retirement", "old age", "senior", "annuity"],
    "entrepreneurship":["startup", "entrepreneur", "venture", "seed fund", "innovation", "incubator"],
    "women":           ["women", "girl", "female", "widow", "maternity", "mahila", "beti", "gender"],
    "skill":           ["skill", "training", "vocational", "apprentice", "iti", "certificate", "diploma"],
    "disability":      ["disabled", "divyang", "handicap", "pwd", "differently abled"],
    "environment":     ["solar", "green", "environment", "renewable", "energy", "water", "sanitation"],
}

CASTE_MAP = {
    "sc":       ["sc", "scheduled caste", "dalit"],
    "st":       ["st", "scheduled tribe", "tribal", "adivasi"],
    "obc":      ["obc", "other backward", "backward class"],
    "ews":      ["ews", "economically weaker"],
    "minority": ["minority", "muslim", "christian", "sikh", "buddhist"],
}


def extract_intent(query: str) -> dict:
    q = query.lower()
    intent = {"occupations": [], "state": None, "categories": [],
               "age": None, "income": None, "caste": None, "raw_keywords": []}

    for occ, kws in OCCUPATION_MAP.items():
        if any(kw in q for kw in kws):
            intent["occupations"].append(occ)

    for state, kws in STATE_MAP.items():
        if any(kw in q for kw in kws):
            intent["state"] = state
            break

    for cat, kws in CATEGORY_MAP.items():
        if any(kw in q for kw in kws):
            intent["categories"].append(cat)

    for caste, kws in CASTE_MAP.items():
        if any(kw in q for kw in kws):
            intent["caste"] = caste
            break

    age_match = re.search(r'\b(\d{1,2})\s*(?:years?\s*old|yr|age)|\bage\s*(\d{1,2})', q)
    if age_match:
        intent["age"] = int(age_match.group(1) or age_match.group(2))

    income_match = re.search(r'(?:income|earn|salary)[^\d]*(\d+\.?\d*)\s*(lakh|lac|k|thousand)?', q)
    if income_match:
        val = float(income_match.group(1))
        unit = income_match.group(2)
        if unit in ("lakh", "lac"): val *= 100000
        elif unit in ("k", "thousand"): val *= 1000
        intent["income"] = int(val)

    stop = {"what", "which", "where", "when", "that", "this", "from", "with", "have",
            "want", "need", "like", "some", "tell", "about", "also", "apply", "schemes",
            "scheme", "government", "india", "indian", "does", "will", "would", "could"}
    intent["raw_keywords"] = [w for w in re.findall(r'\b[a-z]{4,}\b', q) if w not in stop]
    return intent


def get_scheme_text(scheme: dict) -> str:
    parts = [
        scheme.get("name", ""),
        scheme.get("description", ""),
        scheme.get("category", ""),
        scheme.get("ministry", ""),
        scheme.get("state", ""),
        scheme.get("level", ""),
        " ".join(scheme.get("tags", [])),
        " ".join(scheme.get("keywords", [])),
        " ".join(scheme.get("eligibility_text", [])),
        scheme.get("benefits", ""),
    ]
    return " ".join(str(p) for p in parts).lower()


def score_scheme_form(scheme: dict, occupation: str, state: str) -> float:
    """
    Score based on occupation + state match in scheme text/tags.
    Every scheme gets scored differently — no more same 10 results.
    """
    text = get_scheme_text(scheme)
    score = 0.0

    # ── Occupation scoring ──────────────────────────────────────
    occ_keywords = OCCUPATION_MAP.get(occupation.lower(), [occupation.lower()])
    occ_hits = sum(1 for kw in occ_keywords if kw in text)
    score += occ_hits * 2.5

    # Tags are more reliable — bonus for tag match
    tags_text = " ".join(t.lower() for t in scheme.get("tags", []))
    occ_tag_hits = sum(1 for kw in occ_keywords if kw in tags_text)
    score += occ_tag_hits * 3.0

    # ── State scoring ───────────────────────────────────────────
    scheme_state = str(scheme.get("state", "")).lower()
    scheme_level = str(scheme.get("level", "")).lower()
    user_state = state.lower()

    # Central/All schemes are relevant to everyone
    if "central" in scheme_level or "all" in scheme_state or scheme_state == "":
        score += 2.0
    # Exact state match — high bonus
    elif user_state in scheme_state or any(kw in scheme_state for kw in STATE_MAP.get(state, [state.lower()])):
        score += 5.0
    # State in text (description/ministry)
    elif user_state in text or any(kw in text for kw in STATE_MAP.get(state, [])):
        score += 1.5
    else:
        # Different state — penalize but don't eliminate (central schemes may still apply)
        score -= 1.0

    # ── Minimum relevance threshold ─────────────────────────────
    # Scheme must have at least some occupation relevance
    if occ_hits == 0 and occ_tag_hits == 0:
        # Give small chance for generic schemes
        if "all" in tags_text or "general" in tags_text:
            score += 0.5
        else:
            score -= 2.0

    return score


def score_scheme_nlp(scheme: dict, intent: dict) -> float:
    text = get_scheme_text(scheme)
    tags_text = " ".join(t.lower() for t in scheme.get("tags", []))
    score = 0.0

    # Occupation
    for occ in intent["occupations"]:
        kws = OCCUPATION_MAP.get(occ, [occ])
        score += sum(1.5 for kw in kws if kw in text)
        score += sum(2.0 for kw in kws if kw in tags_text)

    # State
    if intent["state"]:
        scheme_state = str(scheme.get("state", "")).lower()
        scheme_level = str(scheme.get("level", "")).lower()
        if "central" in scheme_level or "all" in scheme_state:
            score += 1.5
        elif intent["state"].lower() in scheme_state:
            score += 4.0
        elif intent["state"].lower() in text:
            score += 1.0

    # Category
    for cat in intent["categories"]:
        if cat in text or cat == scheme.get("category", "").lower():
            score += 3.0
        kws = CATEGORY_MAP.get(cat, [])
        score += sum(1.0 for kw in kws if kw in tags_text)

    # Raw keywords
    for kw in intent["raw_keywords"]:
        if kw in text: score += 1.0
        if kw in tags_text: score += 1.5

    # Caste
    if intent["caste"]:
        kws = CASTE_MAP.get(intent["caste"], [])
        score += sum(2.0 for kw in kws if kw in text)

    return score


def get_schemes_by_form(age: int, income: int, occupation: str, state: str, top_k: int = 10):
    scored = []
    for scheme in SCHEMES:
        s = score_scheme_form(scheme, occupation, state)
        scored.append((s, scheme))

    # Sort by score descending
    scored.sort(key=lambda x: -x[0])

    # Take top results with positive score
    results = [s for sc, s in scored if sc > 0][:top_k]
    return results


def get_schemes_by_nlp(query: str, top_k: int = 8):
    intent = extract_intent(query)
    scored = []
    for scheme in SCHEMES:
        s = score_scheme_nlp(scheme, intent)
        if s > 0:
            scored.append((s, scheme))
    scored.sort(key=lambda x: -x[0])
    return [s for _, s in scored[:top_k]], intent


def get_dataset_info():
    return {
        "total_schemes": len(SCHEMES),
        "source": DATA_SOURCE,
        "has_full_dataset": DATA_SOURCE == "full",
    }