# SkillGraph: Architecture & Hidden Skill Discovery Extension

## 1. System Overview & Data Flow

SkillGraph operates as an end-to-end intelligence pipeline. The diagram below illustrates the baseline data flow and the targeted extension point for Evidence-Based Hidden Skill Discovery.

```
[ Candidate CV / Text Input ]
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Text & Evidence Preprocessing                       │
│    - Alias Normalization (e.g. React.js -> React)       │
│    - Sentence / Bullet Segmentation                     │
│    - Action Verb & Context Detection                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Dual-Track Extraction                                │
│    ├─ Track A: Explicit Skills (Keywords, Regex, NER)  │
│    └─ Track B: Evidence Fragments (Context + Actions)   │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Evidence-Based Hidden Skill Discovery [NEW ENGINE]   │
│    - Controlled Capability Profiles                     │
│    - Evidence Thresholding (No single-technology claims)│
│    - Evidence Traceability & Source Context Linking     │
│    - Inference Confidence Scoring                       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Unified Skill Profile                                │
│    - Explicit Skills (Extraction Confidence: 0.80–0.95) │
│    - Inferred Skills (Inference Confidence: 0.00–1.00)  │
│    - Full Supporting Evidence Chains                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Extended Skill Graph & Visualisation                 │
│    - Explicit Nodes & Inferred Capability Nodes         │
│    - Semantic, Domain, and "Supports" Evidence Edges    │
│    - Dual-color/style Node Rendering in Plotly          │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 6. Job Matching & Explainable Insights                  │
│    - Explicit Matches vs Inferred Matches vs Missing    │
│    - Traceable Evidence Explanations in UI              │
│    - Proximity-based Recommendations & Exports          │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Minimal Extension Architecture

To avoid unnecessary complexity, the extension is structured around four minimal touchpoints:

### 2.1 Module Responsibility Separation
- **`skill_extractor.py`**: Retains backward-compatible `extract_skills(text)` while adding `extract_skills_and_evidence(text)`. Performs canonical alias normalization and sentence segmentation to collect action phrases.
- **`hidden_skill_inference.py` [New Module]**: Implements the capability reasoning engine:
  - Controlled capability taxonomy (Backend Development, API Development, Unsupervised Learning / Clustering, Deep Learning Engineering, XR/VR Development, Cloud Infrastructure, Real-Time Application Development).
  - Validation: Requires at least 2 distinct anchor skills or strong anchor + action verb evidence. Prevents speculative leaps (e.g. Python alone $\not\to$ Cybersecurity).
  - Traceability schema linking inferred capabilities to contributing skills and text fragments.
- **`graph_builder.py`**: Extended to accept both explicit and inferred skills. Inferred nodes are tagged with `node_type='inferred'`; directed "supports" edges connect explicit evidence nodes to the inferred capability node.
- **`visualise.py`**: Visualizes explicit and inferred nodes with distinct styling and hover details.
- **`app.py`**: Presents separate Explicit Skills and Inferred Capabilities panels, tripartite job matching (Explicit / Inferred / Missing), and updated JSON/CSV download structures.

---

## 3. Data Schemas

### 3.1 Inferred Skill Object
```json
{
  "skill": "Backend Development",
  "type": "inferred",
  "confidence": 0.91,
  "evidence": ["Python", "FastAPI", "PostgreSQL", "REST APIs"],
  "action_evidence": ["built backend services and data pipelines"],
  "source_context": "Software Engineer with 4 years of experience building backend services..."
}
```

### 3.2 Confidence Separation
- **Extraction Confidence**: $P(\text{word is in text})$ based on substring (0.95), regex (0.85), or NER (0.80).
- **Inference Confidence**: Function of evidence count ratio, average extraction confidence of supporting skills, and contextual action relevance score:
  $$\text{Conf}_{\text{inferred}} = w_1 \cdot \left(\frac{|E|}{\text{MinReq}}\right)_{\text{capped}} + w_2 \cdot \overline{\text{Conf}(E)} + w_3 \cdot \text{ActionScore}$$
