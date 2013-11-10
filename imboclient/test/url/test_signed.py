import imboclient.url.signed as url_signature

class TestSigned:
    def setup(self):
        pass

    def teardown(self):
        pass

    def test_sign_url(self):
        public = 'public'
        private = 'private'
        method = 'put'
        url = 'imbo.local/users/test'
        timestamp = 'timestamp'

        # calculated manually in python2 console with the above attributes
        correct_signature = '885bd7ae21c2afb8978f8163bcef292dde1d57b2f4aee1c54b43a1150d858545'

        signed_url = url_signature.Signed(public, private, method, url, timestamp).str()

        assert signed_url == ('imbo.local/users/test?signature=' + correct_signature + '&timestamp=' + timestamp)

