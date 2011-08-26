
# response object.
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

from common import deprecated_setter, encoding

class Response:
    def __init__(self, url, status=200, headers=None, body='', request=None):
        self.headers = ''
        self.status = int(status)
        self._set_body(body)
        self._set_url(url)
        self.request = request
        self.encoding = encoding(body)['encoding']

    def _get_body(self):
        return self._body

    def _set_body(self, body):
        if isinstance(body, str):
            self._body = body
        elif isinstance(body, unicode):
            raise TypeError("Cannot assign a unicode body to a raw Response. " \
                "Use TextResponse, HtmlResponse, etc")
        elif body is None:
            self._body = ''
        else:
            raise TypeError("Response body must either str or unicode. Got: '%s'" \
                % type(body).__name__)

    body = property(_get_body, deprecated_setter(_set_body, 'body'))

    def _get_url(self):
        return self._url

    def _set_url(self, url):
        if isinstance(url, str):
            self._url = url
        else:
            raise TypeError('%s url must be str, got %s:' % (type(self).__name__, \
                type(url).__name__))

    url = property(_get_url, deprecated_setter(_set_url, 'url'))
