from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv(f"/timeMachine/api.env")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
USERNAME = os.environ.get("USERNAME")
REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    show_dialog=True,
    cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]

playlists = sp.user_playlists('spotify')

date = input("What time would you like to travel to ?(In YYYY-MM-DD format) ")

URL = "https://www.billboard.com/charts/hot-100/" + date

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}

response = requests.get(URL, headers=headers)

url_page = response.text
soup = BeautifulSoup(url_page, 'html.parser')
song_list = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_list]

names = ["List of song", "Titles", "scrape"]

song_uris=[]

year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    if result["tracks"]["items"]:
        song_uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(song_uri)
    else:
        print(f"Song: {song} does not exist on Spotify.")

playlist_name = f"Billboard Hot 100 - {date}" 
description = "Billboard Hot 100 for the year specified by user."

playlist = sp.user_playlist_create(user=user_id,
                                   name=playlist_name,
                                   description=description,
                                   public=False)

if song_uris:
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
    print(f"Playlist '{playlist_name}' created successfully.")
else:
    print("No songs found to add to the playlist.")
    