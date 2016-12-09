from imboclient.url import metadata


class TestUrlMetadata:
    def setup(self):
        self._url_metadata = metadata.UrlMetadata('http://imbo.local', 'public', 'private', 'ffffffffffffffffffffffffffffffff')

    def teardown(self):
        self._url_metadata = None

    def test_url(self):
        test_result = self._url_metadata.url()
        assert test_result == 'http://imbo.local/users/public/images/ffffffffffffffffffffffffffffffff/metadata?accessToken=f9d3135034343eb3f709c19a5fa4fcdf026d6d6a5f1191906e5f83a06e2d8ac6'

    def test_resource_url(self):
        test_result = self._url_metadata.resource_url()
        assert test_result == 'http://imbo.local/users/public/images/ffffffffffffffffffffffffffffffff/metadata'
