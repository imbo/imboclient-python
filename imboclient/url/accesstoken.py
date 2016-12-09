import hmac
import hashlib


class AccessToken:
    def generate_token(self, url, key):
        return hmac.new(bytes(key, 'utf-8'), bytes(url, 'utf-8'), hashlib.sha256).hexdigest()

