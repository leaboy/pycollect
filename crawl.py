#!/usr/bin/python
#-*-coding:utf-8-*-

# The Main class for crawl.
#
# Created: 2011-Jul-12 ‏‎11:01:24
#      By: leaboy.w
#   Email: leaboy.w@gmail.com
#     Lib: Scrapy 0.12.0
#
# GNU Free Documentation License 1.3

import sys, os

class Crawl:
    def __init__ (self):
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'Test.settings')
        sys.path.append("./Test")

        from scrapy.cmdline import execute
        execute(['crawl.py','crawl','sse.com.cn'])

if __name__ == "__main__":
    Crawl()
