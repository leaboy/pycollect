
import eventlet
from common import deprecated
from python import flatten


class HtmlSelectorList(list):

    def __getslice__(self, i, j):
        return self.__class__(list.__getslice__(self, i, j))

    def select(self, xpath):
        return self.__class__(flatten([x.select(xpath) for x in self]))

    def extract(self):
        return [x.extract() for x in self]

    def Link(self):
        return [x.Link() for x in self]


    def re(self, regex):
        return self.__class__(flatten([x.re(regex) for x in self]))