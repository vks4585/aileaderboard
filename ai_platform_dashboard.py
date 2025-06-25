
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🌍 AI Platforms Super Dashboard", layout="wide")

df = pd.read_csv("ai_models_data_enhanced.csv")

# Sidebar filters
st.sidebar.title("🔍 Filter Models")
source_type = st.sidebar.selectbox("Source", ["All", "Startup", "Big Tech"])
max_score = st.sidebar.slider("Max Intelligence Score", 0, 120, 100)
context_options = st.sidebar.multiselect("Context Window", sorted(df['ContextWindow'].dropna().unique()))

# Filter logic
if source_type == "Startup":
    df = df[df["IsStartup"] == True]
elif source_type == "Big Tech":
    df = df[df["IsStartup"] == False]

if context_options:
    df = df[df["ContextWindow"].isin(context_options)]

df = df[df["IntelligenceScore"] <= max_score]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Overview", "📊 Compare", "🚀 Startups", "📈 Trends"])

with tab1:
    st.title("🏠 AI Platforms Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Models", len(df))
    col2.metric("Startups", df['IsStartup'].sum())
    col3.metric("Top Creator", df['Creator'].value_counts().idxmax())

    st.subheader("🌐 Models by Creator")
    fig = px.bar(df['Creator'].value_counts().reset_index(), x='index', y='Creator',
                 labels={'index': 'Creator', 'Creator': 'Model Count'}, title="Models per Creator")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.title("📊 Compare Models")
    selected_models = st.multiselect("Select Models to Compare", options=df['ModelName'].unique())
    if selected_models:
        st.dataframe(df[df['ModelName'].isin(selected_models)][['ModelName', 'Creator', 'ContextWindow', 'IntelligenceScore']])

with tab3:
    st.title("🚀 Innovative Startups")
    startups = df[df["IsStartup"]]
    st.dataframe(startups[['ModelName', 'Creator', 'ContextWindow', 'IntelligenceScore']])
    fig2 = px.box(startups, x="Creator", y="IntelligenceScore", title="Score Spread Across Startups")
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.title("📈 Model Launch Patterns")
    recent_models = df[df['ModelName'].str.contains("2025", na=False)]
    st.subheader("🆕 Recently Launched in 2025")
    st.dataframe(recent_models[['ModelName', 'Creator', 'ContextWindow', 'IntelligenceScore']])
