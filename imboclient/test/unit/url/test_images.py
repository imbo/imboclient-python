from imboclient.url import images


class TestUrlImages:
    def setup(self):
        self._url_images = images.UrlImages('http://imbo.local', 'public', 'private')

    def teardown(self):
        self._url_images = None

    def test_url(self):
        test_result = self._url_images.url()
        assert 'http://imbo.local/users/public/images.json?accessToken=581fcefec5773b6f865fc2d37970442401eee2e9dab13abd826e989f8f9e1e75' == test_result

    def test_resource_url(self):
        test_result = self._url_images.resource_url()
        assert 'http://imbo.local/users/public/images.json' == test_result
