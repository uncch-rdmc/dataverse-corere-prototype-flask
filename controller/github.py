from requests_oauthlib import OAuth2Session

from flask import Blueprint, render_template, abort

app_github = Blueprint('app_github', __name__)

import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import flask

# This information is obtained upon registration of a new GitHub
client_id = os.environ.get("FN_GITHUB_CLIENT_ID", default=False)
client_secret = os.environ.get("FN_GITHUB_CLIENT_SECRET", default=False)
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
BASE_URI = os.environ.get("FN_BASE_URI", default=False)

AUTH_TOKEN_KEY = 'auth_token'

@app_github.route("/github/login")
def github_login():
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)

@app_github.route("/github/callback")
def github_callback():
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,authorization_response=flask.request.url)

    userinfo = github.get('http://api.github.com/user').json()

    flask.session[AUTH_TOKEN_KEY] = token


    flask.session['username'] = userinfo['login']

    name = userinfo['name'].split()
    if len(name) == 1:
        name[1] = name[0]

    flask.session['given_name'] = name[0]
    flask.session['family_name'] = name[1]
    
    return flask.redirect(BASE_URI, code=302)