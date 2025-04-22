import re
import json
import pandas as pd

PII_PATTERNS = {
    "email": r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b",
    "phone_number": r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
    "dob": r"\b(?:\d{1,2}[-/th|st|nd|rd\s]+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-/\s]*\d{2,4})\b",
    "aadhar_num": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    "credit_debit_no": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])/?([0-9]{2})\b"
}

def mask_pii(text):
    masked_text = text
    entities = []

    for ent_type, pattern in PII_PATTERNS.items():
        for match in re.finditer(pattern, masked_text):
            start, end = match.start(), match.end()
            original = match.group()
            masked = masked = "[" + ent_type + "]"

            masked_text = masked_text[:start] + masked + masked_text[end:]
            entities.append({
                "position": [start, start + len(masked)],
                "classification": ent_type,
                "entity": original
            })

    return masked_text, entities

def build_response(input_email, masked_email, entities, category):
    return {
        "input_email_body": input_email,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": category
    }

def prepare_dataset(df):
    texts = []
    labels = []
    for _, row in df.iterrows():
        original_text = row['email']
        label = row['type']
        masked_text, _ = mask_pii(original_text)
        texts.append(masked_text)
        labels.append(label)
    return texts, labels
