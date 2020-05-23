#!/usr/bin/env python3.8

from SpotifyAuthenticator import application, CredentialIngestor
from SpotifyPlaylist import *

main_playlists= {
	"bree and amber and jared's robot": "https://open.spotify.com/user/12164553253/playlist/7715866mwpFJeZ6GkUK2Th?si=EG0FTH6bTWWYJKIyc3agxA",
	"2000's Rock": "https://open.spotify.com/user/believe556/playlist/4ccEeq0sbXWTHRecsFeDHg?si=fDW3FxeYTra_a6h8_lyj9Q"
}

application.run()

credential_manager = CredentialIngestor.CredentialIngestor("credentials.json")

playlist_one = Playlist(url="{}".format(main_playlists["bree and amber and jared's robot"]))

print(playlist_one.track_ids)
