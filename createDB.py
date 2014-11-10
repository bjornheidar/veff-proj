from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData
import os

if not os.path.exists('AppData'):
	os.mkdir('AppData')

engine = create_engine('sqlite:///AppData/Kodemon.sqlite')
connection = engine.connect()

metadata = MetaData()

message_base = Table('message_base', metadata,
	Column('id', Integer, primary_key=True),
	Column('key', String, nullable=False),
	Column('execution_time', Float, nullable=False),
	Column('timestamp', Integer, nullable=False),
	Column('token', String, nullable=False)
)

metadata.create_all(engine)

connection.close()