#!/usr/bin/python
#-*-coding:utf-8-*-

# Common functions or class.
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

import warnings

def deprecated_setter(setter, attrname):
    def newsetter(self, value):
        c = self.__class__.__name__
        warnings.warn("Don't modify %s.%s attribute, use %s.replace() instead" % \
            (c, attrname, c), DeprecationWarning, stacklevel=2)
        return setter(self, value)
    return newsetter

def logger(**kwargs):

    import logging

    options = {
        'name': 'root',
        'level': logging.NOTSET, # DEBUG, INFO, WARNING, ERROR, CRITICAL
        'format': '%(asctime)s [%(name)s] - %(levelname)s %(message)s',
        'filename': 'root.log',
        'filemode': 'a', }

    options.update(kwargs)

    name = options['name']
    logger = logging.getLogger(name)

    Formatter = logging.Formatter(options['format'])
    logHandler = logging.FileHandler(options['filename'], options['filemode'])
    logHandler.setFormatter(Formatter)
    logger.addHandler(logHandler)

    options.pop('filename')
    options.pop('filemode')
    logging.basicConfig(**options)

    return logger