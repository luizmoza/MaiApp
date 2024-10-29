
from app import app
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime

class cl_Opcao(app.base):
    IDOpcao:Mapped[int] = mapped_column(primary_key=True,unique=True)
    Alias:Mapped[str]
    Isin:Mapped[str]	
    Codigo:Mapped[str]	
    PrecoExercicio:Mapped[float]	
    IdMoedaPrecoExercicio:Mapped[int]
    CodVencimento:Mapped[str]	
    CodClassificarInstrumento:Mapped[str]
    TipoOpcao:Mapped[str]	
    TipoEstilo:Mapped[str]
    MultiplicadorContrato:Mapped[float]	
    Quantidade:Mapped[float]		
    LoteAlocacao:Mapped[float]	
    PremioPagoAntecip:Mapped[str]
    idBolsa:Mapped[int]
    idMoeda:Mapped[int]
    IdTipoMercadoriaOpcao:Mapped[int]
    DataVencimento:Mapped[datetime.datetime]		
    DatainicioNegociacao:Mapped[datetime.datetime]	
    DataConclusaoNegociacao:Mapped[datetime.datetime]	
    DataPosicaoAberto:Mapped[datetime.datetime]	
    __tablename__ = "Opcao"
    __table_args__ = {'extend_existing': True}
    __db__ = app.db
    __pk__ = ['IDOpcao']
    __nn__ = ['Codigo','Alias']
    __nnbl__ = []
    __nnint__ = []
    __nndbl__ = []
    __nndt__ = []
    __unics__ = [] 
    __fks__ = {} 

    def __init__(self,**kwargs): 
        self.IDOpcao = kwargs['IDOpcao'] if 'IDOpcao' in kwargs else None
        self.Alias = kwargs['Alias'] if 'Alias' in kwargs else None
        self.Isin = kwargs['Isin'] if 'Isin' in kwargs else None	
        self.Codigo = kwargs['Codigo'] if 'Codigo' in kwargs else None
        self.PrecoExercicio = kwargs['PrecoExercicio'] if 'PrecoExercicio' in kwargs else None
        self.IdMoedaPrecoExercicio = kwargs['IdMoedaPrecoExercicio'] if 'IdMoedaPrecoExercicio' in kwargs else None
        self.CodVencimento = kwargs['CodVencimento'] if 'CodVencimento' in kwargs else None
        self.CodClassificarInstrumento = kwargs['CodClassificarInstrumento'] if 'CodClassificarInstrumento' in kwargs else None
        self.TipoOpcao = kwargs['TipoOpcao'] if 'TipoOpcao' in kwargs else None
        self.TipoEstilo = kwargs['TipoEstilo'] if 'TipoEstilo' in kwargs else None
        self.MultiplicadorContrato = kwargs['MultiplicadorContrato'] if 'MultiplicadorContrato' in kwargs else None
        self.Quantidade = kwargs['Quantidade'] if 'Quantidade' in kwargs else None	
        self.LoteAlocacao = kwargs['LoteAlocacao'] if 'LoteAlocacao' in kwargs else None
        self.PremioPagoAntecip = kwargs['PremioPagoAntecip'] if 'PremioPagoAntecip' in kwargs else None
        self.idBolsa = kwargs['idBolsa'] if 'idBolsa' in kwargs else None
        self.idMoeda = kwargs['idMoeda'] if 'idMoeda' in kwargs else None
        self.IdTipoMercadoriaOpcao = kwargs['IdTipoMercadoriaOpcao'] if 'IdTipoMercadoriaOpcao' in kwargs else None
        self.DataVencimento = kwargs['DataVencimento'] if 'DataVencimento' in kwargs else None		
        self.DatainicioNegociacao = kwargs['DatainicioNegociacao'] if 'DatainicioNegociacao' in kwargs else None
        self.DataConclusaoNegociacao = kwargs['DataConclusaoNegociacao'] if 'DataConclusaoNegociacao' in kwargs else None
        self.DataPosicaoAberto = kwargs['DataPosicaoAberto'] if 'DataPosicaoAberto' in kwargs else None        
      
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

    def get_id_alias(self):
        vv = False
        try:
            myQuery = """
            select IDOpcao from """ + self.__tablename__ + """
            where alias = '""" + self.Alias + """'
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                self.IDOpcao = dfresult['IDOpcao'].iloc[0].item() # Item() para tranformar em int nativo python... pandas devolve um numpy
                vv = True
            else:
                self.IDOpcao = 0
            self.__db__.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv