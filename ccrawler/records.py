#!/usr/bin/python
#-*-coding:utf-8-*-

# system database engine.
#
# Package: SQLAlchemy
#
# GNU Free Documentation License 1.3

import hashlib

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import mapper, scoped_session, sessionmaker

class Records(object):
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "<Records('%s')>" % (self.url)

def init_record(tname):
    tabal_name = hashlib.md5(str(tname)).hexdigest().upper()
    engine = create_engine('sqlite:///records.db', echo=True)
    metadata = MetaData()

    record_table = Table(tabal_name, metadata,
        Column('id', Integer, primary_key=True),
        Column('url', String, index=True)
    )
    metadata.create_all(engine)
    return engine, record_table

engine, table = init_record('1')
mapper(Records, table)

Session = scoped_session(sessionmaker(bind=engine))
q = Records('http://www.baidu.com')
Session.commit()

Session.query(table).all()