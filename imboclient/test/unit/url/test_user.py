from imboclient.url import  user


class TestUrlUser:
    def setup(self):
        self._url_user = user.UrlUser('http://imbo.local', 'public', 'private')

    def teardown(self):
        self._url_user = None

    def test_resource_url(self):
        assert 'http://imbo.local/users/public.json' == self._url_user.resource_url()

    def test_url(self):
        assert 'http://imbo.local/users/public.json?accessToken=86a4c0c0f8a26969949679b556433f82f36bdfdda797cf134f5f61fdda6d3c16' == self._url_user.url()
