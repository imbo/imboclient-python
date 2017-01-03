from imboclient.url import accesstoken

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import json


class Url(object):
    def __init__(self, base_url, public_key, private_key, user=None):
        self._base_url = base_url
        self._public_key = public_key
        self._private_key = private_key
        self._user = user
        self._query_params = []

        self.access_token = accesstoken.AccessToken()

    def __str__(self):
        return self.url()

    def user_url(self, resource):
        u = self._user if self._user else self._public_key

        return self._base_url + '/users/' + u + '/' + resource

    def url(self):
        url = self.resource_url()

        # create copy of list
        params = list(self._query_params)

        # if we have a user, we'll have to supply the public key as a GET argument
        if self._user:
            params.append(('publicKey', self._public_key))

        query_string = self.query_stringify(params)

        if query_string:
            url += '?' + query_string

        if self._public_key is None or self._private_key is None:
            return url

        generated_token = self.access_token.generate_token(url, self._private_key)
        sep = '?' if not query_string else '&'

        return url + sep + 'accessToken=' + generated_token

    def add_query_param(self, key, value):
        if self._query_params is None:
            self._query_params = []

        self._query_params.append((key, value))

        return self

    def add_query(self, query):
        if query:
            self.add_query_param('page', query.page())
            self.add_query_param('limit', query.limit())
            self.add_query_param('from', query.q_from())
            self.add_query_param('to', query.q_to())

        if query.metadata:
            self.add_query_param('query', json.dumps(query.query()))

        return self

    def query_string(self):
        return self.query_stringify(self._query_params)

    def resource_url(self):
        raise NotImplementedError("Missing implementation. You may want to use a Url implementation instead.")

    def reset(self):
        self._query_params = []

        return self

    @classmethod
    def query_stringify(cls, parameters):
        if not parameters:
            return ''

        return urlencode(parameters)