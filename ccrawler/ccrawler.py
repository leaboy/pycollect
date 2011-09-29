
# Main App.
#
# $Author$
# $Id$
#
# Lib: eventlet, lxml
#
# GNU Free Documentation License 1.3

from __future__ import with_statement

import hashlib
import common, settings
import eventlet
from eventlet import queue
from http import Request, Response

from sqlalchemy.orm import mapper
from records import init_record


import logging, traceback
logger = common.logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

class CCrawler:
    def __init__(self, spider):
        self.spider = self._spider(spider)
        self.taskid = getattr(self.spider, 'taskid', 0)
        self.recover = getattr(self.spider, 'recover', True)
        self.workers = getattr(self.spider, 'workers', 100)
        self.timeout = getattr(self.spider, 'timeout', 60)
        self.start_urls = getattr(self.spider, 'start_urls', [])

        self.creq = queue.Queue()
        self.cres = queue.Queue()

        self.pool = eventlet.GreenPool(self.workers)
        self.pool.spawn_n(self.dispatcher)

        self.records, self.session = init_record(self.taskid)

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
        url = self.creq.get()
        response = Request(str(url), self.timeout)
        self.cres.put(response)
        self.pool.spawn_n(self.parse_coroutine)
        logger.info('Fetched: %s (%s)' % (url, response.status))

    def start(self):
        logger.info("CCrawler start...")
        self.pool.waitall()
        logger.info("CCrawler closed.\n")

    def stop(self):
        self.creq.resize(0)
        logger.info("stopping crawl...\n")

    def parse_coroutine(self):
        response = self.cres.get()
        if response.status is not '200':
            return
        res_hash = hashlib.md5(response.body).hexdigest().upper()
        db_record = self.session.query(self.records.hash).filter(self.records.hash==res_hash).first()
        if db_record and not self.recover:
            return
        else:
            item = self._parse(response)
            if item is not None:
                self._pipeliner(item)
            if not db_record:
                query = self.records(res_hash)
                self.session.add(query)
                self.session.commit()

    def _spider(self, spider):
        try:
            if not type(spider).__name__=='instance':
                raise Exception
            else:
                return spider
        except Exception:
            logger.error('Spider not exist!')

    def _parse(self, response):
        '''when spider's parse is empty, then use this replace with do nothing'''
        item_parse = getattr(self.spider, 'parse', None)
        if item_parse:
            return item_parse(response)

    def _pipeliner(self, item):
        '''when spider's process_item is empty, then use this replace with do nothing'''
        process_item = getattr(self.spider, 'process_item', None)
        if process_item:
            process_item(item)