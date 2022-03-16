import time

CREDENTIALS_FILENAME = '.credentials'


class RefreshableToken:
    def __init__(self, access_token: str = None, refresh_token: str = None, expires_at: int = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    def is_expired(self):
        now = round(time.time())
        return now >= self.expires_at if self.expires_at else True


class TokenStorage:

    @staticmethod
    def get_instance():
        return TokenStorage(CREDENTIALS_FILENAME)

    def __init__(self, filename):
        self.filename = filename

    def store(self, token: RefreshableToken):
        with open(self.filename, 'w') as f:
            for (k, v) in token.__dict__.items():
                f.write(f"{k}={v}\n")

    def load(self):
        data = {}
        try:
            with open(self.filename, 'r') as f:
                for line in f.readlines():
                    k, v = line.strip().split('=')
                    data[k] = v
            token = RefreshableToken()
            token.__dict__.update(data)

            if token.access_token:
                token.expires_at = int(token.expires_at)
                return token
            else:
                return None
        except FileNotFoundError:
            return None
