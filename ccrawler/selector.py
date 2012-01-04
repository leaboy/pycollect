
# selector (xpath and regex).
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

import hashlib
import urlparse
import eventlet
from lxml import etree
from http import Request
from python import unicode_to_str
from list import HtmlSelectorList
from common import extract_regex, body_as_utf8, logger

from sqlalchemy.orm import mapper
from records import init_record


import logging
logger = logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

class HtmlSelector:
    __slots__ = ['_text', '_root', '_xpathev', 'expr', 'namespaces', 'base_url']
    _parser = etree.HTMLParser
    _tostring_method = 'html'

    def __init__(self, response=None, text=None, root=None, expr=None, namespaces=None, base_url=None, reversemode=False):
        if response:
            self.response = response
            self.utf8body = body_as_utf8(self.response)
            self.reversemode = response.reversemode
        elif text:
            self.utf8body = unicode_to_str(text)
            self.reversemode = reversemode
        else:
            self.utf8body = ''
            self.reversemode = reversemode

        if not base_url and response:
            self.base_url = response.url
        else:
            self.base_url = base_url

        self._text = text
        self._root = root
        self._xpathev = None
        self.namespaces = namespaces
        self.expr = expr

    @property
    def root(self):
        if self._root is None:
            parser = self._parser(encoding=self.response.encoding, recover=True)
            self._root = etree.fromstring(self.response.body, parser=parser, \
                base_url=self.response.url)
        return self._root

    @property
    def xpathev(self):
        if self._xpathev is None:
            self._xpathev = etree.XPathEvaluator(self.root, namespaces=self.namespaces)
        return self._xpathev

    def select(self, xpath):
        try:
            result = self.xpathev(xpath)
        except etree.XPathError:
            raise ValueError("Invalid XPath: %s" % xpath)

        if hasattr(result, '__iter__'):
            result = [self.__class__(root=x, expr=xpath, namespaces=self.namespaces, base_url=self.base_url, reversemode=self.reversemode) \
                for x in result]
        else:
            result = [self.__class__(root=result, expr=xpath, namespaces=self.namespaces, base_url=self.base_url, reversemode=self.reversemode)]
        result = self.reversemode and result.reverse() or result
        return HtmlSelectorList(result)

    def re(self, regex):
        result = extract_regex(regex, self.utf8body)
        if hasattr(result, '__iter__'):
            result = [self.__class__(text=x, root=self.utf8body, base_url=self.base_url, reversemode=self.reversemode) \
                for x in result]
        else:
            result = [self.__class__(text=result, root=self.utf8body, base_url=self.base_url, reversemode=self.reversemode)]
        result = self.reversemode and result.reverse() or result
        return HtmlSelectorList(result)

    def Link(self, recover=True):
        result = self.extract()
        if result:
            try:
                url = urlparse.urljoin(self.base_url, result)
                url_hash = hashlib.md5(url).hexdigest()

                records, session = init_record(hashlib.md5(self.base_url).hexdigest())
                query_record = session.query(records.hash).filter(records.hash==url_hash).first()

                if query_record!=None and recover==False:
                    return

                if query_record==None:
                    query = records(url_hash)
                    session.add(query)
                    session.commit()

                response = Request(unicode_to_str(url), self.reversemode)
                logger.info('Fetched: %s (%s)' % (url, response.status))
                return self.__class__(response)
            except:
                pass

    def extract(self):
        if isinstance(self._root, etree._ElementUnicodeResult) or isinstance(self._root, etree._ElementStringResult) or isinstance(self._root, etree._Element):
            try:
                return etree.tostring(self.root, method=self._tostring_method, \
                    encoding=unicode)
            except (AttributeError, TypeError):
                return unicode(self.root)
        elif isinstance(self._root, basestring):
            return self._text
