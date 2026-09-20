import logging
import re
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Controlled ontology for higher-level capability discovery.
# Each capability requires a minimum number of supporting skills from its knowledge domain,
# core anchor requirements, and optional contextual action keywords to prevent speculative inference.
CAPABILITY_RULES: Dict[str, Dict[str, Any]] = {
    "Backend Development": {
        "description": "Building, structuring, and maintaining server-side applications, business logic, and databases.",
        "category": "Backend",
        # At least one core backend anchor must be present
        "core_anchors": ["Python", "Flask", "Django", "FastAPI", "Node.js", "Express", "Java", "Spring", "Go", "Rust", "C++", "C#", ".NET"],
        # Supporting technological evidence
        "related_evidence": [
            "REST APIs", "SQL", "PostgreSQL", "MySQL", "MongoDB", "Redis",
            "Microservices", "Docker", "GraphQL", "Cassandra", "Elasticsearch"
        ],
        "action_keywords": ["build", "built", "develop", "developed", "architect", "architected", "maintain", "maintained", "backend", "api", "server"],
        "min_total_evidence": 3,  # Needs core anchor + at least 2 other related tools
    },
    "API Development": {
        "description": "Designing, implementing, and exposing web and microservice communication interfaces.",
        "category": "Backend",
        "core_anchors": ["REST APIs", "GraphQL", "FastAPI", "Flask", "Express"],
        "related_evidence": [
            "Python", "Node.js", "Django", "PostgreSQL", "MongoDB", "Microservices"
        ],
        "action_keywords": ["api", "apis", "restful", "endpoint", "endpoints", "route", "routes", "consume", "consuming", "expose", "exposing", "integrate"],
        "min_total_evidence": 2,
    },
    "Real-Time Application Development": {
        "description": "Engineering interactive low-latency data streaming and real-time client-server communication.",
        "category": "Backend",
        "core_anchors": ["Redis", "FastAPI", "Node.js"],
        "related_evidence": ["WebSocket", "WebSockets", "Kafka", "Socket.io", "REST APIs"],
        "action_keywords": ["real-time", "realtime", "stream", "streaming", "websocket", "websockets", "pub/sub", "pubsub", "low-latency"],
        "min_total_evidence": 2,
    },
    "Authentication / Authorization": {
        "description": "Implementing secure user identity, session management, token handling, and access control.",
        "category": "Other",
        "core_anchors": ["JWT", "OAuth", "OAuth2", "Auth", "Bcrypt"],
        "related_evidence": ["REST APIs", "FastAPI", "Flask", "Django", "Node.js", "PostgreSQL", "Redis"],
        "action_keywords": ["authenticate", "authenticated", "authenticating", "authorization", "authorize", "jwt", "tokens", "session", "login", "security"],
        "min_total_evidence": 2,
    },
    "Unsupervised Learning / Clustering": {
        "description": "Extracting hidden patterns, groupings, and data structures from unlabelled datasets.",
        "category": "Data",
        "core_anchors": ["K-Means", "Clustering", "Silhouette Score", "PCA", "DBSCAN", "Scikit-learn"],
        "related_evidence": ["Pandas", "NumPy", "Python", "Machine Learning", "Data Analysis"],
        "action_keywords": ["cluster", "clustered", "clustering", "unsupervised", "silhouette", "preprocess", "preprocessed", "grouping"],
        "min_total_evidence": 2,
    },
    "Deep Learning Engineering": {
        "description": "Architecting, training, and deploying neural network architectures for complex perception or generation.",
        "category": "Data",
        "core_anchors": ["TensorFlow", "PyTorch", "Deep Learning"],
        "related_evidence": ["Python", "Computer Vision", "NLP", "Machine Learning", "CUDA"],
        "action_keywords": ["train", "trained", "training", "neural", "weights", "fine-tune", "fine-tuned", "finetuning", "loss", "epoch"],
        "min_total_evidence": 2,
    },
    "Cloud Infrastructure & DevOps": {
        "description": "Automating containerized workloads, deployment pipelines, and cloud resource management.",
        "category": "DevOps",
        "core_anchors": ["Docker", "Kubernetes", "AWS", "GCP", "Azure", "Terraform"],
        "related_evidence": ["CI/CD", "Linux", "Git", "Jenkins", "Microservices"],
        "action_keywords": ["deploy", "deployed", "deploying", "containerise", "containerised", "containerize", "containerized", "cloud", "pipeline", "orchestrate", "infrastructure"],
        "min_total_evidence": 3,
    },
    "XR / VR Development": {
        "description": "Developing spatial computing, immersive 3D simulations, and virtual reality experiences.",
        "category": "Other",
        "core_anchors": ["Unity", "Unreal Engine", "OpenXR", "Meta Quest", "XR Interaction Toolkit", "WebXR"],
        "related_evidence": ["Blender", "C#", "C++", "3D Modeling", "Computer Vision"],
        "action_keywords": ["xr", "vr", "virtual reality", "immersive", "spatial", "quest", "headset", "3d", "interactive", "simulation"],
        "min_total_evidence": 2,
    },
    "Frontend Architecture": {
        "description": "Designing responsive, component-driven client-side user interfaces and state management systems.",
        "category": "Frontend",
        "core_anchors": ["React", "Vue", "Angular", "Next.js", "Svelte"],
        "related_evidence": ["TypeScript", "JavaScript", "HTML", "CSS", "Tailwind", "REST APIs"],
        "action_keywords": ["frontend", "ui", "ux", "responsive", "component", "dashboard", "spa", "client-side", "interface"],
        "min_total_evidence": 3,
    }
}

# Negative constraints to strictly prevent overreaching speculative claims
PROHIBITED_INFERENCES = {
    # e.g., Python alone MUST NEVER yield Cybersecurity, Data Science, or AI Research
    "Cybersecurity": {"prohibited_if_only": ["Python", "Linux", "Git", "SQL"]},
    "AI Research": {"prohibited_if_only": ["Python", "Scikit-learn", "Machine Learning"]},
    "Data Science": {"prohibited_if_only": ["Python", "Pandas"]},
}

def infer_hidden_skills(
    explicit_skills: List[str],
    evidence_items: Optional[List[Dict[str, Any]]] = None,
    raw_text: str = ""
) -> List[Dict[str, Any]]:
    """
    Infer higher-level technical capabilities supported by explicit skills and CV action evidence.

    Returns:
        List of inferred skill objects:
        [
            {
                "skill": "Backend Development",
                "type": "inferred",
                "category": "Backend",
                "confidence": 0.91,
                "evidence": ["Python", "FastAPI", "PostgreSQL", "REST APIs"],
                "action_evidence": ["built", "deploy"],
                "source_context": "Software Engineer building backend services..."
            }
        ]
    """
    if not explicit_skills and not raw_text:
        return []

    evidence_items = evidence_items or []
    explicit_set = set(explicit_skills)
    text_lower = raw_text.lower()

    # Collect all actions and context across evidence items
    all_actions = set()
    for item in evidence_items:
        for action in item.get("actions", []):
            all_actions.add(action.lower())

    inferred_results = []

    for cap_name, config in CAPABILITY_RULES.items():
        # Do not infer if already explicitly present in skills
        if cap_name in explicit_set:
            continue

        core_anchors = config["core_anchors"]
        related_evidence = config["related_evidence"]
        action_keywords = config["action_keywords"]
        min_total = config["min_total_evidence"]

        # Check matched core anchors (must have at least one core anchor)
        matched_anchors = [
            anchor for anchor in core_anchors
            if anchor in explicit_set or re.search(r"(?i)\b" + re.escape(anchor) + r"\b", text_lower)
        ]

        if not matched_anchors:
            continue

        # Check matched related tools
        matched_related = [
            tool for tool in related_evidence
            if tool in explicit_set or re.search(r"(?i)\b" + re.escape(tool) + r"\b", text_lower)
        ]

        total_supporting_tech = list(dict.fromkeys(matched_anchors + matched_related))

        # Check contextual actions in CV
        matched_actions = [
            kw for kw in action_keywords
            if kw in all_actions or re.search(r"(?i)\b" + re.escape(kw) + r"\b", text_lower)
        ]

        # Validation Rule: Must have at least min_total technological evidence pieces
        # or (min_total - 1) evidence pieces PLUS at least 1 explicit action verb/keyword
        has_sufficient_tech = len(total_supporting_tech) >= min_total
        has_tech_and_action = (len(total_supporting_tech) >= (min_total - 1)) and (len(matched_actions) > 0)

        if not (has_sufficient_tech or has_tech_and_action):
            continue

        # Check negative constraint check
        speculative = False
        if cap_name in PROHIBITED_INFERENCES:
            prohibited_set = set(PROHIBITED_INFERENCES[cap_name]["prohibited_if_only"])
            if set(total_supporting_tech).issubset(prohibited_set):
                speculative = True
        if speculative:
            continue

        # Calculate explainable inference confidence:
        # 1. Evidence ratio (support count vs target) -> up to 0.50
        # 2. Anchor strength (presence of 1+ primary anchors) -> 0.30
        # 3. Action contextual confirmation -> 0.15
        # Max confidence capped at 0.96 (distinguishable from 1.0 explicit certainty)
        tech_ratio = min(len(total_supporting_tech) / (min_total + 1), 1.0)
        conf_tech = 0.50 * tech_ratio
        conf_anchor = 0.30 if len(matched_anchors) >= 1 else 0.15
        conf_action = min(len(matched_actions) * 0.05, 0.15)
        raw_conf = conf_tech + conf_anchor + conf_action
        inference_conf = round(min(max(raw_conf, 0.65), 0.95), 2)

        # Retrieve source context snippet from evidence items
        source_snippets = []
        for item in evidence_items:
            item_skills = set(item.get("skills", []))
            if any(s in item_skills for s in total_supporting_tech):
                source_snippets.append(item.get("text", ""))

        source_context = " | ".join(source_snippets[:2]) if source_snippets else ""

        inferred_results.append({
            "skill": cap_name,
            "type": "inferred",
            "category": config.get("category", "Other"),
            "confidence": inference_conf,
            "evidence": total_supporting_tech,
            "action_evidence": matched_actions[:4],
            "source_context": source_context
        })

    # Sort inferred skills by confidence descending
    inferred_results.sort(key=lambda x: x["confidence"], reverse=True)
    return inferred_results
