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
REDIRECT_URL = 'http://localhost:5000/oauth'

CLEVER_OAUTH_URL = 'https://clever.com/oauth/tokens'
CLEVER_API_BASE_URL = 'https://api.clever.com'

def incoming(request):
    code = str(request.args.get('code'))
    scopes = request.args.get('scope') 

    payload = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URL
    }

    headers = {
        'Authorization': 'Basic {base64string}'.format(base64string = base64.b64encode(CLIENT_ID + ':' + CLIENT_SECRET)),
        'Content-Type': 'application/json'
    }

    response = requests.post(CLEVER_OAUTH_URL, data=json.dumps(payload), headers=headers).json()

    if 'access_token' in response:
        token = response['access_token']
        results = user(token)
        message = results
    else:
    # Example error response: {u'error_description': u'invalid code', u'error': u'invalid_grant'}
        message = response['error_description']
    return message

def user(token):
# Determine identity of authenticated user

    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }

    me = requests.get(CLEVER_API_BASE_URL + '/me', headers=headers).json()

    user_id = me['data']['id']
    user_type = me['data']['type']
    user_district = me['data']['district']

    if me['data']['type'] == 'district_admin':
        results = requests.get(CLEVER_API_BASE_URL + '/v1.1/district_admins/' + user_id, headers=headers).json()
        user_first_name = str(results['data']['name']['first'])
        user_last_name = str(results['data']['name']['last'])
        message = 'Hello ' + user_first_name + ' ' + user_last_name
    else:
        message = 'TODO'

    return message
