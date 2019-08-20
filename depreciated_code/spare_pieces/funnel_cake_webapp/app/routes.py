#!/usr/bin/env python3.5

from flask import Flask
from flask import render_template
from app import app
from app.form import LoginForm

app=Flask(__name__)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
