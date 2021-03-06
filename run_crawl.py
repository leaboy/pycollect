#!/usr/bin/python
#-*-coding:utf-8-*-

from ccrawler import common
from ccrawler.ccrawler import CCrawler
from ccrawler.selector import HtmlSelector

import logging
logger = common.logger(name=__name__, level=logging.DEBUG)

import os, time, urllib, urllib2, urlparse, base64, hashlib
from common import Func

class DummySpider:
    def __init__(self, task, parent):
        self.taskid = task.taskid
        self.robotid = task.robotid
        self.dataconn = task.dataconn
        self.importSQL = task.importSQL
        robot = task.robotinfo
        self.subjecturlrule = robot.subjecturlrule
        self.subjectrule = robot.subjectrule
        self.subjecturllinkrule   = robot.subjecturllinkrule
        self.timerule = robot.timerule
        self.messagerule = robot.messagerule
        self.reversemode = robot.reversemode
        self.rulemode = robot.rulemode
        self.linkmode = robot.linkmode
        self.downloadmode = robot.downloadmode

        self.start_urls = Func.getStartUrls(robot.listurl, robot.listpagestart, robot.listpageend, robot.wildcardlen, robot.stockdata)
        self.name = self.taskid
        self.workers = robot.threads
        self.timeout = robot.timeout
        self.parent = parent
        self.recover = False
        self.reverse = self.reversemode

    def parse(self, response):
        res = {}
        args = response.args
        res['url'] = response.url
        res['runtime'] = time.mktime(time.localtime())

        hxs = HtmlSelector(response)
        if self.rulemode=='xpath':
            itemlist = hxs.select(self.subjecturlrule)
            if self.linkmode:
                for item in itemlist:
                    res['args'] = args
                    res['title'] = item.select(self.subjectrule).extract()
                    res['time'] = item.select(self.timerule).extract()
                    res['link'] = item.select(self.subjecturllinkrule).extract()
                    res['message'] = ''
                    yield self.result_check(res)
            else:
                pageitem = itemlist.select(self.subjecturllinkrule).Link(self.recover)
                for item in pageitem:
                    if item:
                        res['args'] = args
                        res['link'] = item.base_url
                        res['title'] = item.select(self.subjectrule).extract()
                        res['time'] = item.select(self.timerule).extract()
                        res['message'] = item.select(self.messagerule).extract()
                        yield self.result_check(res)

        elif self.rulemode=='regex':
            itemlist = hxs.re(self.subjecturlrule)
            if self.linkmode:
                for item in itemlist:
                    res['args'] = args
                    res['title'] = item.re(self.subjectrule).extract()
                    res['time'] = item.select(self.timerule).extract()
                    res['link'] = item.re(self.subjecturllinkrule).extract()
                    res['message'] = ''
                    yield self.result_check(res)
            else:
                pageitem = itemlist.re(self.subjecturllinkrule).Link(self.recover)
                for item in pageitem:
                    if item:
                        res['args'] = args
                        res['link'] = item.base_url
                        res['title'] = item.re(self.subjectrule).extract()
                        res['time'] = item.select(self.timerule).extract()
                        res['message'] = item.re(self.messagerule).extract()
                        yield self.result_check(res)

    def process_item(self, result):
        execSQL = ''
        dataconn, dbconn, dbcharset = self.DbConn()
        if dataconn['datatype']=='json':
            for i in result:
                args = i.pop('args')
                try:
                    param_dict = dict([
                        (param_item[0].strip(), param_item[1].strip())
                        for param_item
                        in [
                            part.split('=', 1)
                            for part
                            in dataconn['apiparam'].splitlines()]
                        if len(param_item) == 2])

                    param_dict = self.dict_value(dict(i, **args), param_dict, dbcharset)

                    request = urllib2.Request(dataconn['apiurl'], urllib.urlencode(param_dict))
                    response = urllib2.urlopen(request)
                except:
                    logger.error('Connect API error.')

        elif dataconn['datatype']=='txt':
            basepath = dataconn['txtpath']
            listname = None
            pagepath = None
            if not os.path.exists(basepath):
                os.makedirs(basepath)

            try:
                for i in result:
                    args = i.pop('args')
                    param_dict = dict([
                        (param_item[0].strip(), param_item[1].strip())
                        for param_item
                        in [
                            part.split('=', 1)
                            for part
                            in dataconn['param'].splitlines()]
                        if len(param_item) == 2])

                    param_dict = self.dict_value(dict(i, **args), param_dict, dbcharset, True)
                    param_dict['charset'] = dbcharset

                    # list
                    if listname is None:

                        listname = hashlib.md5(i['url']).hexdigest()
                        pagepath = os.path.join(basepath, listname)

                        listidx = os.path.join(basepath, 'index')
                        fp = open(listidx, 'a')
                        fp.write("%s\n" % listname)
                        fp.close()

                        if not os.path.exists(pagepath):
                            os.makedirs(pagepath)

                    # page
                    pageidx = os.path.join(pagepath, 'index')
                    txtname = hashlib.md5(i['link']).hexdigest()

                    fp = open(pageidx, 'a')
                    fp.write("%s\n" % txtname)
                    fp.close()

                    # file
                    txtfile = os.path.join(pagepath, txtname)

                    fp = open(txtfile, 'w')
                    fp.write(Func.serialize(param_dict))
                    fp.close()
            except:
                logger.error('Connect API error.')

        else:
            for i in result:
                args = i.pop('args')
                comma = (execSQL=='' and [''] or [';'])[0]
                execSQL += comma + self.dict_value(dict(i, **args), self.importSQL, dbcharset)

            if len(execSQL)>0 and dbconn:
                try:
                    execSQL = execSQL.replace('%', '%%')
                    dbconn.execute(execSQL)
                    dbconn.close()
                except:
                    logger.error('Execute SQL error.')

    def DbConn(self):
        dbconn = None
        dataconn = Func.unserialize(self.dataconn)
        dbcharset = ((hasattr(dataconn, 'dbcharset') and dataconn['dbcharset']) and [dataconn['dbcharset']] or ['utf8'])[0]
        if dataconn['datatype']!='json' and dataconn['datatype']!='txt':
            from sqlalchemy import create_engine
            from sqlalchemy.exc import OperationalError
            try:
                save_engine = create_engine('%s://%s:%s@%s/%s?charset=%s' % (dataconn['datatype'], dataconn['dbuser'], dataconn['dbpw'], dataconn['dbhost'], dataconn['dbname'], dbcharset))
                dbconn = save_engine.connect()
            except OperationalError, e:
                code, message = e.orig
                logger.error('Error %s: %s.' % (code, message))
        return dataconn, dbconn, dbcharset

    def result_check(self, res):
        res['title'] = res['title'] and res['title'][0] or ''
        if isinstance(res['link'], list) and len(res['link'])>0:
            res['link'] = urlparse.urljoin(res['url'], res['link'][0])
        res['time'] = res['time'] and res['time'][0] or ''
        res['message'] = res['message'] and res['message'][0] or ''
        return res

    def dict_value(self, adict, paramdict, dbcharset, encoding=False):
        adict['link'] = adict['link'].encode(dbcharset, 'backslashreplace')
        adict['title'] = adict['title'].encode(dbcharset, 'backslashreplace')
        adict['time'] = adict['time'].encode(dbcharset, 'backslashreplace')
        adict['message'] = adict['message'].encode(dbcharset, 'backslashreplace')
        adict = dict([('[%s]' % k, adict[k]) for k in adict])
        for i in paramdict:
            uitem = paramdict[i]
            if uitem in adict:
                paramdict[i] = encoding and base64.b64encode(adict[uitem]) or adict[uitem]
        return paramdict


from PyQt4 import QtCore
from pycollect import Task_Flag_Waiting, Task_Flag_Runing, Task_Flag_Stoped, Task_Flag_Failed

class RunCrawl(QtCore.QThread):
    def __init__(self, taskid, spider, parent):
        QtCore.QThread.__init__(self, parent)
        self.taskid = taskid
        self.spider = spider
        self.parent = parent
        self.crawl = None

    def stop(self, state=Task_Flag_Stoped):
        if self.crawl is not None and self.crawl.creq.qsize()>0:
            self.crawl.stop()

    def run(self):
        self.crawl = CCrawler(self.spider)
        self.crawl.start()
        self.emit(QtCore.SIGNAL("Updated"), self.taskid, Task_Flag_Stoped)