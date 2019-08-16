#!/usr/bin/env python3.5

from flask import Flask, render_template, request
import spotify_playlist
import sys
from app import app
from app.form import * 
import re

url_re = "https:\/\/open\.spotify\.com\/user\/[a-zA-Z0-9].*\/[a-zA-Z0-9].*\?si\=[a-zA-Z0-9].*"
expression = re.compile(url_re)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.route('/', methods=['GET', 'POST'])
def index():
	form = funnel_cake_form()
	if(form.validate_on_submit()):
		url_one = form.url_one.data
		url_two = form.url_two.data
		output_name = form.playlist_output_name.data
		if(expression.match(url_one) and expression.match(url_two)):
			if(url_one == url_two):
				form.url_one.data = ""
				form.url_two.data = ""
				form.playlist_output_name.data = ""

				return render_template('index.html', title='Funnel Cake', form=form)
			playlist_one = spotify_playlist.Playlist(url="{}".format(url_one))
			playlist_two = spotify_playlist.Playlist(url="{}".format(url_two))
			manager = spotify_playlist.PlaylistManager()
			if(manager.is_playlist(output_name)):
				destination = spotify_playlist.Playlist(url="{}".format(manager.get_playlist_url(output_name)))
			else:
				destination = spotify_playlist.Playlist.from_playlists(output_name, playlist_one, playlist_two)

			print("[+] Created destination")
			manager.truncate_playlist(destination)
			print("[+] Truncating newly created playlist")
			manager.append_to_playlist(destination, destination.track_ids)
			print("[+] Added the contents of playlist one and playlist two")
		else: raise Exception("Malformed urls")

	form.url_one.data = ""
	form.url_two.data = ""
	form.playlist_output_name.data = ""
	return render_template('index.html', title='Funnel Cake', form=form)

if __name__ == '__main__':
	app.run(debug=True)
