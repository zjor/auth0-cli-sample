import os
import dotenv
import requests
from cli.client.auth0.protocol import GetDeviceCodeResponse, GetAccessTokenResponse, GetUserInfoResponse

dotenv.load_dotenv()

AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_BASE_URL = os.getenv('AUTH0_BASE_URL')


class Auth0Client:
    __instance = None

    @staticmethod
    def get_instance():
        if not Auth0Client.__instance:
            Auth0Client.__instance = Auth0Client(AUTH0_BASE_URL, AUTH0_CLIENT_ID, AUTH0_AUDIENCE)
        return Auth0Client.__instance

    def __init__(self, base_url, client_id, audience):
        self.base_url = base_url
        self.client_id = client_id
        self.audience = audience

    def get_device_code(self):
        scopes = ['name', 'email', 'profile', 'openid', 'offline_access']
        url = f"{self.base_url}/oauth/device/code"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_id,
            'scope': ' '.join(scopes),
            'audience': self.audience
        }

        response = requests.post(url, data=data, headers=headers)
        return GetDeviceCodeResponse.from_json(response.json())

    def get_access_token(self, device_code):
        url = f"{self.base_url}/oauth/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_id,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'device_code': device_code
        }
        response = requests.post(url, data=data, headers=headers)
        return response.status_code, GetAccessTokenResponse.from_json(response.json())

    def get_user_info(self, access_token):
        url = f"{self.base_url}/userinfo"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return response.status_code, GetUserInfoResponse.from_json(response.json())
