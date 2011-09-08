#!/usr/bin/python
#-*-coding:utf-8-*-

from ccrawler import common
from ccrawler.ccrawler import CCrawler
from ccrawler.selector import HtmlSelector

import logging
logger = common.logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

import time
from common import Func, make_xlat

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
        self.messagerule = robot.messagerule
        self.rulemode = robot.rulemode
        self.linkmode = robot.linkmode
        self.downloadmode = robot.downloadmode

        self.start_urls = Func.getStartUrls(robot.listurl, robot.listpagestart, robot.listpageend, robot.wildcardlen, robot.stockdata)
        self.workers = robot.threads
        self.timeout = robot.timeout
        self.parent = parent

    def parse(self, response):
        res = {}
        res['url'] = response.url

        hxs = HtmlSelector(response)
        if self.rulemode=='xpath':
            itemlist = hxs.select(self.subjecturlrule)
            if self.linkmode:
                for item in itemlist:
                    res['title'] = item.select(self.subjectrule).extract()
                    res['link'] = item.select(self.subjecturllinkrule).extract()
                    res['message'] = ''
                    yield self.result_check(res)
            else:
                pageitem = itemlist.select(self.subjecturllinkrule).Link()
                for item in pageitem:
                    if item:
                        res['link'] = item.base_url
                        res['title'] = item.select(self.subjectrule).extract()
                        res['message'] = item.select(self.messagerule).extract()
                        yield self.result_check(res)


        elif self.rulemode=='regex':
            itemlist = hxs.re(self.subjecturlrule)
            if self.linkmode:
                for item in itemlist:
                    res['title'] = item.re(self.subjectrule).extract()
                    res['link'] = item.re(self.subjecturllinkrule).extract()
                    res['message'] = ''
                    yield self.result_check(res)
            else:
                pageitem = itemlist.re(self.subjecturllinkrule).Link()
                for item in pageitem:
                    if item:
                        res['link'] = item.base_url
                        res['title'] = item.re(self.subjectrule).extract()
                        res['message'] = item.select(self.messagerule).extract()
                        yield self.result_check(res)

    def process_item(self, result):
        execSQL = ''
        datatype, conn, dbcharset = self.DbConn()
        if datatype == 'json':
            pass
        else:
            for i in result:
                adict = {'[link]': i['link'].encode(dbcharset, 'backslashreplace'), '[title]': i['title'].encode(dbcharset, 'backslashreplace'), '[message]': i['message'].encode(dbcharset, 'backslashreplace'), '[runtime]': time.mktime(time.localtime())}
                translate = make_xlat(adict)
                comma = (execSQL=='' and [''] or [';'])[0]
                execSQL += comma + translate(str(self.importSQL))

            if len(execSQL)>0 and conn:
                try:
                    execSQL = execSQL.replace('%', '%%')
                    conn.execute(execSQL)
                    conn.close()
                except:
                    logger.error('Execute SQL error.')

    def DbConn(self):
        dataconn = Func.unserialize(self.dataconn)
        dbcharset = ((hasattr(dataconn, 'dbcharset') and dataconn['dbcharset']) and [dataconn['dbcharset']] or ['utf8'])[0]
        if not dataconn['datatype'] == 'json':
            from sqlalchemy import create_engine
            from sqlalchemy.exc import OperationalError
            try:
                save_engine = create_engine('%s://%s:%s@%s/%s?charset=%s' % (dataconn['datatype'], dataconn['dbuser'], dataconn['dbpw'], dataconn['dbhost'], dataconn['dbname'], dbcharset))
                conn = save_engine.connect()
            except OperationalError, e:
                conn = None
                code, message = e.orig
                logger.error('Error %s: %s.' % (code, message))
        return dataconn['datatype'], conn, dbcharset

    def result_check(self, res):
        res['title'] = res['title'] and res['title'][0] or ''
        if isinstance(res['link'], list) and len(res['link'])>0:
            res['link'] = res['link'][0]
        res['message'] = res['message'] and res['message'][0] or ''
        return res

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