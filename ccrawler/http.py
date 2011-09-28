
# http object.
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

import re, codecs, hashlib
import settings, eventlet
from urlparse import urlparse
from common import deprecated_setter, UnicodeDammit, encoding_exists, resolve_encoding
from headers import Headers
from eventlet.green import urllib2


def Request(url, req_timeout=60, req_data=None, req_headers=settings.DEFAULT_REQUEST_HEADERS):
    body, status, response, params = 'None', '200', None, {}
    request = urllib2.Request(url, req_data, req_headers)
    try:
        response = urllib2.urlopen(request)
        body = response.read()
        response.close()
        parse_url = urlparse(url)
        params = {}
        for part in parse_url[4].split('&'):
            if part.find('=') is not -1:
                k, v = part.split('=')
            else:
                k, v = part, ''
            params[k] = v
    except urllib2.HTTPError, e:
        status = e.code
    except urllib2.URLError, e:
        status = 'URLError: %s.' % e.args[0]
    except eventlet.Timeout, e:
        status = 'Time out.'
    except:
        status = 'URLError: Could not resolve.'
    finally:
        return Response(url, status, req_headers, body, request)(params)


class Response:

    _template = r'''%s\s*=\s*["']?\s*%s\s*["']?'''

    _httpequiv_re = _template % ('http-equiv', 'Content-Type')
    _content_re   = _template % ('content', r'(?P<mime>[^;]+);\s*charset=(?P<charset>[\w-]+)')
    _encoding_re  = _template % ('encoding', r'(?P<charset>[\w-]+)')

    METATAG_RE  = re.compile(r'<meta\s+%s\s+%s' % (_httpequiv_re, _content_re), re.I)
    METATAG_RE2 = re.compile(r'<meta\s+%s\s+%s' % (_content_re, _httpequiv_re), re.I)

    _DEFAULT_ENCODING = settings.DEFAULT_RESPONSE_ENCODING
    _ENCODING_RE = re.compile(r'charset=([\w-]+)', re.I)

    def __init__(self, url, status=200, headers=None, body='', request=None):
        self.headers = Headers(headers or {})
        self.status = status
        self._set_body(body)
        self._set_url(url)
        self.request = request

    def __call__(self, args):
        self.args = args
        return self

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

    @property
    def encoding(self):
        return self._get_encoding(infer=True)

    def _get_encoding(self, infer=False):
        enc = self._declared_encoding()
        if enc and not encoding_exists(enc):
            enc = None
        if not enc and infer:
            enc = self._body_inferred_encoding()
        if not enc:
            enc = self._DEFAULT_ENCODING
        return resolve_encoding(enc)

    def _declared_encoding(self):
        return self._body_declared_encoding()

    def _body_declared_encoding(self):
        chunk = self.body[:5000]
        match = self.METATAG_RE.search(chunk) or self.METATAG_RE2.search(chunk)
        return match.group('charset') if match else None

    def _body_inferred_encoding(self):
        enc = self._get_encoding()
        dammit = UnicodeDammit(self.body, [enc], isHTML=True)
        return dammit.originalEncoding