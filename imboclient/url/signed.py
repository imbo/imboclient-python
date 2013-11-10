
import hmac, hashlib

class Signed:
    def __init__(self, public_key, private_key, method, url, timestamp):
        self._public_key = public_key
        self._private_key = private_key

        self.method = method
        self.url = url
        self.timestamp = timestamp

    def _generate_signature(self):
        data = self.method + '|' + self.url + '|' + self._public_key + '|' + self.timestamp
        return hmac.new(self._private_key, data, hashlib.sha256).hexdigest()

    def str(self):
        def first_delimeter(url):
            if url.find('?') > -1:
                return '&'
            else:
                return '?'

        signature = self._generate_signature()
        return "{}{}signature={}&timestamp={}".format(self.url, first_delimeter(self.url), signature, self.timestamp)
