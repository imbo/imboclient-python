import imboclient.url.status as status

class TestUrlStatus:
    def setup(self):
        self._url_status = status.UrlStatus('http://imbo.local', 'public', 'private')

    def teardown(self):
        self._url_status = None

    def test_url(self):
        assert 'http://imbo.local/users/public/status.json?accessToken=2b05985fbd038f5c6a97006a5dfe56ab4db6c19b31ccf6309a7313bbe85d52b3' == self._url_status.url()

    def test_resource_url(self):
        assert 'http://imbo.local/users/public/status.json' == self._url_status.resource_url()

