from imboclient.url import url as url


class UrlUser(url.Url):
    def resource_url(self):
        return self._base_url + '/users/' + self._public_key + '.json'

