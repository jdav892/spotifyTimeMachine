from bs4 import BeautifulSoup
import requests

#input("What time would you like to travel to ? ")

URL = "https://www.billboard.com/charts/hot-100/2000-08-12"


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