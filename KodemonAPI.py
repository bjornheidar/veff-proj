from flask import Flask, abort, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from KodemonModels import db, MessageBase, MessageExtension
import json, sys, getopt


class KodemonAPI():
	def __init__(self, SERVER_NAME='localhost:4000', db_conn_string='sqlite:///AppData/Kodemon.sqlite'):
		self.app = Flask(__name__)
		#self.app.debug = True

		self.app.config['SERVER_NAME'] = SERVER_NAME
		
		self.app.config['SQLALCHEMY_DATABASE_URI'] = db_conn_string
		self.db = db
		
		self.db.init_app(self.app)
		self.set_routes()

	def run(self):
		self.app.run()

	def set_routes(self):
		@self.app.route("/", methods=['GET'])
		def index():
			return self.app.send_static_file('index.html')


		api_prefix = '/api/v1'

		@self.app.route(api_prefix + '/keys/', methods=['GET'])
		def keys():
			result = []
			for m in MessageBase.query.all():
				if m.key not in result:
					result.append(m.key)

			return json.dumps(result)

		@self.app.route(api_prefix + '/keys/<key>/execution_times/', methods=['GET'])
		def execution_times(key):
			#get query parameters (may be None)
			start_time, end_time = request.args.get('start_time'), request.args.get('end_time')

			if start_time:
				start_time = int(start_time)
			else:
				start_time = 0

			if end_time:
				end_time = int(end_time)
			else:
				end_time = sys.maxint

			#Get execution times
			times = []
			for m in MessageBase.query.filter_by(key=key):
				if start_time <= m.timestamp <= end_time:
					times.append({'execution_time': m.execution_time, 'timestamp': m.timestamp, 'token': m.token})

			result = {'key': key, 'execution_times': times}
			print result
			return json.dumps(result)



if __name__ == '__main__':
	api = KodemonAPI()
	api.run()
