from flask import Flask, render_template
from trial import get_token, search_for_track, parse_song

app = Flask(__name__)

# Load environment variables from .env file
app.config.from_dotenv()

# Define the Spotify client ID and client secret
client_id = app.config["CLIENT_ID"]
client_secret = app.config["CLIENT_SECRET"]

# Get the Spotify access token
token = get_token(client_id, client_secret)


@app.route("/")
def index():
    # Example response from chatGPT
    chatgpt_response = """
    "Riptide" by Vance Joy - A breezy and catchy acoustic song.
    "Take Me Home, Country Roads" by John Denver - A classic that's great for a laid-back mood.
    "Walking on Sunshine" by Katrina and the Waves - An upbeat, feel-good song.
    "I'm Yours" by Jason Mraz - A mellow and cheerful acoustic track.
    "Up&Up" by Coldplay - An uplifting and anthemic song.
    "Island in the Sun" by Weezer - A chill and sunny track.
    "One Love" by Bob Marley - Reggae vibes for a relaxed atmosphere.
    " Budapest" by George Ezra - A catchy and soulful tune.
    "Drops of Jupiter" by Train - A reflective and melodic song.
    "Fly Me to the Moon" by Frank Sinatra - A classic that might set a cool and sophisticated mood.
    """

    # Parse the chatGPT response to get a random song
    song, artist = parse_song(chatgpt_response)

    # If a song is found, search for it on Spotify and get the track URL
    if song and artist:
        track_url = search_for_track(token, artist, song)
        return render_template(
            "index.html", track_url=track_url, song=song, artist=artist
        )
    else:
        return "No song found."


if __name__ == "__main__":
    app.run(debug=True)
