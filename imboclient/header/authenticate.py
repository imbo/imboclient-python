import hmac
import hashlib
import sys

class Authenticate:
    def __init__(self, public_key, private_key, method, url, timestamp):
        self._public_key = public_key
        self._private_key = private_key

        self.method = method
        self.url = url
        self.timestamp = timestamp

    def _generate_auth_hash(self):        
        data = self.method + '|' + self.url + '|' + self._public_key + '|' + self.timestamp
        private_key = self._private_key

        if sys.version_info >= (3,):
            data = bytes(data, 'utf-8')
            private_key = bytes(self._private_key, 'utf-8')

        return hmac.new(private_key, data, hashlib.sha256).hexdigest()

    def headers(self):
        signature = self._generate_auth_hash()
        return {"Accept": "application/json", "X-Imbo-Authenticate-Signature": signature, "X-Imbo-Authenticate-Timestamp": self.timestamp}
