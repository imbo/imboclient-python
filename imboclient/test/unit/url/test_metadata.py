from imboclient.url import metadata

class TestUrlMetadata:

    def setup(self):
        self._url_metadata = metadata.UrlMetadata('http://imbo.local', 'public', 'private', 'ffffffffffffffffffffffffffffffff')

    def teardown(self):
        self._url_metadata = None

    def test_url(self):
        test_result = self._url_metadata.url()
        assert test_result == 'http://imbo.local/users/public/ffffffffffffffffffffffffffffffff/meta.json?accessToken=5bf91fef561910747abba6dfcd468f2157fee8da9266a08d4be9ca69203dee77'

    def test_resource_url(self):
        test_result = self._url_metadata.resource_url()
        assert test_result == 'http://imbo.local/users/public/ffffffffffffffffffffffffffffffff/meta.json'

