from index import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from datetime import datetime


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    given_name = db.Column(db.String(250))
    family_name = db.Column(db.String(250))
    role = db.Column(db.Integer)

    #catalogs = db.relationship("catalog", backref="user")

    def __repr__(self):
        return '["{}","{}","{}","{}","{}"]'.format(self.id,self.email,self.given_name,self.family_name,self.role)


class Catalog(db.Model):
    __tablename__ = 'catalog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(250), default="Draft")
    status2 = db.Column(db.String(250))
    title = db.Column(db.String(250))
    number = db.Column(db.String(250))
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())
    collection = db.Column(db.Boolean)
    publish_r = db.Column(db.Boolean, default=False)
    publish_a = db.Column(db.Boolean, default=False)
    published = db.Column(db.Boolean, default=False)
    archive = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '["{}","{}","{}","{}","{}","{}","{}"."{}","{}","{}","{}","{}","{}"]'.format(self.id,self.user_id,self.status,self.status2, self.title, self.number,
        self.created, self.updated, self.collection, self.publish_r, self.publish_a, self.published, self.archive)

class Meta(db.Model):
     __tablename__ = 'meta'
     id = db.Column(db.Integer,primary_key=True)


     def __repr__(self):
        return '["{}"]'.format(self.id)


class Apikeys(db.Model):
    __tablename__ = 'apikeys'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    api_url = db.Column(db.String(250))
    api_key = db.Column(db.String(250))

    def __repr__(self):
        return '["{}","{}","{}","{}"]'.format(self.id,self.user_id,self.api_url,self.api_key)

