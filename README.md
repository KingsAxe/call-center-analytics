## CallSense-AI

Live link[https://callsense-ai.streamlit.app/]

CallSense-AI is an NLP analytics pipeline and Streamlit dashboard for turning raw call-center transcripts into business intelligence. The project combines behavioural feature engineering, privacy-safe transcript preprocessing, semantic intent clustering, and a friction scorecard for prioritising operational fixes.

## What The Project Does

- Builds a behavioural baseline from call logs in `notebooks/01_eda_and_sql.ipynb`
- Redacts PII, generates MPNet embeddings, and discovers latent intents in `notebooks/02_intent_discovery.ipynb`
- Validates clustering quality and exports an executive scorecard in `notebooks/03_nlp_performance.ipynb`
- Serves a 5-page Streamlit dashboard in `app.py`:
  Problem, Intent Map, Friction Heatmap, Archetype Drilldown, Live Inference

## Stack

- Data: `pandas`, `numpy`, `psycopg2-binary`
- NLP/ML: `transformers`, `torch`, `sentence-transformers`, `hdbscan`, `umap-learn`, `scikit-learn`
- UI: `streamlit`, `plotly`
- Config: `python-dotenv`, `pyyaml`

## Key Outputs

- `data/processed/analytics_base.csv`
- `data/processed/clustered_data.csv`
- `data/processed/executive_friction_scorecard.csv`

## Run Locally

1. Install dependencies.

```bash
pip install -r requirements.txt
```

2. Generate or refresh the pipeline artifacts by running the notebooks in order.

- `notebooks/01_eda_and_sql.ipynb`
- `notebooks/02_intent_discovery.ipynb`
- `notebooks/03_nlp_performance.ipynb`

3. Start the dashboard.

```bash
streamlit run app.py
```

## Notes

- The dashboard expects the processed CSV files under `data/processed/`.
- The live inference page uses the local inference stack in `src/models/inference.py`.
- The repository also contains synthetic data utilities under `src/database/` for local experimentation.


