"""
GramCare AI — Symptom Checker
Loads trained ML model and provides disease predictions from symptoms.
"""
import os
import json
import numpy as np
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


class SymptomChecker:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.symptoms = []
        self.symptom_to_idx = {}
        self.disease_info = {}
        self._load()

    def _load(self):
        model_path = os.path.join(MODEL_DIR, "ensemble_model.pkl")
        le_path = os.path.join(MODEL_DIR, "label_encoder.pkl")
        symptoms_path = os.path.join(MODEL_DIR, "symptoms.json")
        info_path = os.path.join(MODEL_DIR, "disease_info.json")

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                "Model not found. Run 'python train_model.py' first."
            )

        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load(le_path)

        with open(symptoms_path, "r") as f:
            self.symptoms = json.load(f)
        self.symptom_to_idx = {s: i for i, s in enumerate(self.symptoms)}

        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                self.disease_info = json.load(f)

    def predict(self, symptoms_input, top_k=5):
        """
        Predict diseases from a list of symptom strings.
        Returns top_k predictions with confidence, description, and precautions.
        """
        # Normalize input symptoms
        normalized = []
        for s in symptoms_input:
            s_clean = s.strip().lower().replace(" ", "_")
            normalized.append(s_clean)

        # Build feature vector
        feature_vector = np.zeros((1, len(self.symptoms)), dtype=np.int8)
        matched = []
        for s in normalized:
            if s in self.symptom_to_idx:
                feature_vector[0, self.symptom_to_idx[s]] = 1
                matched.append(s)
            else:
                # Fuzzy match: check if symptom string is contained in any known symptom
                for known in self.symptoms:
                    if s in known or known in s:
                        feature_vector[0, self.symptom_to_idx[known]] = 1
                        matched.append(known)
                        break

        if not matched:
            return [{
                "disease": "Unknown",
                "confidence": 0.0,
                "description": "Could not match any symptoms. Please try different symptom names.",
                "precautions": ["Consult a doctor for proper diagnosis"],
                "recommendation": "CONSULT_DOCTOR",
            }]

        # Predict probabilities
        probas = self.model.predict_proba(feature_vector)[0]
        top_indices = np.argsort(probas)[::-1][:top_k]

        predictions = []
        for idx in top_indices:
            if probas[idx] < 0.01:
                continue
            disease = self.label_encoder.inverse_transform([idx])[0]
            info = self.disease_info.get(disease, {})

            confidence = float(probas[idx])
            if confidence > 0.7:
                recommendation = "VISIT_HOSPITAL"
            elif confidence > 0.4:
                recommendation = "TELECONSULT"
            else:
                recommendation = "SELF_CARE"

            predictions.append({
                "disease": disease,
                "confidence": round(confidence, 4),
                "description": info.get("description", ""),
                "precautions": info.get("precautions", []),
                "recommendation": recommendation,
            })

        return predictions if predictions else [{
            "disease": "Inconclusive",
            "confidence": 0.0,
            "description": "The symptoms provided are not conclusive enough.",
            "precautions": ["Please consult a doctor for proper diagnosis"],
            "recommendation": "CONSULT_DOCTOR",
        }]

    def get_symptom_list(self):
        """Return all known symptoms as a list of strings."""
        return self.symptoms

    def get_disease_list(self):
        """Return all known diseases."""
        return list(self.label_encoder.classes_)
