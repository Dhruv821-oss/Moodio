
## 🎧 Mood-Based Music Recommender

A smart Streamlit web app that recommends **Spotify playlists based on your current mood**, powered by **Hugging Face Transformers** and the **Spotify API**.

### 💡 How it works

1. You describe how you're feeling in natural language (e.g., *"I'm feeling anxious but hopeful"*).
2. An emotion classifier (`j-hartmann/emotion-english-distilroberta-base`) detects your underlying emotion.
3. The app maps your emotion to a relevant mood (e.g., *fear → ambient*, *joy → happy*).
4. It fetches a curated Spotify playlist matching your mood and gives you a direct link to listen.

### 🚀 Tech Stack

* 🧠 **Hugging Face Transformers** for emotion detection
* 🎶 **Spotify API** for playlist recommendations
* 🖥️ **Streamlit** for building the user interface

### 🔧 Setup Instructions

1. Clone the repo.
2. Install dependencies with `pip install -r requirements.txt`.
3. Set your Spotify API credentials:

   ```python
   SPOTIPY_CLIENT_ID = 'your_client_id'
   SPOTIPY_CLIENT_SECRET = 'your_client_secret'
   ```
4. Run the app:

   ```bash
   streamlit run app.py
   ```

### 📝 Example Input

> "I feel nostalgic and hopeful about the future."

🎧 Output: A Spotify playlist that matches the mood of **content** or **inspirational**.

