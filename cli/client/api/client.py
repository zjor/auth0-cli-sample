import os
import dotenv
import requests

dotenv.load_dotenv()

BASE_URL = os.getenv('API_BASE_URL')


class ApiClient:
    _instance = None

    @staticmethod
    def get_instance():
        if not ApiClient._instance:
            ApiClient._instance = ApiClient(BASE_URL)
        return ApiClient._instance

    def __init__(self, base_url):
        self.base_url = base_url

    def get_token_info(self, access_token):
        url = f"{self.base_url}/token"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return response.status_code, response.json()

    def get_profile(self, access_token):
        url = f"{self.base_url}/profile"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return response.status_code, response.json()


if __name__ == "__main__":
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVrVnRTQnY4aGFDa2c4S09VMkRJeiJ9.eyJpc3MiOiJodHRwczovL2Rldi1mN3RlYm52cC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDMyNTMyOTMzOTc4NDAzMDg1ODUiLCJhdWQiOlsiaHR0cHM6Ly9kZXYtZjd0ZWJudnAudXMuYXV0aDAuY29tL2FwaS92Mi8iLCJodHRwczovL2Rldi1mN3RlYm52cC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjQ1MjIzNjkxLCJleHAiOjE2NDUzMTAwOTEsImF6cCI6InZXSHdjTjJVeURUN21WckZxVDlaZ3dTeTExT2Y2WDdpIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBvZmZsaW5lX2FjY2VzcyJ9.kKteWILz-iXvDtkxpoSo7fP3weRy6cIm0HBj7mx3VQ1R2Jd9UkbSPpQFBOmQTsOwa_bpvXMWwAImT4zpfNlvr_tumuttch8UIjMn8pk6G7hX-F8wdK06gBYpGo7TkgmWSwdnzP4kn1Y2DJjpyy4KloN8TAPnat9_gaBKqEiu5Uxh9Xxh4y7-_rjmWZ5sklagh56aDsIFlYELSE89cTW92aRyZCWzjjktrFHOIAR64pAkuohkmrmq3R4sQbstVlwHmFMlmjtuCo_EPw0vcg-296lm3XgHYsOFbjw_x7qYhhsoLv33TMPhHmV2mg7neMHkiiPIJRDQveHBXz6Wr10brw"
    client = ApiClient.get_instance()

    code, response = client.get_token_info(access_token)
    print(f"{code}: {response}")

    code, response = client.get_profile(access_token)
    print(f"{code}: {response}")
