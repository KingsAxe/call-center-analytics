#### **CallSense-AI: Enterprise Conversational Analytics Infrastructure**

**Project Overview**
This repository contains a high-fidelity replica of a production-grade conversational analytics engine. The system is designed to ingest unstructured call center transcripts, perform PII redaction, and apply unsupervised machine learning to extract behavioral and sentiment-based insights. Unlike basic NLP demos, this project focuses on the intersection of data engineering (PostgreSQL/JSONB) and behavioral feature engineering.

**Core Architecture**
The system is built on a modular architecture to ensure scalability and maintainability.

1. Data Layer (PostgreSQL)
The foundation utilizes a PostgreSQL database with a JSONB column structure. This approach allows for:

Schema Flexibility: Handling varying transcript lengths and metadata without frequent migrations.

Query Performance: Implementation of GIN (Generalized Inverted Index) indexing for efficient full-text search and JSON attribute retrieval.

Stochastic Simulation: A synthetic data engine that generates non-linear dialogues, typos, and varying turn lengths to simulate real-world data noise.

2. Preprocessing & Ethical Redaction
Prior to analysis, data undergoes a rigorous sanitization pipeline located in src/preprocessing/:

PII Redaction: Named Entity Recognition (NER) is used to identify and mask person names.

Pattern Matching: Regex-based removal of sensitive patterns, including Account IDs and Email addresses.

Normalization: Text cleaning and diarization alignment for transformer compatibility.

3. NLP & Feature Engineering
We move beyond raw text by engineering "Behavioral Physics" features:

Talk-to-Listen Ratio: Calculating agent vs. customer verbosity to predict friction.

Sentiment Volatility: Measuring the delta between call start and call end sentiment.

Transformer Embeddings: Utilizing all-mpnet-base-v2 to generate 768-dimensional dense vectors representing the semantic intent of each interaction.

**Implementation Roadmap**
Phase 1: Infrastructure & EDA
Deployment of the PostgreSQL schema.

Implementation of the Stochastic Data Generator.

Exploratory Data Analysis (EDA) focused on escalation drivers and churn correlation.

Phase 2: Unsupervised Intent Discovery
Dimensionality reduction using UMAP to prepare embeddings for clustering.

HDBSCAN Clustering: Discovery of latent call archetypes (e.g., "High-Friction Billing Disputes" vs. "Routine Technical Support") without pre-defined label bias.

Phase 3: Performance & Reporting
Zero-shot classification to validate cluster purity.

Correlation analysis between engineered behavioral features and human-provided CSAT scores.

**Directory Structure**

Plaintext

call-center-analytics/
├── data/                   # Data versioning (raw, processed, embeddings)
├── models/                 # Serialized model artifacts and encoders
├── notebooks/              # Research, EDA, and Stakeholder presentations
├── src/                    # Production-grade source code
│   ├── database/           # PostgreSQL connections and ingestion logic
│   ├── preprocessing/      # PII redaction and text sanitization
│   ├── features/           # Transformer embeddings and feature engineering
│   └── models/             # Clustering and inference scripts
├── config.yaml             # Centralized project hyperparameters
└── requirements.txt        # System dependencies
Setup Instructions
Environment: Create a virtual environment and install dependencies via pip install -r requirements.txt.

Database: Configure your .env file with PostgreSQL credentials.

Execution: Initialize the database and seed data using python src/database/db_connector.py.

Analysis: Run the notebooks in the notebooks/ directory sequentially (01 to 03)