from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, Boolean
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import backref, relationship
from datetime import datetime
from database import Base

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False, unique=True)
    given_name = Column(String(250))
    family_name = Column(String(250))
    role = Column(Integer)

    #catalogs = relationship("catalog", backref="user")

    def __repr__(self):
        return '["{}","{}","{}","{}","{}"]'.format(self.id,self.email,self.given_name,self.family_name,self.role)


class Catalog(Base):
    __tablename__ = 'catalog'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(250), default="Draft")
    status2 = Column(String(250))
    title = Column(String(250))
    number = Column(String(250))
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())
    collection = Column(Boolean)
    publish_r = Column(Boolean, default=False)
    publish_a = Column(Boolean, default=False)
    published = Column(Boolean, default=False)
    archive = Column(Boolean, default=False)


    def __repr__(self):
        return '["{}","{}","{}","{}","{}","{}","{}"."{}","{}","{}","{}","{}","{}"]'.format(self.id,self.user_id,self.status,self.status2, self.title, self.number,
        self.created, self.updated, self.collection, self.publish_r, self.publish_a, self.published, self.archive)

class Meta(Base):
     __tablename__ = 'meta'
     id = Column(Integer,primary_key=True)


     def __repr__(self):
        return '["{}"]'.format(self.id)


class Apikeys(Base):
    __tablename__ = 'apikeys'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    api_url = Column(String(250))
    api_key = Column(String(250))

    def __repr__(self):
        return '["{}","{}","{}","{}"]'.format(self.id,self.user_id,self.api_url,self.api_key)

