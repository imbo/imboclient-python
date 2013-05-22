from imboclient.url import image

class TestUrlImage:

    def setup(self):
        self._url_image = image.UrlImage('http://imbo.local', 'public', 'private', 'ffffffffffffffffffffffffffffffff')

    def teardown(self):
        self._url_image = None

    def test_url(self):
        test_result = self._url_image.url()
        assert test_result == 'http://imbo.local/users/public/ffffffffffffffffffffffffffffffff?accessToken=b86400becdaacbedf74f22c8d53b59d4bf8519fe6e75abdc1f0c84e9465a0169'

    def test_resource_url(self):
        test_result = self._url_image.resource_url()
        assert test_result == 'http://imbo.local/users/public/ffffffffffffffffffffffffffffffff'

