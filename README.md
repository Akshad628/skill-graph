# SkillGraph — Evidence-Based Hidden Skill Discovery

**An explainable CV skill intelligence platform that discovers demonstrated, higher-level technical capabilities from candidate project evidence, tools, and responsibilities, mapping them into an interactive knowledge network.**

[![Python 3.11](https://img.shields.io/badge/python-3.11.9-blue.svg)](https://www.python.org/downloads/release/python-3119/)
[![Tests](https://img.shields.io/badge/pytest-52%20passed-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Repository: [https://github.com/Akshad628/skill-graph](https://github.com/Akshad628/skill-graph)

---

## Important: Python Version Requirement

> [!CAUTION]
> **This project requires Python 3.11 (specifically verified on Python 3.11.9). Do NOT use Python 3.12 or newer.**

### Why Python 3.11 is Mandatory
The repository dependencies pinned in `requirements.txt` specify `numpy==1.24.3`. 
- **Python 3.12+ Failure**: Pre-built binary wheels for `numpy==1.24.3` are **not** available for Python 3.12+. When attempting installation on Python 3.12+, `pip` attempts to compile NumPy from source, which fails immediately unless a complete C/C++ compiler and Fortran toolchain are configured on the machine.
- **Python 3.11 Success**: Python 3.11 provides official pre-compiled binary wheels for `numpy==1.24.3`, `torch==2.0.1`, and `scikit-learn==1.3.2`, allowing a clean, zero-compilation installation.
- To ensure 100% reproducible execution, use **Python 3.11.x**. Do not randomly upgrade package versions in `requirements.txt`.

---

## Features

- **Multi-Strategy Explicit Extraction**: Extracts declared tools and languages using direct substring matching (0.95 confidence), regex technical acronym detection (0.85 confidence), and entity recognition.
- **Contextual Action & Evidence Parsing**: Analyzes experience bullets and project sentences for technical action verbs (`built`, `developed`, `deployed`, `trained`, `containerised`, `architected`).
- **Evidence-Based Hidden Skill Discovery**: Infers higher-level capabilities (e.g., *Backend Development*, *API Development*, *Unsupervised Learning / Clustering*, *Cloud Infrastructure & DevOps*, *XR / VR Development*) only when demonstrably justified by compound technological evidence.
- **Strict Non-Speculative Policy**: Disallows wild leaps from isolated technologies (e.g. `Python` alone never infers *Cybersecurity*, *Data Science*, or *AI Research*).
- **Interactive Plotly Graph**: Generates a 2D network where nodes represent explicit skills (categorized by domain) and discovered capabilities (amber badge), connected by semantic similarity, domain knowledge, and evidence-support edges.
- **Tripartite Job Role Analysis**: Evaluates candidate fit across 18+ roles by categorizing requirements into **Explicit Matches**, **Inferred Capability Matches**, and **Missing Skills**.
- **Graph Proximity Learning Recommendations**: Prioritizes missing competencies based on shortest-path graph distance to skills already demonstrated.
- **Multi-Format Input & Export**: Supports plain text input, `.pdf`, `.docx`, and `.txt` uploads, with complete JSON and CSV traceability exports.

---

## How It Works: Explicit vs. Inferred Skills

| Dimension | Explicit Skills | Inferred / Hidden Capabilities |
| :--- | :--- | :--- |
| **Definition** | Directly mentioned technologies, languages, or tools | Higher-level competencies evidenced by compound tools & project actions |
| **Examples** | `Python`, `FastAPI`, `PostgreSQL`, `Docker` | `Backend Development`, `API Development`, `Cloud Infrastructure & DevOps` |
| **Detection Method** | Exact substring matching, alias normalization, regex | Anchor validation, thresholded evidence aggregation, action verification |
| **Confidence Type** | **Extraction Confidence** (0.80–0.95): certainty keyword is in text | **Inference Confidence** (0.65–0.95): strength & breadth of supporting evidence |
| **Traceability** | Textual position in CV | Supporting technologies + technical action verbs + CV excerpt snippet |
| **Graph Node** | Category colored (Blue, Green, Amber, Purple, Pink) | Golden amber node with incoming `evidence_support` edges |
| **Role Matching** | Satisfied directly as an **Explicit Match** | Satisfied via demonstrated evidence as an **Inferred Match** |

---

## Architecture

```
Candidate CV / Text (PDF, DOCX, TXT)
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 1. Alias Normalization & Segmentation                   │
│    (skill_extractor.py: extract_skills_and_evidence)    │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Evidence-Based Inference Engine                      │
│    (hidden_skill_inference.py: infer_hidden_skills)     │
│    - Checks core anchor requirements                    │
│    - Evaluates minimum supporting evidence thresholds   │
│    - Enforces negative constraints (no wild leaps)      │
│    - Generates evidence provenance schema               │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Unified Skill Profile & NetworkX Graph               │
│    (graph_builder.py: build_skill_graph)                │
│    - Semantic embeddings (all-MiniLM-L6-v2)             │
│    - Domain knowledge weights                           │
│    - Directed 'evidence_support' edges                  │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Streamlit UI & Explainable Matching (app.py)         │
│    - Explicit vs Inferred Skills Panels                 │
│    - Interactive Plotly Visualisation (visualise.py)    │
│    - Tripartite Job Role Matching & Recommendations     │
│    - JSON & CSV Traceability Exports                    │
└─────────────────────────────────────────────────────────┘
```

---

## Requirements

- **Operating System**: Windows 10/11 (Primary, verified), Linux, or macOS.
- **Python Version**: **Python 3.11.x** (Tested on Python 3.11.9).
- **Core Packages**: Streamlit 1.28.1, Sentence-Transformers 2.7.0, NetworkX 3.2, Plotly 5.17.0, PyTorch 2.0.1, Scikit-learn 1.3.2, Pandas 2.1.1, NumPy 1.24.3.

---

## Setup on Windows

Follow these exact steps in **PowerShell**.

### Step 1 — Check Installed Python Interpreters
On Windows, check which Python versions are available on your system using the Windows Python launcher:
```powershell
py --list
```
and check your default interpreter:
```powershell
python --version
```
If Python 3.11 is not listed, download and install **Python 3.11.9 (64-bit)** from [python.org](https://www.python.org/downloads/release/python-3119/). During installation, ensure you check **"Add python.exe to PATH"** and **"Install launcher for all users (py.exe)"**.

### Step 2 — Clone the Repository
Clone the repository and enter the project folder:
```powershell
git clone https://github.com/Akshad628/skill-graph.git
cd skill-graph
```

### Step 3 — Verify Python 3.11 BEFORE Creating Virtual Environment
Use the Python launcher `py -3.11` to confirm Python 3.11 is detected:
```powershell
py -3.11 --version
```
> [!IMPORTANT]
> **DO NOT continue** if this does not report `Python 3.11.x`. If `python` points to Python 3.12 or 3.13, using a bare `python -m venv` will build a Python 3.12+ environment and fail during dependency installation.

### Step 4 — Create the Virtual Environment
Explicitly create the virtual environment using the Python 3.11 interpreter:
```powershell
py -3.11 -m venv venv
```
*Why `py -3.11 -m venv venv` instead of `python -m venv venv`?*  
On machines with multiple Python versions installed, `python` typically invokes the latest version (e.g., Python 3.12 or 3.13). Using `py -3.11` guarantees that the virtual environment interpreter is strictly Python 3.11.

### Step 5 — Activate the Virtual Environment
Activate the environment in PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```
*(If using Command Prompt `cmd.exe` instead, run: `venv\Scripts\activate.bat`)*

Immediately verify that the active environment is Python 3.11:
```powershell
python --version
```
It **MUST** output `Python 3.11.x`.

> [!TIP]
> **If PowerShell blocks script execution:**
> If you encounter an error stating `cannot be loaded because running scripts is disabled on this system`, run this safe command for the current user:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then re-run `.\venv\Scripts\Activate.ps1`.

### Step 6 — Upgrade pip
Ensure pip is current within the virtual environment:
```powershell
python -m pip install --upgrade pip
```
*(Always use `python -m pip` to guarantee operations target the active environment's interpreter).*

### Step 7 — Install Dependencies
Install the verified requirements:
```powershell
python -m pip install -r requirements.txt
```

### Step 8 — Verify Dependencies
Verify that all packages are satisfied with zero conflicts:
```powershell
python -m pip check
```
Expected output:
```text
No broken requirements found.
```

You can also run a quick import check:
```powershell
python -c "import streamlit, sentence_transformers, networkx, plotly, pandas, numpy; print('All core dependencies OK')"
```
Expected output:
```text
All core dependencies OK
```

### Step 9 — Run the Automated Tests
Run the test suite:
```powershell
pytest -v
```
Expected output:
```text
======================= 52 passed in 7.96s =======================
```
All 52 unit, integration, and hidden skill evaluation tests should pass.

### Step 10 — Start the Application
Launch the Streamlit web application:
```powershell
streamlit run app.py
```
If your default browser does not launch automatically, manually open:
```
http://localhost:8501
```

---

## Virtual Environment Verification & Recovery

If you ever encounter installation errors or suspect your environment is running the wrong version, check:
```powershell
python --version
```
If this shows `Python 3.12.x` or `Python 3.13.x`, your virtual environment was created with the wrong interpreter. Follow this recovery workflow:

1. Deactivate the bad environment:
   ```powershell
   deactivate
   ```
2. Delete the incorrect `venv` directory:
   ```powershell
   Remove-Item -Recurse -Force .\venv
   ```
3. Re-create the environment explicitly with Python 3.11:
   ```powershell
   py -3.11 -m venv venv
   ```
4. Activate the new environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
5. Confirm Python 3.11 is now active:
   ```powershell
   python --version
   ```
6. Reinstall dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```

---

## Setup on Linux / macOS

On Linux or macOS with Python 3.11 installed:

```bash
# Clone repository
git clone https://github.com/Akshad628/skill-graph.git
cd skill-graph

# Verify Python 3.11
python3.11 --version

# Create virtual environment explicitly with Python 3.11
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip & install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Verify installation & run tests
python -m pip check
pytest -v

# Start application
streamlit run app.py
```

---

## Using the Application

1. **Input Your Profile**:
   - Select **"Text Input"** and click **"Load sample CV"** to try the pre-loaded CV profile, or paste your own raw CV text.
   - Alternatively, choose **"Upload File"** to upload a `.pdf`, `.docx`, or `.txt` CV.
2. **Select Target Role (Optional)**:
   - Choose a target industry role (e.g. *Full Stack Developer*, *Backend Developer*, *Machine Learning Engineer*) to compare against.
3. **Generate Skill Graph**:
   - Click the primary **"Generate Skill Graph"** button.
4. **Inspect Discovered Hidden Skills**:
   - Review the **"Discovered Hidden Skills (Evidence-Backed Capabilities)"** expanders to view inferred capabilities, inference confidence scores, contributing explicit technologies, and extracted CV context snippets.
5. **Explore the Skill Graph**:
   - Hover over graph nodes to view connections and evidence provenance. Explicit skills appear in category colors; inferred capabilities appear in golden amber with incoming evidence edges.
6. **Analyze Role Gap**:
   - Inspect the **Explicit Matches**, **Inferred Matches**, and **Missing Skills** breakdown.
   - Review the **Learning Recommendations** ranked by graph proximity.
7. **Export Data**:
   - Download the full profile as structured **JSON** or tabular **CSV** with provenance fields.

---

## Development Workflow

When contributing to SkillGraph:

1. **Activate Environment**:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
2. **Pull Updates**:
   ```powershell
   git pull origin main
   ```
3. **Make Modifications**: Edit code cleanly; do not commit the `venv/` folder or temporary cache files (these are excluded by `.gitignore`).
4. **Execute Tests**:
   ```powershell
   pytest -v
   ```
5. **Verify Dependencies**:
   ```powershell
   python -m pip check
   ```
6. **Test UI Manually**:
   ```powershell
   streamlit run app.py
   ```
7. **Review Diff & Commit**:
   ```powershell
   git status
   git diff
   git add .
   git commit -m "feat/fix: describe your concise change"
   git push origin main
   ```

---

## Troubleshooting

| Problem | Root Cause | Solution |
| :--- | :--- | :--- |
| **`pip install` fails building NumPy wheel** | Python 3.12 or 3.13 was used to create the `venv`. | Follow the [Virtual Environment Recovery](#virtual-environment-verification--recovery) steps to recreate the `venv` with `py -3.11 -m venv venv`. |
| **`python --version` shows 3.12+ inside `venv`** | Virtual environment was initialized with the default `python` command instead of `py -3.11`. | Run `deactivate`, delete `venv`, and recreate with `py -3.11 -m venv venv`. |
| **`Activate.ps1` cannot be loaded (script execution disabled)** | Windows PowerShell default security execution policy. | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` and re-run activation. |
| **`pytest` or `streamlit` is not recognized** | The virtual environment is either not activated or dependencies were not installed into it. | Run `.\venv\Scripts\Activate.ps1`, then run `python -m pip install -r requirements.txt`. |
| **Application does not open automatically** | Browser auto-launch was blocked or delayed by the OS. | Manually open your browser and navigate to `http://localhost:8501`. |

---

## Evaluation & Negative Constraint Benchmarks

The inference engine in `hidden_skill_inference.py` is tested via `test_hidden_skills.py` against both positive capability benchmarks and negative constraint invariants:

- **Backend Development**: Tested with *FastAPI + PostgreSQL + REST APIs + action verbs* $\to$ Inferred with $\ge 0.70$ confidence.
- **Unsupervised Learning / Clustering**: Tested with *K-Means + Scikit-learn + silhouette score analysis* $\to$ Inferred with $\ge 0.70$ confidence.
- **XR / VR Development**: Tested with *Unity + OpenXR + Meta Quest* $\to$ Inferred with $\ge 0.70$ confidence.
- **Negative Invariant (Single Technology Assertion)**: A CV containing only isolated Python scripts (e.g. *"I write Python scripts for basic file operations"*) is evaluated to ensure the system **strictly rejects** inferring *Cybersecurity*, *AI Research*, or *Data Science*.

---

## Project Structure

```
skill-graph/
├── app.py                     # Streamlit application UI & tripartite job matching
├── skill_extractor.py         # Keyword extraction, alias normalization & evidence parsing
├── hidden_skill_inference.py  # Capability discovery ontology, thresholding & scoring
├── graph_builder.py           # NetworkX graph construction & recommendation logic
├── visualise.py               # Plotly interactive network graph & confidence charts
├── job_roles.json             # Industry job role skill catalog (18 roles)
├── config.yaml                # Model, graph layout, and logging settings
├── test_suite.py              # Unit & regression tests (46 tests)
├── test_hidden_skills.py      # Hidden skill evaluation & negative tests (6 tests)
├── PROJECT_ANALYSIS.md        # Baseline project analysis document
├── BASELINE_RESULTS.md        # Baseline benchmark metrics document
├── ARCHITECTURE.md            # System architecture and data flow document
├── requirements.txt           # Pinned dependency specification
├── .gitignore                 # Excluded files (venv, caches, temporary logs)
└── README.md                  # Complete project guide and documentation
```

---

## Limitations

- **Input Scope**: Capabilities are inferred strictly from candidate-provided text (CV, project descriptions, responsibilities). The system deliberately does not crawl unverified external websites, LinkedIn, or GitHub accounts.
- **Controlled Capability Ontology**: The inference layer uses an explainable, transparent ontology of technical capabilities rather than an unconstrained generative LLM to ensure reproducibility and prevent hallucinations.
- **Deterministic Confidence**: Confidence scores represent evidence breadth and action confirmation rather than a subjective assessment of candidate "potential".

---

## License

This project is licensed under the [MIT License](LICENSE).
