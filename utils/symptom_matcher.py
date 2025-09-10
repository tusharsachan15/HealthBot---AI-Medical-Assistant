import pandas as pd
import json
from difflib import SequenceMatcher

# -----------------------
# Load Medical Data (CSV)
# -----------------------
def load_medical_data(csv_path="data/medical_knowledge.csv"):
    """
    Load medical knowledge CSV containing:
    Disease, Symptoms, Description, Medicines, Consultation
    """
    try:
        df = pd.read_csv(csv_path)
        # Ensure Symptoms column is a list
        df['Symptoms'] = df['Symptoms'].apply(lambda x: [s.strip().lower() for s in str(x).split(",")])
        return df
    except Exception as e:
        print(f"Error loading medical data: {e}")
        return pd.DataFrame(columns=["Disease", "Symptoms", "Description", "Medicines", "Consultation"])

# -----------------------
# Load Doctors Data (JSON)
# -----------------------
def load_doctor_data(json_path="data/doctors.json"):
    """
    Load doctors JSON containing:
    [
        {"name":..., "specialty":..., "hospital":..., "contact":..., "diseases":[...]}
    ]
    """
    try:
        with open(json_path, "r") as f:
            doctors = json.load(f)
        return doctors
    except Exception as e:
        print(f"Error loading doctor data: {e}")
        return []

# -----------------------
# Symptom Matching
# -----------------------
def match_symptoms(user_input, medical_df, threshold=0.5):
    """
    Match user symptoms with diseases.
    Returns list of diseases with similarity above threshold.
    """
    user_symptoms = [s.strip().lower() for s in user_input.split(",")]
    matches = []

    for _, row in medical_df.iterrows():
        disease_symptoms = row["Symptoms"]
        # Compute match ratio
        matched_count = sum(1 for s in disease_symptoms if any(SequenceMatcher(None, s, u).ratio() > 0.6 for u in user_symptoms))
        score = matched_count / max(len(disease_symptoms), 1)
        if score >= threshold:
            matches.append({
                "Disease": row["Disease"],
                "Description": row["Description"],
                "Medicines": row["Medicines"],
                "Consultation": row["Consultation"],
                "Score": score
            })

    # Sort by score descending
    matches = sorted(matches, key=lambda x: x["Score"], reverse=True)
    return matches

# -----------------------
# Suggest Doctors
# -----------------------
def suggest_doctors(disease_name, doctors):
    """
    Return all doctors who handle the given disease.
    """
    matching_doctors = []
    for doc in doctors:
        if "diseases" in doc and disease_name.lower() in [d.lower() for d in doc["diseases"]]:
            matching_doctors.append(doc)
    return matching_doctors
