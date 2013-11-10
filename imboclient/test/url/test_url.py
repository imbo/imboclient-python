from imboclient.url import url
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

    def test_add_query(self):
        raise NotImplementedError("Test missing")

    def test_add_query_param(self):
        self._url.add_query_param("testkey", "testvalue").add_query_param("testkey2", "testvalue2")
        assert len(self._url._query_params) == 2
        assert self._url._query_params["testkey"] == "testvalue"
        assert self._url._query_params["testkey2"] == "testvalue2"

    def test_query_string(self):
        self._url.add_query_param("key1", "value1").add_query_param("key2", "value 2")
        assert self._url.query_string() == "key2=value+2&key1=value1"
