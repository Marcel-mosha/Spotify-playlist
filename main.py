import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
date = input("Enter a date in YYYY-MM-DD format: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"
response = requests.get(URL)
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")
music_list = [music.getText().strip() for music in soup.select("li ul li h3")]


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="MarcelMosha",
    )
)
user_id = sp.current_user()["id"]
#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in music_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
