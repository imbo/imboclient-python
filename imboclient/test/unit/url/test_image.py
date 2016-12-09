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
        assert test_result == 'http://imbo.local/users/public/images/ffffffffffffffffffffffffffffffff?accessToken=5754ace791efc0faa130293881ab47aa0d5904dafdaf99287994377f85392738'

    def test_resource_url(self):
        test_result = self._url_image.resource_url()
        assert test_result == 'http://imbo.local/users/public/images/ffffffffffffffffffffffffffffffff'

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

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_crop(self, mock_add_query_param):
        result = self._url_image.crop(1, 1, 1, 1)
        mock_add_query_param.assert_called_once_with('t[]', 'crop:x=1,y=1,width=1,height=1')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_flip_horizontally(self, mock_add_query_param):
        result = self._url_image.flip_horizontally()
        mock_add_query_param.assert_called_once_with('t[]', 'flipHorizontally')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_flip_vertically(self, mock_add_query_param):
        result = self._url_image.flip_vertically()
        mock_add_query_param.assert_called_once_with('t[]', 'flipVertically')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_resize(self, mock_add_query_param):
        result = self._url_image.resize(100, 200)
        mock_add_query_param.assert_called_once_with('t[]', 'resize:width=100,height=200')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_resize_height(self, mock_add_query_param):
        result = self._url_image.resize(None, 200)
        mock_add_query_param.assert_called_once_with('t[]', 'resize:height=200')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_resize_width(self, mock_add_query_param):
        result = self._url_image.resize(100)
        mock_add_query_param.assert_called_once_with('t[]', 'resize:width=100')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_max_size(self, mock_add_query_param):
        result = self._url_image.max_size(100, 200)
        mock_add_query_param.assert_called_once_with('t[]', 'maxSize:width=100,height=200')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_max_size_height(self, mock_add_query_param):
        result = self._url_image.max_size(None, 200)
        mock_add_query_param.assert_called_once_with('t[]', 'maxSize:height=200')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_max_size_width(self, mock_add_query_param):
        result = self._url_image.max_size(300)
        mock_add_query_param.assert_called_once_with('t[]', 'maxSize:width=300')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_rotate(self, mock_add_query_param):
        result = self._url_image.rotate(90, 'ffffff')
        mock_add_query_param.assert_called_once_with('t[]', 'rotate:angle=90,bg=ffffff')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_thumbnail(self, mock_add_query_param):
        result = self._url_image.thumbnail()
        mock_add_query_param.assert_called_once_with('t[]', 'thumbnail:width=50,height=50,fit=outbound')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_canvas(self, mock_add_query_param):
        result = self._url_image.canvas(50, 60, 'testmode', 1, 2, '000000')
        mock_add_query_param.assert_called_once_with('t[]', 'canvas:width=50,height=60,mode=testmode,x=1,y=2,bg=000000')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_transpose(self, mock_add_query_param):
        result = self._url_image.transpose()
        mock_add_query_param.assert_called_once_with('t[]', 'transpose')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_transverse(self, mock_add_query_param):
        result = self._url_image.transverse()
        mock_add_query_param.assert_called_once_with('t[]', 'transverse')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_desaturate(self, mock_add_query_param):
        result = self._url_image.desaturate()
        mock_add_query_param.assert_called_once_with('t[]', 'desaturate')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.image.UrlImage.add_query_param')
    def test_sepia(self, mock_add_query_param):
        result = self._url_image.sepia()
        mock_add_query_param.assert_called_once_with('t[]', 'sepia:threshold=80')
        assert type(result) is imboclient.url.image.UrlImage

    @patch('imboclient.url.url.Url.reset')
    def test_reset(self, mock_url_reset):
        self._url_image._image_identifier = 'ffffffffffffffffffffffffffffffffffff'
        result = self._url_image.reset()
        mock_url_reset.assert_called_once_with()
        assert len(self._url_image._image_identifier) == 32
        assert type(result) is imboclient.url.image.UrlImage
