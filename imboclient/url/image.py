import accesstoken

class UrlImage:

    def __init__(self, host, public_key, private_key, image_identifier):
        self.access_token = accesstoken.AccessToken()
        url = host + '/users/' + public_key + '/' + image_identifier
        self.url = url + '?accessToken=' + self.access_token.generate_token(url, private_key)

    def __str__(self):
        return self.url

