import os
import time
import dotenv
import requests
import logging
from http.client import HTTPConnection
from cli.auth0_protocol import GetDeviceCodeResponse, GetAccessTokenResponse, GetUserInfoResponse

dotenv.load_dotenv()

AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_BASE_URL = os.getenv('AUTH0_BASE_URL')


def enable_debug_logging():
    log = logging.getLogger('urllib3')
    log.setLevel(logging.DEBUG)

    # logging from urllib3 to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)

    # print statements from `http.client.HTTPConnection` to console/stdout
    HTTPConnection.debuglevel = 1


def get_device_code():
    scopes = ['name', 'email', 'profile', 'openid', 'offline_access']
    url = f"{AUTH0_BASE_URL}/oauth/device/code"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': AUTH0_CLIENT_ID,
        'scope': ' '.join(scopes),
        'audience': AUTH0_AUDIENCE
    }

    response = requests.post(url, data=data, headers=headers)
    return GetDeviceCodeResponse.from_json(response.json())


def get_access_token(device_code):
    url = f"{AUTH0_BASE_URL}/oauth/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': AUTH0_CLIENT_ID,
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
        'device_code': device_code
    }
    response = requests.post(url, data=data, headers=headers)
    return response.status_code, GetAccessTokenResponse.from_json(response.json())


def get_user_info(access_token):
    url = f"{AUTH0_BASE_URL}/userinfo"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.status_code, GetUserInfoResponse.from_json(response.json())


if __name__ == "__main__":
    device_code_response = get_device_code()
    print(f"Device code: {device_code_response.device_code}")
    print(f"Please visit URL: {device_code_response.verification_uri_complete}")

    attempts = 0
    while True:
        attempts += 1
        time.sleep(device_code_response.interval)
        print(f"Waiting for the device approval. Attempt: {attempts}")
        code, access_token_response = get_access_token(device_code_response.device_code)
        if attempts >= 15 or code == 200:
            break

    if code == 200:
        print(f"Access token: {access_token_response.access_token}")
        code, user_info = get_user_info(access_token_response.access_token)
        if user_info.error:
            print(f"Failed to get user info: {user_info.error} - {user_info.error_description}")
        else:
            print(f"Subject: {user_info.sub}")
            print(f"Name: {user_info.name}")
            print(f"Email: {user_info.email}")
            print(f"Picture: {user_info.picture}")
    else:
        print("Failed to get access token")
