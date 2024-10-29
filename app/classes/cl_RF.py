
from app import app
from sqlalchemy import orm
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from copy import copy
import datetime

class cl_RF(app.base):
    IDRF:Mapped[int]= mapped_column(primary_key=True,unique=True)		
    Alias:Mapped[str]
    Codigo:Mapped[str]	
    Isin:Mapped[str]
    Situacao:Mapped[str]	
    TipoEmissao:Mapped[str]	
    Garantia:Mapped[str]	
    Classe:Mapped[str]
    Qtd:Mapped[float]		
    QtdEmitida:Mapped[float]	
    ValorNominalEmissao:Mapped[float]	
    ValorNominalAtual:Mapped[float]	
    Indice:Mapped[str]
    TipoCorrecao:Mapped[str]
    DUouDC:Mapped[str]
    PercIndice:Mapped[float]	
    AgenteFiduciario:Mapped[str]	
    CoordenadorLider:Mapped[str]	
    Incentivada:Mapped[bool]
    ResgateAntecipado:Mapped[bool]
    idBolsa:Mapped[int]	
    idMoeda:Mapped[int]	
    idEmissor:Mapped[int]	
    idTipoRF:Mapped[int]	
    Vencimento:Mapped[datetime.datetime]
    Carencia:Mapped[datetime.datetime]	
    CarenciaJuros:Mapped[datetime.datetime]
    Emissao:Mapped[datetime.datetime]	
    AditivoIndice:Mapped[float]	
    EmDefault:Mapped[bool]	
    Indexacao:Mapped[str]
    IncorporaJuros:Mapped[bool]
    DataInicioRentabilidade:Mapped[datetime.datetime]	
    DefasagemIndice:Mapped[int]
    DiasAno:Mapped[int]
    RegistroCVM:Mapped[bool]	
    Coobrigacao:Mapped[bool]	
    RatingEmissao:Mapped[str]
    AgenciaRatingEmissao:Mapped[str]
    RatingEmissaoMAI:Mapped[str]	
    __tablename__ = "RF"
    __table_args__ = {'extend_existing': True}
    __db__ = app.db
    __pk__ = ['IDRF']
    __nn__ = ['Alias','Codigo']
    __nnbl__ = ['ResgateAntecipado','Incentivada']
    __nnint__ = []
    __nndbl__ = []
    __nndt__ = []
    __unics__ = [] 
    __fks__ = {} 
    
    def __init__(self,**kwargs): 
        self.IDRF = kwargs['IDRF'] if 'IDRF' in kwargs else None		
        self.Alias = kwargs['Alias'] if 'Alias' in kwargs else None	
        self.Codigo = kwargs['Codigo'] if 'Codigo' in kwargs else None	
        self.Isin = kwargs['Isin'] if 'Isin' in kwargs else None	
        self.Situacao = kwargs['Situacao'] if 'Situacao' in kwargs else None	
        self.TipoEmissao = kwargs['TipoEmissao'] if 'TipoEmissao' in kwargs else None	
        self.Garantia = kwargs['Garantia'] if 'Garantia' in kwargs else None	
        self.Classe = kwargs['Classe'] if 'Classe' in kwargs else None	
        self.Qtd = kwargs['Qtd'] if 'Qtd' in kwargs else None		
        self.QtdEmitida = kwargs['QtdEmitida'] if 'QtdEmitida' in kwargs else None		
        self.ValorNominalEmissao = kwargs['ValorNominalEmissao'] if 'ValorNominalEmissao' in kwargs else None	
        self.ValorNominalAtual = kwargs['ValorNominalAtual'] if 'ValorNominalAtual' in kwargs else None		
        self.Indice = kwargs['Indice'] if 'Indice' in kwargs else None	
        self.TipoCorrecao = kwargs['TipoCorrecao'] if 'TipoCorrecao' in kwargs else None	
        self.DUouDC = kwargs['DUouDC'] if 'DUouDC' in kwargs else None	
        self.PercIndice = kwargs['PercIndice'] if 'PercIndice' in kwargs else None	
        self.AgenteFiduciario = kwargs['AgenteFiduciario'] if 'AgenteFiduciario' in kwargs else None		
        self.CoordenadorLider = kwargs['CoordenadorLider'] if 'CoordenadorLider' in kwargs else None	
        self.Incentivada = kwargs['Incentivada'] if 'Incentivada' in kwargs else None	
        self.ResgateAntecipado = kwargs['ResgateAntecipado'] if 'ResgateAntecipado' in kwargs else None	
        self.idBolsa = kwargs['idBolsa'] if 'idBolsa' in kwargs else None	
        self.idMoeda = kwargs['idMoeda'] if 'idMoeda' in kwargs else None		
        self.idEmissor = kwargs['idEmissor'] if 'idEmissor' in kwargs else None	
        self.idTipoRF = kwargs['idTipoRF'] if 'idTipoRF' in kwargs else None	
        self.Vencimento = kwargs['Vencimento'] if 'Vencimento' in kwargs else None	
        self.Carencia = kwargs['Carencia'] if 'Carencia' in kwargs else None	
        self.CarenciaJuros = kwargs['CarenciaJuros'] if 'CarenciaJuros' in kwargs else None	
        self.Emissao = kwargs['Emissao'] if 'Emissao' in kwargs else None	
        self.AditivoIndice = kwargs['AditivoIndice'] if 'AditivoIndice' in kwargs else None		
        self.EmDefault = kwargs['EmDefault'] if 'EmDefault' in kwargs else None	
        self.Indexacao = kwargs['Indexacao'] if 'Indexacao' in kwargs else None	
        self.IncorporaJuros = kwargs['IncorporaJuros'] if 'IncorporaJuros' in kwargs else None	
        self.DataInicioRentabilidade = kwargs['DataInicioRentabilidade'] if 'DataInicioRentabilidade' in kwargs else None	
        self.DefasagemIndice = kwargs['DefasagemIndice'] if 'DefasagemIndice' in kwargs else None	
        self.DiasAno = kwargs['DiasAno'] if 'DiasAno' in kwargs else None	
        self.RegistroCVM = kwargs['RegistroCVM'] if 'RegistroCVM' in kwargs else None	
        self.Coobrigacao = kwargs['Coobrigacao'] if 'Coobrigacao' in kwargs else None	
        self.RatingEmissao = kwargs['RatingEmissao'] if 'RatingEmissao' in kwargs else None	
        self.AgenciaRatingEmissao = kwargs['AgenciaRatingEmissao'] if 'AgenciaRatingEmissao' in kwargs else None	
        self.RatingEmissaoMAI = kwargs['RatingEmissaoMAI'] if 'RatingEmissaoMAI' in kwargs else None	


    @orm.reconstructor 
    def init_on_load(self): # Construtor usando ORM
        self.Eventos = []

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



    def insert_full(self):
        vv = True
        try:
            aux = copy(self)
            data = app.tk.ParseNewObjectDict(aux)
            aux = self.__class__(**data)
            self.__db__.session.add(aux)
            self.__db__.session.flush()
            id = getattr(self,self.__pk__[0])
            self.__db__.session.commit()
            setattr(self,self.__pk__[0],id)
            self.__db__.statusquery = 'Inserted successfully'            
            
            if not self.clear_db_events(): vv == False
            if not self.insert_events(): vv == False
        except Exception as e:
            self.__db__.session.rollback()
            self.__db__.statusquery = f'Failed to delete: {repr(e)}'
            vv = False
        return vv
        



    def get_id_alias(self):
        vv = False
        try:
            myQuery = """
            select IDRF from """ + self.__tablename__ + """
            where alias = '""" + self.Alias + """'
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                self.IDRF = dfresult['IDRF'].iloc[0].item() # Item() para tranformar em int nativo python... pandas devolve um numpy
                vv = True
            else:
                self.IDRF = 0
            self.__db__.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv

    def get_events(self):
        vv = False
        try:
            myQuery = """
            select * from FLUXO 
            where IDRF = '""" + str(self.IDRF) + """'
            """
            self.Eventos = app.pd.read_sql_query(myQuery, self.__db__.engine).to_dict('records')
            self.__db__.statusquery = 'Executed'
            if len(self.Eventos)>0:
                vv = True
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv

    def clear_db_events(self):
        vv = False
        try:
            myQuery = """
            delete from FLUXO 
            where IDRF = '""" + str(self.IDRF) + """'
            """
            if not self.__db__.isConnected():self.__db__.connect()
            if self.__db__.execRawQuery(myQuery):
                self.__db__.drop()
                self.__db__.statusquery = 'Executed'
                vv = True
            else:
                self.__db__.drop()
                self.__db__.statusquery = 'Failed Query'
                vv= False
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv

    def insert_events(self):
        vv = True
        try:
            if not self.__db__.isConnected():self.__db__.connect()
            for row in self.Eventos:
                myQuery = """
                insert into FLUXO (ValorLiq,PercEvento,TipoIncidencia,TipoEvento,idRf,Data) 
                Values (
                    '""" + str(row['ValorLiq']) + """',
                    '""" + str(row['PercEvento']) + """',
                    '""" + row['TipoIncidencia'] + """',
                    '""" + row['TipoEvento'] + """',
                    '""" + str(self.IDRF) + """',
                    '""" + row['Data'] + """'
                )
                """
                if self.__db__.execRawQuery(myQuery)==False: vv=False
            self.__db__.drop()
            self.__db__.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv