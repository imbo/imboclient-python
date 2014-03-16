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

    def teardown(self):
        # delete our test image after every test for consistency
        self._delete_test_image()
        self._client = None

    def _add_test_image(self):
        return self._client.add_image(self._valid_image_path)

    def _delete_test_image(self):
        testimage_identifier = self._client.image_identifier(self._valid_image_path)
        return self._client.delete_image(testimage_identifier)

    def test_add_new_image(self):
        result = self._add_test_image()
        assert result.status_code == 201
        assert len(result.json()['imageIdentifier']) > 0

    def test_add_duplicate_image(self):
        # original, 201
        result = self._add_test_image()
        assert result.status_code == 201
        assert len(result.json()['imageIdentifier']) > 0

        #duplicate, 200
        result = self._add_test_image()
        assert result.status_code == 200
        assert len(result.json()['imageIdentifier']) > 0

    def test_add_new_image_from_string(self):
        image_string = open(self._valid_image_path).read()
        result = self._client.add_image_from_string(image_string)
        assert result.status_code == 201
        assert len(result.json()['imageIdentifier']) > 0

    def test_add_new_invalid_image_from_string(self):
        image_string = 'invalidimagedata'
        result = self._client.add_image_from_string(image_string)
        assert result.status_code == 415

    def test_add_new_image_from_url(self):
        image_url = 'https://raw.github.com/andreasrs/ImboclientPython/master/imboclient/test/integration/res/imbologo.png' # TODO remove dependency to github
        result = self._client.add_image_from_url(image_url)
        assert result.status_code == 201
        assert len(result.json()['imageIdentifier']) > 0

    def test_image_exists(self):
        self._add_test_image()
        result = self._client.image_exists(self._valid_image_path)
        assert result
        self._delete_test_image()
        result = self._client.image_exists(self._valid_image_path)
        assert not result

    def test_head_image(self):
        self._add_test_image()
        testimage_identifier = self._client.image_identifier(self._valid_image_path)
        result = self._client.head_image(testimage_identifier)
        assert result.status_code == 200

    def test_edit_metadata(self):
        self._add_test_image()
        testimage_identifier = self._client.image_identifier(self._valid_image_path)
        metadata = {"Key1": "Value1"}
        result = self._client.edit_metadata(testimage_identifier, metadata)
        assert result.status_code == 200
        assert result.json() == metadata

    def test_replace_metadata(self):
        self._add_test_image()
        testimage_identifier = self._client.image_identifier(self._valid_image_path)
        metadata = {"Key1": "Value1"}
        result = self._client.replace_metadata(testimage_identifier, metadata)
        assert result.status_code == 200
        assert result.json() == metadata

    def test_delete_metadata(self):
        self._add_test_image()
        testimage_identifier = self._client.image_identifier(self._valid_image_path)
        result = self._client.delete_metadata(testimage_identifier)
        assert result.status_code == 200

    def test_num_images(self):
        return

    def test_images(self):
        return

    def test_image_data(self):
        return

    def test_image_data_from_url(self):
        return

    def test_image_properties(self):
        return

    def test_image_identifier(self):
        return

    def test_server_status(self):
        return

    def test_user_info(self):
        return


