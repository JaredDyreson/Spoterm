#!/usr/bin/env python

import sys
import os

sys.path.append("./stand_alone_authenticator")
sys.path.append("./spotify_playlists")

import spotify_oauth_flow
import spotify_playlist

spotify_oauth_flow.app.run()

manager = spotify_playlist.PlaylistManager(os.environ.get('user_id'), os.environ.get('oauth_token'))

playlist_url = "https://open.spotify.com/playlist/7715866mwpFJeZ6GkUK2Th?si=qSWP0_PpQcKDiPkW7c-sGA"

playlist = spotify_playlist.SpotifyPlaylist(url="{}".format(playlist_url), track_list=[])
cloned_playlist = spotify_playlist.SpotifyPlaylist(url="", track_list=playlist.get_track_ids())

cloned_playlist.name = "{} - Cloned".format(manager.get_playlist_name(playlist))

if not(manager.is_playlist(cloned_playlist)): manager.create_new_playlist(cloned_playlist)
manager.append_to_playlist(cloned_playlist, cloned_playlist.track_list)

print(manager.get_playlist_url(cloned_playlist))
