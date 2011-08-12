#!/usr/bin/python
#-*-coding:utf-8-*-

# Common functions or class.
#
# $Author$
# $Id$
#
# GNU Free Documentation License 1.3

import re, warnings
from functools import wraps

def deprecated(use_instead=None):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""

    def wrapped(func):
        @wraps(func)
        def new_func(*args, **kwargs):
            message = "Call to deprecated function %s." % func.__name__
            if use_instead:
                message += " Use %s instead." % use_instead
            warnings.warn(message, category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return new_func
    return wrapped

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

def encoding(text):

    import chardet

    try:
        if text is None:
            return {'text': 'None', 'confidence': 1.0, 'encoding': 'ascii'}

        if isinstance(text, unicode):
            return {'text': text, 'confidence': 1.0, 'encoding': 'ascii'}

        elif isinstance(text, basestring):
            char = chardet.detect(text)
            char['text'] = text.decode(char['encoding'])
            return char
    except:
        return

def extract_regex(regex, text):
    """Extract a list of unicode strings from the given text/encoding using the following policies:

    * if the regex contains a named group called "extract" that will be returned
    * if the regex contains multiple numbered groups, all those will be returned (flattened)
    * if the regex doesn't contain any group the entire regex matching is returned
    """

    if isinstance(regex, basestring):
        regex = re.compile(regex)

    try:
        strings = [regex.search(text).group('extract')]   # named group
    except:
        strings = regex.findall(text)    # full regex or numbered groups
    strings = flatten(strings)

    if isinstance(text, unicode):
        return [s for s in strings]
    else:
        return [encoding(s)['text'] for s in strings]

def flatten(x):
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, (8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]"""

    result = []
    for el in x:
        if hasattr(el, "__iter__"):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result