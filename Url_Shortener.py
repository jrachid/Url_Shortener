import string
import os
import base64

class UrlShortener(object):
    def __init__(self, url):
        self.url = url
        self.url_to_id = {}
        self.id_url = 0

    def generate_seed(self, size):
        seed = os.urandom(5)
        return base64.b64encode(seed).decode('utf-8')

    def shorten_url(self):
        if self.url_to_id.get(self.url):
            self.id_url = self.url_to_id[self.url]
            shorten_url = self.id_url
        else:
            shorten_url = self.id_url
            self.id_url = self.generate_seed(5)
            self.url_to_id[self.url] = self.id_url
        return str(self.id_url)

