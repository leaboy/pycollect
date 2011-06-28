#!/usr/bin/python
#-*-coding:utf-8-*-

# The Main App for Data collector.
#
# Created: 2011-Jun-22 06:26:37
#      By: leaboy.w
#   Email: leaboy.w@gmail.com
# Package: phpserialize
#
# GNU Free Documentation License 1.3

import re, sys, time, os
import threading
import httplib, urllib
from urlparse import urlparse,urljoin
import hashlib
from database import *
from phpserialize import *

## Config params
# 最大线程数
threads = 10
# 采集速度控制，单位秒
speed = 3
# 设置提交的header头
headers = {"Accept": "*/*","User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"}
# 数据库连接
DB = Connection(host='localhost',database='pycollect',user='root',password='123456')
# 默认链接规则
defaultLinkReg = '''<a[^>]*?href=(?:\'|\")([^\'\"]+)(?:'|\")[^>]*?>([^<]*)<\/a>'''


class RunTask(threading.Thread):
    def __init__(self, taskinfo):
        threading.Thread.__init__(self)
        self._stop = threading.Event()

        self.taskinfo = taskinfo

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        taskid      = self.taskinfo['taskid']
        robotid     = self.taskinfo['robotid']
        isloop      = self.taskinfo['loop']
        loopperiod  = self.taskinfo['loopperiod']
        runtime     = self.taskinfo['runtime']
        nextruntime = self.taskinfo['nextruntime']

        while(1):
            triggertime = (nextruntime > 0 and [nextruntime] or [runtime])[0]
            currenttime = time.mktime(time.localtime())

            CollectApp(self.taskinfo)

            '''
            if triggertime == currenttime:
                CollectApp(self.taskinfo)
            elif triggertime < currenttime and isloop == 1:
                nextruntime = triggertime + loopperiod
                DB.query("UPDATE `pre_robots_task` SET `nextruntime` = '%d' WHERE `pre_robots_task`.`taskid` = '%d'" % (nextruntime, taskid))
            time.sleep(1)
            '''


class RunCollect(threading.Thread):
    def __init__(self, url, robotinfo):
        threading.Thread.__init__(self)
        self._stop = threading.Event()

        self.url = url
        self.robotinfo = robotinfo

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        Collect(self.url, self.robotinfo)
        time.sleep(1)


class Collect():
    def __init__(self, url, robotinfo):
        '''
        @ return {key: [url, title, content], key: []...}
        '''
        self.url = url
        self.robotinfo = robotinfo

        urlListHtml = self.httpRequest(url)[1]
        urlListHtml = self.parseData(urlListHtml, self.robotinfo['subjecturlrule'], '[list]')
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
                if self.robotinfo['onlylinks']==0:
                    rs = self.httpRequest(i[0])
                    if self.robotinfo['downloadmode'] == 0:
                        tempitem['title'] = (self.robotinfo['onlylinks']==1 and [i[1]] or [self.parseData(rs[1], self.robotinfo['subjectrule'], '[title]')])[0]
                        tempitem['title'] = (tempitem['title']=='' and [i[1]] or [tempitem['title']])[0]
                        tempitem['message'] = (self.robotinfo['onlylinks']==1 and [''] or [self.parseData(rs[1], self.robotinfo['messagerule'], '[message]')])[0]
                listitem.append(tempitem)
                time.sleep(speed)
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
                if isinstance(content, unicode):
                    content = content.encode('utf8')
                elif isinstance(content, str):
                    content = unicode(content, self.robotinfo['encode'], 'ignore').encode('utf8')
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
            logdata = loads(logdata)
            logdata = (isinstance(logdata, dict) and [dict_to_list(logdata)] or [[]])[0]
        except:
            logdata = []
        temUrlList.extend(logdata)
        newUrlList = [i for i in temUrlList if temUrlList.count(i)==1]
        temUrlList = list(set(temUrlList))
        temUrlList = dumps(temUrlList)
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
        DB.execute(execSQL)


class CollectApp():
    def __init__(self, taskinfo):
        taskid  = taskinfo['taskid']
        robotid = taskinfo['robotid']

        robots = DB.query("SELECT importSQL,listurl,listpagestart,listpageend,wildcardlen,reverseorder,encode,subjecturlrule,subjecturllinkrule,subjectrule,messagerule,onlylinks,downloadmode,extension,stockdata FROM `pre_robots` WHERE robotid = %d" % robotid)
        robotinfo = robots[0]

        robotinfo['importSQL']      = robotinfo['importSQL'].encode('utf8')
        robotinfo['subjecturlrule'] = robotinfo['subjecturlrule'].encode('utf8')
        robotinfo['subjecturllinkrule'] = robotinfo['subjecturllinkrule'].encode('utf8')
        robotinfo['subjectrule']    = robotinfo['subjectrule'].encode('utf8')
        robotinfo['messagerule']    = robotinfo['messagerule'].encode('utf8')
        robotinfo['taskid']         = taskid
        robotinfo['robotid']        = robotid
        self.robotinfo = robotinfo

        listurl = self.getListUrl(loads(self.robotinfo['listurl']))
        listurl = list(set(listurl))

        threadList = []
        for i in listurl:
            th = RunCollect(i, robotinfo)
            th.setDaemon(True)
            threadList.append(th)
            th.start()
            time.sleep(speed)

        try:
            while(1):
                pass
        except KeyboardInterrupt:
            for i in threadList:
               i.stop()
            sys.exit()

    def getListUrl(self, url):
        '''
        @ 得到所有待采集列表页的链接
        @ return [list1, list2, ...]
        '''
        if not isinstance(url, dict): return

        listurl = []
        if url.has_key('manual'):
            manualUrl = url['manual']
        if url.has_key('auto'):
            autoUrl = url['auto']

        if autoUrl!='':
            if autoUrl.find('[page]')!=-1:
                pageList = self.getListPageNum()
                for i in pageList:
                    listurl.append(autoUrl.replace('[page]', i))
            elif autoUrl.find('[stock]')!=-1:
                stockList = self.getListStockNum()
                for i in stockList:
                    listurl.append(autoUrl.replace('[stock]', i))

        if len(manualUrl)>0:
            for i in manualUrl:
                listurl.append(manualUrl[i])

        return listurl


    def getListPageNum(self):
        pagestart = (isinstance(self.robotinfo['listpagestart'], int) and [self.robotinfo['listpagestart']] or [0])[0]
        pageend = (isinstance(self.robotinfo['listpageend'], int) and [self.robotinfo['listpageend']] or [0])[0]

        liststep = (pagestart<pageend and [1] or [-1])[0]
        pageList = range(pagestart, pageend+liststep, liststep)

        if not isinstance(self.robotinfo['wildcardlen'], int) or self.robotinfo['wildcardlen']<=0:
            return pageList

        newPageList = []
        for i in pageList:
            newPageList.append(str(i).zfill(self.robotinfo['wildcardlen']))

        return newPageList


    def getListStockNum(self):
        rs = urllib.urlopen(self.robotinfo['stockdata'])
        stockList = eval(rs.read())
        stockList = (isinstance(stockList, list) and [stockList] or [[]])[0]

        return stockList


def MainApp():
    taskList = DB.query("SELECT t.taskid,t.robotid,t.loop,t.loopperiod,t.runtime,t.nextruntime FROM `pre_robots_task` t LEFT JOIN `pre_robots` r ON t.robotid = r.robotid")

    threadList = []
    for i in taskList:
        th = RunTask(i)
        th.setDaemon(True)
        threadList.append(th)
        th.start()

    try:
        while(1):
            pass
    except KeyboardInterrupt:
        for i in threadList:
           i.stop()
        sys.exit()


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


if __name__ == "__main__":
    MainApp()

