# api.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from utils import mask_pii
from models import load_model, predict_category

# Load the trained model once
model = load_model()

# Initialize the FastAPI app
app = FastAPI()

# Request body model
class EmailInput(BaseModel):
    input_email_body: str

# Redirect root to docs UI
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# POST endpoint to classify email
@app.post("/")
async def classify_email(email_input: EmailInput):
    original_text = email_input.input_email_body

    # Step 1: Mask PII from the original email
    masked_text, entities = mask_pii(original_text)

    # Step 2: Predict category using original text (not masked)
    predicted_category = predict_category(original_text, model)

    # Step 3: Return full structured response
    return {
        "input_email_body": original_text,
        "list_of_masked_entities": entities,
        "masked_email": masked_text,
        "category_of_the_email": predicted_category
    }
