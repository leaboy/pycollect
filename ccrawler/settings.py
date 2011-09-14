"""
This module contains the default values for all settings.

"""

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}

DEFAULT_RESPONSE_ENCODING = 'ascii'

ENCODING_ALIASES = {}

ENCODING_ALIASES_BASE = {
    # gb2312 is superseded by gb18030
    'gb2312': 'gb18030',
    'chinese': 'gb18030',
    'csiso58gb231280': 'gb18030',
    'euc- cn': 'gb18030',
    'euccn': 'gb18030',
    'eucgb2312-cn': 'gb18030',
    'gb2312-1980': 'gb18030',
    'gb2312-80': 'gb18030',
    'iso- ir-58': 'gb18030',
    # gbk is superseded by gb18030
    'gbk': 'gb18030',
    '936': 'gb18030',
    'cp936': 'gb18030',
    'ms936': 'gb18030',
    # latin_1 is a subset of cp1252
    'latin_1': 'cp1252',
    'iso-8859-1': 'cp1252',
    'iso8859-1': 'cp1252',
    '8859': 'cp1252',
    'cp819': 'cp1252',
    'latin': 'cp1252',
    'latin1': 'cp1252',
    'l1': 'cp1252',
    # others
    'zh-cn': 'gb18030',
    'win-1251': 'cp1251',
    'macintosh' : 'mac_roman',
    'x-sjis': 'shift_jis',
}