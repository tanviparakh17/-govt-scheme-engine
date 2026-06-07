SCHEMES = [
    {
        "id": 1,
        "name": "PM Kisan Samman Nidhi",
        "category": "agriculture",
        "description": "Direct income support of ₹6,000/year to small and marginal farmers.",
        "benefits": "₹6,000 per year in 3 equal installments of ₹2,000 directly to bank account.",
        "eligibility": {
            "occupation": ["farmer"],
            "max_income": 200000,
            "min_age": 18,
            "max_age": 100,
            "states": ["all"]
        },
        "documents": ["Aadhaar Card", "Bank Passbook", "Land Records (Khasra/Khatauni)", "Mobile Number"],
        "apply_link": "https://pmkisan.gov.in",
        "keywords": ["farmer", "kisan", "agriculture", "farming", "land", "crop"]
    },
    {
        "id": 2,
        "name": "PM Awas Yojana (Urban)",
        "category": "housing",
        "description": "Affordable housing for urban poor through subsidized loans and direct grants.",
        "benefits": "Subsidy up to ₹2.67 lakh on home loans. Direct benefit transfer for house construction.",
        "eligibility": {
            "occupation": ["all"],
            "max_income": 1800000,
            "min_age": 21,
            "max_age": 100,
            "states": ["all"]
        },
        "documents": ["Aadhaar Card", "Income Certificate", "Address Proof", "Bank Account Details"],
        "apply_link": "https://pmaymis.gov.in",
        "keywords": ["housing", "home", "house", "awas", "shelter", "urban", "loan"]
    },
    {
        "id": 3,
        "name": "National Scholarship Portal - Central Schemes",
        "category": "education",
        "description": "Scholarships for students from minority, OBC, SC/ST communities for higher education.",
        "benefits": "₹10,000–₹20,000 per year for college/university students.",
        "eligibility": {
            "occupation": ["student"],
            "max_income": 250000,
            "min_age": 16,
            "max_age": 30,
            "states": ["all"]
        },
        "documents": ["Aadhaar Card", "Income Certificate", "Caste Certificate", "Previous Year Marksheet", "Bank Account"],
        "apply_link": "https://scholarships.gov.in",
        "keywords": ["student", "scholarship", "college", "university", "education", "study", "minority", "obc", "sc", "st"]
    },
    {
        "id": 4,
        "name": "Maharashtra Swadhar Yojana",
        "category": "education",
        "description": "Financial assistance for SC/NavBuddhist students studying in Class 11 and above in Maharashtra.",
        "benefits": "₹51,000 per year covering boarding, lodging, and other expenses.",
        "eligibility": {
            "occupation": ["student"],
            "max_income": 250000,
            "min_age": 16,
            "max_age": 30,
            "states": ["Maharashtra"]
        },
        "documents": ["Caste Certificate", "Income Certificate", "Aadhaar Card", "Marksheet", "Domicile Certificate"],
        "apply_link": "https://mahaeschol.maharashtra.gov.in",
        "keywords": ["maharashtra", "student", "sc", "dalit", "scholarship", "swadhar", "college", "11th", "12th"]
    },
    {
        "id": 5,
        "name": "Rajiv Gandhi Scholarship for Academic Excellence (Maharashtra)",
        "category": "education",
        "description": "Merit-based scholarship for Maharashtra students pursuing higher education abroad or in premier institutes.",
        "benefits": "Full tuition fees + maintenance allowance up to ₹10 lakh/year.",
        "eligibility": {
            "occupation": ["student"],
            "max_income": 800000,
            "min_age": 17,
            "max_age": 35,
            "states": ["Maharashtra"]
        },
        "documents": ["Maharashtra Domicile Certificate", "Marksheets", "Admission Letter", "Income Certificate", "Aadhaar"],
        "apply_link": "https://mahadbt.maharashtra.gov.in",
        "keywords": ["maharashtra", "scholarship", "merit", "abroad", "higher education", "rajiv gandhi"]
    },
    {
        "id": 6,
        "name": "Startup India Seed Fund Scheme",
        "category": "entrepreneurship",
        "description": "Financial support to startups for proof of concept, prototype development, product trials, and market entry.",
        "benefits": "Up to ₹5 crore as grants and soft loans through DPIIT-recognized incubators.",
        "eligibility": {
            "occupation": ["entrepreneur", "self-employed", "startup"],
            "max_income": 10000000,
            "min_age": 18,
            "max_age": 60,
            "states": ["all"]
        },
        "documents": ["DPIIT Recognition Certificate", "Business Plan", "Incorporation Certificate", "PAN Card", "Bank Details"],
        "apply_link": "https://seedfund.startupindia.gov.in",
        "keywords": ["startup", "entrepreneur", "business", "seed fund", "innovation", "dpiit", "incubator"]
    },
    {
        "id": 7,
        "name": "Ayushman Bharat PM-JAY",
        "category": "health",
        "description": "World's largest health assurance scheme providing ₹5 lakh coverage per family per year.",
        "benefits": "₹5 lakh health insurance per year covering 1,500+ medical procedures. Cashless at empanelled hospitals.",
        "eligibility": {
            "occupation": ["all"],
            "max_income": 150000,
            "min_age": 0,
            "max_age": 100,
            "states": ["all"]
        },
        "documents": ["Ration Card / SECC Data", "Aadhaar Card", "Family ID"],
        "apply_link": "https://pmjay.gov.in",
        "keywords": ["health", "medical", "hospital", "insurance", "ayushman", "treatment", "surgery", "poor"]
    },
    {
        "id": 8,
        "name": "Pradhan Mantri Mudra Yojana (PMMY)",
        "category": "business",
        "description": "Loans to non-corporate small business units for income-generating activities.",
        "benefits": "Shishu: up to ₹50,000 | Kishore: ₹50K–5 lakh | Tarun: ₹5–10 lakh. No collateral required.",
        "eligibility": {
            "occupation": ["self-employed", "entrepreneur", "small business", "artisan"],
            "max_income": 5000000,
            "min_age": 18,
            "max_age": 65,
            "states": ["all"]
        },
        "documents": ["Aadhaar Card", "PAN Card", "Business Proof", "Bank Statements", "Passport Photo"],
        "apply_link": "https://mudra.org.in",
        "keywords": ["loan", "business", "mudra", "self-employed", "small business", "msme", "entrepreneur", "shop"]
    },
    {
        "id": 9,
        "name": "PM Scholarship Scheme for Central Armed Police Forces",
        "category": "education",
        "description": "Scholarships for wards/widows of CAPF, AR, and RPF personnel.",
        "benefits": "₹2,500–₹3,000 per month for degree courses.",
        "eligibility": {
            "occupation": ["student"],
            "max_income": 600000,
            "min_age": 17,
            "max_age": 25,
            "states": ["all"]
        },
        "documents": ["Service Certificate of Parent", "Marksheets", "Aadhaar", "Bank Account", "Admission Letter"],
        "apply_link": "https://scholarships.gov.in",
        "keywords": ["scholarship", "student", "defence", "army", "police", "capf", "armed forces"]
    },
    {
        "id": 10,
        "name": "Sukanya Samriddhi Yojana",
        "category": "savings",
        "description": "Government-backed savings scheme for the girl child offering high interest rates.",
        "benefits": "8.2% interest rate (2024). Tax-free returns. Matures when girl turns 21.",
        "eligibility": {
            "occupation": ["all"],
            "max_income": 10000000,
            "min_age": 0,
            "max_age": 10,
            "states": ["all"]
        },
        "documents": ["Birth Certificate of Girl Child", "Parent's Aadhaar", "Address Proof"],
        "apply_link": "https://www.indiapost.gov.in",
        "keywords": ["girl child", "daughter", "savings", "sukanya", "education fund", "marriage fund"]
    },
    {
        "id": 11,
        "name": "Atal Pension Yojana",
        "category": "pension",
        "description": "Pension scheme for unorganized sector workers to ensure social security in old age.",
        "benefits": "Guaranteed pension of ₹1,000–₹5,000/month after age 60 based on contribution.",
        "eligibility": {
            "occupation": ["labour", "worker", "farmer", "self-employed", "daily wage"],
            "max_income": 500000,
            "min_age": 18,
            "max_age": 40,
            "states": ["all"]
        },
        "documents": ["Aadhaar Card", "Bank Account", "Mobile Number"],
        "apply_link": "https://enps.nsdl.com",
        "keywords": ["pension", "retirement", "old age", "atal", "unorganized", "labour", "worker"]
    },
    {
        "id": 12,
        "name": "PM Vishwakarma Yojana",
        "category": "skill",
        "description": "Support to artisans and craftspeople in 18 traditional trades with training, toolkit and loans.",
        "benefits": "₹15,000 toolkit incentive + soft loan up to ₹3 lakh at 5% interest + free skill training.",
        "eligibility": {
            "occupation": ["artisan", "carpenter", "blacksmith", "weaver", "potter", "mason", "tailor"],
            "max_income": 300000,
            "min_age": 18,
            "max_age": 60,
            "states": ["all"]
        },
        "documents": ["Aadhaar Card", "Caste Certificate (if applicable)", "Bank Account", "Mobile"],
        "apply_link": "https://pmvishwakarma.gov.in",
        "keywords": ["artisan", "craftsman", "vishwakarma", "carpenter", "blacksmith", "weaver", "potter", "tailor", "skill", "toolkit"]
    },
    {
        "id": 13,
        "name": "eShram Portal - Social Security Schemes",
        "category": "labour",
        "description": "Registration portal for unorganized workers to access social security benefits.",
        "benefits": "₹2 lakh accident insurance, access to multiple schemes, UAN card for portability of benefits.",
        "eligibility": {
            "occupation": ["daily wage", "labour", "domestic worker", "construction worker", "street vendor"],
            "max_income": 200000,
            "min_age": 16,
            "max_age": 59,
            "states": ["all"]
        },
        "documents": ["Aadhaar Card", "Mobile Linked to Aadhaar", "Bank Account"],
        "apply_link": "https://eshram.gov.in",
        "keywords": ["labour", "worker", "unorganized", "daily wage", "eshram", "construction", "domestic", "street vendor"]
    },
    {
        "id": 14,
        "name": "Beti Bachao Beti Padhao",
        "category": "education",
        "description": "Scheme to address declining child sex ratio and empowerment of girl child.",
        "benefits": "Access to Sukanya Samriddhi, scholarships, and conditional cash transfers for girl education.",
        "eligibility": {
            "occupation": ["all"],
            "max_income": 500000,
            "min_age": 0,
            "max_age": 18,
            "states": ["all"]
        },
        "documents": ["Birth Certificate", "Aadhaar of Parents", "School Enrollment Certificate"],
        "apply_link": "https://wcd.nic.in/bbbp-schemes",
        "keywords": ["girl", "daughter", "beti", "education", "school", "female", "gender"]
    },
    {
        "id": 15,
        "name": "PM SVANidhi - Street Vendor Loan",
        "category": "business",
        "description": "Micro-credit facility for street vendors to resume livelihoods post-COVID.",
        "benefits": "₹10,000 initial loan → ₹20,000 → ₹50,000 on repayment. 7% interest subsidy.",
        "eligibility": {
            "occupation": ["street vendor", "hawker", "small trader"],
            "max_income": 200000,
            "min_age": 18,
            "max_age": 65,
            "states": ["all"]
        },
        "documents": ["Letter of Recommendation from ULB/TVC", "Aadhaar Card", "Bank Account", "Vendor Certificate"],
        "apply_link": "https://pmsvanidhi.mohua.gov.in",
        "keywords": ["street vendor", "hawker", "rehdi", "patri", "thela", "vendor", "loan", "micro credit"]
    },
    {
        "id": 16,
        "name": "National Means-cum-Merit Scholarship (NMMS)",
        "category": "education",
        "description": "Scholarship to meritorious students of economically weaker sections to reduce dropout at Class 8.",
        "benefits": "₹12,000 per year (₹1,000/month) from Class 9 to Class 12.",
        "eligibility": {
            "occupation": ["student"],
            "max_income": 150000,
            "min_age": 13,
            "max_age": 16,
            "states": ["all"]
        },
        "documents": ["Class 7 Marksheet", "Income Certificate", "Aadhaar Card", "Bank Account (Parent)", "Caste Certificate"],
        "apply_link": "https://scholarships.gov.in",
        "keywords": ["scholarship", "school", "class 9", "class 10", "nmms", "merit", "student", "8th", "9th"]
    },
    {
        "id": 17,
        "name": "Kisan Credit Card (KCC)",
        "category": "agriculture",
        "description": "Flexible credit for farmers to meet agricultural and allied needs.",
        "benefits": "Credit limit up to ₹3 lakh at 4% interest (after subsidy). Covers crops, equipment, household needs.",
        "eligibility": {
            "occupation": ["farmer"],
            "max_income": 1000000,
            "min_age": 18,
            "max_age": 75,
            "states": ["all"]
        },
        "documents": ["Land Records", "Aadhaar Card", "Bank Account", "Passport Photo", "Crop Details"],
        "apply_link": "https://www.nabard.org",
        "keywords": ["farmer", "kisan", "credit", "loan", "kcc", "agriculture", "crop", "farming"]
    },
    {
        "id": 18,
        "name": "Mahatma Gandhi NREGA (MGNREGS)",
        "category": "employment",
        "description": "Provides 100 days of guaranteed wage employment in a financial year to rural households.",
        "benefits": "100 days of employment/year at state-level minimum wages (avg ₹200–300/day).",
        "eligibility": {
            "occupation": ["labour", "daily wage", "farmer", "rural worker"],
            "max_income": 200000,
            "min_age": 18,
            "max_age": 100,
            "states": ["all"]
        },
        "documents": ["Aadhaar Card", "Job Card (issued by Gram Panchayat)", "Bank Account"],
        "apply_link": "https://nrega.nic.in",
        "keywords": ["employment", "job", "nrega", "mgnrega", "rural", "wage", "100 days", "labour", "work"]
    },
    {
        "id": 19,
        "name": "Stand Up India",
        "category": "entrepreneurship",
        "description": "Bank loans for SC/ST and women entrepreneurs to set up greenfield enterprises.",
        "benefits": "Loans between ₹10 lakh to ₹1 crore for manufacturing, services, or trading sectors.",
        "eligibility": {
            "occupation": ["entrepreneur", "self-employed", "small business"],
            "max_income": 5000000,
            "min_age": 18,
            "max_age": 65,
            "states": ["all"]
        },
        "documents": ["Aadhaar Card", "PAN Card", "Caste Certificate (for SC/ST)", "Business Plan", "Bank Account"],
        "apply_link": "https://www.standupmitra.in",
        "keywords": ["loan", "business", "sc", "st", "women", "entrepreneur", "startup", "stand up india"]
    },
    {
        "id": 20,
        "name": "PM Ujjwala Yojana",
        "category": "welfare",
        "description": "Free LPG connections to women of BPL households to reduce dependence on biomass cooking.",
        "benefits": "Free LPG connection with first refill and stove (hotplate). Subsidized refills.",
        "eligibility": {
            "occupation": ["all"],
            "max_income": 100000,
            "min_age": 18,
            "max_age": 100,
            "states": ["all"]
        },
        "documents": ["BPL Ration Card", "Aadhaar Card", "Bank Account", "Address Proof"],
        "apply_link": "https://www.pmuy.gov.in",
        "keywords": ["lpg", "gas", "cooking", "ujjwala", "bpl", "women", "household", "fuel"]
    },
    {
        "id": 21,
        "name": "Post Matric Scholarship for OBC Students",
        "category": "education",
        "description": "Scholarship for OBC students pursuing post-matriculation or post-secondary education.",
        "benefits": "₹1,500–₹12,000 per year depending on course and hostel/day scholar status.",
        "eligibility": {
            "occupation": ["student"],
            "max_income": 100000,
            "min_age": 15,
            "max_age": 35,
            "states": ["all"]
        },
        "documents": ["OBC Certificate", "Income Certificate", "Marksheets", "Aadhaar Card", "Bank Account"],
        "apply_link": "https://scholarships.gov.in",
        "keywords": ["obc", "scholarship", "student", "post matric", "college", "vocational", "12th", "degree"]
    },
    {
        "id": 22,
        "name": "Dr. Panjabrao Deshmukh Vasatigruha Anudan Yojana (Maharashtra)",
        "category": "education",
        "description": "Maintenance allowance for OBC, SBC, VJNT students living in hostels in Maharashtra.",
        "benefits": "₹30,000–₹38,000 per year for hostel living expenses.",
        "eligibility": {
            "occupation": ["student"],
            "max_income": 100000,
            "min_age": 16,
            "max_age": 30,
            "states": ["Maharashtra"]
        },
        "documents": ["Caste Certificate (OBC/SBC/VJNT)", "Income Certificate", "Hostel Certificate", "Aadhaar", "Domicile"],
        "apply_link": "https://mahadbt.maharashtra.gov.in",
        "keywords": ["maharashtra", "obc", "hostel", "student", "scholarship", "vjnt", "sbc", "college"]
    }
]
