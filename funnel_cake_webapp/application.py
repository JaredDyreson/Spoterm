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


#SPOTIFY_APP_ID = "e1f239ec0ee443689d6786fd3f397af1" 
#SPOTIFY_APP_SECRET = "cbecd4d200f8482d910cb1db77d6f10c" 

url_re = "https:\/\/open\.spotify\.com\/user\/[a-zA-Z0-9].*\/[a-zA-Z0-9].*\?si\=[a-zA-Z0-9].*"
expression = re.compile(url_re)

application = app = Flask(__name__)
app.debug = False
app.secret_key = 'development'
oauth = OAuth(app)

scope = ['playlist-modify-public', 'user-library-read', 'user-library-modify']
#spotify = oauth.remote_app(
#	'spotify',
#	consumer_key=SPOTIFY_APP_ID,
#	consumer_secret=SPOTIFY_APP_SECRET,
#	request_token_params={'scope': '{}'.format(*scope)},
#	base_url='https://accounts.spotify.com',
#	request_token_url=None,
#	access_token_url='/api/token',
#	authorize_url='https://accounts.spotify.com/authorize'
#)


@app.route('/')
def index():
	return "Hello world"

if __name__ == '__main__':
	app.run(debug=False)
