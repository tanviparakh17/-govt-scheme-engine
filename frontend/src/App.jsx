import { useState } from "react";

const API = "https://govt-scheme-api-ml08.onrender.com";

const OCCUPATIONS = [
  "student", "farmer", "labour", "entrepreneur", "self-employed",
  "artisan", "street vendor", "domestic worker", "construction worker",
  "small business", "daily wage", "government employee", "private employee"
];

const STATES = [
  "Maharashtra", "Delhi", "Karnataka", "Tamil Nadu", "Uttar Pradesh",
  "Gujarat", "Rajasthan", "West Bengal", "Madhya Pradesh", "Andhra Pradesh",
  "Telangana", "Kerala", "Punjab", "Haryana", "Bihar", "Odisha",
  "Jharkhand", "Assam", "Uttarakhand", "Himachal Pradesh"
];

const CATEGORY_COLORS = {
  education: "#3B82F6",
  agriculture: "#22C55E",
  health: "#EF4444",
  business: "#F59E0B",
  housing: "#8B5CF6",
  employment: "#06B6D4",
  welfare: "#EC4899",
  pension: "#64748B",
  entrepreneurship: "#F97316",
  labour: "#84CC16",
  savings: "#10B981",
  skill: "#A855F7",
};

const formatIncome = (val) => {
  if (val >= 100000) return `₹${(val / 100000).toFixed(1)}L`;
  if (val >= 1000) return `₹${(val / 1000).toFixed(0)}K`;
  return `₹${val}`;
};

export default function App() {
  const [tab, setTab] = useState("form");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [expandedId, setExpandedId] = useState(null);
  const [intent, setIntent] = useState(null);

  const [form, setForm] = useState({ age: "", income: "", occupation: "", state: "" });
  const [nlpQuery, setNlpQuery] = useState("");

  const exampleQueries = [
    "I'm a college student from Maharashtra. What scholarships can I apply for?",
    "I am a farmer with income below 2 lakh. What schemes can I get?",
    "I run a small street vendor business in Delhi. Need a loan.",
    "I am an artisan looking for government support and training.",
  ];

  async function handleFormSubmit(e) {
    e.preventDefault();
    if (!form.age || !form.income || !form.occupation || !form.state) {
      setError("Please fill all fields");
      return;
    }
    setLoading(true);
    setError(null);
    setResults(null);
    setIntent(null);
    try {
      const res = await fetch(`${API}/schemes/form`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          age: parseInt(form.age),
          income: parseInt(form.income),
          occupation: form.occupation,
          state: form.state,
        }),
      });
      if (!res.ok) throw new Error("Server error: " + res.status);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      setError(err.message || "Failed to fetch. Is the backend running?");
    }
    setLoading(false);
  }

  async function handleNLPSubmit(e) {
    e.preventDefault();
    if (!nlpQuery.trim() || nlpQuery.length < 5) {
      setError("Please enter a more detailed query");
      return;
    }
    setLoading(true);
    setError(null);
    setResults(null);
    setIntent(null);
    try {
      const res = await fetch(`${API}/schemes/nlp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: nlpQuery }),
      });
      if (!res.ok) throw new Error("Server error: " + res.status);
      const data = await res.json();
      setResults(data);
      setIntent(data.extracted_intent);
    } catch (err) {
      setError(err.message || "Failed to fetch. Is the backend running?");
    }
    setLoading(false);
  }

  return (
    <div style={styles.root}>
      <header style={styles.header}>
        <div style={styles.headerInner}>
          <div style={styles.logoRow}>
            <span style={styles.emblem}>🇮🇳</span>
            <div>
              <div style={styles.title}>Scheme Finder</div>
              <div style={styles.subtitle}>Government Scheme Eligibility Engine</div>
            </div>
          </div>
          <div style={styles.badge}>4700+ Schemes · NLP + RAG</div>
        </div>
      </header>

      <main style={styles.main}>
        <div style={styles.tabRow}>
          <button
            style={{ ...styles.tab, ...(tab === "form" ? styles.tabActive : {}) }}
            onClick={() => { setTab("form"); setResults(null); setError(null); setIntent(null); }}
          >
            📋 Form Mode
          </button>
          <button
            style={{ ...styles.tab, ...(tab === "nlp" ? styles.tabActive : {}) }}
            onClick={() => { setTab("nlp"); setResults(null); setError(null); setIntent(null); }}
          >
            🧠 Ask Yourself
          </button>
        </div>

        {tab === "form" && (
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>📋 Enter Your Details</h2>
            <form onSubmit={handleFormSubmit} style={styles.form}>
              <div style={styles.row2}>
                <div style={styles.field}>
                  <label style={styles.label}>Age</label>
                  <input
                    type="number" min="0" max="120" placeholder="e.g. 22"
                    style={styles.input}
                    value={form.age}
                    onChange={e => setForm({ ...form, age: e.target.value })}
                  />
                </div>
                <div style={styles.field}>
                  <label style={styles.label}>Annual Income (₹)</label>
                  <input
                    type="number" min="0" placeholder="e.g. 150000"
                    style={styles.input}
                    value={form.income}
                    onChange={e => setForm({ ...form, income: e.target.value })}
                  />
                </div>
              </div>
              <div style={styles.row2}>
                <div style={styles.field}>
                  <label style={styles.label}>Occupation</label>
                  <select style={styles.input} value={form.occupation} onChange={e => setForm({ ...form, occupation: e.target.value })}>
                    <option value="">Select occupation</option>
                    {OCCUPATIONS.map(o => <option key={o} value={o}>{o.charAt(0).toUpperCase() + o.slice(1)}</option>)}
                  </select>
                </div>
                <div style={styles.field}>
                  <label style={styles.label}>State</label>
                  <select style={styles.input} value={form.state} onChange={e => setForm({ ...form, state: e.target.value })}>
                    <option value="">Select state</option>
                    {STATES.map(s => <option key={s} value={s}>{s}</option>)}
                  </select>
                </div>
              </div>
              <button type="submit" style={styles.btn} disabled={loading}>
                {loading ? "🔄 Searching..." : "🔍 Find Eligible Schemes"}
              </button>
            </form>
          </div>
        )}

        {tab === "nlp" && (
          <div style={styles.card}>
            <h2 style={styles.cardTitle}>Ask in Your Own Words</h2>
            <form onSubmit={handleNLPSubmit}>
              <textarea
                style={styles.textarea}
                rows={3}
                placeholder="e.g. I'm a college student from Maharashtra. What scholarships can I apply for?"
                value={nlpQuery}
                onChange={e => setNlpQuery(e.target.value)}
              />
              <button type="submit" style={styles.btn} disabled={loading}>
                {loading ? "Analyzing..." : "🧠 Find Matching Schemes"}
              </button>
            </form>
            <div style={styles.examplesRow}>
              <div style={styles.examplesLabel}>Try:</div>
              {exampleQueries.map((q, i) => (
                <button key={i} style={styles.exampleChip} onClick={() => setNlpQuery(q)}>
                  {q.length > 55 ? q.slice(0, 55) + "…" : q}
                </button>
              ))}
            </div>
          </div>
        )}

        {error && (
          <div style={styles.errorBox}>⚠️ {error}</div>
        )}

        {intent && (
          <div style={styles.intentBox}>
            <strong>🔍 Extracted Intent:</strong>
            <div style={styles.intentTags}>
              {intent.occupations?.length > 0 && <span style={styles.intentTag}>👷 {intent.occupations.join(", ")}</span>}
              {intent.state && <span style={styles.intentTag}>📍 {intent.state}</span>}
              {intent.age && <span style={styles.intentTag}>🎂 Age {intent.age}</span>}
              {intent.income && <span style={styles.intentTag}>💰 Income {formatIncome(intent.income)}</span>}
              {intent.categories?.length > 0 && <span style={styles.intentTag}>📂 {intent.categories.join(", ")}</span>}
              {intent.caste && <span style={styles.intentTag}>🏷️ {intent.caste.toUpperCase()}</span>}
            </div>
          </div>
        )}

        {results && (
          <div>
            <div style={styles.resultsHeader}>
              <span style={styles.resultsCount}>{results.count} scheme{results.count !== 1 ? "s" : ""} found</span>
              {results.count === 0 && <span style={styles.noResults}>No matching schemes. Try different values.</span>}
            </div>
            <div style={styles.schemeList}>
              {results.schemes.map((scheme) => (
                <div
                  key={scheme.id}
                  style={{
                    ...styles.schemeCard,
                    borderLeft: `4px solid ${CATEGORY_COLORS[scheme.category] || "#94a3b8"}`
                  }}
                >
                  <div style={styles.schemeHeader} onClick={() => setExpandedId(expandedId === scheme.id ? null : scheme.id)}>
                    <div style={styles.schemeLeft}>
                      <span
                        style={{
                          ...styles.categoryBadge,
                          background: (CATEGORY_COLORS[scheme.category] || "#94a3b8") + "22",
                          color: CATEGORY_COLORS[scheme.category] || "#64748b"
                        }}
                      >
                        {scheme.category}
                      </span>
                      <div style={styles.schemeName}>{scheme.name}</div>
                      <div style={styles.schemeDesc}>{scheme.description}</div>
                    </div>
                    <span style={styles.chevron}>{expandedId === scheme.id ? "▲" : "▼"}</span>
                  </div>

                  {expandedId === scheme.id && (
                    <div style={styles.schemeBody}>
                      <div style={styles.benefitBox}>
                        <div style={styles.sectionLabel}>💰 Benefits</div>
                        <div style={styles.benefitText}>{scheme.benefits}</div>
                      </div>

                      {scheme.documents && scheme.documents.length > 0 && (
                        <div style={styles.docsRow}>
                          <div style={styles.sectionLabel}>📄 Required Documents</div>
                          <ul style={styles.docList}>
                            {scheme.documents.map((d, i) => <li key={i} style={styles.docItem}>{d}</li>)}
                          </ul>
                        </div>
                      )}

                      {scheme.eligibility && (
                        <div style={styles.eligRow}>
                          <div style={styles.sectionLabel}>✅ Eligibility</div>
                          <div style={styles.eligGrid}>
                            <span style={styles.eligChip}>Age: {scheme.eligibility.min_age}–{scheme.eligibility.max_age}</span>
                            <span style={styles.eligChip}>Income: ≤{formatIncome(scheme.eligibility.max_income)}</span>
                            <span style={styles.eligChip}>
                              {scheme.eligibility.states?.includes("all") ? "All States" : scheme.eligibility.states?.join(", ")}
                            </span>
                          </div>
                        </div>
                      )}

                      {scheme.tags && scheme.tags.length > 0 && (
                        <div style={styles.tagsRow}>
                          {scheme.tags.map((tag, i) => (
                            <span key={i} style={styles.tag}>{tag}</span>
                          ))}
                        </div>
                      )}

                      <a
                        href={scheme.apply_link || "https://www.myscheme.gov.in"}
                        target="_blank"
                        rel="noreferrer"
                        style={styles.applyBtn}
                      >
                        🔗 Apply on myscheme.gov.in →
                      </a>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer style={styles.footer}>
        Built with FastAPI + RAG · NLP Intent Extraction · 4700+ Indian Government Schemes · By Tanvi
      </footer>
    </div>
  );
}

const styles = {
  root: {
    fontFamily: "'Noto Sans', 'Segoe UI', sans-serif",
    background: "#F1F5F9",
    minHeight: "100vh",
    color: "#1e293b",
    display: "flex",
    flexDirection: "column",
  },
  header: {
    background: "linear-gradient(135deg, #1a3c6e 0%, #0f5c2e 100%)",
    color: "white",
    padding: "0",
    width: "100%",
  },
  headerInner: {
    width: "100%",
    padding: "24px 40px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    flexWrap: "wrap",
    gap: 12,
    boxSizing: "border-box",
  },
  logoRow: { display: "flex", alignItems: "center", gap: 18 },
  emblem: { fontSize: 44 },
  title: { fontSize: 28, fontWeight: 800, letterSpacing: "-0.5px" },
  subtitle: { fontSize: 14, opacity: 0.8, marginTop: 2 },
  badge: {
    background: "rgba(255,255,255,0.15)",
    border: "1px solid rgba(255,255,255,0.3)",
    borderRadius: 20,
    padding: "6px 16px",
    fontSize: 13,
    fontWeight: 600,
    backdropFilter: "blur(8px)",
  },
  main: {
    width: "100%",
    padding: "32px 40px",
    flex: 1,
    boxSizing: "border-box",
    display: "flex",
    flexDirection: "column",
  },
  tabRow: { display: "flex", gap: 12, marginBottom: 24 },
  tab: {
    padding: "12px 24px",
    borderRadius: 8,
    border: "2px solid #cbd5e1",
    background: "white",
    cursor: "pointer",
    fontWeight: 600,
    fontSize: 15,
    color: "#64748b",
    transition: "all 0.2s",
  },
  tabActive: {
    background: "#1a3c6e",
    color: "white",
    borderColor: "#1a3c6e",
  },
  card: {
    background: "white",
    borderRadius: 16,
    padding: "32px 40px",
    boxShadow: "0 4px 24px rgba(0,0,0,0.07)",
    marginBottom: 24,
  },
  cardTitle: { fontSize: 20, fontWeight: 700, marginBottom: 24, marginTop: 0 },
  form: { display: "flex", flexDirection: "column", gap: 20 },
  row2: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 },
  field: { display: "flex", flexDirection: "column", gap: 8 },
  label: { fontSize: 14, fontWeight: 600, color: "#475569" },
  input: {
    padding: "12px 16px",
    borderRadius: 8,
    border: "1.5px solid #e2e8f0",
    fontSize: 16,
    outline: "none",
    color: "#1e293b",
    background: "#f8fafc",
    transition: "border 0.2s",
    minHeight: "48px",
    boxSizing: "border-box",
  },
  textarea: {
    width: "100%",
    padding: "14px 16px",
    borderRadius: 8,
    border: "1.5px solid #e2e8f0",
    fontSize: 16,
    color: "#1e293b",
    background: "#f8fafc",
    resize: "vertical",
    marginBottom: 12,
    boxSizing: "border-box",
    outline: "none",
    minHeight: "140px",
  },
  btn: {
    padding: "16px 28px",
    background: "linear-gradient(135deg, #1a3c6e, #0f5c2e)",
    color: "white",
    border: "none",
    borderRadius: 8,
    fontSize: 16,
    fontWeight: 700,
    cursor: "pointer",
    marginTop: 8,
    width: "100%",
    transition: "opacity 0.2s",
    minHeight: "52px",
  },
  examplesRow: {
    marginTop: 20,
    display: "flex",
    flexWrap: "wrap",
    gap: 10,
    alignItems: "center",
  },
  examplesLabel: { fontSize: 13, color: "#94a3b8", fontWeight: 600 },
  exampleChip: {
    padding: "7px 14px",
    background: "#f1f5f9",
    border: "1px solid #e2e8f0",
    borderRadius: 20,
    fontSize: 13,
    cursor: "pointer",
    color: "#475569",
    textAlign: "left",
    transition: "background 0.15s",
  },
  errorBox: {
    background: "#fef2f2",
    border: "1px solid #fecaca",
    color: "#b91c1c",
    borderRadius: 8,
    padding: "16px 18px",
    marginBottom: 16,
    fontSize: 15,
  },
  intentBox: {
    background: "#eff6ff",
    border: "1px solid #bfdbfe",
    borderRadius: 10,
    padding: "16px 20px",
    marginBottom: 24,
    fontSize: 15,
    color: "#1e40af",
  },
  intentTags: { display: "flex", gap: 10, flexWrap: "wrap", marginTop: 10 },
  intentTag: {
    background: "#dbeafe",
    padding: "4px 12px",
    borderRadius: 12,
    fontSize: 13,
    fontWeight: 600,
  },
  resultsHeader: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    marginBottom: 20,
  },
  resultsCount: { fontSize: 20, fontWeight: 700, color: "#0f5c2e" },
  noResults: { color: "#94a3b8", fontSize: 15 },
  schemeList: { display: "flex", flexDirection: "column", gap: 16 },
  schemeCard: {
    background: "white",
    borderRadius: 12,
    boxShadow: "0 2px 12px rgba(0,0,0,0.06)",
    overflow: "hidden",
    transition: "box-shadow 0.2s",
  },
  schemeHeader: {
    display: "flex",
    alignItems: "flex-start",
    justifyContent: "space-between",
    padding: "20px 24px",
    cursor: "pointer",
    gap: 16,
  },
  schemeLeft: { flex: 1 },
  categoryBadge: {
    display: "inline-block",
    padding: "3px 12px",
    borderRadius: 12,
    fontSize: 12,
    fontWeight: 700,
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    marginBottom: 8,
  },
  schemeName: { fontSize: 18, fontWeight: 700, color: "#1e293b", marginBottom: 6 },
  schemeDesc: { fontSize: 14, color: "#64748b", lineHeight: 1.6 },
  chevron: { fontSize: 14, color: "#94a3b8", marginTop: 4, flexShrink: 0 },
  schemeBody: {
    padding: "20px 24px",
    borderTop: "1px solid #f1f5f9",
  },
  benefitBox: {
    background: "#f0fdf4",
    borderRadius: 8,
    padding: "14px 18px",
    marginBottom: 16,
  },
  sectionLabel: {
    fontSize: 13,
    fontWeight: 700,
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    color: "#475569",
    marginBottom: 8,
  },
  benefitText: { fontSize: 15, color: "#166534", fontWeight: 600 },
  docsRow: { marginBottom: 16 },
  docList: { margin: 0, paddingLeft: 20, display: "flex", flexWrap: "wrap", gap: "6px 28px" },
  docItem: { fontSize: 14, color: "#374151", marginBottom: 4 },
  eligRow: { marginBottom: 16 },
  eligGrid: { display: "flex", flexWrap: "wrap", gap: 10 },
  eligChip: {
    background: "#f1f5f9",
    border: "1px solid #e2e8f0",
    borderRadius: 6,
    padding: "6px 12px",
    fontSize: 13,
    color: "#475569",
    fontWeight: 600,
  },
  tagsRow: {
    display: "flex",
    flexWrap: "wrap",
    gap: 8,
    marginBottom: 18,
  },
  tag: {
    background: "#f8fafc",
    border: "1px solid #e2e8f0",
    borderRadius: 20,
    padding: "3px 10px",
    fontSize: 12,
    color: "#64748b",
  },
  applyBtn: {
    display: "inline-block",
    padding: "12px 26px",
    background: "linear-gradient(135deg, #1a3c6e, #0f5c2e)",
    color: "white",
    borderRadius: 8,
    textDecoration: "none",
    fontWeight: 700,
    fontSize: 15,
  },
  footer: {
    textAlign: "center",
    padding: "28px 40px",
    color: "#94a3b8",
    fontSize: 13,
    borderTop: "1px solid #e2e8f0",
    background: "white",
    width: "100%",
    boxSizing: "border-box",
  },
};