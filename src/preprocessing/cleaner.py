from transformers import pipeline
import re
from typing import List

class TextSanitizer:
    def __init__(self, device=-1):
        """
        device = -1  → CPU
        device = 0   → GPU (if available)
        """
        self.ner_pipeline = pipeline(
            "ner",
            model="dslim/bert-base-NER",
            aggregation_strategy="simple",
            device=device
        )

        # Precompile regex for performance
        self.email_pattern = re.compile(r'\S+@\S+')
        self.account_pattern = re.compile(r'ACC-\d+')
        
        # Expanded Address Pattern: Captures Number + Name + Street Suffix
        self.address_pattern = re.compile(
            r'\d{1,5}\s\w+\s(way|street|st|ave|avenue|road|rd|lane|ln|drive|dr|court|ct|square|sq|boulevard|blvd)', 
            re.IGNORECASE
        )

    def _regex_redact(self, text: str) -> str:
        """Stage 1: Fast regex-based redaction for predictable patterns."""
        text = self.email_pattern.sub("[EMAIL]", text)
        text = self.account_pattern.sub("[ACCOUNT_ID]", text)
        text = self.address_pattern.sub("[ADDRESS]", text)
        return text

    def batch_redact(self, texts: List[str], batch_size: int = 16) -> List[str]:
        """Stage 2: Transformer-based NER for names and complex entities."""

        # Step 1: Regex pass
        regex_cleaned = [self._regex_redact(t) for t in texts]

        # Step 2: Transformer pass (NER)
        ner_results = self.ner_pipeline(regex_cleaned, batch_size=batch_size)

        redacted_texts = []

        for text, entities in zip(regex_cleaned, ner_results):
            # Replace PERSON entities safely from right-to-left to maintain index accuracy
            for ent in sorted(entities, key=lambda x: x['start'], reverse=True):
                if ent["entity_group"] == "PER":
                    text = text[:ent["start"]] + "[PERSON]" + text[ent["end"]:]
            redacted_texts.append(text)

        return redacted_texts

    def clean_batch(self, texts: List[str]) -> List[str]:
        """Normalization: Lowercase, stripping, and whitespace collapse."""
        cleaned = []
        for t in texts:
            t = t.lower().strip()
            t = re.sub(r"\s+", " ", t)
            cleaned.append(t)
        return cleaned