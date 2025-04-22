from fastapi import FastAPI
from pydantic import BaseModel
from utils import mask_pii, build_response
from models import load_model, predict_category

app = FastAPI()
model, encoder = load_model()

class EmailRequest(BaseModel):
    email: str

@app.post("/classify_email")
def classify_email(request: EmailRequest):
    original_email = request.email
    masked_email, entities = mask_pii(original_email)
    category = predict_category(masked_email, model, encoder)
    return build_response(original_email, masked_email, entities, category)


@app.get("/")
def root():
    return {"message": "FastAPI is working! Visit /docs"}
