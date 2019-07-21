#!/usr/bin/env python3.5

# Please note there is a 50 album limit via the Spotify API so if number of albums is 50, it could be more than that
# the use of a set helps mitigate this

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint as pp
import json

class Artist():
	def __init__(self, name: str):
		self.name = name
	def get_id(self):
		dictionary = {}
		results = sp.search(q='artist:' + self.name, type='artist')
		r = json.dumps(results)
		loaded = json.loads(r)
		for e in loaded['artists']['items']:
			if(e['name'] == self.name):
				return {e['name']: e['id']}
		return dictionary
	def get_number_of_songs(self):
		try:
			art_id = list(self.get_id().values())[0]
		except IndexError:
			return None
		albums = sp.artist_albums(artist_id=art_id, limit=50)
		count = 0
		for element in albums['items']:
			results = sp.album(element['id'])
			album_sole_owner = results['artists'][0]['name']
			if(album_sole_owner == self.name):
				count+=(int(element['total_tracks']))
		return count
	def get_albums(self):
		try:
			art_id = list(self.get_id().values())[0]
		except IndexError:
			return None
		albums = sp.artist_albums(artist_id=art_id, limit=50)	
		# find all albums, return a list
		return sorted(set(e['name'] for e in albums['items']))
	def get_number_of_albums(self):
		return len(self.get_albums())

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

