#!/usr/bin/env python3.5
from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth, OAuthException

# when creating this script, please fill out the appropriate redirect_uri
# in this case it is -> http://127.0.0.1:5000/login/authorized
# fill out this information in the Dashboard under the app in which you are developing

class SpotifyOAuthFlow():
	def __init__(self, application_name: str, application_id: str, application_secret_code: str, scope=[]):
		self.application_name = application_name
		self.app_id =  application_id
		self.secret_key = application_secret_code
		self.scope = scope
		self.application_information = self.fill_application_informaion()
		self.remote_application = self.instantiate_application()
	def instantiate_application(self, scope=[]):
		application = Flask(self.application_name)
		application.debug = True
		application.secret_key = 'development'
		self.fill_application_informaion()
		return application
	def fill_application_informaion(self):
		oauth = OAuth(self.remote_application)
		return oauth.remote_app(
			self.application_name,
			consumer_key=self.app_id,
			consumer_secret=self.secret_key,
# Change the scope to match whatever it us you need
# list of scopes can be found in the url below
# https://developer.spotify.com/web-api/using-scopes/
			request_token_params={'scope': '{}'.format(', '.join(self.scope))},
			base_url='https://accounts.spotify.com',
			request_token_url=None,
			access_token_url='/api/token',
			authorize_url='https://accounts.spotify.com/authorize'
		)
SPOTIFY_APP_ID = 'e1f239ec0ee443689d6786fd3f397af1'
SPOTIFY_APP_SECRET = 'cbecd4d200f8482d910cb1db77d6f10c'
flow = SpotifyOAuthFlow(application_name="Spoterm", application_id=SPOTIFY_APP_ID, application_secret_code=SPOTIFY_APP_SECRET, scope=['user-read-email'])

@flow.remote_application.route('/')
def index():
	return redirect(url_for('login'))

@flow.remote_application.route('/login')
def login():
	callback = url_for(
		'spotify_authorized',
		next=request.args.get('next') or request.referrer or None,
		_external=True
	)
	return flow.remote_application.authorize(callback=callback)

@flow.remote_application.route('/login/authorized')
def spotify_authorized():
	resp = self.flow.authorized_response()
	if resp is None:
		return 'Access denied: reason={0} error={1}'.format(
			request.args['error_reason'],
			request.args['error_description']
		)
	if isinstance(resp, OAuthException):
		return 'Access denied: {0}'.format(resp.message)

	session['oauth_token'] = (resp['access_token'], '')
	me = self.remote_application.get('/me')
	return 'Logged in as id={0} name={1} redirect={2}'.format(
		me.data,
		me.data,
		request.args.get('next')
	)


@flow.remote_application.tokengetter
def get_spotify_oauth_token():
	return session.get('oauth_token')

flow.remote_application.run()
