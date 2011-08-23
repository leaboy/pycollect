#!/usr/bin/python
#-*-coding:utf-8-*-

# Common funtions and others.
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

import os, sys, time, datetime, re
import simplejson

from PyQt4 import QtCore

class Func:
    def toStr(self, strr):
        if type(strr)==QtCore.QString:
            strr = strr.toLocal8Bit().data()
            strr = self.iConv(strr)
        elif strr==None:
            strr = ''
        return strr

    def iConv(self, strr, srcencode='gb2312', dstencode='utf-8'):
        if isinstance(strr, unicode):
            return strr.encode(dstencode)
        elif isinstance(strr, basestring):
            return strr.decode(srcencode).encode(dstencode)
        else:
            return strr

    def toTimestamp(self, val):
        if type(val)==QtCore.QDateTime:
            val = self.toStr(val.toString('yyyy-MM-dd hh:mm:ss'))
            val = time.strptime(val, '%Y-%m-%d %H:%M:%S')
            val = int(time.mktime(val))
        return val

    def fromTimestamp(self, val):
        return str(datetime.datetime.fromtimestamp(int(val)))

    def _variantConv(self, variant, dst):
        """Helper method to cast a QVariant to an integer"""
        res = None
        if not variant.isValid():
            return
        if dst=='int':
            integer, ok = variant.toInt()
            if ok:
                res = integer
        elif dst=='string':
            res = variant.toString()
        return res

    def serialize(obj):
        try:
            return simplejson.dumps(obj)
        except:
            pass

    def unserialize(obj):
        try:
            return simplejson.loads(obj)
        except:
            pass

    def searchFile(self, pattern, root=None):
        import os, fnmatch
        root = root==None and os.curdir
        print root
        for path, dirs, files in os.walk(os.path.abspath(root)):
            for filename in fnmatch.filter(files, pattern):
                yield os.path.join(path, filename)

    def serializeListUrl(self, autourl, manualurl):
        manualurlList = manualurl.splitlines()
        listurl = {'auto': autourl, 'manual': manualurlList}
        return simplejson.dumps(listurl)

    def getStartUrls(self, url, pagestart, pageend, wildcardlen, stockdata):
        '''get start url list'''
        listurl, page_urllist = [], []
        try:
            url = simplejson.loads(url)
        except:
            return listurl

        if url.has_key('manual'):
            manualUrl = url['manual']
        if url.has_key('auto'):
            autoUrl = url['auto']

        if not autoUrl=='':
            if not autoUrl.find('[page]')==-1:
                pageList = self.getListPageNum(pagestart, pageend, wildcardlen)
                for i in pageList:
                    page_urllist.append(autoUrl.replace('[page]', i))
            if not autoUrl.find('[stock]')==-1:
                if not len(page_urllist)>0:
                    page_urllist = [autoUrl]
                stockList = self.getListStockNum(stockdata)
                for stock in stockList:
                    for url in page_urllist:
                        listurl.append(url.replace('[stock]', stock))
            else:
                listurl = page_urllist

        if len(manualUrl)>0:
            for i in manualUrl:
                listurl.append(i)

        return map(str, listurl)

    def getListPageNum(self, pagestart, pageend, wildcardlen):
        pagestart = (isinstance(pagestart, int) and [pagestart] or [0])[0]
        pageend = (isinstance(pageend, int) and [pageend] or [0])[0]

        liststep = (pagestart<pageend and [1] or [-1])[0]
        pageList = range(pagestart, pageend+liststep, liststep)

        if not isinstance(wildcardlen, int) or wildcardlen<=0:
            return map(str, pageList)
        wildPageList = []
        for i in pageList:
            wildPageList.append(str(i).zfill(wildcardlen))
        return wildPageList

    def getListStockNum(self, stockdataurl):
        import urllib
        stockList = []

        try:
            rs = urllib.urlopen(stockdataurl)
            stockdata = rs.read()
            stockList = simplejson.loads(stockdata)
        except:
            return stockList
        stockList = (isinstance(stockList, list) and [stockList] or [stockList])[0]
        return stockList

class make_xlat:
    def __init__(self, *args, **kwds):
        self.adict = dict(*args, **kwds)
        self.rx = self.make_rx()
    def make_rx(self):
        return re.compile('|'.join(map(re.escape, self.adict)))
    def one_xlat(self, match):
        return str(self.adict[match.group(0)])
    def __call__(self, text):
        return self.rx.sub(self.one_xlat, text)

# instance helper functions
Func = Func()