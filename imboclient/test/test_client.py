from mock import patch
from nose import with_setup
from imboclient import client as imbo
import requests
import imboclient.url.image, imboclient.url.images

class TestClient:

    def setup(self):
        self._client = imbo.Client(['http://imbo.local'], 'public', 'private');

    def teardown(self):
        self._client = None

    def test_server_urls_generic(self):
        self._client = imbo.Client(['imbo.local'], 'public', 'private');
        assert self._client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_http(self):
        self._client = imbo.Client(['http://imbo.local'], 'public', 'private');
        assert self._client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_https(self):
        self._client = imbo.Client(['https://imbo.local'], 'public', 'private');
        assert self._client.server_urls[0] == 'https://imbo.local'

    def test_server_urls_port_normal(self):
        self._client = imbo.Client(['http://imbo.local'], 'public', 'private');
        assert self._client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_port_normal_explicit(self):
        self._client = imbo.Client(['http://imbo.local:80'], 'public', 'private');
        assert self._client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_port_ssl(self):
        self._client = imbo.Client(['https://imbo.local:443'], 'public', 'private');
        assert self._client.server_urls[0] == 'https://imbo.local'

    def test_server_urls_port_explicit_without_protocol(self):
        self._client = imbo.Client(['imbo.local:8000'], 'public', 'private');
        assert self._client.server_urls[0] == 'http://imbo.local:8000'

    def test_status_url(self):
        raise NotImplementedError("Test missing")

    def test_user_url(self):
        raise NotImplementedError("Test missing")

    @patch('imboclient.url.images.UrlImages')
    def test_images_url(self, mocked_url_images):
        mocked_url_images_instance = mocked_url_images.return_value
        mocked_url_images_instance.url.return_value = 'correctimagesurl'

        images_url = self._client.images_url()
        mocked_url_images.assert_called_once_with('http://imbo.local', 'public', 'private')
        mocked_url_images_instance.url.assert_called_once()
        assert images_url == 'correctimagesurl'

    @patch('imboclient.url.image.UrlImage')
    def test_image_url(self, mocked_url_image):
        mocked_url_image_instance = mocked_url_image.return_value
        mocked_url_image_instance.url.return_value = 'correctimageurl'

        image_url = self._client.image_url('ff')
        mocked_url_image.assert_called_once_with('http://imbo.local', 'public', 'private', 'ff')
        mocked_url_image_instance.url.assert_called_once()
        assert image_url == 'correctimageurl'

    def test_add_image(self):
        raise NotImplementedError("Test missing")

    def test_add_image_from_string(self):
        raise NotImplementedError("Test missing")

    def test_add_image_from_url(self):
        raise NotImplementedError("Test missing")

    def test_image_exists(self):
        raise NotImplementedError("Test missing")

    @patch('requests.head')
    @patch('imboclient.url.image.UrlImage')
    def test_image_identifier_exists_true(self, mocked_url_image, mocked_requests_head) :
        mocked_requests_head.return_value = self._valid_requests_response_stub_ok()
        mocked_url_image_instance = mocked_url_image.return_value
        mocked_url_image_instance.url.return_value = 'http://imbo.local/users/public/ff?accessToken=aa'

        assert self._client.image_identifier_exists('ff') == True
        mocked_requests_head.assert_called_once_with('http://imbo.local/users/public/ff?accessToken=aa')
        mocked_url_image.assert_called_once_with('http://imbo.local', 'public', 'private', 'ff')

    @patch('requests.head')
    @patch('imboclient.url.image.UrlImage')
    def test_image_identifier_exists_false(self, mocked_url_image, mocked_requests_get):
        mocked_requests_get.return_value = self._invalid_requests_response_stub_not_found()
        mocked_url_image_instance = mocked_url_image.return_value
        mocked_url_image_instance.url.return_value = 'http://imbo.local/users/public/ffa?accessToken=aaf'

        assert self._client.image_identifier_exists('ffa') == False
        mocked_requests_get.assert_called_once_with('http://imbo.local/users/public/ffa?accessToken=aaf')
        mocked_url_image.assert_called_once_with('http://imbo.local', 'public', 'private', 'ffa')

    def test_head_image(self):
        raise NotImplementedError("Test missing")

    def test_delete_image(self):
        raise NotImplementedError("Test missing")

    def test_edit_metadata(self):
        raise NotImplementedError("Test missing")

    def test_replace_metadata(self):
        raise NotImplementedError("Test missing")

    def test_delete_metadata(self):
        raise NotImplementedError("Test missing")

    def test_num_images(self):
        raise NotImplementedError("Test missing")

    def test_images(self):
        raise NotImplementedError("Test missing")

    def test_image_data(self):
        raise NotImplementedError("Test missing")

    def test_image_data_from_url(self):
        raise NotImplementedError("Test missing")

    def test_image_properties_from_url(self):
        raise NotImplementedError("Test missing")

    def test_image_properties(self):
        raise NotImplementedError("Test missing")

    def test_image_identifier(self):
        raise NotImplementedError("Test missing")

    def test_image_identifier_from_string(self):
        raise NotImplementedError("Test missing")

    def test_server_status(self):
        raise NotImplementedError("Test missing")

    def test_user_info(self):
        raise NotImplementedError("Test missing")

    def _valid_requests_response_stub_ok(self):
        class ResponseStub:
            status_code = requests.codes.ok

        return ResponseStub()

    def _invalid_requests_response_stub_not_found(self):
        class ResponseStub:
            status_code = requests.codes.not_found

        return ResponseStub()


