import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime



st.set_page_config(
    page_title="Spotify Feature Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    .stApp, .main {
        background-color: #191414 !important;
    }

    div[data-testid="stToolbar"] {
        background-color: #121212 !important;
    }

    .main * {
        color: #FFFFFF !important;
        font-family: "Arial", sans-serif;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
    }

    button[role="tab"] {
        background-color: transparent !important;
        color: #FFFFFF !important;
        font-weight: 600;
        border: none !important;
        padding: 0.4rem 1rem !important;
        margin-right: 1rem;
    }

    button[role="tab"]:hover {
        color: #1DB954 !important;
    }

    button[role="tab"][aria-selected="true"] {
        color: #FFFFFF !important;     /* <-- ahora blanco */
        font-weight: 700;
        border: none !important;
        border-bottom: 3px solid #1DB954 !important;
        box-shadow: none !important;
    }

    div[data-baseweb="tab-highlight"] {
        background-color: transparent !important;
        height: 0px !important;
    }

    div[data-baseweb="tab-list"] {
        border-bottom: none !important;
    }

    [data-baseweb="tab"]::before {
        background-color: transparent !important;
    }

    h1, h2, h3, h4 {
        color: #1DB954 !important;
    }

    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:#1DB954; font-weight:700;'>Spotify Feature Explorer</h1>", unsafe_allow_html=True)

# CARGA DE DATOS
@st.cache_data
def load_data(path="/content/SpotifyFeatures.csv"):
    return pd.read_csv(path)

df = load_data()



# MÉTRICAS PRINCIPALES
st.header("Main metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Artists", f"{df['artist_name'].nunique():,}")

with col2:
    st.metric("Total songs", f"{df['track_name'].nunique():,}")

with col3:
    st.metric("Total Genres", f"{df['genre'].nunique():,}")

with col4:
    st.metric("Average acousticness", f"{df['acousticness'].mean()*100:.1f}%")

st.markdown("---")




# TABS – 3 SECCIONES PRINCIPALES
tab1, tab2, tab3 = st.tabs([
    "Spotify Insights",
    "Let's Dance",
    "Music Info"
])




# TAB 1 – MÉTRICAS AGRUPADAS
with tab1:
    st.subheader("Metric Analysis by Group")

    c1, c2 = st.columns(2)

    with c1:
        group_col = st.selectbox(
            "Group by:",
            ["genre", "artist_name", "mode", "time_signature"]
        )

    with c2:
        metric_col = st.selectbox(
            "Metric:",
            ["popularity", "duration_ms", "danceability", "energy", "valence", "tempo"]
        )

    df_group = df.groupby(group_col)[metric_col].mean().reset_index()

    fig = px.line(
        df_group,
        x=group_col,
        y=metric_col,
        title=f"Average {metric_col} by {group_col}",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")



# TAB 2 – ENERGY VS DANCEABILITY
with tab2:
    st.subheader("Energy vs Danceability")

    c1, c2 = st.columns(2)

    with c1:
        genre_filter = st.multiselect(
            "Filter by genre:",
            sorted(df["genre"].unique())
        )

    with c2:
        min_popularity = st.slider(
            "Minimum popularity:",
            int(df["popularity"].min()),
            int(df["popularity"].max()),
            value=int(df["popularity"].median())
        )

    df_filtered = df.copy()

    if genre_filter:
        df_filtered = df_filtered[df_filtered["genre"].isin(genre_filter)]

    df_filtered = df_filtered[df_filtered["popularity"] >= min_popularity]

    fig2 = px.scatter(
        df_filtered,
        x="danceability",
        y="energy",
        color="genre",
        size="popularity",
        hover_data=["artist_name", "track_name"],
        title="Energy vs Danceability (filtered)"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")



# TAB 3 – HISTOGRAMAS
with tab3:
    st.subheader("Distribution of Track Metrics")

    h1, h2 = st.columns(2)

    with h1:
        metric_hist = st.selectbox(
            "Metric:",
            ["popularity", "tempo", "duration_ms"]
        )

    with h2:
        genre_hist = st.multiselect(
            "Filter by genre (histogram):",
            sorted(df["genre"].unique())
        )

    df_hist = df.copy()

    if genre_hist:
        df_hist = df_hist[df_hist["genre"].isin(genre_hist)]

    fig3 = px.histogram(
        df_hist,
        x=metric_hist,
        nbins=40,
        color="genre" if genre_hist else None,
        title=f"Distribution of {metric_hist}"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")