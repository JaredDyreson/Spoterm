#!/usr/bin/env python3.5

from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth, OAuthException
from flask_script import Manager, Server
import spotipy
import spotipy.util as util
import threading
from selenium import webdriver
import time
import os
import spotipy
from pprint import pprint as pp



SPOTIFY_APP_ID = 'e1f239ec0ee443689d6786fd3f397af1'
SPOTIFY_APP_SECRET = 'cbecd4d200f8482d910cb1db77d6f10c'

def run_server():
	app = Flask(__name__)
	app.debug = False
	app.secret_key = 'development'
	oauth = OAuth(app)

	scope = ['playlist-modify-public', 'user-library-read', 'user-library-modify']
	spotify = oauth.remote_app(
		'spotify',
		consumer_key=SPOTIFY_APP_ID,
		consumer_secret=SPOTIFY_APP_SECRET,
# Change the scope to match whatever it us you need
# list of scopes can be found in the url below
# https://developer.spotify.com/web-api/using-scopes/
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
		with open("token.txt", "w+") as f:
			f.write(str(session.get('oauth_token')[0]))
		return 'Logged in as id={0} name={1} redirect={2}'.format(
				me.data,
				me.data,
				request.args.get('next')
		)
	@spotify.tokengetter
	def get_spotify_oauth_token():
		return session.get('oauth_token')

	driver = webdriver.Firefox()
	port = 5000
	url = "http://127.0.0.1:{}".format(port)
	threading.Timer(1.25, lambda: driver.get(url) ).start()
	t_webApp = threading.Thread(name='Web App', target=app.run(port=port, debug=False))
	t_webApp.setDaemon(True)
	t_webApp.start()
	driver.quit()
	os.remove("geckodriver.log")
def return_credentials():
	with open("token.txt") as f:
		return f.read()
# run the webdriver then start the webserver. Once the webserver is running, we then open the url to the redirect url
# https://stackoverflow.com/questions/11125196/python-flask-open-a-webpage-in-default-browser

if __name__ == '__main__':

	sp = spotipy.Spotify(auth=token)
	print(len(get_playlist_tracks(sp, "12164553253", "7sls5iyVDsDMTlnXVCakOE")))
