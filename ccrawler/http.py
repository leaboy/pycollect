
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
from headers import Headers, headers_raw_to_dict
from eventlet.green import urllib2

from lxml.html.clean import Cleaner
cleaner = Cleaner(style=True, page_structure=False, links=False)

import pycurl
from cStringIO import StringIO

class Request:

    def __init__(self):
        self.httpheader = settings.DEFAULT_REQUEST_HEADERS_CURL
        self.referer = ''
        self.connnecttimeout = 60
        self.timeout = 300
        self.backheader = 0
        self.cookesfile = "cookies"
        self.proxyuse = False
        self.proxyip = []
        self.proxynodomain = ['localhost','127.0.0.1']

        self.setting_name = 'default'
        self.setting_reverse = False

    def __del__(self):
        pass

    def fetch(self, url, post={}):
        '''
        @ url string
        @ post dict: {'param':'value'}
        '''

        url = url.strip()

        if post:
            post = urllib.urlencode(post)
        else:
            post = None

        self.rep = StringIO()
        self.header = ""

        curl = pycurl.Curl()
        curl.setopt(pycurl.CONNECTTIMEOUT, self.connnecttimeout)
        curl.setopt(pycurl.TIMEOUT, self.timeout)
        curl.setopt(pycurl.HTTPHEADER, self.httpheader)
        curl.setopt(pycurl.HEADER, self.backheader)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.MAXREDIRS, 5)
        curl.setopt(pycurl.AUTOREFERER, 1)
        curl.setopt(pycurl.COOKIEJAR, self.cookesfile)
        curl.setopt(pycurl.COOKIEFILE, self.cookesfile)
        curl.setopt(pycurl.WRITEFUNCTION, self.rep.write)
        curl.setopt(pycurl.HEADERFUNCTION, self.write_header)
        curl.setopt(pycurl.URL, url)

        if self.proxyuse:
            proxyip = self.proxyip[random.randint(0, len(self.proxyip)-1)];
            curl.setopt(pycurl.PROXY, proxyip)
        if post:
            curl.setopt(pycurl.POSTFIELDS, post)
        if self.referer:
            curl.setopt(pycurl.REFERER, self.referer)

        body, status, headers, response, params = 'None', '200', '', None, {}

        try:
            curl.perform()
            status = str(curl.getinfo(pycurl.RESPONSE_CODE))
            body = cleaner.clean_html(self.get_rep())
            headers = self.get_header()
            headers = headers_raw_to_dict(headers)

            parse_url = urlparse(url)
            for part in parse_url[4].split('&'):
                if part.find('=') is not -1:
                    k, v = part.split('=')
                else:
                    k, v = part, ''
                params[k] = v
        except pycurl.error:
            status = curl.errstr()
        finally:
            curl.close()
            response = Response(self.setting_name, url, status, headers, body, None, self.setting_reverse)(params)
            return response

    def write_header(self, string):
        self.header += string

    def get_rep(self):
        value = self.rep.getvalue()
        self.rep.close()
        self.rep = StringIO()
        return value

    def get_header(self):
        h = self.header
        self.header = ""
        return h


class Response:

    _template = r'''%s\s*=\s*["']?\s*%s\s*["']?'''

    _httpequiv_re = _template % ('http-equiv', 'Content-Type')
    _content_re   = _template % ('content', r'(?P<mime>[^;]+);\s*charset=(?P<charset>[\w-]+)')
    _encoding_re  = _template % ('encoding', r'(?P<charset>[\w-]+)')

    METATAG_RE  = re.compile(r'<meta\s+%s\s+%s' % (_httpequiv_re, _content_re), re.I)
    METATAG_RE2 = re.compile(r'<meta\s+%s\s+%s' % (_content_re, _httpequiv_re), re.I)

    _DEFAULT_ENCODING = settings.DEFAULT_RESPONSE_ENCODING
    _ENCODING_RE = re.compile(r'charset=([\w-]+)', re.I)

    def __init__(self, setting_name, url, status='200', headers=None, body='', request=None, reversemode=False):
        self.headers = Headers(headers or {})
        self.name = setting_name
        self.status = status
        self._set_body(body)
        self._set_url(url)
        self.request = request
        self.reversemode = reversemode

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