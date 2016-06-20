# Sample Clever Instant Login integration
# Uses Flask framework and raw HTTP requests to demo OAuth 2.0 flow

import base64
import json
import logging
import os
import requests
import urllib

from flask import request
from logging.handlers import RotatingFileHandler


# Obtain your Client ID and Client secret from your Clever developer dashboard
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

# Clever redirect URIs must be configured from your Clever developer dashboard.
REDIRECT_URL = 'http://localhost:5000/oauth'

CLEVER_OAUTH_URL = 'https://clever.com/oauth/tokens'
CLEVER_API_BASE_URL = 'https://api.clever.com'

# Count of retries in the event of non-200 HTTP response
MAX_ATTEMPTS = 5


def oauth(request):
    """
    Clever will redirect users to your web application
    """
    code = request.args.get('code')
    scopes = request.args.get('scope')
    access_token = None

    access_token = get_access_token(code, scopes)
    message = get_user(access_token)
    return message


def get_access_token(code, scopes):
    """
    Exchange code for an Clever access token for user
    """

    payload = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URL
    }

    headers = {
        'Authorization': 'Basic {base64string}'.format(
            base64string=base64.b64encode(CLIENT_ID + ':' + CLIENT_SECRET)),
        'Content-Type': 'application/json'
    }

    response = requests.post(
        CLEVER_OAUTH_URL,
        data=json.dumps(payload),
        headers=headers)

    if response.status_code is not requests.codes.ok:
        response = retry(
            url=CLEVER_OAUTH_URL,
            data=json.dumps(payload),
            headers=headers,
            method='POST')

    if response is not None:
        results = response.json()
        if 'access_token' in results:
            token = results['access_token']
        else:
            token = None
            print '[CUSTOM] Access token not found in results.' + str(results)
    else:
        token = None
        print '[CUSTOM] Token set to none'
    return token


def get_user(token):
    """
    Returns user first name and last name in message
    GET https://api.clever.com/me and
    GET https://api.clever.com/v1.1/district_admins/{id}
    """
    headers = {
        'Authorization': 'Bearer {token}'.format(token=token)
    }
    response = requests.get(CLEVER_API_BASE_URL + '/me', headers=headers)

    if response.status_code is not requests.codes.ok:
        response = retry(
            url=CLEVER_API_BASE_URL + '/me',
            data=None,
            headers=headers,
            method='GET')

    if response is not None:
        results = response.json()
        user_id = results['data']['id']
        user_type = results['data']['type']
        user_district = results['data']['district']

        if results['data']['type'] == 'district_admin':
            response = requests.get(
                CLEVER_API_BASE_URL + '/v1.1/district_admins/' + user_id,
                headers=headers)
            results = response.json()
            user_first_name = str(results['data']['name']['first'])
            user_last_name = str(results['data']['name']['last'])
            message = user_first_name + ' ' + user_last_name
        else:
            # Functionality limited to Clever user_type = district_admin
            message = None
    else:
        message = None

    return message


def retry(url, data, headers, method, attempts=0):
    """
    Retries failed API calls
    """
    if attempts >= MAX_ATTEMPTS:
        print "[CUSTOM] MAX_ATTEMPTS reached: " + str(method) + ' ' + str(url)
        return None

    attempts += 1

    try:
        response = requests.request(method, url, data=data, headers=headers)
    except requests.exceptions.ConnectionError as e:
        print '[CUSTOM] A Connection Error has occurred: ' + str(e.message)
        response = retry(
            url=url,
            data=data,
            headers=headers,
            method=method,
            attempts=attempts)

    if response.status_code in [400, 401, 412, 499]:
        print '[CUSTOM] An HTTP 4XX Client Error has occurred.'
        response = retry(
            url=url,
            data=data,
            headers=headers,
            method=method,
            attempts=attempts)

    elif response.status_code in [500]:
        time.sleep(2**attempts)
        response = retry(
            url=url,
            data=data,
            headers=headers,
            method=method,
            attempts=attempts)

    return response
