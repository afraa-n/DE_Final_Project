# song.py

import base64
from dotenv import load_dotenv
import json
import os
import random
from requests import get, post, exceptions

# Load variables stored in .env file
load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

def get_token():
    '''
    This function outputs token for Spotify access
    '''
    auth_string = client_id + ":" + client_secret
    auth_bytes  = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
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
    '''
    This function searches for a track on Spotify
    input: artist name and song name, default None
    output: URL to the track on Spotify
    '''
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name, song_name}&type=track&limit=1"
    
    query_url = url + query

    try:
        result = get(query_url, headers=headers, timeout=10)
    except exceptions.Timeout:
        print("Timed out. Server did not respond.")
        
    json_result = json.loads(result.content)
    output_url = json_result['tracks']['items'][0]['external_urls']['spotify']
    
    if len(output_url) == 0:
        print("No soundtrack found...")
        return None
    else:
        return output_url

def get_audio_content(url):
    try:
        result = get(url, timeout=10)
        audio_content = result.content
        return audio_content
    except exceptions.Timeout:
        print("Timed out. Server did not respond.")
        return None

def parse_song(response):
    '''
    This function parses a text response from chatGPT and 
    returns a song name and artist name 
    input: a string of chatGPT response
    output: a tuple of (song name, artist name), both are strings
    '''
    sentences = [x.split(" ") for x in response.split("\n")]
    song_artist_l = list()
    for sent in sentences:
        song_artist = tuple()
        split_ind = None
        song_name, artist_name = None, None
        if len(sent) <= 1:
            pass
        else:
            for i in range(len(sent)):
                if sent[i] == "by":
                    split_ind = i
                elif sent[i] == "-":
                    split_ind = i
        if split_ind != None:
            song_name = " ".join(sent[:split_ind])
            if song_name[0] == '"':
                song_name = song_name[1:]
            if song_name[-1] == '"':
                song_name = song_name[:-1]
            artist_name = " ".join(sent[split_ind+1:])
        if song_name != None or artist_name != None:
            song_artist = (song_name, artist_name)
            song_artist_l.append(song_artist)
    
    if len(song_artist_l) == 0:
        return (None, None)
    else:
        return random.choice(song_artist_l)
