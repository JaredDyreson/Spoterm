#!/usr/bin/env python3.8

from spotutils import Playlist, PlaylistManager

main_playlists= {
	"bree and amber and jared's robot": "https://open.spotify.com/user/12164553253/playlist/7715866mwpFJeZ6GkUK2Th?si=EG0FTH6bTWWYJKIyc3agxA",
	"2000's Rock": "https://open.spotify.com/user/believe556/playlist/4ccEeq0sbXWTHRecsFeDHg?si=fDW3FxeYTra_a6h8_lyj9Q"
}

#source_one = spotify_playlist.Playlist(url="{}".format(main_playlists["bree and amber and jared's robot"]))
source_one = spotify_playlist.Playlist(url="https://open.spotify.com/user/12164553253/playlist/2iEsJnrjv3zfjo2HXX92eS?si=tLtNEnMBQuqH8umqGbg73g")

print("[+] Created playlist one....")
#source_two = spotify_playlist.Playlist(url="{}".format(main_playlists["2000's Rock"]))
source_two = spotify_playlist.Playlist(url="https://open.spotify.com/user/12164553253/playlist/6JdvRkz2k4m0cByFIpHjaD?si=GZNKvmyASLefvE9Ip13-Pg")
print("[+] Created playlist two....")
new_playlist_name = "playlist_three"
manager = spotify_playlist.PlaylistManager()
if(manager.is_playlist(new_playlist_name)):
	destination = spotify_playlist.Playlist(url="{}".format(manager.get_playlist_url(new_playlist_name)))
else:
	destination = spotify_playlist.Playlist.from_playlists(new_playlist_name, source_one, source_two)

print("[+] Created destination")
manager.truncate_playlist(destination)
print("[+] Truncating newly created playlist")
manager.append_to_playlist(destination, destination.track_ids)
print("[+] Added the contents of playlist one and playlist two")
