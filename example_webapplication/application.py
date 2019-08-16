from flask import Flask
from flask import Flask, redirect, url_for, session, request,render_template
from flask_oauthlib.client import OAuth, OAuthException
from flask_script import Manager, Server

from app.form import funnel_cake_form
from app import app

application = Flask(__name__)
application.debug = False
application.secret_key = 'development'
oauth = OAuth(application)
# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % username
def loading():
	return "<p>Hello worlf</p>\n"

def login():
	callback = url_for(
		'spotify_authorized',
		next=request.args.get('next') or request.referrer or None,
		_external=True
	)
	return spotify.authorize(callback=callback)
def util():
	#token = session.get('oauth_token')[0]
	#manager = spotify_playlist.PlaylistManager(token=token)
	return render_template('index.html', title='Funnel Cake')
# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Thelonious</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.

SPOTIFY_APP_ID = "e1f239ec0ee443689d6786fd3f397af1" 
SPOTIFY_APP_SECRET = "cbecd4d200f8482d910cb1db77d6f10c" 
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

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text + loading() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))
application.add_url_rule('/login', 'world', login())
# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
