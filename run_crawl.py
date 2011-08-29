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
        self.dbconn = task.dbconn
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
        res['message'] = 'None'

        hxs = HtmlSelector(response.body)
        if self.rulemode=='xpath':
            itemlist = hxs.select(self.subjecturlrule)
            for item in itemlist:
                res['title'] = item.select(self.subjectrule).extract()[0]
                res['link'] = item.select(self.subjecturllinkrule).extract()[0]
                yield res

        elif self.rulemode=='regex':
            itemlist = hxs.re(self.subjecturlrule)
            for item in itemlist:
                res['title'] = item.re(self.subjectrule)[0]
                res['link'] = item.re(self.subjecturllinkrule)[0]
                yield res

    def process_item(self, item):
        execSQL = ''
        conn, dbcharset = self.DbConn()
        for i in item:
            adict = {'[link]': i['link'].encode(dbcharset, 'backslashreplace'), '[title]': i['title'].encode(dbcharset, 'backslashreplace'), '[runtime]': time.mktime(time.localtime())}
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
        dbconn = Func.unserialize(self.dbconn)
        dbcharset = (dbconn['dbcharset'] and [dbconn['dbcharset']] or ['utf8'])[0]
        from sqlalchemy import create_engine
        from sqlalchemy.exc import OperationalError
        try:
            save_engine = create_engine('%s://%s:%s@%s/%s?charset=%s' % (dbconn['dbtype'], dbconn['dbuser'], dbconn['dbpw'], dbconn['dbhost'], dbconn['dbname'], dbcharset))
            conn = save_engine.connect()
        except OperationalError, e:
            conn = None
            code, message = e.orig
            logger.error('Error %s: %s.' % (code, message))
        return conn, dbcharset


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