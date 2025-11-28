# Phishing Email Detector

## Overview
A machine learning-based phishing email detection system built with Python and Streamlit. The application classifies emails as either phishing or legitimate using a trained ML model.

## Project Structure
```
phishing-detector/
├── train_phishing.py        # Model training script
├── classify_email.py        # Command-line classification tool
├── app_streamlit.py         # Streamlit web interface
├── phishing_model.joblib    # Trained model (auto-generated)
└── dataset/                 # Dataset folder for custom training data
    └── README.md
```

## Components

### train_phishing.py
- Trains a Naive Bayes classifier using TF-IDF vectorization
- Uses a sample dataset of 40 emails (20 phishing, 20 legitimate)
- Can load custom datasets from `dataset/emails.csv`
- Outputs model metrics and saves to `phishing_model.joblib`

### classify_email.py
- Command-line tool for email classification
- Supports: direct text input, file input, interactive mode
- Usage: `python classify_email.py "email text"` or `python classify_email.py --interactive`

### app_streamlit.py
- Web interface for phishing detection
- Features: paste email text, upload email files
- Displays confidence scores and detailed warnings

## Running the Application
```bash
# Train the model (first time)
python train_phishing.py

# Run the web app
streamlit run app_streamlit.py --server.port 5000

# Or use CLI classifier
python classify_email.py "Your email text here"
```

## Technical Stack
- Python 3.11
- Streamlit (web interface)
- scikit-learn (ML model)
- pandas, numpy (data processing)
- joblib (model persistence)

## Recent Changes
- November 28, 2025: Initial project setup with complete phishing detection system
