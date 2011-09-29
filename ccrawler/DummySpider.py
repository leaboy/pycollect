
'''
Example of Usage
'''

import common, re
from ccrawler import CCrawler, Request
from selector import HtmlSelector

import logging
logger = common.logger(name=__name__, filename='ccrawler.log', level=logging.DEBUG)

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

class DummySpider:
    #start_urls = ['http://ustock.finance.ifeng.com/stock_list.php?type=sh']
    #start_urls = ['http://ustock.finance.ifeng.com/stock_list.php?type=sz', 'http://ustock.finance.ifeng.com/stock_list.php?type=gem']
    #start_urls = ['http://www.blueidea.com/photo/gallery/?q=test&flag=0456454']
    #start_urls = ['http://disclosure.szse.cn/m/drgg000001.htm?type=sz&flag=notice', 'http://disclosure.szse.cn/m/drgg000002.htm?type=sz&flag=notice', 'http://disclosure.szse.cn/m/drgg000003.htm?type=sz&flag=notice', 'http://disclosure.szse.cn/m/drgg000004.htm?type=sz&flag=notice', 'http://disclosure.szse.cn/m/drgg000005.htm?type=sz&flag=notice', 'http://disclosure.szse.cn/m/drgg000006.htm?type=sz&flag=notice', 'http://disclosure.szse.cn/m/drgg000007.htm?type=sz&flag=notice', 'http://disclosure.szse.cn/m/drgg000008.htm?type=sz&flag=notice', 'http://disclosure.szse.cn/m/drgg000009.htm?type=sz&flag=notice', 'http://disclosure.szse.cn/m/drgg000010.htm?type=sz&flag=notice', 'http://disclosure.szse.cn/m/drgg000011.htm?type=sz&flag=notice', 'http://disclosure.szse.cn/m/drgg000012.htm?type=sz&flag=notice']
    start_urls = ['http://www.sse.com.cn/sseportal/webapp/datapresent/SSEQueryCompanyStatement?PRODUCTID=600010&COMPANY_CODE=600010&REPORTTYPE2=&REPORTTYPE=ALL&PAGE=1']
    #start_urls = ['http://www.baidu.com', 'http://www.google.com', 'http://www.google.hk']
    workers = 100
    timeout = 8
    #recover = False

    def parse(self, response):
        hxs = HtmlSelector(response)
        #//td[class="content"]/table[bordercolor="#000000"]/tr[bgcolor="#F4F4F4"]/td[1]
        itemlist = hxs.select('//td[@class="content"]/table[@bordercolor="#000000"]/tr[@bgcolor="#F4F4F4"]/td[1]')
        for item in itemlist:
            print item.select('a/@href').extract()
        '''
        Usage re
        '''
        '''
        itemlist = hxs.re('<td class=\'td10\'> .*?<\/td>')
        for item in itemlist:
            title = item.re('<a[^>]*[^>]*>(.*)[^<]*<\/a>')
            print title
        '''

        '''
        itemlist = hxs.re('<tr class=\"(border|pagelight)\">.*?<td nowrap>(.*?)<\/td>')
        linkitem = itemlist.re('<a[^>]*href=\"([^\s\"]+)\"[^>]*>[^<]*<\/a>').Link()
        for item in linkitem:
            title = item.re('<td class="content"><strong>(.*?)</strong></td>').extract()
            print title
        '''

        '''
        itemlist = hxs.re('<tr class=\"(border|pagelight)\">.*?<td nowrap>(.*?)<\/td>')
        for item in itemlist:
            title = item.re('<a[^>]*>(.*)[^<]*<\/a>').extract()
            if title:
                print title
        '''

        '''
        Usage xpath
        '''
        '''
        itemlist = hxs.select('//tr[@class!="listTitle"]/td[@nowrap]')
        for item in itemlist:
            title = item.select('a/text()').extract()
            if title:
                print title
        '''

        '''
        itemlist = hxs.select('//table[@class="border"]/tr[@class!="listTitle"]/td[@nowrap]')
        linkitem = itemlist.select('a/@href').Link()
        for item in linkitem:
            title = item.select('//td[@class="content"]/strong/text()').extract()
            #message = item.select('//table[@class="pageLighter"]/tr/td').extract()
            if title:
                print title
                #print title[0].encode('gb2312', 'backslashreplace')
        '''

        '''
        itemlist = hxs.select('//ul[@id="stocklist"]/li')
        for item in itemlist:
            info = item.select('a/text()').extract()
            if info:
                matchs = re.search('(.*)\((\d+)\)', info[0].encode('utf-8', 'backslashreplace'))
                title = matchs.group(1)
                stockid = matchs.group(2)

                try:
                    save_engine = create_engine('%s://%s:%s@%s/%s?charset=%s' % ('mysql', 'root', '123456', 'localhost', 'ultrax', 'utf8'))
                    dbconn = save_engine.connect()
                    dbconn.execute("INSERT INTO `ultrax`.`pre_stock` (`stockid`, `type`, `stockname`, `desc`) VALUES ('"+stockid+"', 'sz', '"+title+"', '');")
                except OperationalError, e:
                    code, message = e.orig
                    logger.error('Error %s: %s.' % (code, message))
        '''

    def process_item(self, item):
        for i in item:
            print i

class a:
    pass


spider = DummySpider()
crawler = CCrawler(spider)
crawler.start()

