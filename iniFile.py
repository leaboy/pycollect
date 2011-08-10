#   Programmer: limodou
#   E-mail:     chatme@263.net
#
#   Copyleft 2004 limodou
#
#   Distributed under the terms of the GPL (GNU Public License)
#
#   NewEdit is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#   $Id$

import os
import sys
import codecs
from ConfigParser import ConfigParser, NoOptionError, NoSectionError
import types

class IniFile(ConfigParser):

    def __init__(self, inifile, saveimmediately=False, encoding=None):
        ConfigParser.__init__(self)
        self.inifile=inifile
        self.saveimmediately = saveimmediately
        self.encoding = encoding
        if inifile:
            self.read(inifile)

    def read(self, inifile):
        self.inifile=inifile
        if inifile:
            try:
                fp = file(self.inifile, 'rb')
            except:
                fp = None
            if fp:
                if self.encoding:
                    reader = codecs.lookup(self.encoding)[2](fp)
                else:
                    reader = fp
                self.readfp(reader)
                reader.close()

    def get(self, sec, option, default=None):
        """Get an option value for given section or return default"""
        if self.has_option(sec, option):
            return ConfigParser.get(self, sec, option, raw=0, vars=None)
        else:
            return default

    def getint(self, sec, option, default=0):
        if self.has_option(sec, option):
            return ConfigParser.getint(self, sec, option)
        else:
            return default

    def getfloat(self, sec, option, default=0.0):
        if self.has_option(sec, option):
            return ConfigParser.getfloat(self, sec, option)
        else:
            return default

    def getboolean(self, sec, option, default=0):
        if self.has_option(sec, option):
            return ConfigParser.getboolean(self, sec, option)
        else:
            return default

    def set(self, section, option, value):
        if not self.has_section(section):
            self.add_section(section)
        ConfigParser.set(self, section, option, value)
        if self.saveimmediately:
            self.save()

    def remove_section(self, section):
        res=ConfigParser.remove_section(self, section)
        if res and self.saveimmediately:
            self.save()
        return res

    def remove_option(self, section, option):
        try:
            res=ConfigParser.remove_option(self, section, option)
            if res and self.saveimmediately:
                self.save()
            return res
        except NoSectionError:
            return 0

    def add_section(self, section):
        ConfigParser.add_section(self, section)
        if self.saveimmediately:
            self.save()

    def save(self):
        fp=file(self.inifile, "wb")
        if self.encoding:
            writer = codecs.lookup(self.encoding)[3](fp)
        else:
            writer = fp
        self.write(writer)
        writer.close()

    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s = %s\n" % (key, self.strValue(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key != "__name__":
                    fp.write("%s = %s\n" %
                             (key, self.strValue(value).replace('\n', '\n\t')))
            fp.write("\n")

    def strValue(self, value):
        if type(value) in (types.StringType, types.UnicodeType):
            return value
        else:
            return str(value)

