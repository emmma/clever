# Sample Clever Instant Login implementation that handles signing in users from Clever portals
# Uses Flask framework and raw HTTP requests to demo OAuth 2.0 flow

import base64
import json
import os
import requests
import urllib

from flask import request

# Obtain your Client ID and Client secret from your Clever developer dashboard at https://account.clever.com/partner/applications
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']


# Clever redirect URIs must be preregistered for your app in your Clever developer dashboard.
REDIRECT_URI = 'http://localhost:5000/oauth'

CLEVER_OAUTH_URL = 'https://clever.com/oauth/tokens'
CLEVER_API_BASE_URL = 'https://api.clever.com'

def incoming(request):
    code = str(request.args.get('code'))
    scopes = request.args.get('scope') 

    payload = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI
    }

    headers = {
        'Authorization': 'Basic {base64string}'.format(base64string = base64.b64encode(CLIENT_ID + ':' + CLIENT_SECRET)),
        'Content-Type': 'application/json'
    }

    response = requests.post(CLEVER_OAUTH_URL, data=json.dumps(payload), headers=headers).json()

    #TODO handle error when access token not there

    return response['access_token']