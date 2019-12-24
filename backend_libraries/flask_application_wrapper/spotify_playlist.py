import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import requests
import json

import os

from forms import PlaylistMergeForm

class SpotifyPlaylist():
	def __init__(self, url: str, track_list: list):
		self.url = url.replace("\\", "")
		credential_manager = SpotifyClientCredentials(
			client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
			client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET")
		)
		self.non_elevated_credentials = spotipy.Spotify(
			client_credentials_manager=credential_manager
		)
		self.track_list = track_list	
	
	# helper functions #

	def get_track_ids(self):
		# returns a list of track ids for each playlist
		if(len(self.track_list) > 0): return
		list_of_tracks = self.get_playlist_tracks()
		id_list = [list_of_tracks[index]['track']['id'] for index, element in enumerate(list_of_tracks)]
		self.track_list = id_list
		return id_list
	def get_playlist_tracks(self):
		results = self.non_elevated_credentials.user_playlist_tracks(self.user_id(), playlist_id="{}".format(self.playlist_id()))
		tracks = results['items']
		while results['next']:
			results = self.manager.elevated_credentials.next(results)
			tracks.extend(results['items'])
		return tracks
	# parsing functions #

	def url_base(self):
		# returns the ending portion of the string, generally the playlist id
		return self.url.split("/")[len(self.url.split("/"))-1]	

	def user_id(self):
		# returns the user in which the playlist belongs to
		return self.url.split("/")[4]

	def playlist_id(self):
		# either returns the url_base or the first portion of the base_url after the "?si=" delimiter
		try: return self.url_base().split("?si=")[0]
		except IndexError: return self.base()

	# driver code #

	def from_web_application(self, form: PlaylistMergeForm):
		
		manager = spotify_playlist.PlaylistManager(user_id, token)
		url_one = form.playlist_one.data.strip()
		url_two = form.playlist_two.data.strip()
		output_name = form.playlist_output_name.data.strip()

		if(url_one == url_two):
			return {
				"both inputs were the same, please try again": "danger"
			}
		playlist_one = spotify_playlist.Playlist(url="{}".format(url_one), track_list=[])
		playlist_two = spotify_playlist.Playlist(url="{}".format(url_two), track_list=[])

		if(manager.is_playlist(output_name)):
			return {
				"playlist named {} already exists".format(output_name): "danger"
			}
		else: 
			tracks = self.manager.catentate_playlists(playlist_one.track_list, playlist_two.track_list)
			self.manager.create_new_playlist(output_name)
			destination = spotify_playlist.Playlist(url="", track_list=tracks)

		manager.append_to_playlist(destination, destination.track_ids)
		return {
			"Successfully created playlist: {}".format(output_name) : "success"
		}
class PlaylistManager():
	def __init__(self, user_id, token):
		self.user_id = user_id
		self.token = token

		credential_manager = SpotifyClientCredentials(
			client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
			client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET')
		)
		self.non_elevated_credentials = spotipy.Spotify(
			client_credentials_manager=credential_manager
		)
		self.elevated_credentials = spotipy.Spotify(
			auth=self.token
		)
	def create_new_playlist(self, playlist_name: str):
		# create a new playlist
		return self.elevated_credentials.user_playlist_create(
			self.user_id,
			playlist_name
		)
	def is_playlist(self, playlist_name: str):
		# checks if the playlist exists
		# return boolean

		for element in self.get_playlists():
			if(element['name'] == playlist_name): return True
		return False
	def get_playlist_id(self, playlist_name: str):
		for element in self.get_playlists():
			if(element['name'] == playlist_name): return element['id']
		return None
	def get_playlist_url(self, playlist_name: str):
		id_hash = self.get_playlist_id(playlist_name)
		for element in self.get_playlists():
			if(element['id'] == id_hash): return element['external_urls']['spotify']
		return None
	def get_playlists(self):
		
		# return a list of json objects representing playlists
		results = self.elevated_credentials.user_playlists(self.user_id)
		playlist_manifest = results['items']
		while results['next']:
			results = self.elevated_credentials.next(results)
			playlist_manifest.extend(results['items'])
		return playlist_manifest
	def search(self, artist: str, track: str):
		result = self.credentials.search(q="artist: {} track: {}".format(artist, track),type='track')
		if(len(result) == 0): return None
		try: return result['tracks']['items'][0]['id']
		except IndexError: return None
	def append_to_playlist(self, playlist: SpotifyPlaylist, track_list: list):
		track_list_uris = ["spotify:track:{}".format(element) for element in track_list]
		url = "https://api.spotify.com/v1/users/{}/playlists/{}/tracks?position=0".format(self.user_id, playlist.playlist_id())
		headers = {
			'Accept': 'application/json', 
			'Content-Type': 'application/json', 
			'Authorization': 'Bearer {}'.format(self.token)
		}
		chunks = [track_list[x:x+100] for x in range(0, len(track_list), 100)]
		for uri_chunk in chunks:
			payload = {
				"position": 0, 
				"uris": uri_chunk
			}
			req = requests.post(url, headers=headers, data=json.dumps(payload))
			if req.status_code != 201: print('Error: Request returned status code {}. Returned: {}'.format(req.status_code, req.text))
	def truncate_playlist(self, playlist: SpotifyPlaylist):
		self.elevated_credentials.user_playlist_remove_all_occurrences_of_tracks(self.user_id, playlist.playlist_id(), playlist.track_ids)	
	def catentate_playlists(self, track_list_one: list, track_list_two: list):
		return list(set().union(track_list_one, track_list_two))	
