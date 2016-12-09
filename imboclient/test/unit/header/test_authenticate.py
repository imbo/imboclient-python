from imboclient.header import authenticate


class TestAuthenticate:
    def setup(self):
        self._authenticate = authenticate.Authenticate('public', 'private', 'GET', 'http://imbo/', 'timestamp');

    def teardown(self):
        self._authenticate = None

    def test_authenticate(self):
        headers = self._authenticate.headers()
        assert headers['Accept'] == 'application/json'
        assert headers['X-Imbo-Authenticate-Signature'] == '91cc40279b0facfa8139cfd32c41392b18212c21516543827fb0d7d87e6beaef'
        assert headers['X-Imbo-Authenticate-Timestamp'] == 'timestamp'

