"""
Phishing Email Detection - Classification Script
Loads the trained model and classifies emails as phishing or legitimate.
"""

import joblib
import os
import sys
import re


def preprocess_text(text):
    """Clean and preprocess email text (same as training)."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', 'URL', text)
    text = re.sub(r'\S+@\S+', 'EMAIL', text)
    text = re.sub(r'\d+', 'NUMBER', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def load_model(model_path='phishing_model.joblib'):
    """Load the trained model from disk."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at {model_path}. "
            "Please run train_phishing.py first to train the model."
        )
    return joblib.load(model_path)


def classify_email(model, email_text):
    """
    Classify an email as phishing or legitimate.
    
    Args:
        model: Trained sklearn pipeline
        email_text: Raw email text to classify
    
    Returns:
        dict with prediction results
    """
    processed_text = preprocess_text(email_text)
    
    prediction = model.predict([processed_text])[0]
    probabilities = model.predict_proba([processed_text])[0]
    
    result = {
        'is_phishing': bool(prediction),
        'label': 'PHISHING' if prediction == 1 else 'LEGITIMATE',
        'confidence': float(max(probabilities)),
        'phishing_probability': float(probabilities[1]),
        'legitimate_probability': float(probabilities[0]),
    }
    
    return result


def classify_from_file(model, file_path):
    """Classify email content from a file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        email_text = f.read()
    
    return classify_email(model, email_text)


def print_result(result, email_preview=None):
    """Pretty print classification result."""
    print("\n" + "="*50)
    print("CLASSIFICATION RESULT")
    print("="*50)
    
    if email_preview:
        preview = email_preview[:100] + "..." if len(email_preview) > 100 else email_preview
        print(f"\nEmail preview: {preview}")
    
    print(f"\nVerdict: {result['label']}")
    print(f"Confidence: {result['confidence']*100:.1f}%")
    print(f"\nProbability breakdown:")
    print(f"  - Phishing: {result['phishing_probability']*100:.1f}%")
    print(f"  - Legitimate: {result['legitimate_probability']*100:.1f}%")
    
    if result['is_phishing']:
        print("\n⚠️  WARNING: This email appears to be a phishing attempt!")
        print("   Do not click any links or provide personal information.")
    else:
        print("\n✓ This email appears to be legitimate.")
    
    print("="*50)


def interactive_mode(model):
    """Run in interactive mode for testing multiple emails."""
    print("\n" + "="*50)
    print("PHISHING EMAIL DETECTOR - Interactive Mode")
    print("="*50)
    print("\nEnter email text to classify (type 'quit' to exit):")
    print("(For multi-line input, enter an empty line when done)\n")
    
    while True:
        print("-" * 30)
        lines = []
        print("Enter email text:")
        
        while True:
            line = input()
            if line.lower() == 'quit':
                print("\nGoodbye!")
                return
            if line == "" and lines:
                break
            lines.append(line)
        
        email_text = "\n".join(lines)
        
        if email_text.strip():
            result = classify_email(model, email_text)
            print_result(result, email_text)


def main():
    """Main function for command-line usage."""
    model_path = 'phishing_model.joblib'
    
    try:
        model = load_model(model_path)
        print(f"Model loaded from {model_path}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        input_arg = sys.argv[1]
        
        if input_arg == '--interactive' or input_arg == '-i':
            interactive_mode(model)
        elif os.path.isfile(input_arg):
            result = classify_from_file(model, input_arg)
            with open(input_arg, 'r') as f:
                email_text = f.read()
            print_result(result, email_text)
        else:
            email_text = " ".join(sys.argv[1:])
            result = classify_email(model, email_text)
            print_result(result, email_text)
    else:
        print("\nUsage:")
        print("  python classify_email.py <email_text>")
        print("  python classify_email.py <path_to_email_file>")
        print("  python classify_email.py --interactive")
        print("\nExample:")
        print('  python classify_email.py "Click here to claim your prize!"')
        
        print("\n\nRunning quick demo...")
        
        test_emails = [
            "URGENT: Your account has been compromised! Click here to verify immediately.",
            "Hi team, just a reminder about our meeting tomorrow at 10 AM.",
        ]
        
        for email in test_emails:
            result = classify_email(model, email)
            print_result(result, email)


if __name__ == "__main__":
    main()
