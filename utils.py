import re
import spacy

nlp = spacy.load("en_core_web_sm")

PII_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b",
    "credit_debit_no": r"\b(?:\d{4}[- ]?){3}\d{4}\b",
    "aadhar_num": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/([0-9]{2,4})\b"
}

def mask_pii(text):
    masked_text = text
    masked_entities = []

    # Step 1: Regex-based masking
    for entity_type, pattern in PII_PATTERNS.items():
        for match in list(re.finditer(pattern, masked_text)):
            original = match.group()
            masked_value = f"[{entity_type}]"
            if original in masked_text:
                masked_text = masked_text.replace(original, masked_value, 1)
                start = masked_text.find(masked_value)
                if start != -1:
                    end = start + len(masked_value)
                    masked_entities.append({
                        "position": [start, end],
                        "classification": entity_type,
                        "entity": original
                    })

    # Step 2: Phone number masking (context-aware)
    phone_context_patterns = [
        r"(?:call|contact|phone|ring|mobile|reach me at|phone me at|number is|dial|text me at|contact number is|call on)[^\d]{0,10}(\+91[-\s]?\d{5}[-\s]?\d{5}|\+91[-\s]?\d{10}|\d{5}[-\s]?\d{5}|\d{10})",
        r"phone\s*(is|:)?\s*(\+91[-\s]?\d{5}[-\s]?\d{5}|\+91[-\s]?\d{10}|\d{5}[-\s]?\d{5}|\d{10})"
    ]

    for pattern in phone_context_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            phone = None
            if match.lastindex:
                for i in range(1, match.lastindex + 1):
                    group = match.group(i)
                    if group and re.fullmatch(r"(\+91)?[-\s]?\d{5}[-\s]?\d{5}|\d{10}", group):
                        phone = group
                        break
            if phone and phone in masked_text:
                masked_value = "[phone_number]"
                masked_text = masked_text.replace(phone, masked_value, 1)
                start = masked_text.find(masked_value)
                if start != -1:
                    end = start + len(masked_value)
                    masked_entities.append({
                        "position": [start, end],
                        "classification": "phone_number",
                        "entity": phone
                    })

    # Step 3: Name masking (NER + fallback)
    names_found = set()
    name_patterns = [
        r"\bI(?:'m| am)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"\bThis is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"\bIt'?s me[,:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"\bHello[,:\s]+(?:this is|this side)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"\bHey[,:\s]+I(?:'m| am)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"\bMy name is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"\bThis side\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"\bI am\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"\bI’m\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        r"\bHello[,\s]+I(?:'m| am)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)"
    ]

    for pattern in name_patterns:
        matches = re.findall(pattern, text)
        for name in matches:
            names_found.add(name)

    # spaCy-based name detection
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            names_found.add(ent.text)

    for name in names_found:
        masked_value = "[full_name]"
        if name in masked_text:
            masked_text = masked_text.replace(name, masked_value, 1)
            start = masked_text.find(masked_value)
            if start != -1:
                end = start + len(masked_value)
                masked_entities.append({
                    "position": [start, end],
                    "classification": "full_name",
                    "entity": name
                })

    return masked_text, masked_entities
