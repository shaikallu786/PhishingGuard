"""
Phishing Email Detection - Model Training Script
Trains a machine learning model to classify emails as phishing or legitimate.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os
import re


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


def get_sample_dataset():
    """
    Create a sample dataset for training.
    In production, replace this with a larger dataset from the dataset/ folder.
    """
    phishing_emails = [
        "URGENT: Your account has been compromised! Click here immediately to verify your identity and secure your account. Enter your password now.",
        "Congratulations! You've won $1,000,000 in the lottery. Click the link to claim your prize. Provide your bank details for transfer.",
        "Dear Customer, Your PayPal account has been limited. Please verify your information by clicking the link below to restore access.",
        "WARNING: Unusual activity detected on your bank account. Click here to confirm your identity or your account will be suspended.",
        "You have received a secure document. Click here to view it. Enter your email password to access.",
        "Your Apple ID was used to sign in to iCloud. If this wasn't you, click here immediately to secure your account.",
        "Final Notice: Your account will be closed in 24 hours unless you verify your information now. Click here to avoid suspension.",
        "Dear valued customer, we detected unauthorized access to your account. Verify your credentials immediately.",
        "You have been selected for a special promotion! Claim your free iPhone by clicking this link and entering your details.",
        "ALERT: Your Netflix subscription has expired. Update your payment information now to continue watching.",
        "Urgent security update required for your Microsoft account. Click here and enter your password to proceed.",
        "Your Amazon order #12345 cannot be delivered. Click here to update your shipping address and payment method.",
        "IMPORTANT: Tax refund of $3,500 available. Click here to claim before deadline. Enter your SSN to verify.",
        "Your Facebook account has been reported for violation. Verify your identity or face permanent suspension.",
        "Exclusive offer: Get rich quick with our investment program. Send money now and double your earnings!",
        "Dear user, your email storage is full. Click here to upgrade and enter your login credentials.",
        "You have a pending inheritance of $5 million. Reply with your bank details to process the transfer.",
        "Security Alert: Someone tried to access your Google account. Click here to change your password immediately.",
        "Congratulations winner! You've been selected for our giveaway. Claim your prize by providing personal information.",
        "Your Chase account requires immediate attention. Log in through this link to avoid account closure.",
    ]
    
    legitimate_emails = [
        "Hi team, just a reminder about our weekly meeting tomorrow at 10 AM. Please review the agenda I sent earlier.",
        "Thank you for your order! Your package has been shipped and will arrive within 3-5 business days. Tracking number: ABC123.",
        "Dear colleague, I've attached the quarterly report for your review. Let me know if you have any questions.",
        "Meeting notes from yesterday's discussion. Action items are listed at the bottom. Please confirm your tasks.",
        "Happy birthday! Wishing you a wonderful day filled with joy and celebration. Hope to see you at the party!",
        "Hi, I wanted to follow up on our conversation about the project deadline. Can we schedule a call this week?",
        "Your monthly statement is now available. You can view it by logging into your account through our official app.",
        "Team update: We've successfully completed the first phase of the project. Great work everyone!",
        "Reminder: The office will be closed on Monday for the holiday. Enjoy the long weekend!",
        "Hi, thanks for connecting at the conference. I'd love to discuss potential collaboration opportunities.",
        "Your subscription renewal is coming up. You can manage your preferences in your account settings.",
        "Please find attached the invoice for last month's services. Payment is due within 30 days.",
        "Just wanted to check in and see how you're doing. Let's catch up over coffee sometime.",
        "The new company policy document is now available on the intranet. Please review at your convenience.",
        "Thank you for your feedback! We appreciate your input and will use it to improve our services.",
        "Hi, here are the meeting minutes from our last discussion. Please let me know if I missed anything.",
        "Your flight confirmation for next week. Please arrive at the airport 2 hours before departure.",
        "Project status update: We're on track to meet the deadline. Attached is the progress report.",
        "Welcome to our newsletter! Here's what's happening this month in our community.",
        "Friendly reminder about the upcoming training session next Tuesday. Please register if you haven't already.",
    ]
    
    emails = phishing_emails + legitimate_emails
    labels = [1] * len(phishing_emails) + [0] * len(legitimate_emails)
    
    df = pd.DataFrame({'text': emails, 'label': labels})
    return df


def load_dataset(dataset_path=None):
    """
    Load dataset from file or use sample data.
    
    Expected CSV format:
    text,label
    "email content",1  (for phishing)
    "email content",0  (for legitimate)
    """
    if dataset_path and os.path.exists(dataset_path):
        print(f"Loading dataset from {dataset_path}")
        df = pd.read_csv(dataset_path)
        if 'text' not in df.columns or 'label' not in df.columns:
            raise ValueError("Dataset must have 'text' and 'label' columns")
        return df
    else:
        print("Using sample dataset for training...")
        return get_sample_dataset()


def train_model(df, test_size=0.2, random_state=42):
    """Train the phishing detection model."""
    df['processed_text'] = df['text'].apply(preprocess_text)
    
    X = df['processed_text']
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=1,
            max_df=0.95
        )),
        ('classifier', MultinomialNB(alpha=0.1))
    ])
    
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    y_pred = pipeline.predict(X_test)
    
    print("\n" + "="*50)
    print("MODEL EVALUATION")
    print("="*50)
    print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, 
                                target_names=['Legitimate', 'Phishing']))
    print(f"\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    return pipeline


def save_model(model, model_path='phishing_model.joblib'):
    """Save the trained model to disk."""
    joblib.dump(model, model_path)
    print(f"\nModel saved to {model_path}")


def main():
    """Main training function."""
    print("="*50)
    print("PHISHING EMAIL DETECTION - MODEL TRAINING")
    print("="*50)
    
    dataset_path = 'dataset/emails.csv'
    df = load_dataset(dataset_path if os.path.exists(dataset_path) else None)
    
    print(f"\nDataset size: {len(df)} emails")
    print(f"Phishing emails: {sum(df['label'] == 1)}")
    print(f"Legitimate emails: {sum(df['label'] == 0)}")
    
    model = train_model(df)
    
    save_model(model)
    
    print("\n" + "="*50)
    print("Training complete!")
    print("="*50)


if __name__ == "__main__":
    main()
