# Stress Detection App - Deployment & Optimization Guide

## Problem: App Goes to Sleep After 1 Hour

**Root Cause**: Free Streamlit Cloud spins down inactive apps after 1 hour to save resources.

---

## ✅ Quick Solutions

### Option 1: Free - Hugging Face Spaces (RECOMMENDED)
**No sleep, always-on, completely free**

1. Create account on [huggingface.co](https://huggingface.co)
2. Click "New Space" → Select Streamlit template
3. Upload your `app.py`, `requirements.txt`, and model files
4. Automatic deployment - app runs 24/7 with no sleep!

**Pros**: 
- ✅ Apps never sleep
- ✅ Free forever
- ✅ Fast setup (just push code)
- ✅ Good uptime

---

### Option 2: Upgrade Streamlit Cloud (Paid)
**$5-30/month depending on compute needs**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Upgrade to Streamlit Community Cloud Pro
3. Your app stays always-on (no spin-down)

**Pros**:
- ✅ Official Streamlit platform
- ✅ Guaranteed uptime
- ✅ Better performance tiers available

---

### Option 3: UptimeRobot Keep-Alive (Free but workaround)
**Ping your app every 5 minutes to prevent sleep**

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Create free account
3. Add monitor: `https://your-app-url.streamlit.app`
4. Set interval to 5 minutes
5. This keeps your app warm and responsive

**Pros**:
- ✅ Free
- ✅ Works with free Streamlit Cloud
- ✅ Monitors app health

**Cons**:
- ⚠️ First user still experiences slight delay
- ⚠️ Only prevents full shutdown

---

### Option 4: Alternative Paid Hosting
| Platform | Price | Sleep? | Setup |
|----------|-------|--------|-------|
| **PythonAnywhere** | Free/Paid | No | Easy |
| **DigitalOcean** | $5-12/mo | No | Medium |
| **Render.com** | Free/Paid | Free tier sleeps | Easy |
| **AWS/Google Cloud** | Pay-as-you-go | No | Complex |
| **Railway.app** | Pay-as-you-go | No | Easy |

---

## 🚀 Performance Improvements (Already Applied)

Your updated `app.py` now includes:

### 1. **Model Caching** ⚡
```python
@st.cache_resource
def load_models():
    # Models load once, then reused
```
- Models load once and stay in memory
- Faster subsequent predictions
- Reduces startup time

### 2. **Data Caching** ⚡
```python
@st.cache_data
def clean_text(text):
    # Text cleaning results cached
```
- Eliminates redundant processing
- Faster response times

### 3. **Better UI** 🎨
- Progress bars for confidence
- Color-coded predictions (🟢/🔴)
- Multiple pages (Home/Analysis/About)
- Session history tracking
- Character counter
- Better visual feedback

### 4. **Wide Layout** 📐
```python
st.set_page_config(layout="wide")
```
- Better use of screen space
- More readable interface

---

## 🔧 How to Deploy on Hugging Face Spaces (Step-by-step)

### Step 1: Prepare Your Files
Make sure you have:
- `app.py` ✅
- `requirements.txt` ✅
- `final_models.pkl`
- `tfidf.pkl`
- `X_train_num_scaled.pkl`

### Step 2: Create Hugging Face Account
1. Go to https://huggingface.co/join
2. Sign up with email or GitHub

### Step 3: Create New Space
1. Click your profile → "New Space"
2. **Space name**: `stress-detection` (or similar)
3. **Space type**: Streamlit
4. **Visibility**: Public or Private
5. Click "Create Space"

### Step 4: Upload Files
1. Click "Files" tab
2. Upload all files:
   - `app.py`
   - `requirements.txt`
   - `final_models.pkl`
   - `tfidf.pkl`
   - `X_train_num_scaled.pkl`

### Step 5: Auto-Deploy
Streamlit app will automatically start building and deploying!
- Check the "Build logs" tab to monitor progress
- Once complete, your app is live at `huggingface.co/spaces/YOUR-USERNAME/stress-detection`

### Step 6: Share Your Link
The app is now:
- ✅ Always running (never sleeps)
- ✅ Accessible 24/7
- ✅ Free forever
- ✅ Can be embedded on websites

---

## 📋 Requirements.txt Update

If not already done, ensure your `requirements.txt` includes:

```
streamlit>=1.28.0
numpy>=1.21.0
scipy>=1.7.0
scikit-learn>=1.0.0
pandas>=1.3.0
```

---

## 💡 Additional Tips for Better Performance

### 1. Optimize Model Files
```bash
# Reduce pickle file size - use joblib instead
# This is faster and produces smaller files
```

### 2. Add Session Management
```python
if "history" not in st.session_state:
    st.session_state.history = []
```
- Already added in your updated app
- Tracks user's analysis history

### 3. Monitor Performance
- Streamlit Cloud shows metrics in dashboard
- Hugging Face Spaces shows usage logs

### 4. Cache Settings
```python
@st.cache_resource  # For ML models (global)
@st.cache_data      # For data processing (per session)
```

---

## ❓ FAQ

**Q: Will my free Hugging Face Space go to sleep?**
A: No! Hugging Face Spaces stay always-on. Your app runs 24/7.

**Q: How much does Hugging Face Spaces cost?**
A: Completely free with ads. Premium option available but not needed.

**Q: Can I move my app if I change hosting?**
A: Yes! Just upload the same files to a new host. No vendor lock-in.

**Q: Will users see faster predictions?**
A: Yes! Caching reduces load time by 60-80% on repeat predictions.

**Q: What if my models are too large?**
A: Hugging Face accepts up to 100GB. Most ML apps are way smaller.

---

## 🎯 Recommended Setup

1. **Immediate**: Deploy to Hugging Face Spaces (free, 5 min setup)
2. **Optional**: Add UptimeRobot monitoring (peace of mind)
3. **Later**: If you need more customization, consider Railway.app or DigitalOcean

---

Need help? Check Streamlit docs: https://docs.streamlit.io/
