from app import app
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from app.classes.cl_Fundo import cl_Fundo
from app.classes.cl_CodRefCotistaFundo import cl_CodRefCotistaFundo

import datetime

class cl_Passivo(app.base):
    IDPassivo:Mapped[int]= mapped_column(primary_key=True,unique=True)	
    Tipo:Mapped[str] 
    QtdCotas:Mapped[float]
    Cota:Mapped[float]
    Fin:Mapped[float]
    idFundo:Mapped[int]
    DataMovimentacao:Mapped[datetime.datetime]
    DataCotizacao:Mapped[datetime.datetime]	
    DataLiquidacao:Mapped[datetime.datetime]
    TipoLiquidacao:Mapped[str] 
    idCodRefCotistaFundo:Mapped[int]
    Criador:Mapped[str] 
    Aprovador:Mapped[str] 
    DataLog:Mapped[datetime.datetime]	
    refidMov:Mapped[int]
    Up_Load:Mapped[str] 
    __tablename__ = "Passivo"
    __table_args__ = {'extend_existing': True}
    __db__ = app.db
    __pk__ = ['IDPassivo']
    __nn__ = ['Tipo']
    __nnbl__ = []
    __nnint__ = []
    __nndbl__ = []
    __nndt__ = []
    __unics__ = [] 
    __fks__ = {'CodRefCotistaFundo':'idCodRefCotistaFundo','Fundo':'idFundo'} 
        
    def __init__(self,**kwargs): 
        self.IDPassivo = kwargs['IDPassivo'] if 'IDPassivo' in kwargs else None	
        self.Tipo = kwargs['Tipo'] if 'Tipo' in kwargs else None
        self.QtdCotas = kwargs['QtdCotas'] if 'QtdCotas' in kwargs else None
        self.Cota = kwargs['Cota'] if 'Cota' in kwargs else None
        self.Fin = kwargs['Fin'] if 'Fin' in kwargs else None
        self.idFundo = kwargs['idFundo'] if 'idFundo' in kwargs else None
        self.DataMovimentacao = kwargs['DataMovimentacao'] if 'DataMovimentacao' in kwargs else None
        self.DataCotizacao = kwargs['DataCotizacao'] if 'DataCotizacao' in kwargs else None
        self.DataLiquidacao = kwargs['DataLiquidacao'] if 'DataLiquidacao' in kwargs else None
        self.TipoLiquidacao = kwargs['TipoLiquidacao'] if 'TipoLiquidacao' in kwargs else None
        self.idCodRefCotistaFundo = kwargs['idCodRefCotistaFundo'] if 'idCodRefCotistaFundo' in kwargs else None
        self.Criador = kwargs['Criador'] if 'Criador' in kwargs else None
        self.Aprovador = kwargs['Aprovador'] if 'Aprovador' in kwargs else None
        self.DataLog = kwargs['DataLog'] if 'DataLog' in kwargs else None
        self.refidMov = kwargs['refidMov'] if 'refidMov' in kwargs else None
        self.Up_Load = kwargs['Up_Load'] if 'Up_Load' in kwargs else None


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


    def get_id_Aprovador(self):
        vv = False
        try:
            myQuery = """
            select IDPassivo from """ + self.__tablename__ + """
            where Aprovador = '""" + self.Aprovador + """'
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                self.IDPassivo = dfresult['IDPassivo'].iloc[0].item() # Item() para tranformar em int nativo python... pandas devolve um numpy
                vv = True
            else:
                self.IDPassivo = 0
            self._db_.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv