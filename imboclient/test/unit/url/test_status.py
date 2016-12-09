from imboclient.url import status


class TestUrlStatus:
    def setup(self):
        self._url_status = status.UrlStatus('http://imbo.local', 'public', 'private')

    def teardown(self):
        self._url_status = None

    def test_url(self):
        assert 'http://imbo.local/status.json?accessToken=ae0d73a0131e832e05d1eaad1996d5c4cce97f5aa0ecb8137c80d369f2c1e7a8' == self._url_status.url()

    def test_resource_url(self):
        assert 'http://imbo.local/status.json' == self._url_status.resource_url()
