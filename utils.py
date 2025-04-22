import re

# Carefully ordered to prevent misclassification (Aadhar before Expiry/CVV)
PII_PATTERNS = [
    ("aadhar_num", r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b"),
    ("email", r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b"),
    ("phone_number", r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"),
    ("dob", r"\b(?:\d{1,2}(?:st|nd|rd|th)?[-\s]*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[-/\s]*\d{2,4})\b"),
    ("credit_debit_no", r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),
    ("cvv_no", r"\b\d{3}\b"),
    ("expiry_no", r"\b(0[1-9]|1[0-2])/?([0-9]{2})\b"),
    ("rupee_amount", r"₹\s?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?")
]

LABEL_MAPPING = {
    "email": "EMAIL",
    "phone_number": "PHONE",
    "dob": "DOB",
    "aadhar_num": "AADHAR",
    "credit_debit_no": "CARD",
    "cvv_no": "CVV",
    "expiry_no": "EXPIRY",
    "rupee_amount": "AMOUNT"
}

def mask_pii(text):
    entities = []
    matches = []
    occupied = set()

    for ent_type, pattern in PII_PATTERNS:
        for match in re.finditer(pattern, text):
            start, end = match.span()

            # Avoid overlapping spans
            if any(i in occupied for i in range(start, end)):
                continue

            original = match.group()
            matches.append((start, end, ent_type, original))
            occupied.update(range(start, end))

    # Replace text backwards to preserve indexes
    matches.sort(reverse=True, key=lambda x: x[0])
    masked_text = text

    for start, end, ent_type, original in matches:
        label = LABEL_MAPPING.get(ent_type, ent_type.upper())
        mask_token = f"[{label}]"
        masked_text = masked_text[:start] + mask_token + masked_text[end:]
        entities.append({
            "position": [start, start + len(mask_token)],
            "classification": label,
            "entity": original
        })

    return masked_text, entities[::-1]  # Restore original order for output

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
