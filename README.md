<h1 align="center">🛡️ PhishingGuard – AI-Powered Phishing Email Detector</h1>

<p align="center">
<b>PhishingGuard</b> is a machine-learning based project that detects whether an email is 
<b>phishing</b> or <b>genuine</b>.  
<br>
It uses <b>TF-IDF</b> for text vectorization and <b>Logistic Regression</b> for classification.
</p>

<hr>

<h2>🚀 Features</h2>
<ul>
  <li>Detect phishing emails using machine learning</li>
  <li>Lightweight & fast model</li>
  <li>Works on Windows, Linux, and macOS</li>
  <li>Clean Streamlit UI</li>
  <li>Classifies emails instantly</li>
  <li>Easy to extend with more data</li>
</ul>

<h2>📁 Project Structure</h2>

<pre>
PhishingGuard/
│── dataset/
│   └── phishing.csv
│── train_phishing.py
│── classify_email.py
│── app_streamlit.py
│── requirements.txt
│── README.md
</pre>

<h2>🧠 How It Works</h2>

<h3>1️⃣ Preprocessing</h3>
<p>Emails are cleaned by:</p>
<ul>
  <li>Lowercasing</li>
  <li>Removing punctuation</li>
  <li>Removing stopwords</li>
  <li>Tokenizing</li>
</ul>

<h3>2️⃣ Vectorization</h3>
<p>PhishingGuard uses <b>TF-IDF Vectorizer</b> to convert text into numeric form.</p>

<h3>3️⃣ Model Training</h3>
<p>A <b>Logistic Regression</b> model is trained on the dataset.</p>

<h3>4️⃣ Prediction</h3>
<p>The trained model predicts:</p>
<ul>
  <li><b>Phishing</b></li>
  <li><b>Genuine</b></li>
</ul>

<h3>5️⃣ Streamlit UI</h3>
<p>Paste an email → Get instant prediction through the web interface.</p>

<hr>

<h2>⚙️ Installation (Windows, Linux, macOS)</h2>

<h3>Clone the repository</h3>
<pre>
git clone https://github.com/shaikallu786/PhishingGuard.git
cd PhishingGuard
</pre>

<h3>Install dependencies</h3>
<pre>pip install -r requirements.txt</pre>

If <code>requirements.txt</code> is missing:
<pre>pip install scikit-learn pandas joblib streamlit</pre>

<hr>

<h2>🏋️ Train the Model</h2>
<pre>python train_phishing.py</pre>

This generates:
<pre>
model.joblib
vectorizer.joblib
</pre>

<hr>

<h2>🧪 Run the CLI Classifier</h2>
<pre>python classify_email.py "Your email text here"</pre>

Example:
<pre>python classify_email.py "Your account will be locked. Click here to verify."</pre>

<hr>

<h2>🌐 Run Streamlit App</h2>
<pre>streamlit run app_streamlit.py</pre>

Open in browser:
<pre>http://localhost:8501</pre>

<hr>

<h2>🐧 Linux Setup Example (Ubuntu)</h2>

<pre>
sudo apt update
sudo apt install python3 python3-pip -y

pip install scikit-learn pandas joblib streamlit

git clone https://github.com/shaikallu786/PhishingGuard.git
cd PhishingGuard

python3 train_phishing.py
streamlit run app_streamlit.py
</pre>

<hr>

<h2>🤝 Contributing</h2>
<p>Pull requests are welcome. For major changes, open an issue first.</p>

<h2>📜 License</h2>
<p>This project is licensed under the <b>MIT License</b>.</p>
