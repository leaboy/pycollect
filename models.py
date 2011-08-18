#!/usr/bin/python
#-*-coding:utf-8-*-

# system database engine.
#
# Package: SQLAlchemy
#
# GNU Free Documentation License 1.3

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Robot(Base):
    __tablename__ = 'robots'

    robotid     = Column(Integer, primary_key=True)

users_table = User.__table__

sys_engine = create_engine('sqlite:///data.db', echo=True)

if __name__ == "__main__":
    metadata.create_all(sys_engine)