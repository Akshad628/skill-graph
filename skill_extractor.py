import logging
import re
from typing import List, Tuple
import spacy

logger = logging.getLogger(__name__)

# Load small English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

# Comprehensive skill dictionary with categories
SKILL_DATABASE = {
    "Backend": [
        "Python", "Flask", "Django", "FastAPI", "Spring", "Java",
        "Node.js", "Express", "Go", "Rust", "C++", "C#", ".NET"
    ],
    "Frontend": [
        "React", "Vue", "Angular", "JavaScript", "TypeScript", "HTML",
        "CSS", "Tailwind", "Next.js", "Svelte"
    ],
    "Data": [
        "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch",
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
        "Data Analysis", "Statistics", "R", "SAS"
    ],
    "DevOps": [
        "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Jenkins",
        "CI/CD", "Terraform", "Linux", "Git"
    ],
    "Databases": [
        "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis", "Cassandra",
        "Elasticsearch", "DynamoDB"
    ],
    "Other": [
        "REST APIs", "GraphQL", "Microservices", "SOLID", "OOP",
        "Design Patterns", "Agile", "System Design"
    ]
}

COMMON_SKILLS = []
for skills in SKILL_DATABASE.values():
    COMMON_SKILLS.extend(skills)

# Regex patterns for common acronyms/technical terms
TECH_PATTERNS = {
    r"\bML\b": "Machine Learning",
    r"\bDL\b": "Deep Learning",
    r"\bNLP\b": "NLP",
    r"\bAPI\b": "REST APIs",
    r"\bRESTful\b": "REST APIs",
    r"\bOOP\b": "OOP",
}

# Canonical alias mappings for common variations
TECH_ALIASES = {
    "react.js": "React",
    "reactjs": "React",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "express.js": "Express",
    "expressjs": "Express",
    "vue.js": "Vue",
    "vuejs": "Vue",
    "angular.js": "Angular",
    "angularjs": "Angular",
    "nextjs": "Next.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mongo": "MongoDB",
    "mongodb": "MongoDB",
    "k8s": "Kubernetes",
    "amazon web services": "AWS",
    "google cloud": "GCP",
    "google cloud platform": "GCP",
    "microsoft azure": "Azure",
    "restful": "REST APIs",
    "rest api": "REST APIs",
    "rest apis": "REST APIs",
    "rest": "REST APIs",
    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "ci / cd": "CI/CD",
    "cicd": "CI/CD",
}

# Key action verbs indicating technical implementation/responsibilities
ACTION_VERBS = {
    "build", "built", "develop", "developed", "developing", "implement", "implemented",
    "implementing", "design", "designed", "architect", "architected", "deploy", "deployed",
    "deploying", "containerise", "containerised", "containerize", "containerized",
    "train", "trained", "training", "fine-tune", "fine-tuned", "finetuned", "tune",
    "tuned", "optimize", "optimized", "scale", "scaled", "maintain", "maintained",
    "engineer", "engineered", "cluster", "clustered", "preprocess", "preprocessed",
    "stream", "streamed", "authenticate", "authenticated", "integrate", "integrated",
    "orchestrate", "orchestrated", "refactor", "refactored"
}

def normalize_text_aliases(text: str) -> str:
    """Normalize common technology aliases in text for consistent extraction."""
    normalized = text
    for alias, canonical in TECH_ALIASES.items():
        # Match whole words/phrases
        pattern = r"(?i)\b" + re.escape(alias) + r"\b"
        normalized = re.sub(pattern, canonical, normalized)
    return normalized

def extract_skills(text: str) -> Tuple[List[str], List[Tuple[str, float]]]:
    """
    Extract skills from input text using multiple strategies.

    Args:
        text: CV or LinkedIn text

    Returns:
        Tuple of (extracted_skills, confidence_scores)
        confidence_scores is list of (skill, confidence) tuples
    """
    if not text or not text.strip():
        return [], []

    extracted = set()
    confidence_scores = {}

    # Pre-process text to normalize aliases
    normalized_text = normalize_text_aliases(text)

    try:
        # Strategy 1: Direct substring matching (high confidence)
        text_lower = normalized_text.lower()
        for skill in COMMON_SKILLS:
            # Check with word boundary to avoid substring collisions (e.g. 'c' in 'cat')
            pattern = r"(?i)\b" + re.escape(skill) + r"\b"
            if re.search(pattern, normalized_text):
                extracted.add(skill)
                confidence_scores[skill] = 0.95
            elif skill.lower() in text_lower:
                extracted.add(skill)
                confidence_scores[skill] = 0.90
    except Exception as e:
        logger.error(f"Error in substring matching: {e}")

    try:
        # Strategy 2: Regex patterns for acronyms
        for pattern, skill in TECH_PATTERNS.items():
            if re.search(pattern, normalized_text):
                extracted.add(skill)
                confidence_scores[skill] = max(confidence_scores.get(skill, 0.0), 0.85)
    except Exception as e:
        logger.error(f"Error in regex matching: {e}")

    try:
        # Strategy 3: spaCy NER for entities
        if nlp:
            doc = nlp(normalized_text)
            # Extract PERSON entities (often skill names), ORG (frameworks/tools)
            for ent in doc.ents:
                if ent.label_ in ["PRODUCT", "ORG"]:
                    for skill in COMMON_SKILLS:
                        if skill.lower() in ent.text.lower():
                            extracted.add(skill)
                            confidence_scores[skill] = max(confidence_scores.get(skill, 0.0), 0.80)
    except Exception as e:
        logger.error(f"Error in spaCy NER: {e}")

    # Build confidence-scored list, sorted by confidence descending
    results = [(skill, confidence_scores.get(skill, 0.75)) for skill in extracted]
    results.sort(key=lambda x: x[1], reverse=True)

    return [r[0] for r in results], results

def extract_skills_and_evidence(text: str) -> dict:
    """
    Extract explicit skills alongside evidence-bearing text segments (projects, experience, actions).

    Args:
        text: Raw CV or portfolio text

    Returns:
        Dictionary containing:
            - explicit_skills: List of unique skill names
            - confidence_scores: List of (skill, confidence) tuples
            - evidence_items: List of evidence items with text snippet, actions found, and co-occurring skills
    """
    explicit_skills, confidence_scores = extract_skills(text)
    if not text or not text.strip():
        return {
            "explicit_skills": [],
            "confidence_scores": [],
            "evidence_items": []
        }

    # Split into lines/bullets/sentences for contextual evidence segmentation
    raw_segments = re.split(r"[\n\r•\-\*]+|(?<=[.!?])\s+", text)
    evidence_items = []

    for segment in raw_segments:
        clean_segment = segment.strip()
        if len(clean_segment) < 15:
            continue

        words = re.findall(r"\b[a-zA-Z\-]+\b", clean_segment.lower())
        detected_actions = [w for w in words if w in ACTION_VERBS]

        # Find which explicit skills co-occur in this segment
        segment_skills = [
            skill for skill in explicit_skills
            if re.search(r"(?i)\b" + re.escape(skill) + r"\b", clean_segment)
        ]

        # If the segment contains technical skills or technical action verbs, preserve as evidence
        if segment_skills or detected_actions:
            evidence_items.append({
                "text": clean_segment,
                "skills": segment_skills,
                "actions": detected_actions
            })

    return {
        "explicit_skills": explicit_skills,
        "confidence_scores": confidence_scores,
        "evidence_items": evidence_items
    }

def get_skill_category(skill: str) -> str:
    """Return the category of a skill."""
    for category, skills in SKILL_DATABASE.items():
        if skill in skills:
            return category
    return "Other"

# Unit tests
def test_extract_skills():
    """Basic tests for skill extraction."""
    test_cases = [
        ("I use Python and Flask daily", {"Python", "Flask"}),
        ("Machine Learning with TensorFlow and PyTorch", {"Machine Learning", "TensorFlow", "PyTorch"}),
        ("", set()),
        ("No skills here!@#$", set()),
    ]

    for text, expected in test_cases:
        extracted, _ = extract_skills(text)
        assert expected.issubset(set(extracted)), f"Failed for: {text}"

    logger.info("All tests passed!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_extract_skills()