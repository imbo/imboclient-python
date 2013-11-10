from mock import patch
from mock import MagicMock
from nose import with_setup
from nose.tools import raises
import requests
import os
import json
from imboclient import client as imbo
from imboclient.url import image, images, status, user, accesstoken
import __builtin__

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

    @patch('imboclient.url.status.UrlStatus')
    def test_status_url(self, mocked_url_status):
        mocked_url_status_instance = mocked_url_status.return_value
        mocked_url_status_instance.url.return_value = 'correctstatusurl'

        status_url = self._client.status_url()
        mocked_url_status_instance.url.assert_called_once()
        assert status_url == 'correctstatusurl'

    @patch('imboclient.url.user.UrlUser')
    def test_user_url(self, mocked_url_user):
        mocked_url_user_instance = mocked_url_user.return_value
        mocked_url_user_instance.url.return_value = 'correctuserurl'

        user_url = self._client.user_url()
        mocked_url_user_instance.url.assert_called_once()
        assert user_url == 'correctuserurl'

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

    @patch('imboclient.url.signed.Signed.str')
    @patch('requests.put')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('__builtin__.open')
    def test_add_image(self, mocked_open, mocked_os_path_getsize, mocked_os_path_isfile, mocked_requests_put, mocked_url_signature):
        mocked_open_return = MagicMock()
        mocked_open_return.read.return_value = 'content'
        mocked_open.return_value = mocked_open_return

        mocked_os_path_isfile.return_value = True
        mocked_os_path_getsize.return_value = 7

        mocked_url_signature.return_value = 'signedurl'

        result = self._client.add_image('/mocked/image/path.jpg')
        mocked_requests_put.assert_called_once_with('signedurl', 'content')

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

    @patch('requests.get')
    @patch('imboclient.url.user.UrlUser.url')
    def test_num_images(self, mocked_url_user, mocked_requests_get):
        class StubResponse:
            text = '{"numImages": 2}'

        mocked_url_user.return_value = 'http://imbo.local/users/public'
        mocked_requests_get.return_value = StubResponse()

        num_images = self._client.num_images()

        mocked_url_user.resource_url.assert_called_once()
        mocked_requests_get.assert_called_once_with(mocked_url_user.return_value)

        assert num_images == 2

    @patch('imboclient.url.imagesquery.Query')
    @patch('imboclient.url.images.UrlImages.url')
    @patch('imboclient.url.images.UrlImages.add_query')
    @patch('requests.get')
    def test_images(self, mock_requests_get, mock_url_images_addquery, mock_url_images, mock_imagesquery):
        class StubResponse:
            text = '[{"key": "value"}]'

        mock_url_images.return_value = 'http://imbo.local/public/images.json'
        mock_requests_get.return_value = StubResponse()

        images = self._client.images(mock_imagesquery)
        assert len(images) == 1

        mock_requests_get.assert_called_once_with(mock_url_images.return_value)
        mock_url_images_addquery.assert_called_once_with(mock_imagesquery)

    def test_image_data(self):
        raise NotImplementedError("Test missing")

    def test_image_data_from_url(self):
        raise NotImplementedError("Test missing")

    def test_image_properties_from_url(self):
        raise NotImplementedError("Test missing")

    def test_image_properties(self):
        raise NotImplementedError("Test missing")

    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('__builtin__.open')
    def test_image_identifier(self, mocked_open, mocked_os_path_getsize, mocked_os_path_isfile):
        mocked_open_return = MagicMock()
        mocked_open_return.read.return_value = 'content'
        mocked_open.return_value = mocked_open_return

        mocked_os_path_isfile.return_value = True
        mocked_os_path_getsize.return_value = 7

        assert self._client.image_identifier('/path/to/file') == '9a0364b9e99bb480dd25e1f0284c8555'
        mocked_os_path_isfile.assert_called_once_with('/path/to/file')
        mocked_os_path_getsize.assert_called_once_with('/path/to/file')

    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('__builtin__.open')
    @raises(ValueError)
    def test_image_identifier_no_file(self, mocked_open, mocked_os_path_getsize, mocked_os_path_isfile):
        # TODO it would be better to move file related actions to a separately tested module
        mocked_open_return = MagicMock()
        mocked_open_return.read.return_value = 'content'
        mocked_open.return_value = mocked_open_return

        mocked_os_path_isfile.return_value = False
        mocked_os_path_getsize.return_value = 0

        self._client.image_identifier('/dev/null/invalid')
        mocked_os_path_isfile.assert_called_once_with('/dev/null/invalid')

    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @patch('__builtin__.open')
    @raises(ValueError)
    def test_image_identifier_empty_file(self, mocked_open, mocked_os_path_getsize, mocked_os_path_isfile):
        mocked_open_return = MagicMock()
        mocked_open_return.read.return_value = 'content'
        mocked_open.return_value = mocked_open_return

        mocked_os_path_isfile.return_value = True
        mocked_os_path_getsize.return_value = 0

        self._client.image_identifier('/dev/null/invalid')
        mocked_os_path_getsize.assert_called_once_with('/dev/null/invalid')

    def test_image_identifier_from_string(self):
        raise NotImplementedError("Test missing")

    @patch('imboclient.url.status.UrlStatus.url')
    @patch('requests.get')
    def test_server_status(self, mocked_requests_get, mocked_url_status):
        class ResponseStub:
            text = '{"statusKey": "statusValue"}'

        mocked_url_status.return_value = 'http://imbo.local/status.json'
        mocked_requests_get.return_value = ResponseStub()

        server_status = self._client.server_status()

        assert server_status['statusKey'] == 'statusValue'
        mocked_url_status.assert_called_once()
        mocked_requests_get.assert_called_once_with(mocked_url_status.return_value)

    @patch('imboclient.url.user.UrlUser.url')
    @patch('requests.get')
    def test_user_info(self, mocked_requests_get, mocked_url_user):
        class ResponseStub:
            text = '{"public": "publickey"}'

        mocked_requests_get.return_value = ResponseStub()
        mocked_url_user.return_value = 'http://imbo.local/users/public'

        user_info = self._client.user_info()
        assert user_info['public'] == 'publickey'

        mocked_url_user.assert_called_once()
        mocked_requests_get.assert_called_once_with(mocked_url_user.return_value)

    def _valid_requests_response_stub_ok(self):
        class ResponseStub:
            status_code = requests.codes.ok

        return ResponseStub()

    def _invalid_requests_response_stub_not_found(self):
        class ResponseStub:
            status_code = requests.codes.not_found

        return ResponseStub()


