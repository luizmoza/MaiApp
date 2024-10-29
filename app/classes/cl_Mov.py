from app import app
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime #

class cl_Mov(app.base):
    IDMov:Mapped[int]= mapped_column(primary_key=True,unique=True)	
    DataMov:Mapped[datetime.datetime]		
    AliasAtivo:Mapped[str] 	
    AliasOperacao:Mapped[str] 
    Qtd:Mapped[float] 		
    Pu:Mapped[float] 	
    Taxa:Mapped[float] 
    CGC:Mapped[str] 
    idTrader:Mapped[int]
    idCorretora:Mapped[int]	
    idEstrategia:Mapped[int]
    idpassivo:Mapped[int]
    idReferenciaCompromisso:Mapped[int]
    TipoCompromisso:Mapped[str] 
    DataCotizacao:Mapped[datetime.datetime]	
    DataLiquidacao:Mapped[datetime.datetime]	
    DataCompromisso:Mapped[datetime.datetime]	
    PuCompromisso:Mapped[float] 	
    UltimoAlterador:Mapped[str] 	
    DataLog:Mapped[datetime.datetime]		
    TipoBoleta:Mapped[str] 	
    Corretagem:Mapped[float] 	
    Grupo:Mapped[str] 
    Marcacao:Mapped[str] 
    __tablename__ = "Mov"
    __table_args__ = {'extend_existing': True}
    __db__ = app.db
    __pk__ = ['IDMov']
    __nn__ = ['AliasAtivo']
    __nnbl__ = []
    __nnint__ = ['idTrader']
    __nndbl__ = ['Qtd']
    __nndt__ = ['DataMov']
    __unics__ = [] 
    __fks__ = {} 

    
    def __init__(self,**kwargs): 
        self.IDMov = kwargs['IDMov'] if 'IDMov' in kwargs else None
        self.DataMov = kwargs['DataMov'] if 'DataMov' in kwargs else None	
        self.AliasAtivo = kwargs['AliasAtivo'] if 'AliasAtivo' in kwargs else None 	
        self.AliasOperacao = kwargs['AliasOperacao'] if 'AliasOperacao' in kwargs else None
        self.Qtd = kwargs['Qtd'] if 'Qtd' in kwargs else None		
        self.Pu = kwargs['Pu'] if 'Pu' in kwargs else None	
        self.Taxa = kwargs['Taxa'] if 'Taxa' in kwargs else None
        self.CGC = kwargs['CGC'] if 'CGC' in kwargs else None
        self.idTrader = kwargs['idTrader'] if 'idTrader' in kwargs else None
        self.idCorretora = kwargs['idCorretora'] if 'idCorretora' in kwargs else None
        self.idEstrategia = kwargs['idEstrategia'] if 'idEstrategia' in kwargs else None
        self.idpassivo = kwargs['idpassivo'] if 'idpassivo' in kwargs else None
        self.idReferenciaCompromisso = kwargs['idReferenciaCompromisso'] if 'idReferenciaCompromisso' in kwargs else None
        self.TipoCompromisso = kwargs['TipoCompromisso'] if 'TipoCompromisso' in kwargs else None
        self.DataCotizacao = kwargs['DataCotizacao'] if 'DataCotizacao' in kwargs else None
        self.DataLiquidacao = kwargs['DataLiquidacao'] if 'DataLiquidacao' in kwargs else None	
        self.DataCompromisso = kwargs['DataCompromisso'] if 'DataCompromisso' in kwargs else None	
        self.PuCompromisso = kwargs['PuCompromisso'] if 'PuCompromisso' in kwargs else None	
        self.UltimoAlterador = kwargs['UltimoAlterador'] if 'UltimoAlterador' in kwargs else None	
        self.DataLog = kwargs['DataLog'] if 'DataLog' in kwargs else None		
        self.TipoBoleta = kwargs['TipoBoleta'] if 'TipoBoleta' in kwargs else None
        self.Corretagem = kwargs['Corretagem'] if 'Corretagem' in kwargs else None	
        self.Grupo = kwargs['Grupo'] if 'Grupo' in kwargs else None
        self.Marcacao = kwargs['Marcacao'] if 'Marcacao' in kwargs else None

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


    def get_sample(self):
        vv = True
        try:
            myQuery = """
            select top(1) """ + self.__pk__[0] + """ from """ + self.__tablename__ + """
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                setattr(self,self.__pk__[0],dfresult[self.__pk__[0]].iloc[0].item()) 
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



    def LoadListaAtivos(self,request):
        sql = "select 'Erro!' as Nome"
        if (request.form['TipoAtivo']=="RF"): sql = "select Nome from tiporf order by Nome asc"
        elif (request.form['TipoAtivo']=="RV"): sql = "select Nome from tipoRV order by Nome asc"
        elif (request.form['TipoAtivo']=="Futuro"): sql = "select NomeTipoMercadoriaFuturo as Nome from TipoMercadoriaFuturo order by NomeTipoMercadoriaFuturo asc"
        elif (request.form['TipoAtivo']=="Opcao"): sql = "select NomeTipoMercadoriaOpcao as Nome from TipoMercadoriaOpcao order by NomeTipoMercadoriaOpcao asc"
        elif (request.form['TipoAtivo']=="Cota"): sql = "select distinct segmento as Nome from fundo order by segmento asc"
        elif (app.request.form['TipoAtivo']=="Swap"): sql = "select 'Swap' as Nome"
        return self.__db__.loadDf(sql)
    
    
    def get_id_TipoCompromisso(self):
        vv = False
        try:
            myQuery = """
            select IDMov from """ + self.__tablename__ + """
            where TipoCompromisso = '""" + self.TipoCompromisso + """'
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                self.IDMov = dfresult['IDMov'].iloc[0].item() # Item() para tranformar em int nativo python... pandas devolve um numpy
                vv = True
            else:
                self.IDMov = 0
            self._db_.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv