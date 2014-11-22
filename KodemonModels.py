from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
import os

Base = declarative_base()

#message_base object mapping for the UDP Server, vanilla SQLAlchemy
class UDPMessageBase(Base):
    __tablename__ = 'message_base'

    id = Column(Integer, primary_key=True, nullable=False)
    key = Column(String, nullable=False)
    execution_time = Column(Float, nullable=False)
    timestamp = Column(Integer, nullable=False)
    token = Column(String, nullable=False)

    extensions = relationship('UDPMessageExtension')

class UDPMessageExtension(Base):
    __tablename__ = 'message_extension'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    value = Column(String, nullable=False)
    base_id = Column(Integer, ForeignKey('message_base.id'))


#Models for the Kodemon API to retain the query ability provided by Flask-SQLAlchemy extension
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MessageBase(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	key = db.Column(db.String, nullable=False)
	execution_time = db.Column(db.Float, nullable=False)
	timestamp = db.Column(db.Integer, nullable=False)
	token = db.Column(db.String, nullable=False)
	
	extensions = db.relationship('MessageExtension')

	def __init__(key, execution_time, timestamp, token):
		self.key = key
		self.execution_time = execution_time
		self.timestamp = timestamp
		self.token = token


class MessageExtension(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String, nullable=False)
	type = db.Column(db.String, nullable=False)
	value = db.Column(db.String, nullable=False)
	base_id = db.Column(db.Integer, db.ForeignKey('message_base.id'))
	
	base = db.relationship('MessageBase')

	def __init__(name, type, value):
		self.name = name
		self.type = type
		self.value = value

if __name__ == '__main__':
	if not os.path.exists('AppData'):
		os.mkdir('AppData')

	engine = create_engine('sqlite:///AppData/Kodemon.sqlite')
	Base.metadata.create_all(engine)