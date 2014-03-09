from imboclient.url import images

class TestUrlImages:
    def setup(self):
        self._url_images = images.UrlImages('http://imbo.local', 'public', 'private')

    def teardown(self):
        self._url_images = None

    def test_url(self):
        test_result = self._url_images.url()
        assert 'http://imbo.local/users/public/images?accessToken=71ecfc20405e398eb0773ebee91e8ed254ee50450c9449484f19dcea7b8ce9bc' == test_result

    def test_resource_url(self):
        test_result = self._url_images.resource_url()
        assert 'http://imbo.local/users/public/images' == test_result

