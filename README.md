**🔍 Overview**

Traditional firewalls rely on static rules (signatures) which often fail against Zero-Day attacks. WAF Shield is an intelligent security system that analyzes AWS CloudWatch Traffic Logs to identify anomalous behavior.

Using a trained Random Forest Classifier, it distinguishes between Benign (Safe) and Suspicious (DDoS/Exfiltration) traffic patterns instantly, providing Security Analysts with a modern dashboard for threat monitoring.

**📸 Project Visuals**

**Main Dashboard**
<img width="1910" height="927" alt="Main Dashboard" src="https://github.com/user-attachments/assets/ad144e55-ce3c-4439-8a66-7a9975447702" />
**Safe Output**
<img width="1919" height="925" alt="SAFE" src="https://github.com/user-attachments/assets/6d9a1ef0-589c-47da-b4f5-0df697372852" />
**Threat Output**
<img width="1919" height="926" alt="THREAT" src="https://github.com/user-attachments/assets/ca79e79a-86e1-4167-905f-f27e71b70b6e" />

**🌟 Key Features**

1. 🔍 Real-Time Anomaly Detection

Input: Analyzes packet size (Bytes In, Bytes Out), Port (80, 443), and Request Time.

Output: Instant classification as Safe or Malicious.

Accuracy: ~98% detection rate on test data.

2. 🛡️ Interactive Traffic Simulator

Allows users to manually tweak network parameters to test the firewall's robustness.

Simulates scenarios like Data Exfiltration (High Bytes Out) or DDoS (Rapid small packets).

3. 🚨 Actionable Intelligence

Displays a Confidence Score (e.g., "99.2% sure this is an attack").

Recommends specific actions:

Block Source IP

Reset Connection

Flag for Forensics

**🛠️ Tech Stack**

Frontend,Streamlit (Python framework)

Backend Logic,Python 3.9+

Machine Learning,"Scikit-Learn, Random Forest, XGBoost"

Data Processing,"Pandas, NumPy"

Model Saving,Joblib (Serialized models)

Dataset,AWS CloudWatch Logs (40k+ records)

**📊 Model Architecture**

We compared multiple algorithms to find the best balance between speed and accuracy:

Algorithm	          Accuracy	      Precision	Status

Random Forest	      98.4%	High	    ✅ Selected

XGBoost	            97.8%	High	    ⚠️ Backup

Logistic Regression	89.2%	Medium	  ❌ Rejected

The Random Forest model was chosen for its robustness against overfitting on tabular log data.

**🚀 Installation Guide**

Follow these steps to deploy the WAF Shield locally.

Prerequisites

Python 3.8+ installed.

Step 1: Clone the Repository

git clone https://github.com/YOUR-USERNAME/WAF-Shield-Cyber-Threat-Detection.git
cd WAF-Shield-Cyber-Threat-Detection

Step 2: Install Dependencies

Create a requirements.txt file and run:

pip install -r requirements.txt

Step 3: Launch the Dashboard

streamlit run App.py

**📂 Project Structure**

WAF-Shield/
├── 📂 data/                # CloudWatch_Traffic_Web_Attack.csv
├── 📂 models/              # Serialized ML Models
│   ├── waf_rf_classifier.pkl
│   ├── model_columns.pkl
│   └── model_feature_columns.pkl
├── App.py                  # Main Streamlit Application
├── Cybersecurity_Web_Threat_Detection.ipynb  # Training Notebook
├── requirements.txt        # Dependencies
└── README.md               # Documentation

**🔮 Future Scope**

Automated IP Blocking: Integrate with iptables or AWS WAF to block IPs automatically.

Geo-Tagging: Visualize attack origins on a world map.

Deep Learning: Implement LSTM (Long Short-Term Memory) models for sequence-based attack detection.

**⚠️ Disclaimer**

This project is a simulation for educational and research purposes. It uses historical log data and does not interface with live network drivers.

Made with 💻 by Md Salman Farsi

Connect with me on 

LinkedIn: | GitHub:
