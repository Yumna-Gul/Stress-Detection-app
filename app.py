import streamlit as st
import numpy as np
import re
from scipy.sparse import hstack, csr_matrix
import pickle

# Load trained models and preprocessing
with open("final_models.pkl", "rb") as f:
    final_models = pickle.load(f)

with open("tfidf.pkl", "rb") as f:
    tfidf = pickle.load(f)

with open("X_train_num_scaled.pkl", "rb") as f:
    X_train_num_scaled = pickle.load(f)

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#[A-Za-z0-9_]+", "", text)
    text = re.sub(r"[^a-z0-9\s']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def predict_stress(text):
    text_clean = clean_text(text)
    text_vec = tfidf.transform([text_clean])
    avg_num = csr_matrix(X_train_num_scaled.mean(axis=0))
    final_vec = hstack([text_vec, avg_num])

    results = {}
    for name, model in final_models.items():
        pred = model.predict(final_vec)[0]
        if name == "Logistic Regression":
            prob = model.predict_proba(final_vec)[0][1]
            results[name] = {"Prediction": "Stressed" if pred==1 else "Not Stressed",
                             "Probability": round(prob,3)}
        else:
            results[name] = {"Prediction": "Stressed" if pred==1 else "Not Stressed",
                             "Probability": None}
    return results

# Streamlit UI
st.title("🧠 Stress Detection App")
st.write("Enter text to predict stress:")

user_input = st.text_area("Type your text here:")

if st.button("Predict"):
    if user_input.strip() == "":
        st.warning("Please enter some text to predict!")
    else:
        results = predict_stress(user_input)
        for model_name, output in results.items():
            st.subheader(model_name)
            st.write(f"Prediction: {output['Prediction']}")
            if output["Probability"] is not None:
                st.write(f"Probability: {output['Probability']}")
