#!/usr/bin/env python3.5

import sys
import spotify_playlist
import argparse
import os

# TODO
# funnel_cake -S artist (sort alphabetically)
# funnel_cake -S song
# funnel_cake -S song -r (sort reverse alphabetically)
def read_from_file(path: str):
	return [line.strip() for line in open(path).readlines()]

def read_from_comma_list(comma_list: str):
	return comma_list.split(",")


# PARSING THE ARGUMENTS GIVEN

parser = argparse.ArgumentParser(description='Combine multiple Spotify playlists.')

parser.add_argument('-F', action='append', dest='collection',
                    default=[],
                    help='Use multiple files to create many playlists',
)

parser.add_argument('-L', action='append', dest='collection',
                    default=[],
                    help='Use a comma separated list to create many playlists',
)

parser.add_argument('-O', action='store', dest='simple_value',
                    help='Output name for the new playlist',
)
results = parser.parse_args()
urls = []
manager = spotify_playlist.PlaylistManager()

#stdin_content = [element.strip() for element in sys.stdin]

for result in results.collection:
	if(os.path.isfile(result)):
		urls.extend(read_from_file(result))
	elif("," in result):
		urls.extend(read_from_comma_list(result))
#urls.extend(stdin_content)

playlist_manifest = [spotify_playlist.Playlist(url=element, name="") for element in urls]
playlist_manifest_tracks = [element.track_ids for element in playlist_manifest]
print("[+] Converted all urls into playlist objects...")

flatten = lambda playlist_manifest: [item for sublist in playlist_manifest for item in sublist]
flatten_track_ids = flatten(playlist_manifest_tracks)

track_id_manifest = list(set(flatten(playlist_manifest_tracks)))

new_playlist_name = results.simple_value
print("[+] New playlist named {} will be created...".format(new_playlist_name))
new_playlist = spotify_playlist.Playlist(url="", name=new_playlist_name, list_of_tracks=track_id_manifest)
if(not manager.is_playlist(new_playlist_name)):
	print("[+] Playlist does not exist, creating..")
	manager.create_new_playlist(new_playlist_name)
	new_playlist.url = manager.get_playlist_url(new_playlist_name)
	print("[+] Appending track ids from new playlist into the Spoitfy one....")
	manager.append_to_playlist(new_playlist, new_playlist.track_ids)	
print("[+] Check out the new playlist at: {}".format(new_playlist.url))

