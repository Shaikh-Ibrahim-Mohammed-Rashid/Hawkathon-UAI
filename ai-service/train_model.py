"""
GramCare AI — Model Training Script
Trains an ensemble (Random Forest + Gradient Boosting) symptom-disease classifier.
Run: python train_model.py
"""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "..", "datasets")
MODEL_DIR = os.path.join(BASE_DIR, "models")


def load_and_preprocess():
    """Load dataset.csv, clean symptoms, and create binary feature matrix."""
    print("📂 Loading dataset...")
    df = pd.read_csv(os.path.join(DATASET_DIR, "dataset.csv"))

    # Melt symptom columns into a list per row
    symptom_cols = [c for c in df.columns if c.startswith("Symptom")]
    all_symptoms = set()
    for col in symptom_cols:
        df[col] = df[col].str.strip().str.replace(" ", "")
        unique = df[col].dropna().unique()
        all_symptoms.update(unique)

    all_symptoms.discard("")
    all_symptoms = sorted(all_symptoms)
    print(f"   Found {len(all_symptoms)} unique symptoms, {df['Disease'].nunique()} diseases.")

    # Create binary feature matrix
    symptom_to_idx = {s: i for i, s in enumerate(all_symptoms)}
    X = np.zeros((len(df), len(all_symptoms)), dtype=np.int8)

    for row_idx, row in df.iterrows():
        for col in symptom_cols:
            val = row[col]
            if pd.notna(val):
                val = val.strip().replace(" ", "")
                if val in symptom_to_idx:
                    X[row_idx, symptom_to_idx[val]] = 1

    # Encode disease labels
    le = LabelEncoder()
    y = le.fit_transform(df["Disease"])

    return X, y, all_symptoms, le


def train():
    os.makedirs(MODEL_DIR, exist_ok=True)
    X, y, symptoms, label_encoder = load_and_preprocess()

    print(f"\n🧪 Dataset shape: X={X.shape}, y={y.shape}")
    print(f"   Classes: {len(label_encoder.classes_)}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Model 1: Random Forest
    print("\n🌲 Training Random Forest...")
    rf = RandomForestClassifier(
        n_estimators=200, max_depth=30, class_weight="balanced",
        random_state=42, n_jobs=-1,
    )

    # Model 2: Gradient Boosting
    print("🚀 Training Gradient Boosting...")
    gb = GradientBoostingClassifier(
        n_estimators=150, max_depth=10, learning_rate=0.1, random_state=42,
    )

    # Ensemble: Soft Voting
    print("🤝 Building Ensemble (Soft Voting)...")
    ensemble = VotingClassifier(
        estimators=[("rf", rf), ("gb", gb)],
        voting="soft",
    )
    ensemble.fit(X_train, y_train)

    # Evaluate
    y_pred = ensemble.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n📊 Test Accuracy: {accuracy:.4f}")

    cv_scores = cross_val_score(ensemble.estimators_[0][1].fit(X_train, y_train),
                                X, y, cv=5, scoring="accuracy")
    print(f"   5-Fold CV (RF only): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Save models and metadata
    print("\n💾 Saving models...")
    joblib.dump(ensemble, os.path.join(MODEL_DIR, "ensemble_model.pkl"))
    joblib.dump(label_encoder, os.path.join(MODEL_DIR, "label_encoder.pkl"))

    # Save symptom list
    with open(os.path.join(MODEL_DIR, "symptoms.json"), "w") as f:
        json.dump(symptoms, f, indent=2)

    # Save disease descriptions and precautions
    _save_disease_info()

    # Save severity map
    _save_severity_map()

    print("✅ Model training complete!")
    print(f"   Model saved to: {MODEL_DIR}")
    print(f"   Accuracy: {accuracy:.2%}")

    return accuracy


def _save_disease_info():
    """Load disease descriptions and precautions from CSV files."""
    desc_path = os.path.join(DATASET_DIR, "symptom_Description.csv")
    prec_path = os.path.join(DATASET_DIR, "symptom_precaution.csv")
    info = {}

    if os.path.exists(desc_path):
        df_desc = pd.read_csv(desc_path)
        for _, row in df_desc.iterrows():
            disease = row.iloc[0]
            desc = row.iloc[1] if len(row) > 1 else ""
            info[disease] = {"description": str(desc), "precautions": []}

    if os.path.exists(prec_path):
        df_prec = pd.read_csv(prec_path)
        for _, row in df_prec.iterrows():
            disease = row.iloc[0]
            precs = [str(row.iloc[i]) for i in range(1, min(5, len(row))) if pd.notna(row.iloc[i])]
            if disease in info:
                info[disease]["precautions"] = precs
            else:
                info[disease] = {"description": "", "precautions": precs}

    with open(os.path.join(MODEL_DIR, "disease_info.json"), "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2, ensure_ascii=False)

    print(f"   Saved disease info for {len(info)} diseases.")


def _save_severity_map():
    """Load symptom severity weights from CSV."""
    sev_path = os.path.join(DATASET_DIR, "Symptom-severity.csv")
    severity = {}

    if os.path.exists(sev_path):
        df = pd.read_csv(sev_path)
        for _, row in df.iterrows():
            symptom = str(row.iloc[0]).strip().replace(" ", "")
            weight = int(row.iloc[1]) if pd.notna(row.iloc[1]) else 3
            severity[symptom] = weight

    with open(os.path.join(MODEL_DIR, "severity_map.json"), "w") as f:
        json.dump(severity, f, indent=2)

    print(f"   Saved severity weights for {len(severity)} symptoms.")


if __name__ == "__main__":
    train()
