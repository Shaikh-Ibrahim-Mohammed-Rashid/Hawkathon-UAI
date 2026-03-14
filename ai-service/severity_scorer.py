"""
GramCare AI — Severity Scorer
Scores symptom severity and determines triage level.
"""
import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


class SeverityScorer:
    def __init__(self):
        self.severity_map = {}
        self._load()

    def _load(self):
        path = os.path.join(MODEL_DIR, "severity_map.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                self.severity_map = json.load(f)

    def score(self, symptoms):
        """
        Calculate total severity score and triage level.
        Returns: {"score": int, "triage_level": str, "details": list}
        """
        total = 0
        details = []
        for s in symptoms:
            s_clean = s.strip().lower().replace(" ", "_")
            weight = self.severity_map.get(s_clean, 3)  # Default weight 3
            total += weight
            details.append({"symptom": s_clean, "weight": weight})

        if total <= 5:
            triage = "LOW"
        elif total <= 10:
            triage = "MEDIUM"
        else:
            triage = "HIGH"

        return {
            "score": total,
            "triage_level": triage,
            "details": details,
        }
