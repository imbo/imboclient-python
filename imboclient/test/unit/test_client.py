from mock import (
    patch,
    MagicMock,
    mock_open,
)
from nose import with_setup
from nose.tools import raises
import requests
import os
import json
import hashlib
from imboclient import client as imbo
from imboclient.url import image, images, status, user, accesstoken, metadata
import sys


class TestClient:
    def setup(self):
        self._client = imbo.Client(['http://imbo.local'], 'public', 'private')
        self._client_with_user = imbo.Client(['http://imbo.local'], 'public', 'private', user='foo')

    def teardown(self):
        self._client = None
        self._client_with_user = None

    def test_server_urls_generic(self):
        client = imbo.Client(['imbo.local'], 'public', 'private')
        assert client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_http(self):
        client = imbo.Client(['http://imbo.local'], 'public', 'private')
        assert client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_https(self):
        client = imbo.Client(['https://imbo.local'], 'public', 'private')
        assert client.server_urls[0] == 'https://imbo.local'

    def test_server_urls_port_normal(self):
        client = imbo.Client(['http://imbo.local'], 'public', 'private')
        assert client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_port_normal_explicit(self):
        client = imbo.Client(['http://imbo.local:80'], 'public', 'private')
        assert client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_port_ssl(self):
        client = imbo.Client(['https://imbo.local:443'], 'public', 'private')
        assert client.server_urls[0] == 'https://imbo.local'

    def test_server_urls_port_explicit_without_protocol(self):
        client = imbo.Client(['imbo.local:8000'], 'public', 'private')
        assert client.server_urls[0] == 'http://imbo.local:8000'

    def test_server_urls_as_string(self):
        client = imbo.Client('imbo.local', 'public', 'private')
        assert client.server_urls[0] == 'http://imbo.local'

    def test_server_urls_from_identifiers(self):
        hosts = ('imbo.local', 'imbo.local2', )
        client = imbo.Client(hosts, 'public', 'private')

        host1 = str(client.image_url('foo')).split('/')[2]

        # the default method uses the ord() value of the chars, so increase by one to get a different host
        host2 = str(client.image_url('goo')).split('/')[2]

        assert host1 != host2
        assert host1 in hosts
        assert host2 in hosts

    @patch('imboclient.url.status.UrlStatus')
    def test_status_url(self, mocked_url_status):
        status_url = self._client.status_url()
        mocked_url_status.assert_called_once_with('http://imbo.local', 'public', 'private')
        assert status_url == mocked_url_status()

    @patch('imboclient.url.user.UrlUser')
    def test_user_url(self, mocked_url_user):
        user_url = self._client.user_url()
        mocked_url_user.assert_called_once_with('http://imbo.local', 'public', 'private')
        assert user_url == mocked_url_user()

    @patch('imboclient.url.images.UrlImages')
    def test_images_url(self, mocked_url_images):
        images_url = self._client.images_url()
        mocked_url_images.assert_called_once_with('http://imbo.local', 'public', 'private', user=None)
        assert images_url == mocked_url_images()

    @patch('imboclient.url.images.UrlImages')
    def test_images_url_with_user(self, mocked_url_images):
        images_url = self._client_with_user.images_url()
        mocked_url_images.assert_called_once_with('http://imbo.local', 'public', 'private', user='foo')
        assert images_url == mocked_url_images()

    def test_images_url_with_user_used(self):
        images_url = self._client_with_user.images_url()
        assert images_url.url().startswith('http://imbo.local/users/foo/images')
        assert 'publicKey=public' in images_url.url()

    @patch('imboclient.url.image.UrlImage')
    def test_image_url(self, mocked_url_image):
        image_url = self._client.image_url('ff')
        mocked_url_image.assert_called_once_with('http://imbo.local', 'public', 'private', 'ff', user=None)
        assert image_url == mocked_url_image()

    @patch('imboclient.url.image.UrlImage')
    def test_image_url_with_user(self, mocked_url_image):
        image_url = self._client_with_user.image_url('ff')
        mocked_url_image.assert_called_once_with('http://imbo.local', 'public', 'private', 'ff', user='foo')
        assert image_url == mocked_url_image()

    def test_image_url_with_user_used(self):
        image_url = self._client_with_user.image_url('ff')
        assert image_url.url().startswith('http://imbo.local/users/foo/images/ff?')
        assert 'publicKey=public' in image_url.url()

    @patch('imboclient.url.metadata.UrlMetadata')
    def test_metadata_url(self, mocked_url_metadata):
        metadata_url = self._client.metadata_url('ff')
        mocked_url_metadata.assert_called_once_with('http://imbo.local', 'public', 'private', 'ff', user=None)
        assert metadata_url == mocked_url_metadata()

    @patch('imboclient.url.metadata.UrlMetadata')
    def test_metadata_url_with_user(self, mocked_url_metadata):
        metadata_url = self._client_with_user.metadata_url('ff')
        mocked_url_metadata.assert_called_once_with('http://imbo.local', 'public', 'private', 'ff', user='foo')
        assert metadata_url == mocked_url_metadata()

    def test_metadata_url_with_user_used(self):
        metadata_url = self._client_with_user.metadata_url('ff')
        assert metadata_url.url().startswith('http://imbo.local/users/foo/images/ff/metadata?')
        assert 'publicKey=public' in metadata_url.url()

    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('imboclient.url.images.UrlImages.url')
    @patch('requests.post')
    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_add_image(self, mocked_os_path_getsize, mocked_os_path_isfile, mocked_requests_post, mocked_url, mocked_headers):
        mocked_os_path_isfile.return_value = True
        mocked_os_path_getsize.return_value = 7

        response_mock = MagicMock()
        response_mock.status_code = 201

        mocked_requests_post.return_value = response_mock

        mocked_url.return_value = 'url'
        mocked_headers.return_value = {'Accept': 'application/json'}

        content = 'content'
        m = '__builtin__'

        if sys.version_info >= (3,):
            m = 'builtins'

        mocked_open = mock_open(read_data=content)

        with patch(m + '.open', mocked_open):
            result = self._client.add_image('/mocked/image/path.jpg')
            mocked_requests_post.assert_called_once_with('url', data='content', headers={'Accept': 'application/json'})


    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('requests.post')
    @patch('imboclient.url.images.UrlImages.url')
    def test_add_image_from_string(self, mock_image_url, mock_requests_post, mock_headers):
        mock_image_url.return_value = 'imageurl'
        mock_headers.return_value = {'Accept': 'application/json'}

        response_mock = MagicMock()
        response_mock.status_code = 201

        mock_requests_post.return_value = response_mock

        result = self._client.add_image_from_string('imagestring')

        mock_requests_post.assert_called_once_with('imageurl', data='imagestring', headers={'Accept': 'application/json'})
        assert result

    @raises(imbo.Client.ImboTransportError)
    def test_wrap_result_transport_failure(self):
        def fails(self):
            raise requests.exceptions.RequestException('Fail')

        self._client._wrap_result(fails, [200], 'error')

    @raises(imbo.Client.ImboInternalError)
    def test_wrap_result_internal_failure(self):
        def fails(self):
            class Response(object):
                pass

            response = Response()
            response.status_code = 400
            response.text = 'err'

            return response

        self._client._wrap_result(fails, [200], 'error')

    @patch('imboclient.client.Client.add_image_from_string')
    @patch('requests.get')
    def test_add_image_from_url(self, mock_requests_get, mock_add_image_from_string):
        response_mock = MagicMock()
        response_mock.status_code = 200
        response_mock.content = 'imagedatafromhttp'

        mock_requests_get.return_value = response_mock

        self._client.add_image_from_url('validimageurl')
        mock_requests_get.assert_called_once_with('validimageurl')
        mock_add_image_from_string.assert_called_once_with('imagedatafromhttp')

    @patch('imboclient.client.Client.image_identifier_exists')
    def test_image_exists(self, mock_image_identifier_exists):
        mock_image_identifier_exists.return_value = True

        image_exists = self._client.image_exists('identifier')

        assert image_exists is True
        mock_image_identifier_exists.assert_called_once_with('identifier')

    @patch('requests.head')
    @patch('imboclient.url.image.UrlImage')
    def test_image_identifier_exists_true(self, mocked_url_image, mocked_requests_head):
        mocked_requests_head.return_value = self._valid_requests_response_stub_ok()
        mocked_url_image_instance = mocked_url_image.return_value
        mocked_url_image_instance.url.return_value = 'http://imbo.local/users/public/ff?accessToken=aa'

        assert self._client.image_identifier_exists('ff') is True
        mocked_requests_head.assert_called_once_with('http://imbo.local/users/public/ff?accessToken=aa')

    @patch('requests.head')
    @patch('imboclient.url.image.UrlImage')
    def test_image_identifier_exists_false(self, mocked_url_image, mocked_requests_get):
        mocked_requests_get.return_value = self._invalid_requests_response_stub_not_found()
        mocked_url_image_instance = mocked_url_image.return_value
        mocked_url_image_instance.url.return_value = 'http://imbo.local/users/public/ffa?accessToken=aaf'

        assert self._client.image_identifier_exists('ffa') is False
        mocked_requests_get.assert_called_once_with('http://imbo.local/users/public/ffa?accessToken=aaf')

    @patch('imboclient.url.image.UrlImage.url')
    @patch('requests.head')
    def test_head_image(self, mock_requests_head, mock_image_url):
        class StubResponse:
            status_code = 200

        mock_image_url.return_value = "imageurl"
        mock_requests_head.return_value = StubResponse()

        self._client.head_image("ff")
        mock_image_url.assert_called_once_with()
        mock_requests_head.assert_called_once_with("imageurl")

    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('imboclient.url.image.UrlImage.url')
    @patch('requests.delete')
    def test_delete_image(self, mock_requests_delete, mock_image_url, mock_headers):
        class StubResponse:
            status_code = 200
            text = '{}'

            def json(self):
                return {}

        mock_image_url.return_value = "imageurl"
        mock_headers.return_value = {}
        mock_requests_delete.return_value = StubResponse()

        self._client.delete_image("imageidentifier")
        mock_image_url.assert_called_once_with()
        mock_requests_delete.assert_called_once_with("imageurl", headers={})

    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('imboclient.url.metadata.UrlMetadata.url')
    @patch('requests.post')
    def test_edit_metadata(self, mock_requests_post, mock_metadata_url, mock_headers):
        class StubResponse:
            status_code = 200
            text = '{}'

            def json(self):
                return {}

        mock_metadata_url.return_value = 'metadataurl'
        mock_headers.return_value = {}

        metadata = {"field1": "value1", "field2": "value2"}
        mock_requests_post.return_value = StubResponse()

        self._client.edit_metadata('identifier', metadata)
        metadata = json.dumps(metadata).encode('utf-8')

        mock_requests_post.assert_called_once_with('metadataurl',
                                                   data=metadata,
                                                   headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'Content-MD5': hashlib.md5(metadata).hexdigest()}
                                                   )

    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('imboclient.url.metadata.UrlMetadata.url')
    @patch('requests.put')
    def test_replace_metadata(self, mock_requests_put, mock_metadata_url, mock_headers):
        class StubResponse:
            status_code = 200
            text = '{}'

            def json(self):
                return {}

        mock_metadata_url.return_value = 'metadataurl'
        mock_headers.return_value = {}

        metadata = {"field1": "value1", "field2": "value2"}
        mock_requests_put.return_value = StubResponse()

        self._client.replace_metadata('identifier', metadata)
        metadata = json.dumps(metadata).encode('utf-8')

        mock_requests_put.assert_called_once_with('metadataurl',
                                                  data=metadata,
                                                  headers={'Accept': 'application/json', 'Content-Type': 'application/json', 'Content-MD5': hashlib.md5(metadata).hexdigest()}
                                                  )

    @patch('imboclient.header.authenticate.Authenticate.headers')
    @patch('imboclient.url.metadata.UrlMetadata.url')
    @patch('requests.delete')
    def test_delete_metadata(self, mock_requests_delete, mock_metadata_url, mock_headers):
        class StubResponse:
            status_code = 200
            text = '{}'

            def json(self):
                return {}

        mock_metadata_url.return_value = 'metadataurl'
        mock_headers.return_value = {'Accept': 'application/json'}
        mock_requests_delete.return_value = StubResponse()

        self._client.delete_metadata('identifier')

        mock_requests_delete.assert_called_once_with('metadataurl', headers={'Accept': 'application/json'})

    @patch('requests.get')
    @patch('imboclient.url.user.UrlUser.url')
    def test_num_images(self, mocked_url_user, mocked_requests_get):
        class StubResponse:
            status_code = 200
            text = '{"numImages": 2}'

            def json(self):
                return json.loads(self.text)

        mocked_url_user.return_value = 'http://imbo.local/users/public'
        mocked_requests_get.return_value = StubResponse()

        num_images = self._client.num_images()

        mocked_url_user.assert_called_once_with()
        mocked_requests_get.assert_called_once_with(mocked_url_user.return_value, headers={'Accept': 'application/json'})

        assert num_images == 2

    @patch('imboclient.url.imagesquery.Query')
    @patch('imboclient.url.images.UrlImages.url')
    @patch('imboclient.url.images.UrlImages.add_query')
    @patch('requests.get')
    def test_images(self, mock_requests_get, mock_url_images_addquery, mock_url_images, mock_imagesquery):
        class StubResponse:
            status_code = 200
            text = '[{"key": "value"}]'

            def json(self):
                return json.loads(self.text)

        mock_url_images.return_value = 'http://imbo.local/public/images.json'
        mock_requests_get.return_value = StubResponse()

        images = self._client.images(mock_imagesquery)
        assert len(images) == 1

        mock_requests_get.assert_called_once_with(mock_url_images.return_value, headers={'Accept': 'application/json'})
        mock_url_images_addquery.assert_called_once_with(mock_imagesquery)

    @patch('imboclient.url.image.UrlImage.url')
    @patch('imboclient.client.Client.image_data_from_url')
    def test_image_data(self, mock_image_data_from_url, mock_image_url):
        mock_image_data_from_url.return_value = 'data'
        mock_image_url.return_value = 'validimageurl'

        image_data = self._client.image_data('ff')
        mock_image_data_from_url.assert_called_once_with('validimageurl')
        assert image_data == 'data'

    @patch('requests.get')
    def test_image_data_from_url(self, mock_requests_get):
        class ResponseStub:
            status_code = 200
            text = 'data'

        mock_requests_get.return_value = ResponseStub()
        image_data = self._client.image_data_from_url('validurl')
        mock_requests_get.assert_called_once_with('validurl')

        assert image_data.text == 'data'

    @patch('imboclient.client.Client.head_image')
    def test_image_properties(self, mock_head_image):
        class ResponseStub:
            headers = {
                    "x-imbo-originalwidth": "width",
                    "x-imbo-originalheight": "height",
                    "x-imbo-originalfilesize": "size",
                    "x-imbo-originalmimetype": "mime",
                    "x-imbo-originalextension": "ext"
                    }

        mock_head_image.return_value = ResponseStub()

        image_properties = self._client.image_properties('ff')
        assert image_properties["x-imbo-originalwidth"] == 'width'
        assert image_properties["x-imbo-originalheight"] == 'height'
        assert image_properties["x-imbo-originalfilesize"] == 'size'
        assert image_properties["x-imbo-originalmimetype"] == 'mime'
        assert image_properties["x-imbo-originalextension"] == 'ext'

    @patch('os.path.isfile')
    @patch('os.path.getsize')
    def test_image_identifier(self, mocked_os_path_getsize, mocked_os_path_isfile):
        content = 'content'
        m = '__builtin__'

        if sys.version_info >= (3,):
            content = b'content'
            m= 'builtins'

        mocked_open = mock_open(read_data=content)

        with patch(m + '.open', mocked_open):
            mocked_os_path_isfile.return_value = True
            mocked_os_path_getsize.return_value = 7

            assert self._client.image_identifier("/path/to/file") == "9a0364b9e99bb480dd25e1f0284c8555"
            mocked_os_path_isfile.assert_called_once_with('/path/to/file')
            mocked_os_path_getsize.assert_called_once_with('/path/to/file')

    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @raises(ValueError)
    def test_image_identifier_no_file(self, mocked_os_path_getsize, mocked_os_path_isfile):
        # TODO it would be better to move file related actions to a separately tested module
        mocked_os_path_isfile.return_value = False
        mocked_os_path_getsize.return_value = 0

        self._client.image_identifier('/dev/null/invalid')
        mocked_os_path_isfile.assert_called_once_with('/dev/null/invalid')

    @patch('os.path.isfile')
    @patch('os.path.getsize')
    @raises(ValueError)
    def test_image_identifier_empty_file(self, mocked_os_path_getsize, mocked_os_path_isfile):
        mocked_os_path_isfile.return_value = True
        mocked_os_path_getsize.return_value = 0

        self._client.image_identifier('/dev/null/invalid')
        mocked_os_path_getsize.assert_called_once_with('/dev/null/invalid')

    @patch('imboclient.client.Client._generate_image_identifier')
    def test_image_identifier_from_string(self, mock_generate_image_identifier):
        self._client.image_identifier_from_string('imagestring')
        mock_generate_image_identifier.assert_called_once_with('imagestring')

    @patch('imboclient.url.status.UrlStatus.url')
    @patch('requests.get')
    def test_server_status(self, mocked_requests_get, mocked_url_status):
        class ResponseStub:
            status_code = 200
            text = '{"statusKey": "statusValue"}'

            def json(self):
                return json.loads(self.text)

        mocked_url_status.return_value = 'http://imbo.local/status.json'
        mocked_requests_get.return_value = ResponseStub()

        server_status = self._client.server_status()

        assert server_status['statusKey'] == 'statusValue'
        mocked_url_status.assert_called_once_with()
        mocked_requests_get.assert_called_once_with(mocked_url_status.return_value, headers={'Accept': 'application/json'})

    @patch('imboclient.url.user.UrlUser.url')
    @patch('requests.get')
    def test_user_info(self, mocked_requests_get, mocked_url_user):
        class ResponseStub:
            status_code = 200
            text = '{"public": "publickey"}'

            def json(self):
                return json.loads(self.text)

        mocked_requests_get.return_value = ResponseStub()
        mocked_url_user.return_value = 'http://imbo.local/users/public'

        user_info = self._client.user_info()
        assert user_info['public'] == 'publickey'

        mocked_url_user.assert_called_once_with()
        mocked_requests_get.assert_called_once_with(mocked_url_user.return_value, headers={'Accept': 'application/json'})

    def _valid_requests_response_stub_ok(self):
        class ResponseStub:
            status_code = requests.codes.ok

        return ResponseStub()

    def _invalid_requests_response_stub_not_found(self):
        class ResponseStub:
            status_code = requests.codes.not_found

        return ResponseStub()
