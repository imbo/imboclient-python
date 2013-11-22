import imboclient
from mock import patch
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

    def test_border_default(self):
        raise NotImplementedError("Test and implementation missing")

    def test_border(self):
        raise NotImplementedError("Test and implementation missing")

    def test_compress(self):
        raise NotImplementedError("Test and implementation missing")

    def test_convert(self):
        raise NotImplementedError("Test and implementation missing")

    def test_gif(self):
        raise NotImplementedError("Test and implementation missing")

    def test_jpg(self):
        raise NotImplementedError("Test and implementation missing")

    def test_png(self):
        raise NotImplementedError("Test and implementation missing")

    def test_crop(self):
        raise NotImplementedError("Test and implementation missing")

    def test_flip_horizontally(self):
        raise NotImplementedError("Test and implementation missing")

    def test_flip_vertically(self):
        raise NotImplementedError("Test and implementation missing")

    def test_resize(self):
        raise NotImplementedError("Test and implementation missing")

    def test_max_size(self):
        raise NotImplementedError("Test and implementation missing")

    def test_rotate(self):
        raise NotImplementedError("Test and implementation missing")

    def test_thumbnail(self):
        raise NotImplementedError("Test and implementation missing")

    def test_canvas(self):
        raise NotImplementedError("Test and implementation missing")

    def test_desaturate(self):
        raise NotImplementedError("Test and implementation missing")

    def test_sepia(self):
        raise NotImplementedError("Test and implementation missing")

    def test_reset(self):
        raise NotImplementedError("Test and implementation missing")

