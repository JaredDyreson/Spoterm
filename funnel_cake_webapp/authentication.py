#!/usr/bin/env python3.5

from flask import Flask, redirect, url_for, session, request,render_template
from flask_oauthlib.client import OAuth, OAuthException
from flask_script import Manager, Server

import spotify_playlist
import sys
from app import app
from app.form import * 
import re


# Change the scope to match whatever it us you need
# list of scopes can be found in the url below
# https://developer.spotify.com/web-api/using-scopes/


SPOTIFY_APP_ID = "e1f239ec0ee443689d6786fd3f397af1" 
SPOTIFY_APP_SECRET = "cbecd4d200f8482d910cb1db77d6f10c" 

url_re = "https:\/\/open\.spotify\.com\/user\/[a-zA-Z0-9].*\/[a-zA-Z0-9].*\?si\=[a-zA-Z0-9].*"
expression = re.compile(url_re)

app = Flask(__name__)
app.debug = False
app.secret_key = 'development'
oauth = OAuth(app)

scope = ['playlist-modify-public', 'user-library-read', 'user-library-modify']
spotify = oauth.remote_app(
	'spotify',
	consumer_key=SPOTIFY_APP_ID,
	consumer_secret=SPOTIFY_APP_SECRET,
	request_token_params={'scope': '{}'.format(*scope)},
	base_url='https://accounts.spotify.com',
	request_token_url=None,
	access_token_url='/api/token',
	authorize_url='https://accounts.spotify.com/authorize'
)


@app.route('/')
def index():
	return redirect(url_for('login'))


@app.route('/login')
def login():
	callback = url_for(
		'spotify_authorized',
		next=request.args.get('next') or request.referrer or None,
		_external=True
	)
	return spotify.authorize(callback=callback)


@app.route('/login/authorized')
def spotify_authorized():
	resp = spotify.authorized_response()
	if resp is None:
		return 'Access denied: reason={0} error={1}'.format(
			request.args['error_reason'],
			request.args['error_description']
		)
	if isinstance(resp, OAuthException):
		return 'Access denied: {0}'.format(resp.message)

	session['oauth_token'] = (resp['access_token'], '')
	me = spotify.get('/me')
	return redirect(url_for('util'))
@spotify.tokengetter
def get_spotify_oauth_token():
	return session.get('oauth_token')

@app.route('/util', methods=['GET', 'POST'])
def util():
	token = session.get('oauth_token')[0]
	manager = spotify_playlist.PlaylistManager(token=token)
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
			print("[+] Created both playlists")
			if(manager.is_playlist(output_name)):
				destination = spotify_playlist.Playlist(url="{}".format(manager.get_playlist_url(output_name)))
			else:
				destination = spotify_playlist.Playlist.from_playlists(output_name, playlist_one, playlist_two, token)

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
	app.run(debug=False)
