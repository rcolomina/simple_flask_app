from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    id        = Column(Integer, primary_key=True)
    username  = Column(String, unique=True)
    email     = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    surname   = Column(String, nullable=False)

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




#class Email(Base):
#    __tablename__ =
