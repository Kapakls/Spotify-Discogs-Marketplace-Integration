from datetime import datetime
from flask import Flask, redirect, jsonify, request, session
import requests
import urllib.parse
import json 
import os
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(24)

output = ''                                                     # output = Your output folder for the spotify album data
searchlistings = ''                                             # searchlistings = Your path to searchlistings.py

client_ID = ''                                                  # client_ID = Spotify API client ID                                                
clien_secret = ''                                               # client_secret = Spotify API secret client ID
redirect_URL = 'http://localhost:5000/callback'

# No editing beyond this point

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'    
API_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    return ('Welcome to Spotify - Discogs Marketplace Integration<br>'
            '<a href="/login">Login with Spotify</a>'
            )


@app.route('/login')
def login():    
    scope = 'user-top-read user-library-read'

    params = {
        'client_id': client_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': redirect_URL,  
        'show_dialog': True
    }

    auth_URL = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"  
    
    return redirect(auth_URL)


@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']}) 

    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],  
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_URL,
            'client_id': client_ID,
            'client_secret': clien_secret
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        print('Debug - Token info:', token_info)

        return redirect('/data')
    

@app.route('/data')
def get_data():
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh_token')

    limit = 50

    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    
    params = {
    'limit': limit
    }

    if not os.path.exists(output):
        os.makedirs(output)

    albums_file_path = os.path.join(output, 'albums.json')
    if not os.path.exists(albums_file_path):
        with open(albums_file_path, 'w') as new_file:
            json.dump({}, new_file, indent=2)

    response = requests.get(API_URL + 'me/albums', headers=headers, params=params)
    albums = response.json()
    with open(albums_file_path, 'w') as new_file:
        json.dump(albums, new_file, indent=2)

    subprocess.run(['python', searchlistings])

    return (
        'Script running...<br>'
        '[✓] getdata.py accessed<br>'
        '[✓] searchlistings.py accessed<br>'
        '[✓] filter.py accessed - saving URLs localy'
    )


@app.route('/refresh_token')
def refresh_token():
    if 'refresh_token' not in session: 
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': client_ID,
            'client_secret': clien_secret
        }

        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_i  n']

        return redirect('/playlist')

if __name__ == '__main__':        
    app.run(host='0.0.0.0', debug=True)

