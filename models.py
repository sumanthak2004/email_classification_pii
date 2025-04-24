import pandas as pd
import pickle
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# Step 1: Preprocess the text (cleaning up unwanted characters)
def preprocess_text(text):
    """
    Clean and preprocess the text for training and prediction.
    - Converts to lowercase
    - Removes unwanted characters (keeping only alphanumeric, @, ., :, etc.)
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"[^a-zA-Z0-9\s\[\]_@.:/-]", "", text)  # Keep only alphanumeric characters, and common symbols like @, ., :, etc.
    return text

# Step 2: Train the classification model
def train_model(csv_path="data/combined_emails_with_natural_pii.csv", model_path="email_model.pkl"):
    """
    Train the model with emails and their respective types, and save the trained model.
    """
    # Load the dataset
    df = pd.read_csv(csv_path)
    df.dropna(inplace=True)  # Drop any rows with missing data

    # Apply text preprocessing to clean the email text
    df['clean_text'] = df['email'].apply(preprocess_text)

    # Split the data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(df['clean_text'], df['type'], test_size=0.2, random_state=42)

    # Create a pipeline with TF-IDF vectorizer + Naive Bayes classifier
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000)),  # Use top 5000 features (words)
        ("clf", MultinomialNB())  # Naive Bayes classifier
    ])

    # Train the model using the training data
    pipe.fit(X_train, y_train)

    # Predict the labels on the test set
    y_pred = pipe.predict(X_test)

    # Print classification report to evaluate the model
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Save the trained model to a file for future use
    with open(model_path, "wb") as f:
        pickle.dump(pipe, f)

# Step 3: Load the pre-trained model
def load_model(model_path="email_model.pkl"):
    """
    Load the pre-trained model from disk.
    """
    with open(model_path, "rb") as f:
        return pickle.load(f)

# Step 4: Predict the category of the email based on keywords and model
def predict_category(text, model):
    """
    Predict the category of the email.
    First, attempt to classify based on context keywords.
    If no match, use the trained machine learning model for prediction.
    """
    # Preprocess the input text
    clean_text = preprocess_text(text)

    # Define keywords for each category
    keywords_request = [
    "refund", "please issue", "return", "send me", "need help", "request", "apply", "can I get", 
    "request a refund", "refund request", "return request", "request assistance", "issue a refund", 
    "ask for refund", "refund status", "refund due", "please return", "request for help", 
    "could you return", "help me return", "please issue refund", "want a refund"
]

    keywords_incident = [
    "not working", "can't log in", "error", "issue", "failed", "bug", "problem", "lost", "loose", 
    "login issue", "cannot login", "cannot access", "can't access", "not responding", "failed to log in", 
    "unable to access", "login problem", "system error", "can't open", "not functioning", "failure to login", 
    "failed login attempt", "problem logging in", "lost access", "loose connection", "can't sign in", 
    "unable to sign in", "can't reach", "unable to reach"
]

    keywords_change = [
    "update", "change", "modify", "edit", "correct", "alter", "revise", "adjust", "amend", "rework", 
    "improve", "customize", "refine", "shift", "replace", "adjustment", "change details", "modify settings", 
    "edit details", "update info", "change contact", "correct info", "adjust settings", "reassign", 
    "alter settings", "change preferences", "update account", "change password"
]

    keywords_problem = [
    "crash", "break", "unable", "stopped", "failure", "not responding", "lost", "loose", "broken", 
    "failure to start", "unable to start", "crashed", "stuck", "stop working", "system crash", "app crash", 
    "frozen", "unable to connect", "not opening", "error occurred", "application failure", "system failure", 
    "program crash", "failure in app", "broken app", "unable to load", "freeze", "not functioning", "problem loading", 
    "app not starting", "connection failure", "stopped working", "not accessible", "not available", "unable to proceed"
]


    lowered_text = text.lower()

    # Keyword-based override
    if any(k in lowered_text for k in keywords_request):
        return "Request"
    elif any(k in lowered_text for k in keywords_incident):
        return "Incident"
    elif any(k in lowered_text for k in keywords_change):
        return "Change"
    elif any(k in lowered_text for k in keywords_problem):
        return "Problem"

    # If no keyword match, use the trained model for prediction
    predicted_label = model.predict([clean_text])[0]
    return predicted_label



