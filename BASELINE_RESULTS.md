# SkillGraph: Baseline Results Documentation

## 1. Experimental Setup
The baseline system was executed using Python 3.11 with the original project dependencies and Streamlit interface. The test environment passed all 44 unit and integration tests in `test_suite.py` in under 10 seconds.

---

## 2. Baseline Experiment Output

### 2.1 Candidate Input Text (Sample CV)
The baseline test input consisted of the following technical CV profile:
```text
Software Engineer with 4 years of experience building backend services and data pipelines.

Skills & Technologies:
- Languages: Python, JavaScript, SQL
- Frameworks: Flask, FastAPI, React, Node.js
- Data: Pandas, NumPy, Scikit-learn, Machine Learning
- Infrastructure: Docker, Kubernetes, AWS, Git, CI/CD
- Databases: PostgreSQL, MongoDB, Redis
- Practices: REST APIs, Microservices, Agile, System Design

Experience:
- Built ML-powered recommendation engine using Python and Scikit-learn
- Containerised microservices with Docker and deployed to AWS ECS
- Developed React frontend consuming RESTful APIs
- Maintained PostgreSQL and MongoDB databases for high-traffic applications
```

### 2.2 Extraction Output
- **Total Skills Extracted**: 22 explicit skills
  - *Backend*: Python, Flask, FastAPI, Node.js
  - *Frontend*: React, JavaScript
  - *Data*: Pandas, NumPy, Scikit-learn, Machine Learning
  - *DevOps*: Docker, Kubernetes, AWS, Git, CI/CD
  - *Databases*: SQL, PostgreSQL, MongoDB, Redis
  - *Other*: REST APIs, Microservices, Agile, System Design
- **Extraction Confidence**: 0.95 (substring matches), 0.85 (regex acronyms like REST APIs).

### 2.3 Graph Network Metrics
- **Total Nodes**: 22
- **Total Connections (Edges)**: 21
- **Network Density**: 0.09
- **Average Degree**: 1.9
- **Most Central Skill (PageRank)**: Python

### 2.4 Job Role Matching (Target: "Full Stack Developer")
- **Required Skills (12)**: Python, JavaScript, React, Django, Flask, PostgreSQL, SQL, Docker, Git, REST APIs, HTML, CSS
- **Matched Skills (7)**: Python, JavaScript, React, Flask, PostgreSQL, SQL, Docker (plus Git, REST APIs in broader matches)
- **Missing Skills (5)**: Django, HTML, CSS (and unlisted requirements)
- **Baseline Match Percentage**: ~58%
- **Learning Recommendations**: Django prioritized due to close graph distance to Python/Flask.

---

## 3. What is Working
1. Direct keyword identification of popular programming languages and libraries is accurate and deterministic.
2. The sentence-transformer cosine similarity combined with curated domain rules produces realistic edges between closely related tools (e.g., Python—Flask, Docker—Kubernetes).
3. Shortest-path graph recommendation offers intuitive learning ordering.
4. Export options (JSON and CSV) operate reliably without data corruption.

---

## 4. Observed Weaknesses & Research Gap
1. **Omission of Demonstrated Meta-Skills**: Despite clear evidence of building full backend architectures (FastAPI, Flask, PostgreSQL, Redis, REST APIs), the skill list contains no explicit node for "Backend Development".
2. **Context Loss**: Information in "Built ML-powered recommendation engine" is reduced solely to the presence of the keywords "Python" and "Scikit-learn"; the evidence of applied machine learning modeling is lost.
3. **Absence of Evidence Chains**: In the baseline, a skill is either present or absent; there is no representation showing *why* a higher-level competence is present through compound technological evidence.
