from flask import Flask, render_template, url_for, flash, redirect, request, session, Response
from flask_wtf import FlaskForm

import re
import json
import requests
import os
import sys

sys.path.append("../spotify_playlists/")
sys.path.append("../front_end_assets/")
sys.path.append("../stand_alone_authenticator/")
from forms import PlaylistMergeForm


import spotify_oauth_flow
import spotify_playlist

spotify_oauth_flow.app.run()

class EndpointAction(object):

	def __init__(self, action):
		self.action = action

	def __call__(self, *args):
		answer = self.action()
		self.response = Response(answer, status=200, headers={})
		return self.response

class FlaskAppWrapper(object):

	def __init__(self, name):
		self.app = Flask(name)
		self.app.config['SECRET_KEY'] = os.environ.get('SPOTIFY_SECRET_KEY')

	def add_all_endpoints(self):
		self.add_endpoint(endpoint="/", endpoint_name="index", handler=self.index)
		self.add_endpoint(endpoint="/about", endpoint_name="about", handler=self.about)
	def run(self):
		self.app.run()

	def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
		self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=['GET', 'POST']) 

	def index(self):
		form = PlaylistMergeForm(request.form)
		if(form.validate_on_submit()):
			flash("testing", "success")
			form = PlaylistMergeForm(formdata=None)
			return render_template('home.html', form=form)

		return render_template('home.html', form=form)

	def about(self):
		return render_template('about.html', title='About')

a = FlaskAppWrapper('funnel_cake_main')
a.add_all_endpoints()
a.run()
