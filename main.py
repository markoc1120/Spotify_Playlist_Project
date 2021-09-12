import os
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy import oauth2

# GETTING TOP 100 SONG
date = input('What year would you like to travel to? Type the year in the format of YYYY-MM-DD: ')
only_year = date.split('-')[0]
BASIC_URL = 'https://www.billboard.com/charts/hot-100/'
response = requests.get(url=f'{BASIC_URL}{date}')
response.raise_for_status()

website = response.text
soup = BeautifulSoup(website, 'html.parser')
titles = [title.getText() for title in soup.find_all(name='span', class_='chart-element__information__song')]

# INTERACTING WITH SPOTIFY
sp = spotipy.Spotify(
    auth_manager=oauth2.SpotifyOAuth(
        scope='playlist-modify-private',
        redirect_uri='http://example.com',
        client_id=os.environ.get('client_id'),
        client_secret=os.environ.get('client_secret'),
        cache_path='token.txt'
    )
)
user_id = sp.current_user()['id']

tracks_uris = []
for title in titles:
    q = f'track: {title} year: {only_year}'
    try:
        uri = sp.search(q=q, type='track')['tracks']['items'][0]['uri']
        tracks_uris.append(uri)
    except IndexError:
        continue

playlist_name = f'{date} Billboard 100'
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=tracks_uris)
