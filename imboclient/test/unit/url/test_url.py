from imboclient.url import url
import imboclient.url.images
import imboclient.url.imagesquery
from mock import patch
import nose.tools


class TestUrl:
    def setup(self):
        self._url = url.Url('http://imbo.local', 'public', 'private')

    def teardown(self):
        self._url = None

    @nose.tools.raises(NotImplementedError)
    def test_url(self):
        self._url.url()

    @nose.tools.raises(NotImplementedError)
    def test_resource_url(self):
        self._url.resource_url()

    @patch('imboclient.url.url.Url.url')
    def test_str_returns_url(self, mock_url):
        mock_url.return_value = 'url'
        result = self._url.url()
        assert str(self._url) == result

    def test_add_query(self):
        stub_query = imboclient.url.imagesquery.Query()
        stub_metadata = {"field1": "value1", "field2": "value2"}

        stub_query.q_from("fromdate").metadata(True).q_to("todate").query(stub_metadata)
        images_url = imboclient.url.images.UrlImages('baseurl', 'public', 'private')
        images_url.add_query(stub_query)

        assert images_url._query_params[0] == ('page', 1)
        assert images_url._query_params[1] == ('limit', 20)
        assert images_url._query_params[2] == ('from', 'fromdate')
        assert images_url._query_params[3] == ('to', 'todate')
        assert images_url._query_params[4] == ('query', '{"field2": "value2", "field1": "value1"}') or ('query', '{"field1": "value1", "field2": "value2"}')

    def test_add_query_param(self):
        self._url.add_query_param("testkey", "testvalue").add_query_param("testkey2", "testvalue2")
        assert len(self._url._query_params) == 2
        assert self._url._query_params[0] == ("testkey", "testvalue")
        assert self._url._query_params[1] == ("testkey2", "testvalue2")

    def test_query_string(self):
        self._url.add_query_param("key1", "value1").add_query_param("key2", "value 2")
        assert self._url.query_string() == "key1=value1&key2=value+2"

    def test_reset(self):
        self._url._query_params = [True]
        result = self._url.reset()
        assert len(self._url._query_params) == 0
        assert type(result) is url.Url
