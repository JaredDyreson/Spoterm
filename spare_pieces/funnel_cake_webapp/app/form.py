#!/usr/bin/env python3.5

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = StringField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')
class funnel_cake_form(FlaskForm):
	url_one = StringField('Spotify Playlist URL One', validators=[DataRequired()])
	url_two = StringField('Spotify Playlist URL Two', validators=[DataRequired()])
	playlist_output_name = StringField('Output Name', validators=[DataRequired()])
	submit = SubmitField('Submit')
