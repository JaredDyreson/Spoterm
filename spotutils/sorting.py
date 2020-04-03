#!/usr/bin/env python3.8

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
def get_all_unique_artists(lst: list):
	a = set()
	for element in lst:
		a.add(*list(element.keys()))
	return a



p = spotify_playlist.Playlist(url="https://open.spotify.com/user/12164553253/playlist/4YyT7ryyOem7MpTXKzqWOi?si=jCMRMOE8S66Pc8UlsVm7xA")
tracks = p.get_playlist_tracks()
l = []
for index, track in enumerate(tracks):
	track_id, track_name, track_artist = parse_for_sorting(track)
	l.append(convert_for_sorting(track_id, track_artist, track_name))
new_dict = {}
old_dict = l[0]

def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return 
def combine(dict_one: dict, dict_two: dict, path=None):
	# merge dict_two into dict_one
	if path is None: path=[]
	for key in dict_two:
		if(key in dict_one):
			if(isinstance(dict_one[key], dict) and isinstance(dict_two[key], dict)):
				combine(dict_one[key], dict_two[key], path.append(str(key)))
			elif(dict_one[key] == dict_two[key]):
				pass
				# same leaf value
			else:
				raise Exception("Conflict at {} : {}".format(path, str(key)))
		else:
			dict_one[key] = dict_two[key]
	return
merge(new_dict, old_dict)
pp(old_dict)
#unique_artists = sorted(get_all_unique_artists(l))
#e = {}
#for artist in unique_artists:
#	if(artist not in e.keys()):
#		e[artist] = {}
#	else:
#		d = e[artist]
#		print("got here")
#		if("song" not in d.keys()):
#			e[artist]["song"] = "some_number"








example_dict = {
	"Metallica": {
		"Master of Puppets": "identification",
		"Ride the Lightning": "identification"
	},
	"A Day to Remember": {
		"Good Things": "identification",
		"Bad Vibrations": "identification"
	}
}

#for artist in sorted(list(example_dict.keys())):
#	print(artist)
#	for track in sorted(list(example_dict[artist].keys())):
#		print("\tTrack: {}\tid: {}".format(track, example_dict[artist][track]))
#a = ["Metallica", "A Day to Remember", "Godsmack"]
#for artist in a:
#	if(artist not in example_dict.keys()):
#		example_dict[artist] = {}
#	else:
#		if(not "song" in example_dict[artist].keys()):
#			example_dict[artist]["song"] = "some_id"
#print(example_dict)
#print(convert_for_sorting(track_id, track_artist, track_name))
