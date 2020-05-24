#!/usr/bin/env python3.8

from SpotifyPlaylist import SpotifyPlaylist, PlaylistManager
from pprint import pprint as pp

"""
This is where all the helper functions go for Frogger
"""

def get_base_api_list(src: SpotifyPlaylist):
    list_of_tracks = src.get_playlist_tracks()
    return [list_of_tracks[index]['track'] for index, element in enumerate(list_of_tracks)]

def list_songs(src: SpotifyPlaylist):
  for index, element in enumerate(get_base_api_list(src)):
    print("[{}]: {}".format(index, element['name']))
    print("   - {}".format(
          ', '.join(artist['name'] for artist in element['artists'])
    ))
