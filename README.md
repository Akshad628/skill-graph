# SkillGraph: Evidence-Based Hidden Skill Discovery

**An explainable CV skill intelligence platform that discovers demonstrated higher-level technical capabilities from project evidence, technologies, and responsibilities, mapping them into an interactive knowledge network.**

---

## 1. Project Overview & Research Motivation

Traditional skill extraction tools rely almost exclusively on **explicit keyword spotting**. If a candidate's CV lists:
- *Python*, *FastAPI*, *REST APIs*, *PostgreSQL*, and *JWT authentication*
- along with bullet points such as *"Built scalable backend services and microservice endpoints"*

conventional parsers match only the explicit library names. They fail to identify the higher-level meta-capability: **Backend Development** or **API Development**. Conversely, unconstrained AI platforms often make wild, speculative predictions (e.g. guessing *Cybersecurity* or *AI Research* merely because a candidate wrote a Python script).

SkillGraph addresses this fundamental research question:
> **"Can a CV-based skill graph infer higher-level technical capabilities from combinations of explicitly stated technologies, project work, responsibilities, and experience evidence, rather than relying only on directly mentioned skills?"**

The system provides **explainable, evidence-backed capability discovery**: Every inferred capability is strictly grounded in candidate-provided evidence, completely traceable, and clearly demarcated from explicit skills.

---

## 2. Core Concepts: Explicit vs. Inferred Skills

| Dimension | Explicit Skills | Inferred / Hidden Capabilities |
| :--- | :--- | :--- |
| **Definition** | Directly named technologies, tools, or libraries | Higher-level technical competencies evidenced by compound actions & tools |
| **Example** | `FastAPI`, `PostgreSQL`, `React`, `Docker` | `Backend Development`, `API Development`, `XR / VR Development` |
| **Detection Method** | Canonical substring matching, regex acronyms, and spaCy NER | Anchor validation, evidence aggregation thresholding, action confirmation |
| **Confidence Metric** | **Extraction Confidence** (0.80–0.95): certainty that the keyword exists in text | **Inference Confidence** (0.65–0.95): strength and breadth of supporting evidence |
| **Traceability** | Direct textual span in CV | Explicit supporting technologies + action verbs + CV excerpt snippets |
| **Graph Representation** | Category-colored circle nodes | Amber-highlighted capability nodes with incoming "evidence_support" edges |
| **Job Role Matching** | Direct requirement satisfaction (**Explicit Match**) | Competence-level requirement satisfaction (**Inferred Match**) |

### Strict Non-Speculative Guarantee
The system **never** makes speculative leaps from isolated technologies. For example:
- `Python` alone $\not\to$ *Cybersecurity*, *Data Science*, or *AI Research*
- `Python` + `Pandas` + `Scikit-learn` + `K-Means` + action evidence *"clustered"* $\to$ **Unsupervised Learning / Clustering** (Supported)

---

## 3. System Architecture & Pipeline

```
Candidate CV / Text (PDF, DOCX, TXT)
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Alias Normalization & Preprocessing                  │
│    (e.g., React.js -> React, Postgres -> PostgreSQL)    │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Dual-Track Extraction (skill_extractor.py)           │
│    ├─ Explicit Skills + Extraction Confidence           │
│    └─ Contextual Action Phrases & Experience Bullets    │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Hidden Skill Discovery (hidden_skill_inference.py)   │
│    ├─ Anchor Requirements & Capability Profiles         │
│    ├─ Evidence Count Thresholding (min 2-3 supports)    │
│    ├─ Negative Invariant Checks                         │
│    └─ Traceability Schema Generation                    │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Unified Graph Network (graph_builder.py)             │
│    ├─ Semantic Embeddings (all-MiniLM-L6-v2)            │
│    ├─ Domain Knowledge Relationships                    │
│    └─ Inferred Capability "evidence_support" Edges      │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Explainable Analytics & Job Matching (app.py)        │
│    ├─ Tripartite Match (Explicit / Inferred / Missing)  │
│    ├─ Interactive Plotly Visualisation (visualise.py)   │
│    ├─ Proximity-based Recommendations                   │
│    └─ JSON & CSV Traceability Exports                   │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Quick Start

### Prerequisites
- Python 3.10 or 3.11
- Virtual environment recommended

### Installation
```bash
# Clone the repository
git clone https://github.com/Akshad628/skill-graph.git
cd skill-graph

# Setup virtual environment
python -m venv venv
venv\Scripts\activate      # On Linux/macOS: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Launch the Streamlit application
streamlit run app.py
```

Open your browser at `http://localhost:8501`. Click **"Load sample CV"** and then **"Generate Skill Graph"** to inspect explicit skills, discovered capabilities, interactive network graphs, and role alignments.

---

## 5. Traceability Schema & Data Model

Every inferred skill is accompanied by complete provenance:
```json
{
  "skill": "Backend Development",
  "type": "inferred",
  "category": "Backend",
  "confidence": 0.91,
  "evidence": [
    "Python",
    "FastAPI",
    "PostgreSQL",
    "REST APIs"
  ],
  "action_evidence": [
    "built",
    "deploy"
  ],
  "source_context": "Software Engineer with 4 years of experience building backend services and data pipelines."
}
```

---

## 6. Testing & Evaluation

Run the automated test suites:
```bash
# Run all regression and hidden-skill evaluation tests
pytest test_suite.py test_hidden_skills.py -v
```

The test suites validate:
1. **Core NLP Extraction**: Keyword substring matching, acronym parsing, spaCy NER, and alias normalization.
2. **Backwards Compatibility**: Baseline graph construction, PageRank, degree centrality, and shortest-path recommendations.
3. **Controlled Positive Capabilities**: Backend Development, Unsupervised Learning / Clustering, XR / VR Development, and API Engineering.
4. **Negative Constraint Assertions**: Rejecting speculative leaps from isolated languages (e.g. verifying Python alone never infers Cybersecurity).
5. **Edge Cases**: Empty text, sparse profiles, unicode strings, and graceful fallbacks.

---

## 7. Project Structure

```
skill-graph/
├── app.py                     # Streamlit UI, tripartite job matching, exports
├── skill_extractor.py         # Multi-strategy extraction & contextual evidence parsing
├── hidden_skill_inference.py  # Controlled capability ontology, thresholding & scoring
├── graph_builder.py           # NetworkX graph construction & proximity recommendations
├── visualise.py               # Plotly interactive network graph & confidence charts
├── job_roles.json             # Industry job role benchmark definitions
├── config.yaml                # Model, graph, and UI configuration
├── test_suite.py              # Baseline unit and integration tests
├── test_hidden_skills.py      # Hidden skill evaluation and negative test cases
├── PROJECT_ANALYSIS.md        # Phase 1 deep-dive into baseline codebase
├── BASELINE_RESULTS.md        # Phase 1 baseline experimental metrics
├── ARCHITECTURE.md            # Phase 1 architecture & data flow documentation
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```
