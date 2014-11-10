from SocketServer import UDPServer, BaseRequestHandler
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from KodemonModels import UDPMessageBase, UDPMessageExtension

class KodemonUDPHandler(BaseRequestHandler):
    def handle(self):
        #Get the request data and decode to json
        data = self.request[0].strip()
        jdat = json.loads(data)

        #create message_base to add to database
        msg_base = UDPMessageBase(key=jdat['key'], 
            execution_time=jdat['execution_time'], 
            timestamp=jdat['timestamp'], 
            token=jdat['token']
            )

        #create message_extened to add to the database
        

        #start session/connect to db
        session = self.server.Session()

        #insert and commit
        session.add(msg_base)
        session.commit()

class KodemonUDPServer(UDPServer):
    def __init__(self, HOST='localhost', PORT=4000, handler=KodemonUDPHandler, db_conn_string='sqlite:///AppData/Kodemon.sqlite'):
        #Set up the server
        UDPServer.__init__(self, (HOST, PORT), handler)

        #Set up the database connection
        engine = create_engine(db_conn_string, echo=True)
        self.Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    print 'Starting Kodemon UPD Server'
    server = KodemonUDPServer()
    server.serve_forever()
