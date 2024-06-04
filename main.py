from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SPOTIFY_CLIENT = 'aa1e1520000d492fb57322bdc8c313f6'
SPOTIFY_SECRET = 'bffe3d9ed31648759c36ea59997762e2'
USER_ID = '31ir2a6t5a7joh5mydmgbo5urea'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT,
        client_secret=SPOTIFY_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

date = input("Which date do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f'https://www.billboard.com/charts/hot-100/{date}')
contents = response.text

soup = BeautifulSoup(contents, 'html.parser')
first_song = soup.find_all(name='h3', id='')
f_song = first_song[0].getText()
songs = soup.find_all(name='h3', class_='c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 '
                                        'lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 '
                                        'u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 '
                                        'u-max-width-230@tablet-only')
songs = [song.getText().strip() for song in songs]
songs.insert(0, f_song.strip())

song_uris = []
year = date.split("-")[0]
for song in songs:
    result = sp.search(q=f'track:{song} year:{year}', type='track')
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
