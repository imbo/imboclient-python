from imboclient.url import accesstoken
import mock
import hmac, hashlib


class TestAccessToken:
    def setup(self):
        self._access_token = accesstoken.AccessToken()

    def teardown(self):
        self._access_token = None

    def test_generate_token(self):
        test_url = 'http://imbo.local/users/public/randomfeature.json'
        test_key = 'private'

        test_result = self._access_token.generate_token(test_url, test_key)
        assert test_result == 'd247e6b332a4bb48fd936e81bc3f9510ac3b23d5ec07880afe3217a9b7d6ff5e'

