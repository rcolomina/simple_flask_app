import datetime,time

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.types import DateTime

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    id        = Column(Integer, primary_key=True)
    username  = Column(String, unique=True)
    email     = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    surname   = Column(String, nullable=False)
    emails    = relationship("Email")
    creationDateTime = Column(DateTime,
                              default=datetime.datetime.utcnow(),
                              nullable=False)
        
    def __init__(self, username=None,email=None,firstname=None,surname=None):
        self.username  = username
        self.email     = email
        self.firstname = firstname
        self.surname   = surname        
        self.creationDateTime = datetime.datetime.utcnow()
        
    def __repr__(self):
        return '{}-{}-{}-{}-{}'.format(self.username,  self.email,
                                       self.firstname, self.surname,
                                       self.creationDateTime)
    def toDict(self):
        mydict={}
        mydict["username"]  = self.username
        mydict["email"]     = self.email
        mydict["firstname"] = self.firstname
        mydict["surname"]   = self.surname
        mydict["creationDateTime"]   = time.mktime(self.creationDateTime.timetuple())
        return mydict
        
    def toJson(self):
        import json
        return json.dumps(self.toDict())

class Email(Base):
    __tablename__ = 'emails'
    id       = Column(Integer, primary_key=True)
    email    = Column(String, nullable=False)
    username = Column(String, ForeignKey('contacts.id'))
    
    def __init__(self, username=None,email=None):
        self.username  = username
        self.email     = email
        
    def __repr__(self):
        return '{}-{}'.format(self.username,self.email)
    
    def toDict(self):
        mydict={}
        mydict["username"]  = self.username
        mydict["email"]     = self.email
        return mydict

    def toJson(self):
        import json
        return json.dumps(self.toDict())
        
