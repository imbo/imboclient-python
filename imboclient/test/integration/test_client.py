import imboclient.test.integration.config as config
import imboclient.client as imbo
import os
import json


class TestClient:
    def setup(self):
        self._host = config.server['host'] + ":" + config.server['port']
        self._public = config.server['public']
        self._private = config.server['private']
        self._client = imbo.Client([self._host], self._public, self._private)
        self._res_path = os.path.dirname(__file__)
        self._valid_image_path = self._res_path + '/res/imbologo.png'
        self._last_imbo_id = None

    def teardown(self):
        # delete our test image after every test for consistency
        if self._last_imbo_id:
            self._delete_test_image(self._last_imbo_id)

        self._client = None

    def _add_test_image(self):
        res = self._client.add_image(self._valid_image_path)

        if 'imageIdentifier' in res:
            self._last_imbo_id = res['imageIdentifier']

        return res

    def _delete_test_image(self, imbo_id):
        return self._client.delete_image(imbo_id)

    def test_add_new_image(self):
        result = self._add_test_image()
        assert len(result['imageIdentifier']) > 0

    def test_add_new_image_from_string(self):
        image_string = open(self._valid_image_path, 'rb').read()
        result = self._client.add_image_from_string(image_string)
        assert len(result['imageIdentifier']) > 0

        self._client.delete_image(result['imageIdentifier'])

    def test_add_new_invalid_image_from_string(self):
        image_string = 'invalidimagedata'
        try:
            result = self._client.add_image_from_string(image_string)
            assert False
        except self._client.ImboInternalError:
            pass

    def test_add_new_image_from_url(self):
        image_url = 'https://raw.github.com/andreasrs/ImboclientPython/master/imboclient/test/integration/res/imbologo.png'  # TODO remove dependency to github
        result = self._client.add_image_from_url(image_url)
        assert result['imageIdentifier']

        self._client.delete_image(result['imageIdentifier'])

    def test_image_exists(self):
        imbo_id = self._add_test_image()['imageIdentifier']
        self._delete_test_image(imbo_id)
        result = self._client.image_exists(imbo_id)
        assert not result

    def test_head_image(self):
        imbo_id = self._add_test_image()['imageIdentifier']
        result = self._client.head_image(imbo_id)
        assert result.status_code == 200

    def test_edit_metadata(self):
        imbo_id = self._add_test_image()['imageIdentifier']
        metadata = {"Key1": "Value1"}
        result = self._client.edit_metadata(imbo_id, metadata)
        assert result == metadata

    def test_replace_metadata(self):
        imbo_id = self._add_test_image()['imageIdentifier']
        metadata = {"Key1": "Value1"}
        result = self._client.replace_metadata(imbo_id, metadata)
        assert result == metadata

    def test_delete_metadata(self):
        imbo_id = self._add_test_image()['imageIdentifier']
        result = self._client.delete_metadata(imbo_id)

    def test_num_images(self):
        result = self._client.num_images()
        assert result >= 0

    def test_images(self):
        result = self._client.images()

        assert 'images' in result
        assert result['search']
        assert 'count' in result['search']
        assert 'hits' in result['search']
        assert result['search']['limit'] > 0
        assert result['search']['page'] == 1

    def test_image_data(self):
        imbo_id = self._add_test_image()['imageIdentifier']
        result = self._client.image_data(imbo_id)
        assert result.status_code == 200
        assert result.text

    def test_image_data_from_url(self):
        image_url = 'https://raw.github.com/andreasrs/ImboclientPython/master/imboclient/test/integration/res/imbologo.png'  # TODO remove dependency to github
        result = self._client.image_data_from_url(image_url)
        assert result.status_code == 200
        assert result.text

    def test_image_properties(self):
        imbo_id = self._add_test_image()['imageIdentifier']
        result = self._client.image_properties(imbo_id)
        assert result['x-imbo-originalwidth']
        assert result['x-imbo-originalfilesize']
        assert result['x-imbo-originalheight']
        assert result['x-imbo-originalextension']
        assert result['x-imbo-originalmimetype']

    def test_server_status(self):
        result = self._client.server_status()
        assert result['date']
        assert result['storage']
        assert result['database']

    def test_user_info(self):
        result = self._client.user_info()
        assert result['user']
        assert result['lastModified']
        assert result['numImages'] >= 0
