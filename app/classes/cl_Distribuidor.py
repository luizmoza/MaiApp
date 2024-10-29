
from app import app
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class cl_Distribuidor(app.base):
    IDDistribuidor:Mapped[int] = mapped_column(primary_key=True,unique=True)
    Nome:Mapped[str]	
    CGC:Mapped[str]	
    Conta1Banco:Mapped[str]	
    Conta1Agencia:Mapped[str]	
    Conta1Conta:Mapped[str]	
    Conta2Banco:Mapped[str]	
    Conta2Agencia:Mapped[str]	
    Conta2Conta:Mapped[str]	
    Conta3Banco:Mapped[str]	
    Conta3Agencia:Mapped[str]
    Conta3Conta:Mapped[str]
    CodigoBradesco:Mapped[str]
    RazaoSocial:Mapped[str]
    __tablename__ = "Distribuidor"
    __table_args__ = {'extend_existing': True}
    __db__ = app.db
    __pk__ = ['IDDistribuidor']
    __nn__ = ['Nome','CGC']
    __nnbl__ = []
    __nnint__ = []
    __nndbl__ = []
    __nndt__ = []
    __unics__ = [] 
    __fks__ = {} 

    def __init__(self,**kwargs):
        self.IDDistribuidor = kwargs['IDDistribuidor'] if 'IDDistribuidor' in kwargs else None
        self.Nome = kwargs['Nome'] if 'Nome' in kwargs else None
        self.CGC = kwargs['CGC'] if 'CGC' in kwargs else None	
        self.Conta1Banco = kwargs['Conta1Banco'] if 'Conta1Banco' in kwargs else None
        self.Conta1Agencia = kwargs['Conta1Agencia'] if 'Conta1Agencia' in kwargs else None
        self.Conta1Conta = kwargs['Conta1Conta'] if 'Conta1Conta' in kwargs else None
        self.Conta2Banco = kwargs['Conta2Banco'] if 'Conta2Banco' in kwargs else None	
        self.Conta2Agencia = kwargs['Conta2Agencia'] if 'Conta2Agencia' in kwargs else None
        self.Conta2Conta = kwargs['Conta2Conta'] if 'Conta2Conta' in kwargs else None	
        self.Conta3Banco = kwargs['Conta3Banco'] if 'Conta3Banco' in kwargs else None	
        self.Conta3Agencia = kwargs['Conta3Agencia'] if 'Conta3Agencia' in kwargs else None
        self.Conta3Conta = kwargs['Conta3Conta'] if 'Conta3Conta' in kwargs else None
        self.CodigoBradesco = kwargs['CodigoBradesco'] if 'CodigoBradesco' in kwargs else None
        self.RazaoSocial = kwargs['RazaoSocial'] if 'RazaoSocial' in kwargs else None
        

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


    def get_id_by_Nome(self):
        vv = False
        try:
            myQuery = """
            select IDDistribuidor from """ + self.__tablename__ + """
            where Nome = '""" + self.Nome + """'
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                self.IDDistribuidor = dfresult['IDDistribuidor'].iloc[0].item() # Item() para tranformar em int nativo python... pandas devolve um numpy
                vv = True
            else:
                self.IDDistribuidor = 0
            self._db_.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv