import os
import torch
import numpy as np
from typing import Dict, List, Union
from src.preprocessing.cleaner import TextSanitizer
from src.features.embeddings import VectorEngine
from transformers import pipeline

class CallAnalyticsEngine:
    def __init__(self, device: int = -1):
        """
        Production-grade inference engine for the CallSense-AI pipeline.
        device: -1 for CPU, 0 for GPU.
        """
        print("Initializing Inference Engine...")
        self.sanitizer = TextSanitizer(device=device)
        self.vector_engine = VectorEngine() # Uses all-mpnet-base-v2
        
        # Zero-Shot Classifier for Business Labeling
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=device
        )
        
        self.candidate_labels = [
            "Technical Support & Error Troubleshooting", 
            "Billing, Payment, and Invoice Disputes",   
            "Subscription Cancellation & Account Closure", 
            "Account Access, Security & Hacking",        
            "Onboarding, Setup & Initial Training",
            "General Inquiry & Miscellaneous Questions"
        ]

    def analyze_call(self, raw_transcript: str, talk_ratio: float = 0.5, duration: int = 300) -> Dict:
            # 1. Sanitize (Ensure your cleaner.py handles addresses - see below)
            redacted_list = self.sanitizer.batch_redact([raw_transcript])
            clean_text = self.sanitizer.clean_batch(redacted_list)[0]

            # 2. Classify Intent
            classification = self.classifier(clean_text, self.candidate_labels)
            
            # Logic Fix: If 'General' is the top but second is close, consider a deeper check
            # For now, we'll just use the expanded labels which usually fixes the 404 issue
            top_intent = classification['labels'][0]
            confidence = classification['scores'][0]
            
            # 3. Probability Distribution for UI
            all_scores = dict(zip(classification['labels'], classification['scores']))

            # ... (keep existing risk logic)
            return {
                "clean_text": clean_text,
                "intent": top_intent,
                "confidence": round(confidence, 4),
                "all_scores": all_scores, # ADDED for the new UI dropdown
                "risk_level": risk_level,
                "risk_score": risk_score
            }


    def process_transcript(self, raw_transcript: str) -> Dict[str, Union[str, float, List]]:
        """
        Takes a raw string and returns a full suite of analytics.
        """
        # 1. Sanitize & Redact
        # We use batch_redact even for single strings to maintain logic consistency
        sanitized_list = self.sanitizer.batch_redact([raw_transcript])
        clean_text = self.sanitizer.clean_batch(sanitized_list)[0]

        # 2. Vectorize (for potential similarity search later)
        embedding = self.vector_engine.generate_embeddings([clean_text])[0]

        # 3. Classify Business Intent
        classification = self.classifier(clean_text, self.candidate_labels)
        
        # 4. Extract Key Insights
        top_intent = classification['labels'][0]
        confidence = classification['scores'][0]

        return {
            "sanitized_text": clean_text,
            "top_intent": top_intent,
            "confidence_score": round(confidence, 4),
            "embedding": embedding.tolist(),
            "all_intents": dict(zip(classification['labels'], classification['scores']))
        }

    def predict_friction_risk(self, talk_ratio: float, duration_sec: int, intent: str) -> str:
        """
        A heuristic-based risk engine using the logic discovered in Notebook 03.
        """
        risk_score = 0
        
        # Logic derived from our "Friction Index"
        if intent == "Subscription Cancellation": risk_score += 40
        if talk_ratio > 1.2: risk_score += 30
        if duration_sec > 500: risk_score += 30
        
        if risk_score >= 70: return "HIGH RISK"
        if risk_score >= 40: return "MEDIUM RISK"
        return "LOW RISK"

# Test logic (Optional: Only runs if you execute this file directly)
if __name__ == "__main__":
    engine = CallAnalyticsEngine()
    test_call = "My name is Sarah Connor. I want to cancel my subscription immediately. The price is too high!"
    results = engine.process_transcript(test_call)
    print(f"Result: {results['top_intent']} ({results['confidence_score']})")