import base64
from dotenv import load_dotenv
import json
import os
import random
from requests import get, post, exceptions

# load variables stored in .env file
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    """
    This function outputs token for spotify access
    """
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    try:
        result = post(url, headers=headers, data=data, timeout=10)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token
    except exceptions.Timeout:
        print("Timed out. Server did not respond.")
        return None


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_track(token, artist_name=None, song_name=None):
    """
    This function searches for a track on spotify
    input: artist name and song name, defalut None
    output: url to the track on spotify
    """
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name, song_name}&type=track&limit=1"

    query_url = url + query

    try:
        result = get(query_url, headers=headers, timeout=10)
    except exceptions.Timeout:
        print("Timed out. Server did not respond.")

    json_result = json.loads(result.content)
    output_url = json_result["tracks"]["items"][0]["external_urls"]["spotify"]

    if len(output_url) == 0:
        print("No soundtrack found...")
        return None
    else:
        return output_url


example = """
Certainly! Here's a mix of songs that you might enjoy while waiting for your plane. Whether you're looking for something upbeat or mellow, these songs cover a range of genres:

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
Remember to adjust the volume to your liking, especially if you're in a public space like an airport. I hope these songs add a pleasant soundtrack to your wait, and safe travels!
"""


def parse_song(response):
    """
    This function parses a text response from chatGPT and
    returns a song name and aartist name
    input: a string of chatGPT response
    output: a tuple of (song name, artist name), both are strings
    """
    sentences = [x.split(" ") for x in response.split("\n")]
    song_artist_l = list()
    for sent in sentences:
        song_artist = tuple()
        song_start, song_end = None, None
        artist_start, artist_end = None, None
        song_name, artist_name = None, None
        if len(sent) <= 1:
            pass
        else:
            for i in range(len(sent)):
                if sent[i][0] == '"':
                    song_start = i
                if sent[i][-1] == '"':
                    song_end = i
                if sent[i] == "by":
                    artist_start = i + 1
                if sent[i] == "-":
                    artist_end = i - 1
        if song_start != None and song_end != None:
            song_name = " ".join(sent[song_start : song_end + 1])[1:-1]
        if artist_start != None and artist_end != None:
            artist_name = " ".join(sent[artist_start : artist_end + 1])
        if song_name != None or artist_name != None:
            song_artist = (song_name, artist_name)
            song_artist_l.append(song_artist)
    if len(song_artist_l) == 0:
        return (None, None)
    else:
        return random.choice(song_artist_l)


print(parse_song(example))
