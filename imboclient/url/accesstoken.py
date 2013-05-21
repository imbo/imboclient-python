import hmac, hashlib

class AccessToken:
    def generate_token(self, url, key):
        return hmac.new(key, url, hashlib.sha256).hexdigest()

