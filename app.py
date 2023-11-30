# app.py

import streamlit as st
import os
import io  # Import io for BytesIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pydub import AudioSegment  # Import AudioSegment from pydub
from song import get_token, search_for_track, parse_song, get_audio_content

# Load Spotify API credentials from environment variables
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-library-read"
))

# Streamlit App
st.title("Spotify Song Player")

# Get Spotify access token
token = get_token()

# Input text area for the user to input songs
user_input = st.text_area("Enter songs (one per line):", "")

# Process user input and get a random song
if st.button("Get Random Song"):
    song_artist = parse_song(user_input)
    if song_artist[0] and song_artist[1]:
        artist_name, song_name = song_artist
        st.write(f"Searching for: {song_name} by {artist_name}")
        spotify_url = search_for_track(token, artist_name, song_name)
        st.write(f"Spotify URL: {spotify_url}")  # Add this line
        if spotify_url:
            st.success("Song Found! Play it below:")
            track_id = sp.search(q=f"{song_name} {artist_name}", type='track')['tracks']['items'][0]['id']
            track_info = sp.track(track_id)
            preview_url = track_info['preview_url']
            
            # Get audio content
            audio_content = get_audio_content(preview_url)
            st.write(f"Audio Content: {audio_content}")  # Add this line
            
            if audio_content:
                # Convert to OGG format using pydub
                audio = AudioSegment.from_file(io.BytesIO(audio_content))
                audio_content_ogg = audio.export(format='ogg').read()
                
                # Play the audio in the Streamlit app
                st.audio(audio_content_ogg, format='audio/ogg', start_time=0)
            else:
                st.warning("No preview available for this song.")
        else:
            st.warning("Song not found on Spotify.")

# Add some example songs
st.subheader("Example Songs:")
example_list = """
"Shape of You" - Ed Sheeran
"Blinding Lights" - The Weeknd
"Dance Monkey" - Tones and I
"Watermelon Sugar" - Harry Styles
"Savage Love" - Jawsh 685, Jason Derulo
"""
st.text(example_list)

st.write("Copy and paste examples above into the input box and click 'Get Random Song' to play.")
