import hmac
import hashlib
import sys


class AccessToken:
    def generate_token(self, url, key):
        if sys.version_info < (3,):
            return hmac.new(key, url, hashlib.sha256).hexdigest()
        else:
            return hmac.new(bytes(key, 'utf-8'), bytes(url, 'utf-8'), hashlib.sha256).hexdigest()

