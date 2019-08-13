#!/usr/bin/env python3.5

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint as pp

#client_credentials_manager = SpotifyClientCredentials()
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def base(playlist_url: str):
	return playlist_url.split("/")[len(playlist_url.split("/"))-1]	
def get_user_id(playlist_url: str):
	return playlist_url.split("/")[4]
def get_playlist_id(playlist_url: str):
	return base(playlist_url).split("?si=")[0]
def get_ids(playlist_url: str):
	list_of_tracks = sp.user_playlist_tracks(get_user_id(playlist_url), playlist_id="{}".format(get_playlist_id(playlist_url)))
	id_list = []
	for index in enumerate(list_of_tracks['items']):
		id_list.append(list_of_tracks['items'][index]['track']['artists'][0]['id'])
	return id_list
#a = get_ids("https://open.spotify.com/user/12164553253/playlist/0fJvs82cTQIkDSWcCGCcp5?si=YDOSShtYTxSOKMsawJ1hiQ")
#print(a)
#print(len(a))


class Playlist():
	def __init__(self, url: str, list_of_tracks=[]):
		self.url = url
		self.track_ids = list_of_tracks
		self.credentials = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
	#@classmethod
	#def from_track_ids(cls, list_of_track_ids: list):
		#return cls(list_of_tracks=list_of_track_ids)
	def base(self):
		return self.url.split("/")[len(self.url.split("/"))-1]	
	def user_id(self):
		return self.url.split("/")[4]
	def playlist_id(self):
		return self.base(self.url).split("?si=")[0]

	def get_track_ids(self):
		list_of_tracks = self.credentials.user_playlist_tracks(get_user_id(self.url), playlist_id="{}".format(get_playlist_id(self.url)))
		id_list = []
		for index, element in enumerate(list_of_tracks['items']):
			id_list.append(list_of_tracks['items'][index]['track']['artists'][0]['id'])
		return id_list
	def create_new_playlist(self, name: str):
		scope = 'user-library-modify'
		util.prompt_for_user_token(self.user_id(), scope, client_id='e1f239ec0ee443689d6786fd3f397af1', client_secret='cbecd4d200f8482d910cb1db77d6f10c', redirect_uri='your-app-redirect-url')
		self.credentials.user_playlist_create(self.user_id(), name)
a = Playlist(url="https://open.spotify.com/user/12164553253/playlist/0fJvs82cTQIkDSWcCGCcp5?si=YDOSShtYTxSOKMsawJ1hiQ")
a.create_new_playlist("Bubba")
