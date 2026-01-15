import streamlit as st
import pandas as pd
import plotly.express as px
import os
from src.models.inference import CallAnalyticsEngine

# --- APP CONFIG ---
st.set_page_config(page_title="CallSense-AI Dashboard", layout="wide")

@st.cache_resource
def load_engine():
    return CallAnalyticsEngine(device=-1)

@st.cache_data
def load_project_data():
    # Load the files
    df = pd.read_csv('data/processed/clustered_data.csv')
    scorecard = pd.read_csv('data/processed/executive_friction_scorecard.csv')
    
    # FIX: If cluster_id is the index, move it to a column
    if 'cluster_id' not in scorecard.columns:
        scorecard = scorecard.reset_index().rename(columns={'index': 'cluster_id'})
    
    # Ensure cluster_id is integer type for perfect matching
    scorecard['cluster_id'] = scorecard['cluster_id'].astype(int)
    df['cluster_id'] = df['cluster_id'].astype(int)

    # Create the mapping and apply it
    mapping = dict(zip(scorecard['cluster_id'], scorecard['archetype_name']))
    df['archetype_name'] = df['cluster_id'].map(mapping).fillna("Unclassified / Noise")
    
    return df, scorecard

# --- SIDEBAR ---
st.sidebar.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
st.sidebar.title("CallSense-AI Engine")
menu = st.sidebar.radio("Navigation", ["Executive Summary", "Intent Map", "Live Inference"])

# Load Data
try:
    df, scorecard = load_project_data()
except FileNotFoundError:
    st.error("Data files not found. Please run Notebook 01 and 02 first.")
    st.stop()

# --- 1. EXECUTIVE SUMMARY (Notebook 03 Insights) ---
if menu == "Executive Summary":
    st.title("Executive Performance Scorecard")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Avg CSAT", f"{df['csat_score'].mean():.2f}")
    m2.metric("High-Risk Archetype", scorecard.iloc[0]['archetype_name'])
    m3.metric("Total ROI Impact", f"${scorecard['call_cost'].sum():,.0f}")

    st.subheader("Friction Index by Archetype")
    fig = px.bar(scorecard, x='archetype_name', y='Friction_Index', color='Friction_Index',
                 color_continuous_scale='Reds', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(scorecard)

# --- 2. INTENT MAP (Notebook 02 Visuals) ---
elif menu == "Intent Map":
    st.title("Semantic Intent Clusters")
    st.markdown("This map shows how calls are grouped by the AI based on conversation context.")
    
    # Ensure x_coord and y_coord are in your clustered_data.csv from Notebook 02
    fig = px.scatter(df, x='x_coord', y='y_coord', color='archetype_name',
                     hover_data=['clean_text', 'csat_score'], 
                     title="2D UMAP Projection of Call Intents",
                     template="plotly_dark")
    
    fig.update_layout(
        width=1600, 
        height=850,
        xaxis=dict(scaleanchor="y", scaleratio=1), # Maintain aspect ratio
        yaxis=dict(constrain='domain')
    )

    st.plotly_chart(fig, use_container_width=False)

# --- 3. LIVE INFERENCE ---
elif menu == "Live Inference":
    st.title("Real-Time Call Analysis")
    raw_input = st.text_area("Paste Transcript:", height=150)
    t_ratio = st.slider("Talk Ratio", 0.0, 2.0, 1.0)
    
    if st.button("Analyze Call"):
        engine = load_engine()
        res = engine.analyze_call(raw_input, talk_ratio=t_ratio)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Detected Intent", res['intent'])
            st.metric("Risk Level", res['risk_level'])
        with col_b:
            st.write("**Sanitized Transcript:**")
            st.caption(res['clean_text'])