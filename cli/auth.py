import time
import logging
import colorama
from termcolor import colored
from http.client import HTTPConnection
from cli.client.auth0.client import Auth0Client
from cli.client.auth0.stored_token import RefreshableToken, TokenStorage

colorama.init()


def white_bold(text):
    return colored(text, 'white', attrs=['bold'])


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

    refreshableToken = TokenStorage.get_instance().load()
    if refreshableToken:
        # skip authentication
        # try to use accessToken
        # if expired use refreshToken
        # retry API call
        # if fails -> fallback to authentication
        print(f"{refreshableToken.__dict__}")
    else:
        auth0_client = Auth0Client.get_instance()

        device_code_response = auth0_client.get_device_code()
        print(f"Device code: {white_bold(device_code_response.device_code)}")
        print(f"Please visit URL: {white_bold(device_code_response.verification_uri_complete)}")

        attempts = 0
        while True:
            attempts += 1
            time.sleep(device_code_response.interval)
            print(f"Waiting for the device approval. Attempt: {attempts}")
            code, access_token_response = auth0_client.get_access_token(device_code_response.device_code)
            if attempts >= 15 or code == 200:
                break

        if code == 200:
            print(f"\nAccess token: {access_token_response.access_token}\n")

            TokenStorage.get_instance().store(RefreshableToken(
                access_token=access_token_response.access_token,
                refresh_token=access_token_response.refresh_token,
                expires_at=access_token_response.expires_in + round(time.time())
            ))

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
