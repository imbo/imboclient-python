import imboclient.url.url
import nose.tools

class TestUrl:

    def setup(self):
        self._url = imboclient.url.url.Url('http://imbo.local', 'public', 'private')

    def teardown(self):
        self._url = None

    @nose.tools.raises(NotImplementedError)
    def test_url(self):
        self._url.url()

    @nose.tools.raises(NotImplementedError)
    def test_resource_url(self):
        self._url.resource_url()

