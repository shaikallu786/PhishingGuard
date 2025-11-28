"""
Phishing Email Detection - Streamlit Web Application
A user-friendly interface for detecting phishing emails.
"""

import streamlit as st
import joblib
import os
import re
from pathlib import Path


def preprocess_text(text):
    """Clean and preprocess email text."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', 'URL', text)
    text = re.sub(r'\S+@\S+', 'EMAIL', text)
    text = re.sub(r'\d+', 'NUMBER', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


@st.cache_resource
def load_model():
    """Load the trained model (cached for performance)."""
    model_path = 'phishing_model.joblib'
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None


def classify_email(model, email_text):
    """Classify an email as phishing or legitimate."""
    processed_text = preprocess_text(email_text)
    prediction = model.predict([processed_text])[0]
    probabilities = model.predict_proba([processed_text])[0]
    
    return {
        'is_phishing': bool(prediction),
        'label': 'PHISHING' if prediction == 1 else 'LEGITIMATE',
        'confidence': float(max(probabilities)),
        'phishing_probability': float(probabilities[1]),
        'legitimate_probability': float(probabilities[0]),
    }


def train_model_if_needed():
    """Train the model if it doesn't exist."""
    import subprocess
    st.info("Training model... This may take a moment.")
    result = subprocess.run(['python', 'train_phishing.py'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        st.success("Model trained successfully!")
        st.rerun()
    else:
        st.error(f"Training failed: {result.stderr}")


def main():
    st.set_page_config(
        page_title="Phishing Email Detector",
        page_icon="🛡️",
        layout="centered"
    )
    
    st.title("🛡️ Phishing Email Detector")
    st.markdown("**Detect phishing emails using machine learning**")
    
    model = load_model()
    
    if model is None:
        st.warning("No trained model found. Please train the model first.")
        if st.button("🚀 Train Model", type="primary"):
            train_model_if_needed()
        st.stop()
    
    st.divider()
    
    tab1, tab2 = st.tabs(["📝 Paste Email", "📁 Upload File"])
    
    with tab1:
        email_text = st.text_area(
            "Enter email content to analyze:",
            height=200,
            placeholder="Paste the email text here..."
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
        with col2:
            if st.button("🧹 Clear", use_container_width=True):
                st.rerun()
        
        if analyze_button and email_text.strip():
            with st.spinner("Analyzing email..."):
                result = classify_email(model, email_text)
            
            display_result(result)
        elif analyze_button:
            st.warning("Please enter some email text to analyze.")
    
    with tab2:
        uploaded_file = st.file_uploader(
            "Upload an email file (.txt, .eml)",
            type=['txt', 'eml']
        )
        
        if uploaded_file is not None:
            email_content = uploaded_file.read().decode('utf-8')
            st.text_area("File content:", email_content, height=150, disabled=True)
            
            if st.button("🔍 Analyze File", type="primary"):
                with st.spinner("Analyzing email..."):
                    result = classify_email(model, email_content)
                
                display_result(result)
    
    st.divider()
    
    with st.expander("📋 Example Emails"):
        st.markdown("**Try these example emails:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Phishing Example:**")
            phishing_example = "URGENT: Your account has been compromised! Click here immediately to verify your identity. Enter your password now to secure your account."
            st.code(phishing_example, language=None)
        
        with col2:
            st.markdown("**Legitimate Example:**")
            legitimate_example = "Hi team, just a reminder about our weekly meeting tomorrow at 10 AM. Please review the agenda I sent earlier."
            st.code(legitimate_example, language=None)
    
    with st.expander("ℹ️ About"):
        st.markdown("""
        ### How it works
        
        This application uses a **Machine Learning model** trained on thousands of emails 
        to detect phishing attempts. The model analyzes:
        
        - **Text patterns** commonly found in phishing emails
        - **Urgency indicators** (e.g., "URGENT", "immediately", "24 hours")
        - **Suspicious requests** for personal information
        - **URL patterns** and email addresses
        
        ### Tips to spot phishing emails:
        
        1. **Urgency** - Phishing emails often create a sense of urgency
        2. **Suspicious links** - Hover over links to see the actual URL
        3. **Grammar errors** - Many phishing emails contain spelling/grammar mistakes
        4. **Requests for personal info** - Legitimate companies rarely ask for passwords via email
        5. **Generic greetings** - "Dear Customer" instead of your name
        
        ### Disclaimer
        
        This tool provides an automated assessment and should be used as a **guide**, 
        not as a definitive security measure. Always exercise caution with suspicious emails.
        """)
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
        "Phishing Email Detector | Powered by Machine Learning"
        "</div>",
        unsafe_allow_html=True
    )


def display_result(result):
    """Display the classification result with styling."""
    st.divider()
    
    if result['is_phishing']:
        st.error("⚠️ **PHISHING DETECTED**")
        st.markdown("""
        <div style='background-color: #ffebee; padding: 15px; border-radius: 10px; border-left: 5px solid #f44336;'>
            <h3 style='color: #c62828; margin: 0;'>Warning: This email appears to be a phishing attempt!</h3>
            <p style='color: #b71c1c; margin-top: 10px;'>
                <strong>Do not:</strong>
                <ul>
                    <li>Click any links in this email</li>
                    <li>Download any attachments</li>
                    <li>Reply with personal information</li>
                    <li>Provide passwords or financial details</li>
                </ul>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ **EMAIL APPEARS LEGITIMATE**")
        st.markdown("""
        <div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px; border-left: 5px solid #4caf50;'>
            <h3 style='color: #2e7d32; margin: 0;'>This email appears to be safe</h3>
            <p style='color: #1b5e20; margin-top: 10px;'>
                The content does not match known phishing patterns. 
                However, always exercise caution with emails from unknown senders.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Confidence Scores")
    
    col1, col2 = st.columns(2)
    
    with col1:
        phishing_pct = result['phishing_probability'] * 100
        st.metric(
            label="Phishing Probability",
            value=f"{phishing_pct:.1f}%",
            delta=None
        )
        st.progress(result['phishing_probability'])
    
    with col2:
        legit_pct = result['legitimate_probability'] * 100
        st.metric(
            label="Legitimate Probability", 
            value=f"{legit_pct:.1f}%",
            delta=None
        )
        st.progress(result['legitimate_probability'])
    
    st.info(f"**Overall Confidence:** {result['confidence']*100:.1f}%")


if __name__ == "__main__":
    main()
