
# Stress Detection App

A machine learning & Streamlit app that detects whether a person is stressed based on their text input.  
The app uses **Logistic Regression** and **K-Nearest Neighbors (KNN)** models with **TF-IDF** text features and numeric scaling.

---

## Features

- Predicts **Stressed** or **Not Stressed** from text input
- Uses **Logistic Regression** and **KNN** models
- Interactive web interface built with **Streamlit**
- Easily extensible for new models or features

---

## Demo

You can try the app live here:  
[Streamlit App Link](https://stress-detection-app-mujpcqwlwugyqzkax5cufh.streamlit.app/)

---

## Installation (Local)

1. Clone the repository:

```bash
git clone https://github.com/Yumna-Gul/Stress-Detection-app.git
cd Stress-Detection-app

Usage

Enter your text in the input box

Select the model (Logistic Regression / KNN)

Get prediction (Stressed or Not Stressed) and probability

Project Structure
app.py                 # Main Streamlit app
final_models.pkl       # Saved trained ML models
tfidf.pkl              # Saved TF-IDF vectorizer
X_train_num_scaled.pkl # Scaled numeric features
requirements.txt       # Python packages
README.md              # Project description

Technologies Used

Python 3.x

Streamlit

scikit-learn

pandas & numpy

matplotlib & seaborn
