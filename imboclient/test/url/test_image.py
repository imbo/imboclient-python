import imboclient
from mock import patch
from mock import MagicMock
from nose import with_setup
from nose.tools import raises
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

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_border_default(self, mock_add_query_param):
        result = self._url_image.border()
        mock_add_query_param.assert_called_once_with('t[]', 'border:color=000000,width=1,height=1')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_border(self, mock_add_query_param):
        result = self._url_image.border('ffffff', 100, 100)
        mock_add_query_param.assert_called_once_with('t[]', 'border:color=ffffff,width=100,height=100')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_compress_default(self, mock_add_query_param):
        result = self._url_image.compress()
        mock_add_query_param.assert_called_once_with('t[]', 'compress:quality=75')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_compress(self, mock_add_query_param):
        result = self._url_image.compress(55)
        mock_add_query_param.assert_called_once_with('t[]', 'compress:quality=55')
        assert type(result) is imboclient.url.image.UrlImage

    def test_convert(self):
        result = self._url_image.convert('jpg')
        assert self._url_image._image_identifier == 'ffffffffffffffffffffffffffffffff.jpg'
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.convert')
    def test_gif(self, mock_convert):
        result = self._url_image.gif()
        mock_convert.assert_called_once_with('gif')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.convert')
    def test_jpg(self, mock_convert):
        result = self._url_image.jpg()
        mock_convert.assert_called_once_with('jpg')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.convert')
    def test_png(self, mock_convert):
        result = self._url_image.png()
        mock_convert.assert_called_once_with('png')
        assert type(result) is imboclient.url.image.UrlImage

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

