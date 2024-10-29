
from app import app
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime

class cl_FechamentoRF(app.base):
    IDFechamentoRF:Mapped[int] = mapped_column(primary_key=True,unique=True)
    idRF:Mapped[int]
    Data:Mapped[datetime.datetime]
    aliasoperacao:Mapped[str]	
    Codigo:Mapped[str]	
    TaxaCompra:Mapped[float]	
    TaxaVenda:Mapped[float]	
    TaxaMinima:Mapped[float]	
    TaxaMaxima:Mapped[float]	
    TaxaIndicativa:Mapped[float]	
    Pu:Mapped[float]	
    PuMin:Mapped[float]	
    PuMax:Mapped[float]	
    Volume:Mapped[float]	
    PuPar:Mapped[float]	
    Duration:Mapped[float]	
    Convexidade:Mapped[float]	
    TipoFechamento:Mapped[str]
    IndiceCorrecao:Mapped[str]	
    __tablename__ = "FechamentoRF"
    __table_args__ = {'extend_existing': True}
    __db__ = app.db
    __pk__ = ['IDFechamentoRF']
    __nn__ = ['Codigo']
    __nnbl__ = []
    __nnint__ = []
    __nndbl__ = []
    __nndt__ = ['Data']
    __unics__ = [] 
    __fks__ = {} 

    def __init__(self,**kwargs): 
        self.IDFechamentoRF = kwargs['IDFechamentoRF'] if 'IDFechamentoRF' in kwargs else None
        self.idRF = kwargs['idRF'] if 'idRF' in kwargs else None
        self.Data = kwargs['Data'] if 'Data' in kwargs else None
        self.aliasoperacao = kwargs['aliasoperacao'] if 'aliasoperacao' in kwargs else None
        self.Codigo = kwargs['Codigo'] if 'Codigo' in kwargs else None
        self.TaxaCompra = kwargs['TaxaCompra'] if 'TaxaCompra' in kwargs else None
        self.TaxaVenda = kwargs['TaxaVenda'] if 'TaxaVenda' in kwargs else None
        self.TaxaMinima = kwargs['TaxaMinima'] if 'TaxaMinima' in kwargs else None	
        self.TaxaMaxima = kwargs['TaxaMaxima'] if 'TaxaMaxima' in kwargs else None
        self.TaxaIndicativa = kwargs['TaxaIndicativa'] if 'TaxaIndicativa' in kwargs else None
        self.Pu = kwargs['Pu'] if 'Pu' in kwargs else None
        self.PuMin = kwargs['PuMin'] if 'PuMin' in kwargs else None
        self.PuMax = kwargs['PuMax'] if 'PuMax' in kwargs else None	
        self.Volume = kwargs['Volume'] if 'Volume' in kwargs else None
        self.PuPar = kwargs['PuPar'] if 'PuPar' in kwargs else None
        self.Duration = kwargs['Duration'] if 'Duration' in kwargs else None
        self.Convexidade = kwargs['Convexidade'] if 'Convexidade' in kwargs else None
        self.TipoFechamento = kwargs['TipoFechamento'] if 'TipoFechamento' in kwargs else None
        self.IndiceCorrecao = kwargs['IndiceCorrecao'] if 'IndiceCorrecao' in kwargs else None       


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





    def get_id_data_idasset(self,db):
        vv = False
        try:
            myQuery = """
            select IDFechamentoRF from """ + self.__tablename__ + """
            where data = '""" + self.data.strftime('%Y-%m-%d') + """'
            and idRF = """ + str(self.idRF) + """
            """
            dfresult = app.pd.read_sql_query(myQuery, db.engine)
            if len(dfresult)>0:
                self.IDFechamentoRF = dfresult['IDFechamentoRF'].iloc[0].item() # Item() para tranformar em int nativo python... pandas devolve um numpy
                vv = True
            else:
                self.IDFechamentoRF = 0
            db.statusquery = 'Executed'
        except Exception as e:
            db.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv