"""
http headers

"""

class CaselessDict(dict):

    __slots__ = ()

    def __init__(self, seq=None):
        super(CaselessDict, self).__init__()
        if seq:
            self.update(seq)

    def __getitem__(self, key):
        return dict.__getitem__(self, self.normkey(key))

    def __setitem__(self, key, value):
        dict.__setitem__(self, self.normkey(key), self.normvalue(value))

    def __delitem__(self, key):
        dict.__delitem__(self, self.normkey(key))

    def __contains__(self, key):
        return dict.__contains__(self, self.normkey(key))
    has_key = __contains__

    def __copy__(self):
        return self.__class__(self)
    copy = __copy__

    def normkey(self, key):
        """Method to normalize dictionary key access"""
        return key.lower()

    def normvalue(self, value):
        """Method to normalize values prior to be setted"""
        return value

    def get(self, key, def_val=None):
        return dict.get(self, self.normkey(key), self.normvalue(def_val))

    def setdefault(self, key, def_val=None):
        return dict.setdefault(self, self.normkey(key), self.normvalue(def_val))

    def update(self, seq):
        seq = seq.iteritems() if isinstance(seq, dict) else seq
        iseq = ((self.normkey(k), self.normvalue(v)) for k, v in seq)
        super(CaselessDict, self).update(iseq)

    @classmethod
    def fromkeys(cls, keys, value=None):
        return cls((k, value) for k in keys)

    def pop(self, key, *args):
        return dict.pop(self, self.normkey(key), *args)


class Headers(CaselessDict):
    """Case insensitive http headers dictionary"""

    __slots__ = ['encoding']

    def __init__(self, seq=None, encoding='utf-8'):
        self.encoding = encoding
        super(Headers, self).__init__(seq)

    def normkey(self, key):
        """Headers must not be unicode"""
        if isinstance(key, unicode):
            return key.title().encode(self.encoding)
        return key.title()

    def normvalue(self, value):
        """Headers must not be unicode"""
        if isinstance(value, unicode):
            value = value.encode(self.encoding)

        if isinstance(value, (list, tuple)):
            return list(value)
        return [value]

    def __getitem__(self, key):
        try:
            return super(Headers, self).__getitem__(key)[-1]
        except IndexError:
            return None

    def get(self, key, def_val=None):
        try:
            return super(Headers, self).get(key, def_val)[-1]
        except IndexError:
            return None

    def getlist(self, key, def_val=None):
        try:
            return super(Headers, self).__getitem__(key)
        except KeyError:
            if def_val is not None:
                return self.normvalue(def_val)
            return []

    def setlist(self, key, list_):
        self[key] = list_

    def setlistdefault(self, key, default_list=()):
        return self.setdefault(key, default_list)

    def appendlist(self, key, value):
        lst = self.getlist(key)
        lst.extend(self.normvalue(value))
        self[key] = lst

    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        return ((k, self.getlist(k)) for k in self.keys())

    def values(self):
        return [self[k] for k in self.keys()]

    def to_string(self):
        return headers_dict_to_raw(self)

    def __copy__(self):
        return self.__class__(self)
    copy = __copy__


def headers_raw_to_dict(headers_raw):
    """
    Convert raw headers (single multi-line string)
    to the dictionary.

    For example:
    >>> headers_raw_to_dict("Content-type: text/html\\n\\rAccept: gzip\\n\\n")
    {'Content-type': ['text/html'], 'Accept': ['gzip']}

    Incorrect input:
    >>> headers_raw_to_dict("Content-typt gzip\\n\\n")
    {}

    Argument is None:
    >>> headers_raw_to_dict(None)
    """
    if headers_raw is None:
        return None
    return dict([
        (header_item[0].strip(), [header_item[1].strip()])
        for header_item
        in [
            header.split(':', 1)
            for header
            in headers_raw.splitlines()]
        if len(header_item) == 2])


def headers_dict_to_raw(headers_dict):
    """
    Returns a raw HTTP headers representation of headers

    For example:
    >>> headers_dict_to_raw({'Content-type': 'text/html', 'Accept': 'gzip'})
    'Content-type: text/html\\r\\nAccept: gzip'
    >>> from twisted.python.util import InsensitiveDict
    >>> td = InsensitiveDict({'Content-type': ['text/html'], 'Accept': ['gzip']})
    >>> headers_dict_to_raw(td)
    'Content-type: text/html\\r\\nAccept: gzip'

    Argument is None:
    >>> headers_dict_to_raw(None)

    """
    if headers_dict is None:
        return None
    raw_lines = []
    for key, value in headers_dict.items():
        if isinstance(value, (str, unicode)):
            raw_lines.append("%s: %s" % (key, value))
        elif isinstance(value, (list, tuple)):
            for v in value:
                raw_lines.append("%s: %s" % (key, v))
    return '\r\n'.join(raw_lines)
