import streamlit as st
from transformers import pipeline
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# ---- Spotify Setup ----
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET))

# ---- Load Emotion Classifier ----
@st.cache_resource
def load_emotion_classifier():
    return pipeline(
        "text-classification", 
        model="j-hartmann/emotion-english-distilroberta-base", 
        top_k=1
    )

classifier = load_emotion_classifier()

# ---- Emotion to Mood Mapping ----
emotion_to_mood = {
    "joy": "happy",
    "sadness": "sad",
    "anger": "intense",
    "fear": "ambient",
    "love": "romantic",
    "surprise": "experimental",
    "content": "chill",
    "admiration": "inspirational",
    "amusement": "upbeat"
}

# ---- Get Spotify Playlist ----
def get_playlist_link(mood_keyword):
    try:
        results = sp.search(q=f"{mood_keyword} playlist", type='playlist', limit=1)
        if results['playlists']['items']:
            return results['playlists']['items'][0]['external_urls']['spotify']
        return None
    except Exception as e:
        st.error(f"Spotify API error: {e}")
        return None

# ---- Streamlit UI ----
st.title("🎧 Mood-Based Music Recommender")
st.write("Tell me how you feel, and I'll recommend a Spotify playlist that matches your vibe!")

user_input = st.text_area("How are you feeling right now?")

if st.button("Find Playlist") and user_input.strip():
    with st.spinner("Analyzing your mood..."):
        try:
            result = classifier(user_input)
            st.write("🔍 Classifier output:", result)  # Optional: comment out if not needed

            # Handle possible nested format: [[{'label': ..., 'score': ...}]]
            if isinstance(result, list):
                if isinstance(result[0], dict) and 'label' in result[0]:
                    emotion_label = result[0]['label'].lower()
                elif isinstance(result[0], list) and isinstance(result[0][0], dict) and 'label' in result[0][0]:
                    emotion_label = result[0][0]['label'].lower()
                else:
                    raise ValueError("Unrecognized classifier output format.")
            else:
                raise ValueError("Classifier output is not a list.")

            st.success(f"Detected emotion: **{emotion_label.capitalize()}**")

            mood_keyword = emotion_to_mood.get(emotion_label, "chill")
            playlist_link = get_playlist_link(mood_keyword)

            if playlist_link:
                st.markdown(f"### 🎵 Recommended Playlist for a **{mood_keyword}** mood:")
                st.markdown(f"[▶️ Open Playlist in Spotify]({playlist_link})")
            else:
                st.warning("Couldn't find a suitable playlist. Try expressing your mood differently.")

        except Exception as e:
            st.error(f"Error detecting emotion: {e}")

# ---- Footer ----
st.markdown("---")
st.caption("Built with 🤖 Transformers, 🎶 Spotify, and ❤️ Streamlit")

