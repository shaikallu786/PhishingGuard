# 🛡️ PhishingGuard – AI-Powered Phishing Email Detector

PhishingGuard is a machine-learning based project that detects whether an email
is **phishing** or **genuine**.  
It uses **TF-IDF** for text vectorization and **Logistic Regression** for
classification.  
The project includes:

- A training script  
- A command-line classifier  
- A Streamlit web app  
- A sample phishing dataset

  ## 🚀 Features

- Detect phishing emails with ML  
- Lightweight & fast model (Logistic Regression)  
- Works on **Windows**, **Linux**, and **macOS**  
- Clean Streamlit UI  
- Classifies emails instantly  
- Easy to extend with more data

## 📁 Project Structure

PhishingGuard/
│── dataset/
│ └── phishing.csv
│── train_phishing.py
│── classify_email.py
│── app_streamlit.py
│── requirements.txt
│── README.md

# 🧠 How It Works

### 1️⃣ Preprocessing  
Emails are cleaned by:
- Lowercasing  
- Removing punctuation  
- Removing stopwords  
- Tokenizing  

### 2️⃣ Vectorization  
PhishingGuard uses **TF-IDF Vectorizer** to convert text into numeric form.

### 3️⃣ Model Training  
A **Logistic Regression** model is trained on the email dataset.

### 4️⃣ Prediction  
The trained model predicts:
- `Phishing`
- `Genuine`

### 5️⃣ Streamlit UI  
The web interface allows users to paste an email and get prediction results instantly.

---

# ⚙️ Installation (Windows, Linux, macOS)

### Clone the repository

git clone https://github.com/shaikallu786/PhishingGuard.git
cd PhishingGuard

##Install dependencies

pip install -r requirements.txt

If requirements.txt is missing, install manually:

pip install scikit-learn pandas joblib streamlit

##🏋️ Train the Model
python train_phishing.py
This will generate:
-->model.joblib
-->vectorizer.joblib

##Run the CLI Classifier
python classify_email.py "Your email text here"
Example: python classify_email.py "Your account will be locked. Click here to verify."

##Run Streamlit App
Windows / Linux / macOS: streamlit run app_streamlit.py
Open in browser: http://localhost:8501


##🐧 Linux Setup Example (Ubuntu)

PhishingGuard works perfectly in Linux because:
->It uses pure Python
->No OS-specific dependencies
->Streamlit behaves the same on all platforms
Commands:
sudo apt update
sudo apt install python3 python3-pip -y
pip install scikit-learn pandas joblib streamlit
git clone https://github.com/shaikallu786/PhishingGuard.git
cd PhishingGuard
python3 train_phishing.py
streamlit run app_streamlit.py

##🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss the change

##📜 License
This project is licensed under the MIT License.
