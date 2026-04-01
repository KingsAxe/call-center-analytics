import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from src.models.inference import CallAnalyticsEngine

# ─────────────────────────────────────────────────────────────
# APP CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CallSense-AI | Business Intelligence",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# THEME — slide palette injected as CSS
# White bg · Dark Gray text · Teal accents · Red critical
# ─────────────────────────────────────────────────────────────
TEAL   = "#0D9488"
TEAL_L = "#CCFBF1"
TEAL_D = "#115E59"
RED    = "#DC2626"
GRAY   = "#2F2F2F"
WHITE  = "#FFFFFF"
BG     = "#F8FAFC"
BORDER = "#E2E8F0"
SLATE  = "#475569"
SLATE_L = "#64748B"

st.html(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {BG};
    color: {GRAY};
}}
.main .block-container {{
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1300px;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {WHITE};
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] * {{
    color: {GRAY} !important;
}}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] div,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] label p,
[data-testid="stSidebar"] .stRadio div,
[data-testid="stSidebar"] .stRadio p {{
    color: {GRAY} !important;
}}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {{
    color: {GRAY};
    font-weight: 700;
}}

/* ── Radio nav ── */
[data-testid="stSidebar"] .stRadio > div {{
    gap: 0.15rem;
}}
[data-testid="stSidebar"] .stRadio label {{
    font-size: 0.92rem;
    font-weight: 600;
    color: {GRAY} !important;
    padding: 8px 10px;
    border-radius: 10px;
    background: rgba(13, 148, 136, 0.06);
    border: 1px solid rgba(13, 148, 136, 0.12);
}}
[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(13, 148, 136, 0.1);
}}
[data-testid="stSidebar"] .stRadio input:checked + div {{
    color: {TEAL_D} !important;
    font-weight: 700 !important;
}}

/* ── Page title ── */
h1 {{ color: {GRAY}; font-weight: 800; letter-spacing: -0.5px; }}
h2 {{ color: {GRAY}; font-weight: 700; }}
h3 {{ color: {TEAL};  font-weight: 600; }}

/* ── Metric cards ── */
[data-testid="stMetric"] {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-top: 4px solid {TEAL};
    border-radius: 12px;
    padding: 1rem 1.2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}}
[data-testid="stMetric"] label {{ color: {SLATE}; font-size: 0.78rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }}
[data-testid="stMetric"] [data-testid="stMetricValue"] {{ color: {GRAY}; font-size: 1.9rem; font-weight: 800; }}

/* ── Insight cards ── */
.insight-card {{
    background: {WHITE};
    border: 1px solid {BORDER};
    border-left: 5px solid {TEAL};
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}
.insight-card.critical {{ border-left-color: {RED}; }}
.insight-card .label {{
    font-size: 0.72rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.08em; color: {SLATE}; margin-bottom: 4px;
}}
.insight-card .value {{ font-size: 1.45rem; font-weight: 800; color: {GRAY}; }}
.insight-card .value.red {{ color: {RED}; }}
.insight-card .desc {{ font-size: 0.83rem; color: {SLATE}; margin-top: 3px; line-height: 1.5; }}

/* ── Section header ── */
.section-header {{
    display: flex; align-items: center; gap: 8px;
    background: linear-gradient(90deg, #ECFDF5 0%, #F8FAFC 100%);
    border: 1px solid #A7F3D0;
    border-left: 4px solid {TEAL_D};
    border-radius: 10px;
    padding: 0.7rem 0.9rem;
    margin: 1.5rem 0 1rem;
    font-size: 1.02rem; font-weight: 800; color: {TEAL_D};
}}

/* ── Framework box ── */
.framework-box {{
    background: {WHITE}; border: 1px solid {BORDER};
    border-radius: 12px; padding: 1.1rem 1.25rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05); height: 100%;
}}
.framework-box .step-label {{
    display: inline-block;
    font-size: 0.72rem; font-weight: 800; text-transform: uppercase;
    letter-spacing: 0.08em; color: {TEAL_D};
    background: #DCFCE7;
    border: 1px solid #86EFAC;
    border-radius: 999px;
    padding: 0.2rem 0.5rem;
    margin-bottom: 0.45rem;
}}
.framework-box h4 {{ margin: 0 0 0.5rem; font-size: 0.95rem; color: {GRAY}; font-weight: 700; }}
.framework-box ul {{ margin: 0; padding-left: 1.1rem; font-size: 0.85rem; color: {SLATE}; line-height: 1.55; }}

/* ── Risk badge ── */
.badge {{
    display: inline-block; padding: 3px 10px; border-radius: 999px;
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.04em;
}}
.badge-high   {{ background: #FEE2E2; color: {RED}; }}
.badge-medium {{ background: #FEF3C7; color: #D97706; }}
.badge-low    {{ background: #D1FAE5; color: #059669; }}

/* ── Drilldown card ── */
.drilldown-card {{
    background: {TEAL_L}; border: 1px solid #99F6E4;
    border-radius: 10px; padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem; font-size: 0.84rem; color: #134E4A; line-height: 1.6;
}}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{ border-radius: 8px; border: 1px solid {BORDER}; }}
</style>
""")

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading AI inference engine…")
def load_engine():
    return CallAnalyticsEngine(device=-1)

@st.cache_data(show_spinner="Loading project data…")
def load_data():
    df = pd.read_csv('data/processed/clustered_data.csv')
    sc = pd.read_csv('data/processed/executive_friction_scorecard.csv')
    if 'cluster_id' not in sc.columns:
        sc = sc.reset_index().rename(columns={'index': 'cluster_id'})
    sc['cluster_id'] = sc['cluster_id'].astype(int)
    df['cluster_id']  = df['cluster_id'].astype(int)
    mapping = dict(zip(sc['cluster_id'], sc['archetype_name']))
    df['archetype_name'] = df['cluster_id'].map(mapping).fillna("Unclassified / Noise")
    if 'avg_duration' not in sc.columns and 'duration_sec' in sc.columns:
        sc['avg_duration'] = sc['duration_sec']
    if 'escalation_rate' not in sc.columns and 'escalated' in sc.columns:
        sc['escalation_rate'] = sc['escalated']
    if 'resolution_rate' not in sc.columns and 'resolved' in df.columns:
        resolution_map = df.groupby('archetype_name')['resolved'].mean().to_dict()
        sc['resolution_rate'] = sc['archetype_name'].map(resolution_map)
    if 'call_cost' not in sc.columns and 'avg_duration' in sc.columns:
        sc['call_cost'] = (sc['avg_duration'] / 60 * 6.5).round(2)
    return df, sc

def teal_bar(fig):
    """Apply consistent teal/red theme to a bar chart."""
    fig.update_layout(
        paper_bgcolor=WHITE, plot_bgcolor=WHITE,
        font=dict(family="Inter", color=GRAY),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor=WHITE, bordercolor=BORDER, borderwidth=1),
    )
    fig.update_xaxes(showgrid=False, linecolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER, linecolor=BORDER)
    return fig

def styled_scatter(fig):
    fig.update_layout(
        paper_bgcolor=WHITE, plot_bgcolor="#F0FDFA",
        font=dict(family="Inter", color=GRAY),
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(bgcolor=WHITE, bordercolor=BORDER, borderwidth=1, title_font_size=11),
    )
    fig.update_xaxes(showgrid=True, gridcolor=BORDER, zeroline=False, title="")
    fig.update_yaxes(showgrid=True, gridcolor=BORDER, zeroline=False, title="")
    return fig

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.html(f"""
    <div style='text-align:center; padding: 1rem 0 0.5rem;'>
        <div style='background:{TEAL}; width:52px; height:52px; border-radius:14px;
                    display:flex; align-items:center; justify-content:center;
                    margin:0 auto 0.6rem; font-size:1.6rem;'>📞</div>
        <div style='font-weight:800; font-size:1.1rem; color:{GRAY};'>CallSense-AI</div>
        <div style='font-size:0.78rem; color:{SLATE}; font-weight:600;'>Business Intelligence Platform</div>
    </div>
    <hr style='border:none; border-top:1px solid {BORDER}; margin:0.75rem 0;'>
    """)

    menu = st.radio(
        "Navigation",
        ["🏠  Problem", "🗺️  Intent Map", "🔥  Friction Heatmap",
         "🔍  Archetype Drilldown", "⚡  Live Inference"],
        label_visibility="collapsed"
    )

    st.html(f"""
    <hr style='border:none; border-top:1px solid {BORDER}; margin:0.75rem 0;'>
    <div style='font-size:0.76rem; color:{SLATE}; padding:0 0.25rem; line-height:1.6;'>
        <div style='font-weight:700; color:{GRAY}; margin-bottom:4px;'>Model Stack</div>
        🧠 MPNet — Embeddings<br>
        🎯 BART-MNLI — Classification<br>
        🛡️ BERT-NER — PII Redaction<br>
        📐 UMAP + HDBSCAN — Clustering
    </div>
    """)

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
try:
    df, sc = load_data()
except FileNotFoundError:
    st.error("⚠️ Data files not found. Please run Notebooks 01 → 02 → 03 first.")
    st.stop()

page = menu.split("  ", 1)[-1]   # strip icon prefix

# ─────────────────────────────────────────────────────────────
# PAGE 1 — BUSINESS PROBLEM (Case Study Walkthrough)
# ─────────────────────────────────────────────────────────────
if page == "Problem":
    st.markdown(f"# 🏠 From Business Problem to Clear Requirements")
    st.html(
        f"<div style='color:{SLATE}; font-size:0.98rem; margin-bottom:1.5rem; line-height:1.6;'>"
        f"A live walkthrough of the analytical framework applied in the CallSense-AI case study.</div>"
    )

    # ── The Problem ──
    st.html(f"<div class='section-header'>⚠️ Step 1 — The Business Problem</div>")
    c1, c2 = st.columns(2)
    with c1:
        st.html(f"""
        <div class='framework-box'>
            <div class='step-label'>Symptoms Reported</div>
            <h4>What leadership saw</h4>
            <ul>
                <li>Sales revenue declining quarter-over-quarter</li>
                <li>Customer reviews trending negative</li>
                <li>Support call volume increasing</li>
            </ul>
        </div>""")
    with c2:
        st.html(f"""
        <div class='framework-box'>
            <div class='step-label'>The Real Question</div>
            <h4>What was actually driving churn?</h4>
            <ul>
                <li>Was it a product quality issue?</li>
                <li>Was it a pricing / billing friction?</li>
                <li>Was it a customer support failure?</li>
            </ul>
        </div>""")

    # ── Stakeholders ──
    st.html(f"<div class='section-header'>👥 Step 2 — Stakeholders Identified</div>")
    cols = st.columns(4)
    stakeholders = [
        ("Customer Support", "Needed visibility into ticket patterns and escalation triggers"),
        ("Sales Team",       "Needed to understand why customers were cancelling subscriptions"),
        ("Product Team",     "Needed to identify recurring technical issues from call data"),
        ("Leadership",       "Needed an ROI-linked view of operational friction costs"),
    ]
    for col, (name, desc) in zip(cols, stakeholders):
        with col:
            st.html(f"""
        <div class='framework-box'>
            <div class='step-label'>Stakeholder</div>
            <h4>{name}</h4>
            <p style='font-size:0.84rem; color:{SLATE}; margin:0; line-height:1.55;'>{desc}</p>
        </div>""")

    # ── Requirements ──
    st.html(f"<div class='section-header'>⚙️ Step 3 — Requirements Identified</div>")
    r1, r2 = st.columns(2)
    with r1:
        st.html(f"""
        <div class='framework-box'>
            <div class='step-label'>Data Requirements</div>
            <h4>What we needed to know</h4>
            <ul>
                <li>Visibility into customer intent behind every call</li>
                <li>Root causes of escalations — beyond just call volume</li>
                <li>Recurring friction patterns across support archetypes</li>
            </ul>
        </div>""")
    with r2:
        st.html(f"""
        <div class='framework-box'>
            <div class='step-label'>Technical Requirements</div>
            <h4>What we needed to build</h4>
            <ul>
                <li>NLP pipeline to analyze 1,000+ call transcripts</li>
                <li>PII redaction before any downstream processing</li>
                <li>Unsupervised clustering to surface hidden intent archetypes</li>
            </ul>
        </div>""")

    # ── Success Metrics ──
    st.html(f"<div class='section-header'>📊 Step 4 — Success Metrics</div>")

    avg_csat     = df['csat_score'].mean()
    top_archetype = sc.sort_values('Friction_Index', ascending=False).iloc[0]['archetype_name']
    top_friction  = sc.sort_values('Friction_Index', ascending=False).iloc[0]['Friction_Index']
    total_cost    = sc['call_cost'].sum()
    cancel_vol    = sc[sc['archetype_name'].str.contains('Cancell', na=False)]['Call_Volume'].sum() if 'Call_Volume' in sc.columns else 0
    total_vol     = sc['Call_Volume'].sum() if 'Call_Volume' in sc.columns else 1

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Avg CSAT Score",        f"{avg_csat:.2f} / 5")
    m2.metric("Highest-Risk Archetype", top_archetype)
    m3.metric("Peak Friction Index",   f"{top_friction:.2f}",  delta="Subscription Cancellation", delta_color="inverse")
    m4.metric("Total Call Cost",        f"${total_cost:,.0f}",  delta="Monthly exposure", delta_color="inverse")

    # ── Key Discovery ──
    st.html(f"<div class='section-header'>🔎 Key Discovery</div>")
    ka, kb, kc = st.columns(3)
    with ka:
        st.html(f"""
        <div class='insight-card critical'>
            <div class='label'>Critical Finding</div>
            <div class='value red'>38% Escalations</div>
            <div class='desc'>Driven by Subscription Cancellations — only 25% of call volume</div>
        </div>""")
    with kb:
        st.html(f"""
        <div class='insight-card critical'>
            <div class='label'>ROI Impact</div>
            <div class='value red'>$3,400+/month</div>
            <div class='desc'>Lost to Talk-Ratio Overload in technical support calls</div>
        </div>""")
    with kc:
        st.html(f"""
        <div class='insight-card'>
            <div class='label'>Privacy Compliance</div>
            <div class='value'>100% PII</div>
            <div class='desc'>Redacted via BERT-NER before any downstream analysis</div>
        </div>""")

    st.html(f"<div class='section-header'>📊 Business Case Scorecard</div>")
    sc_sorted = sc.sort_values('Friction_Index', ascending=False)
    top_row = sc_sorted.iloc[0]
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Avg CSAT Score", f"{df['csat_score'].mean():.2f} / 5")
    s2.metric("Total Calls Analysed", f"{len(df):,}")
    s3.metric("Highest-Risk Archetype", top_row['archetype_name'])
    s4.metric("Monthly Exposure", f"${sc['call_cost'].sum():,.0f}")

    fig_case = go.Figure(go.Bar(
        x=sc_sorted['archetype_name'],
        y=sc_sorted['Friction_Index'],
        marker_color=[RED if i == 0 else TEAL for i in range(len(sc_sorted))],
        text=[f"{v:.2f}" for v in sc_sorted['Friction_Index']],
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Friction Index: %{y:.2f}<extra></extra>",
    ))
    fig_case.update_layout(
        title="Higher Friction Index = Higher Business Risk",
        title_font_size=13,
        title_font_color="#64748B",
        xaxis_tickfont_size=11,
        yaxis_title="Friction Index",
        showlegend=False,
        height=360,
    )
    teal_bar(fig_case)
    st.plotly_chart(fig_case, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# LEGACY EXECUTIVE SUMMARY (unused)
# ─────────────────────────────────────────────────────────────
elif page == "__legacy_executive_summary__":
    st.markdown("# 📊 Executive Performance Scorecard")
    st.markdown(
        f"<div style='color:#64748B; font-size:0.95rem; margin-bottom:1.5rem;'>"
        f"KPI overview across all 1,000 analysed calls with archetype-level friction ranking.</div>",
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Avg CSAT Score",       f"{df['csat_score'].mean():.2f} / 5")
    m2.metric("Total Calls Analysed", f"{len(df):,}")
    m3.metric("Highest-Risk Archetype", sc.sort_values('Friction_Index', ascending=False).iloc[0]['archetype_name'])
    m4.metric("Total Monthly Exposure", f"${sc['call_cost'].sum():,.0f}")

    st.markdown(f"<div class='section-header'>📈 Friction Index by Call Archetype</div>", unsafe_allow_html=True)

    sc_sorted = sc.sort_values('Friction_Index', ascending=False)
    bar_colors = [RED if i == 0 else TEAL for i in range(len(sc_sorted))]

    fig_bar = go.Figure(go.Bar(
        x=sc_sorted['archetype_name'],
        y=sc_sorted['Friction_Index'],
        marker_color=bar_colors,
        text=[f"{v:.2f}" for v in sc_sorted['Friction_Index']],
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Friction Index: %{y:.2f}<extra></extra>",
    ))
    fig_bar.update_layout(
        title="Higher Friction Index = Higher Business Risk",
        title_font_size=13, title_font_color="#64748B",
        xaxis_tickfont_size=11, yaxis_title="Friction Index",
        showlegend=False,
    )
    teal_bar(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown(f"<div class='section-header'>📋 Full Archetype Scorecard</div>", unsafe_allow_html=True)

    def highlight_top(row):
        if row.name == sc_sorted.index[0]:
            return [f'background-color: #FEE2E2; color: {RED}; font-weight:700'] * len(row)
        return [''] * len(row)

    st.dataframe(
        sc_sorted.style.apply(highlight_top, axis=1).format({
            'Friction_Index': '{:.2f}',
            'call_cost':      '${:,.2f}',
            'csat_score':     '{:.2f}',
        }),
        use_container_width=True, height=260
    )

# ─────────────────────────────────────────────────────────────
# PAGE 2 — INTENT MAP
# ─────────────────────────────────────────────────────────────
elif page == "Intent Map":
    st.markdown("# 🗺️ Semantic Intent Clusters")
    st.html(
        f"<div style='color:{SLATE}; font-size:0.97rem; margin-bottom:1.5rem; line-height:1.6;'>"
        f"2D UMAP projection of 1,000 call transcripts. Each dot is a call; colour = AI-discovered archetype. "
        f"The AI found these groupings with <b>zero human labelling</b>.</div>"
    )

    # Colour palette matching slide theme
    palette = {
        "Subscription Cancellation":    RED,
        "Technical Troubleshooting":    TEAL,
        "Billing & Payment Disputes":   "#D97706",
        "Account Access & Security":    "#7C3AED",
        "Onboarding & Setup":           "#059669",
        "Unclassified / Noise":         "#94A3B8",
    }
    df['color'] = df['archetype_name'].map(palette).fillna("#94A3B8")

    hover_cols = [c for c in ['clean_text', 'csat_score', 'talk_ratio', 'duration_sec'] if c in df.columns]

    fig_sc = px.scatter(
        df, x='x_coord', y='y_coord',
        color='archetype_name',
        color_discrete_map=palette,
        hover_data={c: True for c in hover_cols},
        title="2D UMAP — Call Intent Landscape",
        labels={'archetype_name': 'Archetype'},
        opacity=0.75,
        size_max=8,
    )
    fig_sc.update_traces(marker=dict(size=6, line=dict(width=0.3, color='white')))

    # Annotate highest-friction cluster
    cancel_df = df[df['archetype_name'].str.contains('Cancell', na=False)]
    if not cancel_df.empty:
        cx, cy = cancel_df['x_coord'].mean(), cancel_df['y_coord'].mean()
        fig_sc.add_annotation(
            x=cx, y=cy,
            text="⚠️ 38% Escalations",
            showarrow=True, arrowhead=2,
            arrowcolor=RED, font=dict(color=RED, size=11, family="Inter"),
            bgcolor="white", bordercolor=RED, borderwidth=1.5,
            ax=60, ay=-40,
        )

    styled_scatter(fig_sc)
    fig_sc.update_layout(height=600, legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0))
    st.plotly_chart(fig_sc, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# PAGE 3 — FRICTION HEATMAP
# ─────────────────────────────────────────────────────────────
elif page == "Friction Heatmap":
    st.markdown("# 🔥 Friction Heatmap — Archetype × KPI")
    st.html(
        f"<div style='color:{SLATE}; font-size:0.97rem; margin-bottom:1.5rem; line-height:1.6;'>"
        f"A cross-KPI risk matrix. Darker red = higher friction / business risk. "
        f"Read row-by-row to identify which archetype needs intervention first.</div>"
    )

    sc_sorted = sc.sort_values('Friction_Index', ascending=False)
    top_row = sc_sorted.iloc[0]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Avg CSAT Score", f"{df['csat_score'].mean():.2f} / 5")
    m2.metric("Total Calls Analysed", f"{len(df):,}")
    m3.metric("Highest-Risk Archetype", top_row['archetype_name'])
    m4.metric("Total Monthly Exposure", f"${sc['call_cost'].sum():,.0f}")

    # Build matrix from scorecard
    kpi_cols = {c: c for c in ['Friction_Index', 'call_cost', 'csat_score',
                                'escalation_rate', 'avg_duration', 'resolution_rate']
                if c in sc.columns}

    matrix_df = sc.set_index('archetype_name')[list(kpi_cols.keys())]
    # Normalise 0-1 per column for heatmap coloring
    normed = (matrix_df - matrix_df.min()) / (matrix_df.max() - matrix_df.min() + 1e-9)

    # Invert csat & resolution so that "bad" is always dark
    for col in ['csat_score', 'resolution_rate']:
        if col in normed.columns:
            normed[col] = 1 - normed[col]

    pretty_labels = {
        'Friction_Index':   'Friction Index',
        'call_cost':        'Call Cost ($)',
        'csat_score':       'Low CSAT ↑',
        'escalation_rate':  'Escalation Rate',
        'avg_duration':     'Avg Duration',
        'resolution_rate':  'Unresolved Rate ↑',
    }

    fig_heat = go.Figure(go.Heatmap(
        z=normed.values,
        x=[pretty_labels.get(c, c) for c in normed.columns],
        y=normed.index.tolist(),
        colorscale=[[0, TEAL_L], [0.5, "#FDE68A"], [1, RED]],
        showscale=True,
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:.2f}<extra></extra>",
        text=[[f"{matrix_df.iloc[i, j]:.2f}" for j in range(len(normed.columns))]
              for i in range(len(normed))],
        texttemplate="%{text}",
        textfont=dict(size=11, family="Inter"),
    ))
    fig_heat.update_layout(
        height=420,
        paper_bgcolor=WHITE, plot_bgcolor=WHITE,
        font=dict(family="Inter", color=GRAY),
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(side="top"),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.html(f"<div class='section-header'>📈 Friction Index by Call Archetype</div>")
    fig_bar = go.Figure(go.Bar(
        x=sc_sorted['archetype_name'],
        y=sc_sorted['Friction_Index'],
        marker_color=[RED if i == 0 else TEAL for i in range(len(sc_sorted))],
        text=[f"{v:.2f}" for v in sc_sorted['Friction_Index']],
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Friction Index: %{y:.2f}<extra></extra>",
    ))
    fig_bar.update_layout(
        title="Higher Friction Index = Higher Business Risk",
        title_font_size=13, title_font_color="#64748B",
        xaxis_tickfont_size=11, yaxis_title="Friction Index",
        showlegend=False, height=360,
    )
    teal_bar(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)

    # Ranked verdict
    st.html(f"<div class='section-header'>🏆 Intervention Priority Ranking</div>")
    ranked = sc.sort_values('Friction_Index', ascending=False).reset_index(drop=True)
    for i, row in ranked.iterrows():
        badge_cls = "badge-high" if i == 0 else "badge-medium" if i == 1 else "badge-low"
        badge_txt = "HIGH RISK" if i == 0 else "MEDIUM" if i <= 2 else "LOW"
        cost_str  = f"${row['call_cost']:,.0f}" if 'call_cost' in row else "—"
        fri_str   = f"{row['Friction_Index']:.2f}"
        st.html(f"""
        <div class='insight-card {"critical" if i == 0 else ""}'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <span class='badge {badge_cls}'>{badge_txt}</span>
                    <span style='font-weight:700; font-size:0.95rem; margin-left:8px;'>{row['archetype_name']}</span>
                </div>
                <div style='text-align:right; font-size:0.82rem; color:{SLATE};'>
                    Friction: <b style='color:{"#DC2626" if i==0 else TEAL};'>{fri_str}</b> &nbsp;|&nbsp; Cost: <b>{cost_str}</b>
                </div>
            </div>
        </div>""")

    st.html(f"<div class='section-header'>📋 Full Archetype Scorecard</div>")

    def highlight_top(row):
        if row.name == sc_sorted.index[0]:
            return [f'background-color: #FEE2E2; color: {RED}; font-weight:700'] * len(row)
        return [''] * len(row)

    formatters = {'Friction_Index': '{:.2f}'}
    if 'call_cost' in sc_sorted.columns:
        formatters['call_cost'] = '${:,.2f}'
    if 'csat_score' in sc_sorted.columns:
        formatters['csat_score'] = '{:.2f}'
    if 'avg_duration' in sc_sorted.columns:
        formatters['avg_duration'] = '{:.0f}s'
    if 'escalation_rate' in sc_sorted.columns:
        formatters['escalation_rate'] = '{:.1%}'
    if 'resolution_rate' in sc_sorted.columns:
        formatters['resolution_rate'] = '{:.1%}'

    st.dataframe(
        sc_sorted.style.apply(highlight_top, axis=1).format(formatters),
        use_container_width=True, height=260
    )

# ─────────────────────────────────────────────────────────────
# PAGE 4 — ARCHETYPE DRILLDOWN
# ─────────────────────────────────────────────────────────────
elif page == "Archetype Drilldown":
    st.markdown("# 🔍 Archetype Deep Dive")
    st.html(
        f"<div style='color:{SLATE}; font-size:0.97rem; margin-bottom:1.5rem; line-height:1.6;'>"
        f"Select an archetype to inspect call-level behaviour, customer sentiment, and resolution patterns.</div>"
    )

    archetypes = sorted(df['archetype_name'].dropna().unique().tolist())
    selected   = st.selectbox("Select Archetype", archetypes)

    sub     = df[df['archetype_name'] == selected]
    sc_row  = sc[sc['archetype_name'] == selected]

    ka, kb, kc, kd = st.columns(4)
    ka.metric("Call Volume",     f"{len(sub):,}")
    kb.metric("Avg CSAT",        f"{sub['csat_score'].mean():.2f}")
    kc.metric("Avg Duration",    f"{sub['duration_sec'].mean():.0f}s")
    if 'resolved' in sub.columns:
        kd.metric("Resolution Rate", f"{sub['resolved'].mean() * 100:.1f}%")
    if not sc_row.empty:
        st.metric("Friction Index", f"{sc_row.iloc[0]['Friction_Index']:.2f}")

    col_l, col_r = st.columns([1.1, 1])

    with col_l:
        st.html(f"<div class='section-header'>📊 CSAT Distribution vs. Overall Mean</div>")
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=df['csat_score'], name="All Calls", opacity=0.4,
            marker_color=TEAL, nbinsx=20,
        ))
        fig_hist.add_trace(go.Histogram(
            x=sub['csat_score'], name=selected, opacity=0.85,
            marker_color=RED if selected == sc.sort_values('Friction_Index', ascending=False).iloc[0]['archetype_name'] else TEAL,
            nbinsx=20,
        ))
        fig_hist.add_vline(
            x=df['csat_score'].mean(), line_dash="dot", line_color="#94A3B8",
            annotation_text=f"Overall mean {df['csat_score'].mean():.2f}",
            annotation_font_size=10,
        )
        fig_hist.update_layout(
            barmode='overlay', height=320,
            paper_bgcolor=WHITE, plot_bgcolor=WHITE,
            font=dict(family="Inter"), margin=dict(l=5, r=5, t=10, b=5),
            legend=dict(orientation="h", y=1.05),
            yaxis_title="# Calls", xaxis_title="CSAT Score",
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_r:
        st.html(f"<div class='section-header'>📞 Talk Ratio Distribution</div>")
        if 'talk_ratio' in sub.columns:
            fig_box = go.Figure()
            fig_box.add_trace(go.Box(
                y=df['talk_ratio'], name="All Calls",
                marker_color=TEAL, line_color=TEAL, opacity=0.5,
            ))
            fig_box.add_trace(go.Box(
                y=sub['talk_ratio'], name=selected,
                marker_color=RED, line_color=RED,
            ))
            fig_box.add_hline(y=1.1, line_dash="dot", line_color="#D97706",
                               annotation_text="Risk threshold (1.1)", annotation_font_size=10)
            fig_box.update_layout(
                height=320,
                paper_bgcolor=WHITE, plot_bgcolor=WHITE,
                font=dict(family="Inter"), margin=dict(l=5, r=5, t=10, b=5),
                yaxis_title="Talk Ratio (Agent / Customer)",
                legend=dict(orientation="h", y=1.05),
            )
            st.plotly_chart(fig_box, use_container_width=True)

    # Sample transcripts
    st.html(f"<div class='section-header'>📝 Sample Redacted Transcripts</div>")
    text_col = next((c for c in ['clean_text', 'sanitized_text', 'transcript'] if c in df.columns), None)
    if text_col:
        samples = sub[text_col].dropna().sample(min(4, len(sub)), random_state=42)
        for i, txt in enumerate(samples, 1):
            st.html(f"""
            <div class='drilldown-card'>
                <span style='font-weight:700; font-size:0.7rem; text-transform:uppercase;
                             letter-spacing:0.08em; color:{TEAL_D};'>Call Sample {i}</span><br>
                {str(txt)[:300]}{"…" if len(str(txt)) > 300 else ""}
            </div>""")

# ─────────────────────────────────────────────────────────────
# PAGE 5 — LIVE INFERENCE
# ─────────────────────────────────────────────────────────────
elif page == "Live Inference":
    st.markdown("# ⚡ Real-Time Call Analyzer")
    st.html(
        f"<div style='color:{SLATE}; font-size:0.97rem; margin-bottom:1.5rem; line-height:1.6;'>"
        f"Paste a raw call transcript. The AI pipeline will redact PII, detect intent, score friction, "
        f"and recommend an action — in seconds.</div>"
    )

    col_in, col_out = st.columns([1.1, 1])

    with col_in:
        st.html(f"<div class='section-header'>✍️ Input</div>")
        raw_input = st.text_area(
            "Paste call transcript here:",
            placeholder="e.g. Hi, my name is John Smith, account ACC-98432. I've been charged twice this month and I want to cancel my subscription immediately...",
            height=180, label_visibility="collapsed"
        )
        c1, c2 = st.columns(2)
        t_ratio  = c1.slider("Agent Talk Ratio", 0.0, 2.0, 1.0, 0.05,
                              help="Ratio of agent words to customer words. >1.1 = agent over-talking")
        duration = c2.number_input("Call Duration (seconds)", min_value=30, max_value=3600, value=300, step=30)
        run_btn = st.button("🔍 Analyse Call", use_container_width=True, type="primary")

    with col_out:
        st.html(f"<div class='section-header'>📋 Call Report Card</div>")

        if run_btn and raw_input.strip():
            with st.spinner("Running NLP pipeline…"):
                engine = load_engine()
                res    = engine.analyze_call(raw_input, talk_ratio=t_ratio, duration=int(duration))

            risk = res['risk_level']
            badge_cls = {"HIGH": "badge-high", "MEDIUM": "badge-medium", "LOW": "badge-low"}[risk]
            risk_color = {"HIGH": RED, "MEDIUM": "#D97706", "LOW": "#059669"}[risk]

            # Intent confidence chart
            all_scores = res.get('all_scores', {})
            if all_scores:
                scores_df = pd.DataFrame(list(all_scores.items()), columns=['Intent', 'Score'])
                scores_df = scores_df.sort_values('Score', ascending=True)
                fig_conf = go.Figure(go.Bar(
                    x=scores_df['Score'], y=scores_df['Intent'], orientation='h',
                    marker_color=[RED if i == scores_df.index[-1] else TEAL for i in scores_df.index],
                    text=[f"{v:.1%}" for v in scores_df['Score']], textposition='outside',
                ))
                fig_conf.update_layout(
                    height=260, paper_bgcolor=WHITE, plot_bgcolor=WHITE,
                    font=dict(family="Inter", size=11), margin=dict(l=5, r=60, t=10, b=5),
                    xaxis=dict(range=[0, 1.1], showgrid=False, showticklabels=False),
                    yaxis=dict(showgrid=False), showlegend=False,
                    title="Intent Confidence Scores", title_font_size=12,
                )
                st.plotly_chart(fig_conf, use_container_width=True)

            # Result cards
            st.html(f"""
            <div class='insight-card {"critical" if risk=="HIGH" else ""}' style='margin-top:0.5rem;'>
                <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                    <div>
                        <div class='label'>Detected Intent</div>
                        <div style='font-weight:700; font-size:0.95rem;'>{res['intent']}</div>
                    </div>
                    <span class='badge {badge_cls}'>{risk} RISK</span>
                </div>
                <div style='margin-top:0.6rem; display:flex; gap:1.5rem;'>
                    <div>
                        <div class='label'>Friction Score</div>
                        <div style='font-weight:700; color:{risk_color};'>{res['risk_score']} / 100</div>
                    </div>
                    <div>
                        <div class='label'>Confidence</div>
                        <div style='font-weight:700;'>{res['confidence']:.1%}</div>
                    </div>
                </div>
            </div>""")

            # Recommended action
            actions = {
                "Subscription Cancellation & Account Closure":
                    "🔴 Escalate immediately to the Retention Team. Offer a personalised discount or pause option.",
                "Technical Support & Error Troubleshooting":
                    "🟡 Route to Tier-2 Support. Flag for talk-ratio coaching if agent ratio > 1.1.",
                "Billing, Payment, and Invoice Disputes":
                    "🟡 Transfer to Billing Specialist. Verify charge history before call ends.",
                "Account Access, Security & Hacking":
                    "🔴 Escalate to Security Team immediately. Follow account lockdown protocol.",
                "Onboarding, Setup & Initial Training":
                    "🟢 Send post-call onboarding resources. Schedule a follow-up check-in.",
                "General Inquiry & Miscellaneous Questions":
                    "🟢 Standard resolution. Log and close. No escalation required.",
            }
            action = actions.get(res['intent'], "🟢 Standard handling. Log and close.")
            st.html(f"""
            <div class='framework-box' style='margin-top:0.75rem;'>
                <div class='step-label'>Recommended Action</div>
                <div style='font-size:0.88rem; color:{GRAY}; margin-top:4px;'>{action}</div>
            </div>""")

            # Redacted transcript
            with st.expander("🛡️ View Redacted Transcript (PII Removed)"):
                st.html(f"<div style='font-size:0.85rem; line-height:1.75; color:{SLATE};'>{res['clean_text']}</div>")

        elif run_btn:
            st.warning("Please paste a transcript before running the analysis.")
        else:
            st.html(f"""
            <div style='height:220px; display:flex; flex-direction:column;
                        align-items:center; justify-content:center;
                        border:2px dashed {BORDER}; border-radius:12px;
                        color:{SLATE}; font-size:0.92rem; text-align:center; gap:8px;'>
                <div style='font-size:2rem;'>⚡</div>
                <div>Paste a transcript and click <b>Analyse Call</b></div>
                <div style='font-size:0.8rem; color:{SLATE_L};'>PII will be automatically redacted before analysis</div>
            </div>""")
