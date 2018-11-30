from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    id        = Column(Integer, primary_key=True)
    username  = Column(String, unique=True)
    email     = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    surname   = Column(String, nullable=False)
    emails    = relationship("Email")
    
    def __init__(self, username=None,email=None,firstname=None,surname=None):
        self.username  = username
        self.email     = email
        self.firstname = firstname
        self.surname   = surname

    def __repr__(self):
        return '{}-{}-{}-{}'.format(self.username,self.email,self.firstname,self.surname)
        
    def toDict(self):
        mydict={}
        mydict["username"]  = self.username
        mydict["email"]     = self.email
        mydict["firstname"] = self.firstname
        mydict["surname"]   = self.surname
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

    def toDict(self):
        mydict={}
        mydict["username"]  = self.username
        mydict["email"]     = self.email
        return mydict

    def toJson(self):
        import json
        return json.dumps(self.toDict())
        
#    owner_id = Column(Integer, ForeigKey('contact.id')
#    owner    = relationship(Contact, back_populates="emails") 
