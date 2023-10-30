# the_date = input("what Year would you like to travel to? Input the date in this format: YYYY-MM-DD")

import os
from bs4 import BeautifulSoup
import requests
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set your sensitive information as environment variables
os.environ["SPOTIPY_CLIENT_ID"] = "your_client_id"
os.environ["SPOTIPY_CLIENT_SECRET"] = "your_client_secret"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

the_date = input("Enter the date you want to travel to. Enter the date in YYYY-MM-DD format: ")

playlist = sp.user_playlist_create(user= user_id, name=f"{the_date} Billboard Hot 100", public=False)


URL = f"https://www.billboard.com/charts/hot-100/{the_date}/"
response = requests.get(URL)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

# top_songs = soup.find_all(name="h3", id = "title-of-a-story")
top_songs = soup.select("li > h3#title-of-a-story")
song_titles = [song.getText().strip() for song in top_songs]

song_uris = []
the_year = the_date.split("-")[0]
# print(the_year)
for song in song_titles:
    result = sp.search(q=f"track:{song} year:{the_year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")




sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

# \\

# print(top_songs)