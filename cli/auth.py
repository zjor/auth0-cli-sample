import os
import time
import dotenv
import requests
import logging
import colorama
from termcolor import colored
from http.client import HTTPConnection
from cli.auth0_client import Auth0Client
from cli.auth0_protocol import GetDeviceCodeResponse, GetAccessTokenResponse, GetUserInfoResponse

colorama.init()

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


if __name__ == "__main__":
    auth0_client = Auth0Client.get_instance()

    device_code_response = auth0_client.get_device_code()
    print(f"Device code: {device_code_response.device_code}")
    print(f"Please visit URL: {device_code_response.verification_uri_complete}")

    attempts = 0
    while True:
        attempts += 1
        time.sleep(device_code_response.interval)
        print(f"Waiting for the device approval. Attempt: {attempts}")
        code, access_token_response = auth0_client.get_access_token(device_code_response.device_code)
        if attempts >= 15 or code == 200:
            break

    if code == 200:
        print(f"Access token: {access_token_response.access_token}")
        code, user_info = auth0_client.get_user_info(access_token_response.access_token)
        if user_info.error:
            print(f"Failed to get user info: {user_info.error} - {user_info.error_description}")
        else:
            print(f"Subject: {user_info.sub}")
            print(f"Name: {user_info.name}")
            print(f"Email: {user_info.email}")
            print(f"Picture: {user_info.picture}")
    else:
        print("Failed to get access token")
