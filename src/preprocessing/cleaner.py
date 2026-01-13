# src/preprocessing/cleaner.py
import re
import spacy

class TextSanitizer:
    def __init__(self):
        # Load a lightweight SpaCy model for Entity Recognition
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # Fallback if model isn't downloaded
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

    def redact_pii(self, text: str) -> str:
        """Redacts Names, Emails, and Account Numbers."""
        # 1. Redact Emails using Regex
        text = re.sub(r'\S+@\S+', '[EMAIL]', text)
        
        # 2. Redact Account Numbers (Pattern: ACC-XXXXX)
        text = re.sub(r'ACC-\d+', '[ACCOUNT_ID]', text)
        
        # 3. Redact Names using SpaCy NER
        doc = self.nlp(text)
        sanitized_text = text
        for ent in doc.ents:
            if ent.label_ in ["PERSON"]:
                sanitized_text = sanitized_text.replace(ent.text, f"[{ent.label_}]")
        
        return sanitized_text

    def clean_transcript(self, text: str) -> str:
        """General text cleaning (lowercase, remove extra whitespace)."""
        text = text.lower().strip()
        text = re.sub(r'\s+', ' ', text)
        return text