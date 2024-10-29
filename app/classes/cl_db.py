from app import app
from sqlalchemy.orm import sessionmaker as sessionmaker

class cl_db:
    def __init__(self):
        self.server = app.server
        self.database = app.database
        self.usr = app.usr
        self.pwd = app.pwd
        self.params = app.params
        self.statusquery = ''
        self.engine = app.engine
        self.base = app.base
        self.session = None
        self.conn = None
        self.cursor = None
        self.last_error = None
        self.status = 'not Connected'
    
    def Session_Start(self):
        self.session = sessionmaker(bind=self.engine,autoflush=True)()

    def Session_Close(self):
        self.engine.dispose()
        
    def connect(self):
        vv = False
        try:
            if self.conn is None:
                self.engine = app.engine
                self.conn = self.engine.raw_connection()
                self.cursor = self.conn.cursor()
            else:
                if self.isConnected() == False:
                    self.engine = app.engine
                    self.conn = self.engine.raw_connection()
                    self.cursor = self.conn.cursor()
            vv = True
            self.statusquery = 'Connected'
        except Exception as e: 
            self.statusquery = 'Failed to Connect : %s', repr(e)
        return vv

    def isConnected(self):
        vv = False
        if self.conn is not None:
            try:
                vv = self.conn.cursor()
                vv = True
                self.statusquery = 'Tested Connection!'
            except Exception as e: 
                self.statusquery = 'Connection Failed : %s', repr(e)
                vv = False
        return vv    

    def drop(self):
        vv = False
        if self.isConnected():
            self.conn.close()
            self.conn = None
            self.cursor = None
        vv = True
        return vv
            
    def execQuery(self,query,args):
        vv = False
        if self.connect():
                try:
                    self.cursor.execute(query, args)
                    self.conn.commit()
                    self.drop()
                    vv = True
                    self.statusquery = 'Query Succeeded'
                except Exception as e:
                    self.conn.rollback()
                    self.statusquery = 'Failed Query: %s', repr(e)
                    self.drop()
        else:
          self.statusquery = 'Connection Failed'
        return vv

    def execRawQuery(self,query):
        vv = False
        if self.connect():
                try:
                    self.cursor.execute(query)
                    self.conn.commit()
                    self.drop()
                    vv = True
                    self.statusquery = 'Query Succeeded'
                except Exception as e:
                    self.conn.rollback()
                    self.statusquery = 'Failed Query: %s', repr(e)
                    self.drop()
        else:
          self.statusquery = 'Connection Failed'
        return vv
    
    def loadDf(self,query):
        result = app.pd.DataFrame.from_dict({})
        if self.connect():
          result = app.pd.read_sql(query,self.conn)
          self.drop()
        return result
        

