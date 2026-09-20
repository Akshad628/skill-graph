# SkillGraph: Original Project Analysis

## 1. Executive Summary
SkillGraph is an open-source NLP and graph-based intelligence tool designed to parse technical resumes (CVs), extract technical skills, model skill relationships as a weighted network, and evaluate candidate profiles against predefined job roles. This document provides an architectural analysis of the baseline codebase prior to introducing Evidence-Based Hidden Skill Discovery.

---

## 2. Repository Structure and Modules

The baseline project consists of the following core modules:

- **`app.py`**: The Streamlit user interface and application entry point. Handles user inputs (raw text, `.pdf`, `.docx`, `.txt`), triggers extraction and graph pipelines, coordinates job role comparisons, visualizes metrics, and provides JSON/CSV exports.
- **`skill_extractor.py`**: The skill extraction engine using a hybrid of dictionary lookup, regex abbreviation matching, and spaCy Named Entity Recognition (NER).
- **`graph_builder.py`**: NetworkX graph constructor utilizing pre-trained sentence transformer embeddings (`all-MiniLM-L6-v2`) and a curated set of domain-specific relationship weights. It also computes graph metrics and calculates proximity-based learning recommendations.
- **`visualise.py`**: Plotly visualization module that generates interactive 2D spring-layout network diagrams and extraction confidence bar charts.
- **`job_roles.json`**: Predefined catalog of 18 industry job profiles mapping role titles to sets of expected technical skills.
- **`config.yaml`**: System configuration defining model parameters, graph layout constants, logging configurations, and UI options.
- **`test_suite.py`**: Pytest suite covering unit tests, integration pipelines, error handling, edge cases, and performance checks.

---

## 3. Detailed Algorithmic Breakdown

### 3.1 Skill Extraction Pipeline (`skill_extractor.py`)
Extraction combines three complementary strategies:
1. **Direct Substring Matching (Confidence: 0.95)**:
   - Scans normalized lowercase text for exact matches against a predefined `COMMON_SKILLS` vocabulary (~50 skills across Backend, Frontend, Data, DevOps, Databases, Other).
2. **Regex Pattern Matching (Confidence: 0.85)**:
   - Identifies specific technical acronyms with word-boundary regexes (`\bML\b` $\rightarrow$ Machine Learning, `\bNLP\b` $\rightarrow$ NLP, `\bAPI\b` $\rightarrow$ REST APIs).
3. **spaCy Named Entity Recognition (Confidence: 0.80)**:
   - Identifies `PRODUCT` and `ORG` entities via `en_core_web_sm` and cross-references them against `COMMON_SKILLS` to mitigate false positives.

### 3.2 Graph Construction and Weighting (`graph_builder.py`)
Graph vertices represent extracted skills. Edges are weighted undirected connections determined by:
1. **Semantic Embeddings**: Skills are encoded using `SentenceTransformer('all-MiniLM-L6-v2')`. Cosine similarity is computed between all node pairs; edges with similarity exceeding `similarity_threshold` (default 0.3) are added.
2. **Domain Knowledge Overlay**: A table of 25+ curated domain associations (e.g., `Python`-`FastAPI`: 0.95, `Docker`-`Kubernetes`: 0.92) updates edge weights with prioritized domain scores.
3. **Graph Metrics**: Computes node degree, network density, and PageRank to identify central skills.

### 3.3 Recommendation Algorithm
Calculates learning priority for missing job skills based on shortest-path proximity to the candidate's existing skill nodes:
$$\text{score}(s_{\text{missing}}) = \sum_{s \in S_{\text{candidate}}} \frac{1}{\text{dist}_G(s, s_{\text{missing}}) + 1}$$

---

## 4. Current Limitations of Explicit-Only Extraction

1. **Blindness to Higher-Level Capabilities**: If a candidate writes *"Architected distributed microservices in FastAPI and PostgreSQL with JWT auth and WebSocket streaming"*, the system extracts the individual tools but fails to recognize meta-capabilities such as **Backend Development**, **API Design**, or **Real-Time Application Development**.
2. **Vocabulary Rigidity**: Candidate skills described with minor variations or alternative phrasings (e.g. `React.js` vs `React`) may be overlooked unless explicitly normalized.
3. **Disregard for Action Context**: Verbs and implementation context (e.g., *"containerised"*, *"deployed"*, *"designed"*) are currently discarded by substring filtering, losing critical evidence regarding how technologies were used.
4. **Job Match Penalty**: Job roles in `job_roles.json` requiring high-level concepts (e.g., System Design, Cloud Architecture) severely penalize candidates who demonstrated those capabilities through project evidence without using exact keyword strings.
