
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

import base64

class DummySpider:
    #start_urls = ['http://ustock.finance.ifeng.com/stock_list.php?type=sh']
    #start_urls = ['http://ustock.finance.ifeng.com/stock_list.php?type=sz', 'http://ustock.finance.ifeng.com/stock_list.php?type=gem']
    #start_urls = ['http://www.blueidea.com/photo/gallery', 'http://www.blueidea.com/photo/gallery/index_2.asp', 'http://www.blueidea.com/photo/gallery/index_3.asp', 'http://www.blueidea.com/photo/skill/index.asp', 'http://www.blueidea.com/photo/skill/index_2.asp', 'http://www.blueidea.com/photo/skill/index_3.asp', 'http://www.blueidea.com/photo/skill/index_4.asp', 'http://www.blueidea.com/photo/skill/index_5.asp', 'http://www.blueidea.com/photo/skill/index_6.asp', 'http://www.blueidea.com/photo/camera/index.asp', 'http://www.blueidea.com/photo/camera/index_2.asp']
    start_urls = ['http://disclosure.szse.cn/m/drgg000001.htm', 'http://disclosure.szse.cn/m/drgg000002.htm']
    #start_urls = ['http://www.sse.com.cn/sseportal/webapp/datapresent/SSEQueryCompanyStatement?PRODUCTID=600010&COMPANY_CODE=600010&REPORTTYPE2=&REPORTTYPE=ALL&PAGE=1']
    #start_urls = ['http://money.finance.sina.com.cn/corp/go.php/vCB_AllNewsStock/symbol/sh600299.phtml']
    #start_urls = ['http://www.baidu.com', 'http://www.google.com', 'http://www.google.hk']
    #start_urls = ['http://money.finance.sina.com.cn/corp/view/vCB_AllNewsStock.php?symbol=sz000001&Page=1']
    #start_urls = ['http://www.tuaaa.com/eread/']
    workers = 100
    timeout = 8
    #recover = False
    #reverse = True

    def parse(self, response):
        hxs = HtmlSelector(response)

        '''
        itemlist = hxs.select('//div[@class="nr_left"]/ul/li[@class="nr_left2"]')
        linkitem = itemlist.select('a/@href').Link()
        print len(linkitem)

        for item in linkitem:
            title = item.select('//div[@class="nr_left"]/div[@class="nr_left_top"]/div[@class="nr_left_top1"]/text()').extract()
            content = item.select('//div[@class="nr_left"]/div[@class="nr_left_center"]').extract()
            print title
        '''

        itemlist = hxs.select('//td[@class="td2"]')
        for item in itemlist:
            title = item.select('a/text()').extract()
            link = item.select('a/@href').extract()
            print link

        '''
        #//td[@class="content"]/table[@bordercolor="#000000"]/tr[@bgcolor="#F4F4F4"]/td[1]
        #//td[@class="datelist"]/ul
        itemlist = hxs.select('//div[@class="datelist"]/ul/a')
        linkitem = itemlist.select('@href').Link()
        for item in linkitem:
            #print item.select('//div[@class="blkContainerSblk"]/h1[@id="artibodyTitle"]/text()').extract()
            title = item.select('//div[@class="blkContainerSblk"]/h1[@id="artibodyTitle"]/text()').extract()
            content = item.select('//div[@class="blkContainerSblkCon"]').extract()

            if len(content)>0:
                fp = open(base64.b64encode(item.base_url), 'w')
                fp.write(content[0].encode('gb2312', 'backslashreplace'))
                fp.close()
        '''

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

