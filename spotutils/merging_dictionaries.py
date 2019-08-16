#!/usr/bin/env python3.5
from pprint import pprint as pp
import spotify_playlist

def parse_for_sorting(track_output: dict):
	track_id = track_output['track']['id']
	track_name = track_output['track']['name']
	track_artist = track_output['track']['artists'][0]['name']
	return track_id, track_name, track_artist

def convert_for_sorting(track_id: str, track_artist: str, track_name: str):
	new_example = {
		track_artist: {
			track_name: track_id
		}
	}
	return new_example

def combine(dict_one: dict, dict_two: dict, path=None):
	# merge dict_two into dict_one
	if path is None: path=[]
	for key in dict_two:
		if(key in dict_one):
			# if the tree is continuing to descend, we need to recursively call the function
			if(isinstance(dict_one[key], dict) and isinstance(dict_two[key], dict)):
				combine(dict_one[key], dict_two[key], path+[str(key)])
			elif(dict_one[key] == dict_two[key]):
				# a leaf value
				pass

			else:
				raise Exception("Conflict at {} : {}".format(path, str(key)))
		else:
			dict_one[key] = dict_two[key]
	return
base = {}

# NOTE
# this only works when the playlist is already present
# needs to be modified to reverse search Spotify API by [artist name] - [track name] along with the album to prevent edge cases

p = spotify_playlist.Playlist(url="https://open.spotify.com/user/12164553253/playlist/1WLzRlCnEw8CWGJaS3x6nj?si=RRpisW4mRECAQw_q0S7zAg")
manager = spotify_playlist.PlaylistManager()
tracks = p.get_playlist_tracks()

l = []

for index, track in enumerate(tracks):
	track_id, track_name, track_artist = parse_for_sorting(track)
	l.append(convert_for_sorting(track_id, track_artist, track_name))
for element in l:
	combine(base, element)

id_list = []
for artist in sorted(list(base.keys())):
	for track in sorted(list(base[artist].keys())):
		id_list.append(base[artist][track])
		#print("\tTrack: {}\tid: {}".format(track, base[artist][track]))
manager.truncate_playlist(p)
manager.append_to_playlist(p, id_list)
