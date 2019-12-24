from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_oauthlib.client import OAuth, OAuthException
from forms import RegistrationForm, LoginForm, PlaylistMergeForm
from flask_wtf import FlaskForm

from spotipy.oauth2 import SpotifyClientCredentials

import spotipy

import spotify_playlist
import re
import json
import requests

url_re = "^(https:\/\/open.spotify.com\/user\/spotify\/playlist\/|spotify:user:spotify:playlist:)([a-zA-Z0-9]+)(.*)$"
expression = re.compile(url_re)

application = Flask(__name__)
application.config['SECRET_KEY'] = '84c1c81be6f347629bf01b97fbbe883c'

# TODO
# make these environment variables in web server and read them

SPOTIFY_APP_ID = "e1f239ec0ee443689d6786fd3f397af1"
SPOTIFY_APP_SECRET = "cbecd4d200f8482d910cb1db77d6f10c"

scope = ['playlist-modify-public', 'user-library-read', 'user-library-modify', 'user-read-email', 'user-read-private']

oauth_application = OAuth(application)

spotify = oauth_application.remote_app(
	'spotify',
	consumer_key=SPOTIFY_APP_ID,
	consumer_secret=SPOTIFY_APP_SECRET,
	request_token_params={'scope': '{}'.format(*scope)},
	base_url='https://accounts.spotify.com',
	request_token_url=None,
	access_token_url='/api/token',
	authorize_url='https://accounts.spotify.com/authorize'
)

@application.route("/", methods=['GET', 'POST'])
def index():
	try:
		token = session.get('oauth_token')[0]
		user_id = session.get('user_id')
	except TypeError:
		token = "" 
		user_id = ""
	form = PlaylistMergeForm(request.form)
	if(form.validate_on_submit()):
		manager = spotify_playlist.PlaylistManager(user_id, token)
		url_one = form.playlist_one.data
		url_two = form.playlist_two.data
		output_name = form.playlist_output_name.data
		if((url_one == url_two)):
			flash("both inputs were the same, please try again", 'danger')
			form = PlaylistMergeForm(formdata=None)
			return render_template('home.html', form=form)
		#elif not(expression.match(url_one) or expression.match(url_two)):
		#	flash("malformed spotify url, pleases try again", 'danger')
		#	return render_template('home.html', form=form)
		playlist_one = spotify_playlist.Playlist(url="{}".format(url_one))
		playlist_two = spotify_playlist.Playlist(url="{}".format(url_two))

		if(manager.is_playlist(output_name)):
			flash("playlist named {} already exists".format(output_name), 'danger')
			form = PlaylistMergeForm(formdata=None)
			return render_template('home.html', form=form)
		else: destination = spotify_playlist.Playlist.from_playlists(output_name, playlist_one, playlist_two, token, user_id)

		manager.truncate_playlist(destination)
		manager.append_to_playlist(destination, destination.track_ids)
		flash("Successfully created playlist: {}".format(output_name), 'success')

	form = PlaylistMergeForm(formdata=None)

	return render_template('home.html', form=form)


@application.route("/about")
def about():
	return render_template('about.html', title='About')

@application.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if(form.validate_on_submit()):
		flash("Account created for {}".format(form.username.data), 'success')
		return redirect(url_for('index'))
	return render_template('register.html', title='Register', form=form)
@application.route("/authenticate", methods=['GET', 'POST'])
def authenticate():
		
	callback = url_for(
		'spotify_authorized',
		next=request.args.get('next') or request.referrer or None,
		_external=True
	)
	return callback
	return spotify.authorize(callback=callback)
	# here we authenticate the user

@application.route('/authenticate/authorized')
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

	url = "https://api.spotify.com/v1/me"
	headers = {
		'Accept': 'application/json', 
		'Content-Type': 'application/json', 
		'Authorization': 'Bearer {}'.format(session.get('oauth_token')[0])
	}

	req = requests.get(url, headers=headers)
	text_response = json.loads(req.text)

	session['user_id'] = text_response.get('id')
	session['username'] = text_response.get('display_name')

	flash("Successfully authenticated user: {}!".format(session.get('username')), 'success')
	return redirect(url_for('index'))

@spotify.tokengetter
def get_spotify_oauth_token():
	return session.get('oauth_token')
if __name__ == '__main__':
	application.run()
