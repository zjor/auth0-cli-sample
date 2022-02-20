import os
import time

from cli.client.auth0.stored_token import RefreshableToken, TokenStorage

STORAGE_FILENAME = '.credentials'


class TestRefreshableToken:
    def test_is_expired(self):
        now = round(time.time())
        token = RefreshableToken()

        token.expires_at = now + 1
        assert not token.is_expired()

        token.expires_at = now - 1
        assert token.is_expired()


class TestTokenStorage:
    @staticmethod
    def remove_storage():
        if os.path.exists(STORAGE_FILENAME):
            os.remove(STORAGE_FILENAME)

    def test_should_store_and_load_token(self):
        TestTokenStorage.remove_storage()

        now = round(time.time())
        token = RefreshableToken('access_token', 'refresh_token', now + 1)
        storage = TokenStorage(STORAGE_FILENAME)
        storage.store(token)

        loaded = storage.load()
        assert loaded.access_token == token.access_token
        assert loaded.refresh_token == token.refresh_token
        assert loaded.expires_at == token.expires_at

    def test_should_return_none_if_not_stored(self):
        TestTokenStorage.remove_storage()

        storage = TokenStorage(STORAGE_FILENAME)
        loaded = storage.load()
        assert not loaded
