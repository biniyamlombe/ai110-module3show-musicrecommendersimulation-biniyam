import streamlit as st
import pandas as pd
import sys
import os

# Add project root to sys.path so 'src' can be imported when running via Streamlit
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.recommender import load_songs, recommend_songs

# Configure the Streamlit page
st.set_page_config(page_title="VibeFinder 1.0", page_icon="🎧", layout="centered")

st.title("🎧 VibeFinder 1.0")
st.write("Welcome to the interactive Music Recommender Simulation! Tweak your preferences below to dynamically generate a playlist.")

# Cache the data loading so it doesn't read the CSV on every slider move
@st.cache_data
def get_songs():
    return load_songs("data/songs.csv")

songs = get_songs()

# Sidebar for User Profile Inputs
st.sidebar.header("Your Taste Profile")
name = st.sidebar.text_input("What's your name?", value="Guest")
genre = st.sidebar.selectbox("Favorite Genre", options=["pop", "lofi", "metal", "rock", "classical", "edm", "hip hop", "acoustic", "reggae", "jazz"])
mood = st.sidebar.selectbox("Current Mood", options=["happy", "chill", "sad", "energetic", "focus", "romantic"])

st.sidebar.subheader("Audio Features")
energy = st.sidebar.slider("Target Energy", 0.0, 1.0, 0.5, 0.05)
valence = st.sidebar.slider("Target Happiness (Valence)", 0.0, 1.0, 0.5, 0.05)

st.sidebar.subheader("Picky Listener Settings")
priority = st.sidebar.radio("What matters most to you?", options=["Balanced", "Exact Genre", "Exact Energy"])

# Determine weights based on priority
weight_genre = 1.0
weight_energy = 2.0
if priority == "Exact Genre":
    weight_genre = 5.0
    weight_energy = 0.5
elif priority == "Exact Energy":
    weight_genre = 0.0
    weight_energy = 5.0

# Build the user profile dictionary
user_profile = {
    "name": name,
    "genre": genre,
    "mood": mood,
    "energy": energy,
    "valence": valence,
    "weight_genre": weight_genre,
    "weight_energy": weight_energy
}

st.header(f"Recommendations for {name}")

# Run the core recommendation engine
recommendations = recommend_songs(user_profile, songs, k=5)

# Display results
if recommendations:
    # Convert results to a list of dicts for pandas DataFrame
    df_data = []
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        df_data.append({
            "Rank": i,
            "Title": song.get("title", "Unknown"),
            "Artist": song.get("artist", "Unknown"),
            "Score": f"{score:.2f}",
            "Why we picked this": explanation
        })
    
    df = pd.DataFrame(df_data)
    
    # Render table without the default pandas index
    st.table(df.set_index("Rank"))
    
    st.success("✨ Playlist Generated! Adjust the sliders on the left to see these results update in real-time.")
else:
    st.warning("No songs found matching your criteria.")
