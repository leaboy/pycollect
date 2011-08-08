#!/usr/bin/python
#-*-coding:utf-8-*-

# A crawl class.
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

import re, sys, time, os
import httplib, urllib
from urlparse import urlparse,urljoin
import hashlib
import simplejson

## Config params
# 最大线程数
threads = 10
# 采集速度控制，单位秒
speed = 3
# 设置提交的header头
headers = {"Accept": "*/*","User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"}
# 默认链接规则
defaultLinkReg = '''<a[^>]*?href=(?:\'|\")([^\'\"]+)(?:'|\")[^>]*?>([^<]*)<\/a>'''

class Crawl2():
    def __init__(self, url, robotinfo, parent):
        '''
        @ return {key: [url, title, content], key: []...}
        '''
        self.url = url
        self.parent = parent

        iconv = lambda v: toutf8((v==None and [''] or [v])[0])
        robotinfo['importSQL']      = iconv(robotinfo['importSQL'])
        robotinfo['subjecturlrule'] = iconv(robotinfo['subjecturlrule'])
        robotinfo['subjecturllinkrule'] = iconv(robotinfo['subjecturllinkrule'])
        robotinfo['subjectrule']    = iconv(robotinfo['subjectrule'])
        robotinfo['messagerule']    = iconv(robotinfo['messagerule'])

        self.robotinfo = robotinfo


        urlListHtml = self.httpRequest(url)[1]
        urlListHtml = self.parseData(urlListHtml, self.robotinfo['subjecturlrule'], '[list]')
        urlListHtml = (urlListHtml==None and [''] or [urlListHtml])[0]
        urlList = self.getURL(url, urlListHtml)
        urlList = self.filterData(url, urlList)

        listlength = len(urlList)
        if urlList!=None and listlength>0:
            listitem = []
            for k,i in urlList.iteritems():
                if not isinstance(i, list) or len(i)<2: continue
                tempitem = {}
                tempitem['key'] = hashlib.md5(i[0]).hexdigest().upper()
                tempitem['url'] = i[0]
                tempitem['title'] = i[1]
                tempitem['message'] = ''
                if self.robotinfo['linkmode']==0:
                    rs = self.httpRequest(i[0])
                    if self.robotinfo['downloadmode']==0:
                        tempitem['title'] = (self.robotinfo['linkmode']==1 and [i[1]] or [self.parseData(rs[1], self.robotinfo['subjectrule'], '[title]')])[0]
                        tempitem['title'] = (tempitem['title']=='' and [i[1]] or [tempitem['title']])[0]
                        tempitem['message'] = (self.robotinfo['onlylinks']==1 and [''] or [self.parseData(rs[1], self.robotinfo['messagerule'], '[message]')])[0]
                    else:
                        pass
                listitem.append(tempitem)
            self.saveData(listitem)
            print 'Finished: %s (%d).' % (url, listlength)
        else:
            print 'Finished: %s (Null).' % url

    def clearBlank(self, html):
        html = re.sub('\r|\n|\t','',html)
        return html

    def parseData(self, html, regx, spe):
        rule = regx.split(spe)
        html = self.clearBlank(html)
        html = (len(rule)>=2 and [self.sect(html, rule[0], rule[1])] or [html])[0]
        return html

    def getURL(self, listUrl, html):
        '''
        @ 得到某个列表页中所有内容的链接
        @ return [[url,title],[]...]
        '''
        linkReg = (self.robotinfo['subjecturllinkrule'] and [self.robotinfo['subjecturllinkrule']] or [defaultLinkReg])[0]

        try:
            urls = re.findall(linkReg, html, re.I)
        except TypeError:
            return

        path = listUrl[::-1][listUrl[::-1].find('/'):][::-1]
        urlList = {}
        for i in urls:
            tempurl = temptitle = ''
            if isinstance(i, str):
                tempurl = i
            elif isinstance(i, tuple):
                tempurl = i[0]
                temptitle = (len(i)>1 and [i[1]] or [''])[0]
            if len(tempurl)==0 : continue
            tempurlPars = urlparse(tempurl)
            tempurl = (tempurlPars[0]=='' and [urljoin(path, tempurl)] or [tempurl])[0]
            urlList[hashlib.md5(tempurl).hexdigest().upper()] = [tempurl, temptitle]

        return urlList

    def sect(self, html, rulestart, ruleend, cls=''):
        if len(html)==0 : return
        reHTML = re.search(rulestart + '(.*?)' + ruleend, html, re.I|re.M)
        if reHTML == None : return
        reHTML = reHTML.group()
        intStart = re.search(rulestart, reHTML, re.I|re.M).end()
        intEnd = re.search(ruleend, reHTML, re.I|re.M).start()
        R = reHTML[intStart:intEnd]
        if cls != '' :
            R = self.clear(R,cls)
        return R

    def clear(self, html, regexs):
        if regexs == '' : return html
        for regex in regexs.split(chr(10)):
            regex = regex.strip()
            if regex != '' :
                if regex[:1]==chr(40) and regex[-1:]==chr(41):
                    html = re.sub(regex,'',html,re.I|re.S)
                else :
                    html = html.replace(regex,'')
        return html

    def httpRequest(self, url):
        print "GET:",url
        urls = urlparse(url); path = urls[2];
        if urls[4]!='' : path += '?' + urls[4]
        content = contentType = ''

        try:
            http = httplib.HTTPConnection(urls[1])
            http.request(method="GET", url=path, headers=headers)
            rs = http.getresponse()
            if rs.status!=200 :
                print 'Error: %s (%d).' % (url,rs.status)
            else:
                content = rs.read()
                contentType = rs.getheader('Content-Type')

            if contentType == 'text/html':
                content = toutf8(content)
            else:
                if self.robotinfo['downloadmode'] == 0:
                    content = ''
            http.close()
        except:
            print 'Error: %s (Faild).' % url

        return [urls, content]

    def filterData(self, url, urlList):
        '''
        @ Return new url and Update log file
        '''
        R = {}
        temUrlList = (isinstance(urlList, dict) and [urlList.keys()] or [[]])[0]
        path = 'log/%s' % str(self.robotinfo['taskid'])
        if not os.path.exists(path):
            os.makedirs(path)
        logname = '%s/%s' % (path, hashlib.md5(url).hexdigest().upper())
        if not os.path.isfile(logname):
            fp = open(logname, 'w')
            fp.close()
        fp = open(logname, 'r')
        logdata = fp.read()
        fp.close()
        try:
            logdata = simplejson.loads(logdata)
        except:
            logdata = []
        temUrlList.extend(logdata)
        newUrlList = [i for i in temUrlList if temUrlList.count(i)==1]
        temUrlList = list(set(temUrlList))
        temUrlList = simplejson.dumps(temUrlList)
        fp = open(logname, 'w')
        fp.write(temUrlList)
        fp.close()
        for i in newUrlList:
            if i in urlList: R[i] = urlList[i]
        return R

    def saveData(self, listitem):
        '''
        @ use data like: [taskid], [robotid], [key], [url], [title], [content], [runtime]
        '''
        listitem = (isinstance(listitem, list) and [listitem] or [[]])[0]
        importSQL = self.robotinfo['importSQL']
        execSQL = ''
        for i in listitem:
            adict = {'[taskid]': self.robotinfo['taskid'], '[robotid]': self.robotinfo['robotid'], '[key]': i['key'], '[url]': i['url'], '[title]': i['title'], '[message]': i['message'], '[runtime]': time.mktime(time.localtime())}
            comma = (execSQL=='' and [''] or [';'])[0]
            translate = make_xlat(adict)
            execSQL += comma + translate(importSQL)
        _G = self.parent.getConnection()
        _G['DB'].execute(execSQL)
        '''
        try:
            _G = self.parent.getConnection()
            _G['DB'].execute(execSQL)
            print 'saveData success.'
        except:
            print 'saveData err.'
        '''


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


import chardet

def toutf8(strr):
    if isinstance(strr, unicode):
        strr = strr.encode('utf8')
    elif isinstance(strr, str):
        srcencode = (chardet.detect(strr) and [chardet.detect(strr)['encoding']] or ['utf8'])[0]
        strr = not srcencode==None and unicode(strr, srcencode, 'ignore').encode('utf8')

    return strr