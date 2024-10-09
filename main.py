from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv(f"C:/Users/jay-5/Documents/code/pythonProj/timeMachine/api.env")
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
    username=USERNAME,
    )
)
user_id = sp.current_user()["id"]


playlists = sp.user_playlists('spotify')


date = input("What time would you like to travel to ? ")

URL = "https://www.billboard.com/charts/hot-100/" + date


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
}

response = requests.get(URL, headers=headers)

if response.status_code == 200:
    url_page = response.text
    soup = BeautifulSoup(url_page, 'html.parser')

    song_list = soup.select("li ul li h3")
    song_names = [song.getText().strip() for song in song_list]

    print(song_names)
else:
    print("Failed to retrieve page Status Code: ", response.status_code)