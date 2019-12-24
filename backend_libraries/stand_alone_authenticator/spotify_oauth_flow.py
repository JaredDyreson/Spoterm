#!/usr/bin/env python3.5

from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth, OAuthException
from multiprocessing import Process
import os
import requests
import json

SPOTIFY_APP_ID = os.environ.get("SPOTIFY_AUTHENTICATOR_CLIENT_ID")
SPOTIFY_APP_SECRET = os.environ.get("SPOTIFY_AUTHENTICATOR_CLIENT_SECRET")



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


@app.route('/authenticate')
def login():
	callback = url_for(
		'spotify_authorized',
		next=request.args.get('next') or request.referrer or None,
		_external=True
	)
	return spotify.authorize(callback=callback)


@app.route('/authenticate/authorized')
def spotify_authorized():
	resp = spotify.authorized_response()
	if resp is None:
		return 'Access denied: reason={0} error={1}'.format(
			request.args['error_reason'],
			request.args['error_description']
		)
	if isinstance(resp, OAuthException):
		return 'Access denied: {0}'.format(resp.message)


	session['oauth_token'] = resp['access_token']

	url = "https://api.spotify.com/v1/me"
	headers = {
		'Accept': 'application/json', 
		'Content-Type': 'application/json', 
		'Authorization': 'Bearer {}'.format(session.get('oauth_token'))
	}
	req = requests.get(url, headers=headers)
	text_response = json.loads(req.text)
	
	os.environ['user_id'] = text_response.get('id')
	os.environ['username'] = text_response.get('display_name')
	os.environ['oauth_token'] = resp['access_token']

	session['user_id'] = text_response.get('id')
	session['username'] = text_response.get('display_name')

	request.environ.get('werkzeug.server.shutdown')()
	return ""

@spotify.tokengetter
def get_spotify_oauth_token():
	return session.get('oauth_token')
