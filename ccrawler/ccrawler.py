#!/usr/bin/python
#-*-coding:utf-8-*-

# Main App.
#
# $Author$
# $Id$
#
# Lib: eventlet, lxml
#
# GNU Free Documentation License 1.3

from __future__ import with_statement

import common
import eventlet
from eventlet import queue
from eventlet.green import urllib2
from response import Response

import logging, traceback
logger = common.logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

class CCrawler:
    def __init__(self, spider):
        self.spider = GetAttr(spider)
        self.workers = GetAttr(self.spider, 'workers', 10)
        self.timeout = GetAttr(self.spider, 'timeout', 120)
        self.start_urls = GetAttr(self.spider, 'start_urls', [])

        self.creq = queue.Queue()
        self.cres = queue.Queue()

        self.pool = eventlet.GreenPool(self.workers)
        self.pool.spawn_n(self.dispatcher)
        self.task_done = 0

    def dispatcher(self):
        try:
            for url in self.start_urls:
                self.creq.put(url)
            for i in range(self.workers):
                self.pool.spawn_n(self.fetch_coroutine)
        except Exception:
            logger.error("dispatcher Error!")

    def fetch_coroutine(self):
        while not self.creq.empty():
            self.fetcher()

    def fetcher(self):
        url, body, status, headers, response = self.creq.get(), None, 200, None, None
        errormsg = '200'
        request = urllib2.Request(url)
        t = eventlet.Timeout(self.timeout, False)
        try:
            response = urllib2.urlopen(request)
            body = response.read()
        except urllib2.HTTPError, e:
            status = errormsg = e.code
        except urllib2.URLError, e:
            errormsg = 'URLError: %s.' % e.args[0]
        except eventlet.Timeout, e:
            errormsg = 'Time out.'
        except:
            errormsg = 'URLError: Could not resolve.'
        finally:
            t.cancel()
            response = Response(url, status, headers, body, request)
            self.cres.put(response)
            self.pool.spawn_n(self.parse_coroutine)
            logger.info('Fetched: %s (%s)' % (url, errormsg))
            self.task_done += 1

    def start(self):
        logger.info("CCrawler start...")
        self.pool.waitall()
        logger.info("CCrawler closed.\n")

    def stop(self):
        self.creq.resize(0)
        logger.info("stopping crawl...\n")

    def parse_coroutine(self):
        while self.creq.empty() and not self.cres.empty():
            response = self.cres.get()
            item = self._parse(response)
            self._pipeliner(item)

    def _parse(self, response):
        '''when spider's parse is empty, then use this replace with do nothing'''
        parse = GetAttr(self.spider, 'parse', None)
        if parse:
            return parse(response)

    def _pipeliner(self, item):
        '''when spider's process_item is empty, then use this replace with do nothing'''
        process_item = GetAttr(self.spider, 'process_item', None)
        if process_item:
            process_item(item)



def GetAttr(object, name=None, default=None):
    try:
        if object is None:
            return default
        elif not type(object).__name__=='instance':
            raise Exception

        if name==None:
            return object
        else:
            if not hasattr(object, str(name)):
                return default
            else:
                return getattr(object, name)
    except Exception:
        logger.error('Spider not exist!')