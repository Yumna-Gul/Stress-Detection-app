import streamlit as st
import numpy as np
import re
from scipy.sparse import hstack, csr_matrix
import pickle

# Configure page for better performance
st.set_page_config(
    page_title="Stress Detection",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache models to prevent reloading
@st.cache_resource
def load_models():
    with open("final_models.pkl", "rb") as f:
        final_models = pickle.load(f)
    with open("tfidf.pkl", "rb") as f:
        tfidf = pickle.load(f)
    with open("X_train_num_scaled.pkl", "rb") as f:
        X_train_num_scaled = pickle.load(f)
    return final_models, tfidf, X_train_num_scaled

final_models, tfidf, X_train_num_scaled = load_models()

@st.cache_data
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
            results[name] = {
                "Prediction": "Stressed" if pred == 1 else "Not Stressed",
                "Probability": round(prob, 3),
                "Confidence": round(max(prob, 1-prob) * 100, 1)
            }
        else:
            results[name] = {
                "Prediction": "Stressed" if pred == 1 else "Not Stressed",
                "Probability": None,
                "Confidence": None
            }
    return results

# Custom CSS for styling
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .stMetric { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation and info
with st.sidebar:
    st.title("⚙️ Settings")
    page = st.radio("Navigate", ["🏠 Home", "📊 Analysis", "ℹ️ About"])
    st.markdown("---")
    st.info("💡 **Tip**: Keep this app open to avoid sleep timeout!\nFor best experience, use paid Streamlit Cloud or self-hosted deployment.")

if page == "🏠 Home":
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🧠 Stress Detection System")
        st.subheader("AI-Powered Mental Health Analysis")
    
    st.markdown("---")
    
    # Input section
    col1, col2 = st.columns([2, 1])
    with col1:
        user_input = st.text_area(
            "📝 Share your thoughts or feelings:",
            height=120,
            placeholder="Type something that's on your mind...",
            help="The more detailed, the better the prediction"
        )
        char_count = len(user_input)
        st.caption(f"Characters: {char_count} | Recommended: 20-500")
    
    with col2:
        st.metric("Input Length", f"{char_count}", delta="chars")
    
    st.markdown("---")
    
    # Prediction button
    col1, col2, col3 = st.columns(3)
    with col2:
        predict_btn = st.button("🔍 Analyze Now", use_container_width=True, key="predict")
    
    # Results display
    if predict_btn:
        if user_input.strip() == "":
            st.warning("⚠️ Please enter some text to analyze!")
        else:
            with st.spinner("🤔 Analyzing your text..."):
                results = predict_stress(user_input)
            
            st.success("✅ Analysis Complete!")
            st.markdown("---")
            
            # Display results with better visualization
            st.subheader("📈 Results")
            
            for idx, (model_name, output) in enumerate(results.items()):
                with st.container():
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**{model_name}**")
                        
                        # Status indicator
                        if output['Prediction'] == "Stressed":
                            st.error(f"🔴 {output['Prediction']}")
                        else:
                            st.success(f"🟢 {output['Prediction']}")
                    
                    with col2:
                        if output["Confidence"] is not None:
                            st.metric("Confidence", f"{output['Confidence']}%")
                    
                    # Probability bar
                    if output["Probability"] is not None:
                        progress_val = output["Probability"]
                        st.progress(progress_val, text=f"Stress Probability: {output['Probability']*100:.1f}%")
                    
                    st.markdown("---")
            
            # Store in session history
            if "history" not in st.session_state:
                st.session_state.history = []
            
            st.session_state.history.append({
                "text": user_input[:50] + "..." if len(user_input) > 50 else user_input,
                "results": results
            })

elif page == "📊 Analysis":
    st.title("📊 Analysis History")
    
    if "history" in st.session_state and len(st.session_state.history) > 0:
        st.info(f"Total analyses: {len(st.session_state.history)}")
        
        for idx, item in enumerate(reversed(st.session_state.history[-10:])):
            with st.expander(f"Analysis #{len(st.session_state.history) - idx}"):
                st.write(f"**Input:** {item['text']}")
                
                for model_name, output in item['results'].items():
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**{model_name}**")
                    with col2:
                        st.write(output['Prediction'])
                    with col3:
                        if output['Confidence']:
                            st.write(f"{output['Confidence']}%")
    else:
        st.info("No analysis history yet. Start by analyzing some text!")

elif page == "ℹ️ About":
    st.title("ℹ️ About This App")
    
    st.markdown("""
    ### What is Stress Detection?
    This AI-powered application analyzes text to detect potential stress levels based on linguistic patterns.
    
    ### How it Works
    - **Text Processing**: Your input is cleaned and normalized
    - **Feature Extraction**: TF-IDF and other features are extracted
    - **Model Prediction**: Multiple ML models vote on stress prediction
    - **Confidence Score**: Probability indicates prediction confidence
    
    ### Models Used
    - Logistic Regression
    - And other ensemble methods
    
    ### Important Notes
    - This is for **informational purposes only**
    - Not a medical diagnosis tool
    - Always consult professionals for mental health concerns
    
    ### Deployment Issues & Solutions
    
    #### App Going to Sleep?
    **Problem**: Free Streamlit Cloud spins down after 1 hour of inactivity
    
    **Solutions**:
    1. **Upgrade to Streamlit Community Cloud Pro** (recommended, $5-30/month)
    2. **Use Alternative Hosting**:
       - PythonAnywhere (free tier available)
       - DigitalOcean App Platform ($6-12/month)
       - Hugging Face Spaces (free, no sleep)
       - Render.com (free tier available)
       - AWS/Google Cloud (pay-as-you-go)
    3. **Keep-Alive Service**: Use UptimeRobot (free) to ping your app every 5 mins
    
    #### Performance Issues?
    - ✅ Already implemented: Model caching with @st.cache_resource
    - ✅ Better UI with visualizations
    - ✅ Session state for history tracking
    
    """)
    
    st.info("""
    🚀 **Recommended**: Deploy on **Hugging Face Spaces** for free without sleep limits!
    - No pay required
    - Apps stay always-on
    - Fast deployment from GitHub
    """)

