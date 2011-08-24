#!/usr/bin/python
#-*-coding:utf-8-*-

# system database engine.
#
# Package: SQLAlchemy
#
# GNU Free Documentation License 1.3

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Robot(Base):
    __tablename__ = 'robots'

    robotid             = Column(Integer, primary_key=True)
    robotname           = Column(String(20), nullable=False)
    timeout             = Column(SmallInteger, default=1)
    threads             = Column(SmallInteger, default=100)
    listurl             = Column(Text, nullable=False)
    stockdata           = Column(Text, nullable=False)
    listpagestart       = Column(SmallInteger, default=0)
    listpageend         = Column(SmallInteger, default=0)
    wildcardlen         = Column(SmallInteger, default=0)
    subjecturlrule      = Column(Text, nullable=False)
    subjecturllinkrule  = Column(Text, nullable=False)
    subjectrule         = Column(Text, nullable=False)
    messagerule         = Column(Text, nullable=False)
    reversemode         = Column(SmallInteger, default=0)
    rulemode            = Column(String(6), default='xpath')
    linkmode            = Column(SmallInteger, default=0)
    downloadmode        = Column(SmallInteger, default=0)

    def __init__(self, robotname, listurl):
        self.robotname   = robotname
        self.listurl  = listurl

    def __repr__(self):
        return "<Robot('%s', '%s')>" % (self.robotname, self.listurl)


class Task(Base):
    __tablename__ = 'tasks'

    taskid      = Column(Integer, primary_key=True)
    robotid     = Column(Integer, ForeignKey('robots.robotid'))
    taskname    = Column(String(20), nullable=False)
    loop        = Column(SmallInteger, default=0)
    loopperiod  = Column(Integer, default=86400)
    runtime     = Column(Integer, default=0)
    nextruntime = Column(Integer, default=0)
    dbconn      = Column(Text)
    importSQL   = Column(Text)

    robotinfo = relationship(Robot, backref = backref("tasks", foreign_keys=robotid))

    def __init__(self, robotid, taskname):
        self.robotid   = robotid
        self.taskname  = taskname

    def __repr__(self):
        return "<Task('%s', '%s')>" % (self.robotid, self.taskname)


robots_table = Robot.__table__
tasks_table = Task.__table__

sys_engine = create_engine('sqlite:///sys.db')
Session = scoped_session(sessionmaker(bind=sys_engine))