---
title: Email Classifier with PII Masking
emoji: 📧
colorFrom: indigo
colorTo: blue
sdk: docker
app_file: app.py
pinned: false
---

#  Email Classification with PII Masking — FastAPI Project

A production-ready project that classifies incoming emails into categories while detecting and masking Personally Identifiable Information (PII). This project uses Regex and spaCy for PII detection and a Naive Bayes model for classification. It exposes a FastAPI POST endpoint for inference.

---

##  Features

- ✅ PII detection using regex (email, phone, card, etc.) and spaCy NER (name)
- ✅ Email classification (e.g., Request, Incident, Change, Problem)
- ✅ FastAPI backend with Swagger UI for testing
- ✅ JSON output in a strict format
- ✅ Automatically opens Swagger UI on app launch

---

## 🧠 Project Structure

```plaintext
email_classifier_project/
├── data/
│   └── combined_emails_with_natural_pii.csv  # Dataset with 'email' and 'type' columns
├── api.py                                  # FastAPI endpoint & response handling
├── app.py                                  # Main launcher (opens Swagger UI)
├── Dockerfile                              # Docker deployment configuration
├── Procfile                                # For deployment on Heroku
├── email_model.pkl                         # Saved model after training
├── email_classification_report.txt         # Classification report after training
├── models.py                               # Model training & prediction
├── utils.py                                # PII detection & masking (regex + spaCy)
├── requirements.txt                        # Python dependencies
└── README.md                               # Project documentation

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/email-classifier-pii.git
cd email-classifier-pii
```

### 2. Create virtual environment & activate
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Place Dataset
Ensure this file exists:
```
data/combined_emails_with_natural_pii.csv
```
It should contain two columns: `email`, `type`

### 5. Run the App
```bash
python app.py
```
✅ This will:
- Train the model (if not already trained)
- Launch FastAPI server on http://127.0.0.1:8000
- Auto-open Swagger UI at http://127.0.0.1:8000/docs

---

## 🧠 Flow to Use the API

1. Launch the app using app.py  
2. Browser auto-opens to Swagger at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
3. Click on the POST method ( / )  
4. Click “Try it out”  
5. Enter input in this format:

```json
{
  "input_email_body": "Hey, I'm Raj. My email is raj@example.com and card is 1234-5678-9876-5432."
}
```

### Sample Response:
```json
{
  "input_email_body": "Hey, I'm Raj. My email is raj@example.com and card is 1234-5678-9876-5432.",
  "list_of_masked_entities": [
    {
      "position": [26, 33],
      "classification": "email",
      "entity": "raj@example.com"
    },
    {
      "position": [46, 63],
      "classification": "credit_debit_no",
      "entity": "1234-5678-9876-5432"
    }
  ],
  "masked_email": "Hey, I'm Raj. My email is [email] and card is [credit_debit_no].",
  "category_of_the_email": "Request"
}
```

---

## 🧠 Techniques Used

- Regex for structured PII (email, phone, card)
- spaCy NER for person name detection
- Text vectorization with TfidfVectorizer
- Multinomial Naive Bayes for classification
- FastAPI + Swagger UI for quick testing

---

## 🧾 License
This project is for educational and demonstration purposes. Adapt freely.

---

## 🙌 Author
Made with 💻 by [A.Sumanth]
