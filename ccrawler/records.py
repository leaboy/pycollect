#!/usr/bin/python
#-*-coding:utf-8-*-

# system database engine.
#
# Package: SQLAlchemy
#
# GNU Free Documentation License 1.3

import os

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import mapper, scoped_session, sessionmaker

def init_record(spider_name, dbname):
    db_path = os.path.join('records', str(spider_name))
    tabal_name = 'records'
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    db_file = os.path.join(db_path, str(dbname))
    engine = create_engine('sqlite:///%s' % db_file)
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