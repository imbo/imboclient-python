import hmac
import hashlib
import sys


class AccessToken:
    def __init__(self, token_key='accessToken'):
        self._token_key = token_key

    def generate_token(self, url, key):
        if sys.version_info < (3,):
            return hmac.new(key, url, hashlib.sha256).hexdigest()
        else:
            return hmac.new(bytes(key, 'utf-8'), bytes(url, 'utf-8'), hashlib.sha256).hexdigest()

    def token_key(self):
        return self._token_key
