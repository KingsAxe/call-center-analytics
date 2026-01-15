## **CallSense-AI: Intelligence-Driven Contact Center Analytics**

CallSense-AI is an end-to-end NLP research pipeline and decision-support system that transforms raw call transcripts into actionable business intelligence. By leveraging unsupervised latent intent discovery and zero-shot classification, this project identifies operational friction points that traditional metrics like Average Handle Time (AHT) miss.

## **The Business Problem**
Contact centers generate massive amounts of unstructured text. Traditional analytics rely on manual QA or keyword spotting, which are:

Unscalable: Only <2% of calls are usually reviewed [(https://www.sqmgroup.com/resources/library/blog/automated-vs-manual-qa-how-to-improve-accuracy-insights-and-cost-efficiency)].

Reactive: Issues are found after customer churn.

Surface-Level: High AHT is flagged, but the root cause (e.g., specific billing friction vs. technical debt) remains hidden.

## **The Solution**
CallSense-AI solves this by implementing a "State Machine" pipeline across three stages:

Behavioral Intelligence: Extracting talk-to-listen ratios, sentiment volatility, and turn-based dynamics.

Latent Intent Discovery: Using MPNet Transformers and UMAP+HDBSCAN to discover hidden conversational archetypes without human labeling.

Risk Quantification: Developing a Friction Index that correlates semantic intent with CSAT and Escalation rates to prioritize business interventions.

## **Key Results**
Friction Identification: Discovered 6 distinct intent archetypes, identifying that Subscription Cancellations drove 38% of all escalations despite being only 25% of volume.

Operational ROI: Identified a $3,400+ monthly loss attributed to "Talk-Ratio Overload" in technical support calls.

Data Privacy: Implemented a Transformer-based NER (BERT) pipeline to ensure 100% PII redaction (Names, Emails, IDs) before any downstream analysis.

## **Technical Stack**
Models: all-mpnet-base-v2 (Embeddings), BART-Large-MNLI (Zero-Shot), BERT-base-NER (PII Redaction).

Dimensionality/Clustering: UMAP & HDBSCAN.

Data Pipeline: PostgreSQL (JSONB), Pandas, NumPy.

Interface: Streamlit & Plotly.

## **How to Run**
1. **Environment Setup**
Bash

git clone https://github.com/your-username/call-center-analytics.git
pip install -r requirements.txt

2. **Pipeline Execution (Sequential)**
The project is structured as a state-driven pipeline. Each step must be run to generate the checkpoint files for the 

next:

- notebooks/01_eda_and_sql.ipynb: Connects to DB, engineers behavioral features, and exports analytics_base.csv.


- notebooks/02_clustering_exploration.ipynb: Performs PII redaction, generates embeddings, and discovers archetypes.     Exports clustered_data.csv.


- notebooks/03_nlp_performance_report.ipynb: Validates clusters via Silhouette Scores and creates the final              executive_friction_scorecard.csv.

3. **Launching the Dashboard**
Once the data checkpoints are created, launch the interactive decision-support system:

Bash

streamlit run app.py


