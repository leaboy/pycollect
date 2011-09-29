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

def init_record(tname):
    tabal_name = hashlib.md5(str(tname)).hexdigest().upper()
    engine = create_engine('sqlite:///records.db')
    metadata = MetaData()

    record_table = Table(tabal_name, metadata,
        Column('id', Integer, primary_key=True),
        Column('hash', String, index=True)
    )

    class Records(object):
        def __init__(self, hash):
            self.hash = hash

        def __repr__(self):
            return "<Records('%s')>" % (self.hash)

    mapper(Records, record_table)
    metadata.create_all(engine)
    session = scoped_session(sessionmaker(bind=engine))

    return Records, session