#!/usr/bin/env python3.5

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import authentication
import os
import requests
import json
from pprint import pprint as pp

token_location = "/home/jared/Applications/funnel_cake/credentials/token"
class Playlist():
	def __init__(self, url: str, name="", list_of_tracks=[]):
		self.url = url.replace("\\", "")
		self.credentials = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
		self.manager = PlaylistManager()
		if(len(list_of_tracks) == 0):
			self.track_ids = self.get_track_ids()
		else:
			self.track_ids = list_of_tracks

	@classmethod
	def from_track_ids(cls, list_of_track_ids: list):
		return cls(url="", list_of_tracks=list_of_track_ids)
	@classmethod
	def from_playlists(cls, name: str, source_one, source_two):
		manager = PlaylistManager()
		new_playlist = Playlist.from_track_ids(source_one+source_two)
		if(not manager.is_playlist(name)):
			manager.create_new_playlist(name)
			new_playlist.url = manager.get_playlist_url(name)

		else:
			print("[+] Playlist already exists, not sending API request")
		return new_playlist
	def __add__(self, other):
		return list(set().union(self.get_track_ids(), other.get_track_ids()))	
	def base(self):
		return self.url.split("/")[len(self.url.split("/"))-1]	
	def user_id(self):
		return self.url.split("/")[4]
	def playlist_id(self):
		try:
			return self.base().split("?si=")[0]
		except IndexError:
			return self.base()
	def get_track_ids(self):
		list_of_tracks = self.get_playlist_tracks()
		id_list = []
		for index, element in enumerate(list_of_tracks):
			id_list.append(list_of_tracks[index]['track']['id'])
		return id_list
	def get_playlist_tracks(self):
		results = self.credentials.user_playlist_tracks(self.user_id(), playlist_id="{}".format(self.playlist_id()))
		tracks = results['items']
		while results['next']:
			results = self.manager.elevated_credentials.next(results)
			tracks.extend(results['items'])
		return tracks
	def combine(self, other):
		return list(set().union(self.get_track_ids(), other.get_track_ids()))	
class PlaylistManager():
	def __init__(self, user_id="12164553253"):
		self.user_id = user_id
		self.credentials = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
		if(not os.path.isfile(token_location)):
			authentication.run_server()
		else:
			try:
				self.elevated_credentials = spotipy.Spotify(auth=authentication.return_credentials())
				self.get_playlists()
			except spotipy.client.SpotifyException: 
				authentication.run_server()
				self.elevated_credentials = spotipy.Spotify(auth=authentication.return_credentials())
	def create_new_playlist(self, name: str):
		return self.elevated_credentials.user_playlist_create(self.user_id, name)
	def is_playlist(self, playlist_name: str):
		# checks if playlist exists based on name
		# return: boolean
		for index, element in enumerate(self.get_playlists()):
			if(element['name'] == playlist_name):
				return True
		return False
	def get_playlist_id(self, name: str):
		for index, element in enumerate(self.get_playlists()):
			if(element['name'] == name):
				return element['id']
		return None
	def get_playlist_url(self, name: str):
		identification_hash = self.get_playlist_id(name)
		for index, element in enumerate(self.get_playlists()):
			if(element['name'] and element['id'] == identification_hash):
				return element['external_urls']['spotify']
	def get_playlists(self):
		# return a list of json objects representing playlists
		results = self.elevated_credentials.user_playlists(self.user_id)
		playlist_manifest = results['items']
		while results['next']:
			results = self.elevated_credentials.next(results)
			playlist_manifest.extend(results['items'])
		return playlist_manifest
	def append_to_playlist(self, playlist: Playlist, track_list: list):
		url = "https://api.spotify.com/v1/users/{}/playlists/{}/tracks?position=0".format(self.user_id, playlist.playlist_id())
		headers = {
			'Accept': 'application/json', 
			'Content-Type': 'application/json', 
			'Authorization': 'Bearer {}'.format(authentication.return_credentials())
		}
		chunks = [track_list[x:x+100] for x in range(0, len(track_list), 100)]
		for chunk in chunks:
			payload = {
				"position": 0, 
				"uris": ["spotify:track:{}".format(element) for element in chunk] 
			}
			req = requests.post(url, headers=headers, data=json.dumps(payload))
			if req.status_code != 201:
				print('Error: Request returned status code {}. Returned: {}'.format(req.status_code, req.text))

	def truncate_playlist(self, playlist: Playlist):
		# remove the contents of a playlist
		self.elevated_credentials.user_playlist_remove_all_occurrences_of_tracks(self.user_id, playlist.playlist_id(), playlist.track_ids)

