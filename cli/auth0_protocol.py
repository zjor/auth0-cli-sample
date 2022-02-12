class GetDeviceCodeResponse:
    def __init__(self):
        self.device_code: str = None
        self.user_code: str = None
        self.verification_uri: str = None
        self.expires_in: int = None
        self.interval: int = None
        self.verification_uri_complete: str = None,
        self.error: str = None
        self.error_description: str = None

    @staticmethod
    def from_json(json):
        i = GetDeviceCodeResponse()
        i.__dict__.update(json)
        return i


class GetAccessTokenResponse:
    def __init__(self):
        self.access_token: str = None
        self.refresh_token: str = None
        self.id_token: str = None
        self.scope: str = None
        self.expires_in: int = None
        self.token_type: str = None
        self.error: str = None
        self.error_description: str = None

    @staticmethod
    def from_json(json):
        i = GetAccessTokenResponse()
        i.__dict__.update(json)
        return i


class GetUserInfoResponse:
    def __init__(self):
        self.sub: str = None
        self.given_name: str = None
        self.family_name: str = None
        self.nickname: str = None
        self.name: str = None
        self.picture: str = None
        self.locale: str = None
        self.updated_at: str = None
        self.email: str = None
        self.email_verified: bool = None
        self.error: str = None
        self.error_description: str = None

    @staticmethod
    def from_json(json):
        i = GetUserInfoResponse()
        i.__dict__.update(json)
        return i

