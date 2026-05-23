import streamlit as st
import pandas as pd
import plotly.express as px
import time
import base64

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Spotify Analytics Dashboard",
    page_icon="🎵",
    layout="wide"
)

# =====================================================
# HIDE STREAMLIT DEFAULT UI
# =====================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD IMAGE FUNCTION
# =====================================================

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# =====================================================
# BACKGROUND IMAGE
# =====================================================

bg_img = get_base64("assets/spotify_bg.jpg")

# =====================================================
# LOADING SCREEN
# =====================================================

loading_container = st.empty()

loading_html = f"""
<style>

.loading-screen {{
    background-image: url("data:image/jpg;base64,{bg_img}");
    background-size: cover;
    background-position: center;
    height: 90vh;
    border-radius: 25px;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.loading-box {{
    background: rgba(0,0,0,0.65);
    padding: 50px;
    border-radius: 25px;
    text-align: center;
    backdrop-filter: blur(12px);
    box-shadow: 0px 0px 40px rgba(29,185,84,0.5);
}}

.spotify-title {{
    color: #1DB954;
    font-size: 60px;
    font-weight: bold;
    text-shadow: 0 0 20px #1DB954;
}}

.loading-text {{
    color: white;
    font-size: 24px;
    margin-top: 15px;
}}

.loader {{
    margin-top: 30px;
    border: 6px solid #222;
    border-top: 6px solid #1DB954;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    animation: spin 1s linear infinite;
    margin-left: auto;
    margin-right: auto;
}}

@keyframes spin {{
    100% {{
        transform: rotate(360deg);
    }}
}}

</style>

<div class="loading-screen">

    <div class="loading-box">

        <div class="spotify-title">
            🎵 Spotify Analytics
        </div>

        <div class="loading-text">
            Loading your music universe...
        </div>

        <div class="loader"></div>

    </div>

</div>
"""

loading_container.markdown(
    loading_html,
    unsafe_allow_html=True
)

time.sleep(3)

loading_container.empty()

# =====================================================
# CUSTOM SPOTIFY THEME
# =====================================================

st.markdown("""
<style>

/* Main App */
.stApp {
    background: linear-gradient(to bottom right, #0f0f0f, #121212);
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #121212;
    border-right: 1px solid #1DB954;
}

/* Sidebar Text */
[data-testid="stSidebar"] * {
    color: white;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: rgba(24,24,24,0.85);
    border: 1px solid rgba(29,185,84,0.5);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 0px 15px rgba(29,185,84,0.2);
    transition: 0.3s;
}

[data-testid="metric-container"]:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 25px rgba(29,185,84,0.5);
}

/* Charts */
.plot-container {
    border-radius: 20px;
    overflow: hidden;
}

/* Titles */
h1, h2, h3 {
    color: #1DB954;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #1DB954;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    columns_needed = [
        'track_name',
        'artists',
        'popularity',
        'danceability',
        'energy',
        'acousticness',
        'valence',
        'tempo',
        'track_genre'
    ]

    df = pd.read_excel(
        "spotify-tracks-dataset.xlsx",
        usecols=columns_needed
    )

    # Better random sample
    df = df.sample(min(20000, len(df)))

    return df

df = load_data()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown("""
<h1 style='color:#1DB954; text-align:center;'>
🎵 Spotify
</h1>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🎧 Genre Selection")

genre_list = sorted(df['track_genre'].dropna().unique())

selected_genre = st.sidebar.radio(
    "Choose Genre",
    genre_list
)

filtered_df = df[df['track_genre'] == selected_genre]

# =====================================================
# HERO SECTION
# =====================================================

st.markdown("""
<div style="
    background: linear-gradient(to right, #1DB954, #121212);
    padding: 40px;
    border-radius: 25px;
    margin-bottom: 30px;
">

<h1 style="
    color:white;
    font-size:55px;
">
🎵 Spotify Analytics Dashboard
</h1>

<p style="
    color:white;
    font-size:22px;
">
Discover music trends, artist popularity and audio insights
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# KPI CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🎵 Total Songs",
        len(filtered_df)
    )

with col2:
    st.metric(
        "🎤 Artists",
        filtered_df['artists'].nunique()
    )

with col3:
    st.metric(
        "🔥 Avg Popularity",
        round(filtered_df['popularity'].mean(), 2)
    )

with col4:
    st.metric(
        "⚡ Avg Energy",
        round(filtered_df['energy'].mean(), 2)
    )

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# ROW 1
# =====================================================

col1, col2 = st.columns(2)

# -----------------------------------------------------
# TOP ARTISTS
# -----------------------------------------------------

with col1:

    top_artists = (
        filtered_df['artists']
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_artists.columns = ['Artist', 'Songs']

    fig_artist = px.bar(
        top_artists,
        x='Artist',
        y='Songs',
        color='Songs',
        template='plotly_dark',
        title='🎤 Top Artists'
    )

    fig_artist.update_layout(
        paper_bgcolor='#181818',
        plot_bgcolor='#181818',
        font_color='white',
        height=400
    )

    st.plotly_chart(
        fig_artist,
        use_container_width=True
    )

# -----------------------------------------------------
# POPULARITY DISTRIBUTION
# -----------------------------------------------------

with col2:

    fig_popularity = px.histogram(
        filtered_df,
        x='popularity',
        nbins=30,
        template='plotly_dark',
        title='📈 Popularity Distribution'
    )

    fig_popularity.update_layout(
        paper_bgcolor='#181818',
        plot_bgcolor='#181818',
        font_color='white',
        height=400
    )

    st.plotly_chart(
        fig_popularity,
        use_container_width=True
    )

# =====================================================
# ROW 2
# =====================================================

col3, col4 = st.columns(2)

# -----------------------------------------------------
# AUDIO FEATURES
# -----------------------------------------------------

with col3:

    features = [
        'danceability',
        'energy',
        'acousticness',
        'valence'
    ]

    feature_avg = (
        filtered_df[features]
        .mean()
        .reset_index()
    )

    feature_avg.columns = ['Feature', 'Value']

    fig_radar = px.line_polar(
        feature_avg,
        r='Value',
        theta='Feature',
        line_close=True,
        template='plotly_dark',
        title='🌊 Audio Feature Analysis'
    )

    fig_radar.update_traces(fill='toself')

    fig_radar.update_layout(
        paper_bgcolor='#181818',
        font_color='white',
        height=400
    )

    st.plotly_chart(
        fig_radar,
        use_container_width=True
    )

# -----------------------------------------------------
# ENERGY VS DANCEABILITY
# -----------------------------------------------------

with col4:

    sample_df = filtered_df.sample(
        min(2000, len(filtered_df))
    )

    fig_scatter = px.scatter(
        sample_df,
        x='energy',
        y='danceability',
        color='popularity',
        hover_data=['track_name', 'artists'],
        template='plotly_dark',
        title='⚡ Energy vs Danceability'
    )

    fig_scatter.update_layout(
        paper_bgcolor='#181818',
        plot_bgcolor='#181818',
        font_color='white',
        height=400
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<hr style="border:1px solid #1DB954;">

<div style="
    text-align:center;
    color:gray;
    padding:20px;
">

🎵 Spotify Inspired Dashboard | Built with Streamlit & Plotly

</div>
""", unsafe_allow_html=True)