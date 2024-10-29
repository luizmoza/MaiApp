
from app import app
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime

class cl_FechamentoFuturo(app.base):
    IDFechamentoFuturo:Mapped[int] = mapped_column(primary_key=True,unique=True)
    idFuturo:Mapped[int]
    Ticker:Mapped[str]
    PuD0:Mapped[float]	
    PuD1:Mapped[float]	
    Variacao:Mapped[float]	
    Ajuste:Mapped[float]	
    PuFechamento:Mapped[float]	
    Data:Mapped[datetime.datetime]	
    __tablename__ = "FechamentoFuturo"
    __table_args__ = {'extend_existing': True}
    __db__ = app.db
    __pk__ = ['IDFechamentoFuturo']
    __nn__ = []
    __nnbl__ = []
    __nnint__ = ['idFuturo']
    __nndbl__ = []
    __nndt__ = ['Data']
    __unics__ = [] 
    __fks__ = {} 

    
    def __init__(self,**kwargs): 
        self.IDFechamentoFuturo = kwargs['IDFechamentoFuturo'] if 'IDFechamentoFuturo' in kwargs else None
        self.idFuturo = kwargs['idFuturo'] if 'idFuturo' in kwargs else None
        self.Ticker = kwargs['Ticker'] if 'Ticker' in kwargs else None
        self.PuD0 = kwargs['PuD0'] if 'PuD0' in kwargs else None
        self.PuD1 = kwargs['PuD1'] if 'PuD1' in kwargs else None
        self.Variacao = kwargs['Variacao'] if 'Variacao' in kwargs else None
        self.Ajuste = kwargs['Ajuste'] if 'Ajuste' in kwargs else None
        self.PuFechamento = kwargs['PuFechamento'] if 'PuFechamento' in kwargs else None
        self.Data = kwargs['Data'] if 'Data' in kwargs else None
        
 #################################################################################################################################################
 #################################################################Métodos Genéricos###############################################################
        
    def __repr__(self): return str(self.__dict__)
    
    def bulk(self,df):
        vv = False
        try:
            df.to_sql(self.__tablename__, self.__db__.engine, if_exists='append', index=False)
            vv = True
            self.__db__.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = f'Failed to query: {repr(e)}'
        return vv  

    def read(self, id):
        vv = True
        try:
            self.__db__.session.expire_all()
            record = self.__db__.session.get(self.__class__,id)
            self.__db__.statusquery = 'Executed'
            if record:
                for key, value in app.tk.ParseObjectDict(record).items():setattr(self, key, value)
            else:
                vv = False
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to query: {repr(e)}'
        return vv

    def get(self): # Usa os dados do próprio objeto
        vv = True
        id = getattr(self,self.__pk__[0])
        try:
            self.__db__.session.expire_all()
            record = self.__db__.session.get(self.__class__,id)
            self.__db__.statusquery = 'Executed'
            if record:
                for key, value in app.tk.ParseObjectDict(record).items():setattr(self, key, value)
            else:
                vv = False
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to query: {repr(e)}'
        return vv

    def create(self,data):
        vv = True
        try:
            newrecord = self.__class__(**data)
            newrecord.__db__.session.add(newrecord)
            newrecord.__db__.session.flush()
            id = getattr(newrecord,newrecord.__pk__[0])
            self.__db__.session.commit()
            setattr(self,self.__pk__[0],id)
            self.__db__.statusquery = 'Inserted successfully'
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to insert: {repr(e)}'
            if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def insert(self): # Usa os dados do próprio objeto
        vv = True
        try:
            self.__db__.session.add(self)
            self.__db__.session.flush()
            id = getattr(self,self.__pk__[0])
            self.__db__.session.commit()
            setattr(self,self.__pk__[0],id)
            self.__db__.statusquery = 'Inserted successfully'
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to insert: {repr(e)}'
            if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def update(self, id, updated_data):
        vv = True
        try:
            record = self.__db__.session.get(self.__class__,id)
            if record:
                for key, value in updated_data.items():setattr(record, key, value)
                self.__db__.session.commit()
                self.__db__.statusquery = 'Updated successfully'
            else:
                self.__db__.statusquery = 'Record not found'
                vv = False
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to update: {repr(e)}'
            if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def set(self): # Usa os dados do próprio objeto
        vv = True
        id = getattr(self,self.__pk__[0])
        data = app.tk.ParseObjectDict(self)
        try:
            record = self.__db__.session.get(self.__class__,id)
            if record:
                for key, value in data.items():setattr(record, key, value)
                self.__db__.session.commit()
                self.__db__.statusquery = 'Updated successfully'
            else:
                self.__db__.statusquery = 'Record not found'
                vv = False
        except Exception as e:
           vv = False
           self.__db__.statusquery = f'Failed to update: {repr(e)}'
           if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def delete(self, id):
        vv = True
        try:
            record = self.__db__.session.get(self.__class__,id)
            if record:
                self.__db__.session.delete(record)
                self.__db__.session.commit()
                self.__db__.statusquery = 'Deleted successfully'
            else:
                self.__db__.statusquery = 'Record not found'
                vv = False
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to delete: {repr(e)}'
            if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def remove(self): # Usa os dados do próprio objeto
        vv = True
        id = getattr(self,self.__pk__[0])
        try:
            record = self.__db__.session.get(self.__class__,id)
            if record:
                self.__db__.session.delete(record)
                self.__db__.session.commit()
                self.__db__.statusquery = 'Deleted successfully'
            else:
                self.__db__.statusquery = 'Record not found'
                vv = False
        except Exception as e:
            vv = False
            self.__db__.statusquery = f'Failed to delete: {repr(e)}'
            if self.__db__.session is not None: self.__db__.session.rollback()
        return vv

    def get_sample_fk(self):
        vv = True
        for k,v in self.__fks__.items():
            try:
                myQuery = """
                select top(1) """ + v + """ from """ + k + """
                """
                dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
                if len(dfresult)>0:
                    setattr(self,v,dfresult[v].iloc[0].item()) 
                    self.__db__.statusquery = 'Executed'
                else:
                    vv = False
                    self.__db__.statusquery = 'Table is empty'
            except Exception as e:
                vv = False  
                self.__db__.statusquery = 'Failed Query: %s', repr(e)
            return vv
        
#################################################################Métodos Génericos#############################################################
###############################################################################################################################################


    def get_id_data_idasset(self):
        vv = False
        try:
            myQuery = """
            select IDFechamentoFuturo from """ + self.__tablename__ + """
            where data = '""" + self.Data.strftime('%Y-%m-%d') + """'
            and idFuturo = """ + str(self.idFuturo) + """
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                self.IDFechamentoFuturo = dfresult['IDFechamentoFuturo'].iloc[0].item() # Item() para tranformar em int nativo python... pandas devolve um numpy
                vv = True
            else:
                self.IDFechamentoFuturo = 0
            self.__db__.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv