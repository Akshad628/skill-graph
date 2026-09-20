import pytest
from hidden_skill_inference import infer_hidden_skills
from skill_extractor import extract_skills_and_evidence

class TestHiddenSkillInference:
    """Evaluation suite testing evidence-based capability discovery and negative constraints."""

    def test_backend_development_inference(self):
        """Should infer Backend Development given FastAPI, PostgreSQL, and REST APIs with action evidence."""
        cv_text = "Built a FastAPI backend service with PostgreSQL and REST APIs."
        extracted = extract_skills_and_evidence(cv_text)
        inferred = infer_hidden_skills(
            extracted["explicit_skills"],
            extracted["evidence_items"],
            raw_text=cv_text
        )
        inferred_names = [item["skill"] for item in inferred]
        assert "Backend Development" in inferred_names
        
        backend_inf = next(item for item in inferred if item["skill"] == "Backend Development")
        assert backend_inf["type"] == "inferred"
        assert backend_inf["confidence"] >= 0.70
        assert "FastAPI" in backend_inf["evidence"]
        assert "PostgreSQL" in backend_inf["evidence"]
        assert len(backend_inf["evidence"]) >= 3

    def test_unsupervised_learning_inference(self):
        """Should infer Unsupervised Learning / Clustering from clustering evidence."""
        cv_text = "Implemented customer segmentation using K-Means and Scikit-learn with silhouette score analysis."
        extracted = extract_skills_and_evidence(cv_text)
        inferred = infer_hidden_skills(
            extracted["explicit_skills"],
            extracted["evidence_items"],
            raw_text=cv_text
        )
        inferred_names = [item["skill"] for item in inferred]
        assert "Unsupervised Learning / Clustering" in inferred_names
        
        cluster_inf = next(item for item in inferred if item["skill"] == "Unsupervised Learning / Clustering")
        assert "Scikit-learn" in cluster_inf["evidence"]
        assert cluster_inf["confidence"] >= 0.70

    def test_xr_vr_development_inference(self):
        """Should infer XR / VR Development from Unity, OpenXR, Meta Quest evidence."""
        cv_text = "Developed immersive simulation in Unity with OpenXR and Meta Quest integration."
        extracted = extract_skills_and_evidence(cv_text)
        inferred = infer_hidden_skills(
            extracted["explicit_skills"],
            extracted["evidence_items"],
            raw_text=cv_text
        )
        inferred_names = [item["skill"] for item in inferred]
        assert "XR / VR Development" in inferred_names
        xr_inf = next(item for item in inferred if item["skill"] == "XR / VR Development")
        assert "Unity" in xr_inf["evidence"] or "OpenXR" in xr_inf["evidence"]

    def test_negative_single_python_no_cybersecurity(self):
        """CRITICAL: Single technology (Python) must NOT infer Cybersecurity, AI Research, or Data Science."""
        cv_text = "I write Python scripts for basic file operations."
        extracted = extract_skills_and_evidence(cv_text)
        inferred = infer_hidden_skills(
            extracted["explicit_skills"],
            extracted["evidence_items"],
            raw_text=cv_text
        )
        inferred_names = [item["skill"] for item in inferred]
        assert "Cybersecurity" not in inferred_names
        assert "AI Research" not in inferred_names
        assert "Data Science" not in inferred_names
        assert "Backend Development" not in inferred_names  # Insufficient supporting evidence

    def test_no_crash_on_empty_or_sparse_cv(self):
        """Should handle empty or irrelevant text without throwing exceptions."""
        assert infer_hidden_skills([], [], "") == []
        assert infer_hidden_skills(["Nonexistent"], [], "Hello world") == []

    def test_traceability_schema(self):
        """Verifies each inferred skill contains valid traceability fields."""
        cv_text = "Engineered microservices using Docker, Kubernetes, and AWS deployment pipelines."
        extracted = extract_skills_and_evidence(cv_text)
        inferred = infer_hidden_skills(
            extracted["explicit_skills"],
            extracted["evidence_items"],
            raw_text=cv_text
        )
        for item in inferred:
            assert "skill" in item
            assert item["type"] == "inferred"
            assert 0.0 <= item["confidence"] <= 1.0
            assert isinstance(item["evidence"], list)
            assert len(item["evidence"]) > 0
            assert "source_context" in item
