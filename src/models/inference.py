import os
import torch
import numpy as np
import re
from typing import Dict, List, Union
from transformers import pipeline
from src.preprocessing.cleaner import TextSanitizer
from src.features.embeddings import VectorEngine

class CallAnalyticsEngine:
    def __init__(self, device: int = -1):
        """
        Production-grade inference engine.
        device: -1 for CPU, 0 for GPU.
        """
        # Load custom modules
        self.sanitizer = TextSanitizer(device=device)
        self.vector_engine = VectorEngine()
        
        # Load Zero-Shot Classifier
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=device
        )
        
        # Expanded labels to improve BART's ability to distinguish subtle intents
        self.candidate_labels = [
            "Technical Support & Error Troubleshooting", 
            "Billing, Payment, and Invoice Disputes", 
            "Subscription Cancellation & Account Closure", 
            "Account Access, Security & Hacking",
            "Onboarding, Setup & Initial Training",
            "General Inquiry & Miscellaneous Questions"
        ]

    def analyze_call(self, raw_transcript: str, talk_ratio: float = 0.5, duration: int = 300) -> Dict:
        """
        Runs the full pipeline: Sanitize -> Classify -> Risk Assessment.
        """
        # 1. Sanitize (Regex + NER)
        redacted_list = self.sanitizer.batch_redact([raw_transcript])
        clean_text = self.sanitizer.clean_batch(redacted_list)[0]

        # 2. Classify Intent
        classification = self.classifier(clean_text, self.candidate_labels)
        top_intent = classification['labels'][0]
        confidence = classification['scores'][0]
        
        # Store all scores for the UI dropdown
        all_scores = dict(zip(classification['labels'], classification['scores']))

        # 3. Calculate Risk (Heuristic from Notebook 03 results)
        risk_score = 0
        # Map specific intent keywords to risk
        if "Cancellation" in top_intent: 
            risk_score += 40
        
        if talk_ratio > 1.1: 
            risk_score += 30
            
        if duration > 500: 
            risk_score += 30
        
        risk_level = "HIGH" if risk_score >= 70 else "MEDIUM" if risk_score >= 40 else "LOW"

        return {
            "clean_text": clean_text,
            "intent": top_intent,
            "confidence": round(confidence, 4),
            "all_scores": all_scores,  # Passed to Streamlit for the expander
            "risk_level": risk_level,
            "risk_score": risk_score
        }