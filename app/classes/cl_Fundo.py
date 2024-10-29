from app import app
from sqlalchemy.orm import Mapped
from sqlalchemy import orm
from sqlalchemy.orm import mapped_column
import datetime

class cl_Fundo(app.base):
    IDFundo:Mapped[int]	 = mapped_column(primary_key=True,unique=True)	
    CGC:Mapped[str]	
    Nome:Mapped[str]	
    AliasCota:Mapped[str]	
    Tipo:Mapped[str]	
    RegraResgate:Mapped[str]	
    RegraAplicacao:Mapped[str]	
    Administrador:Mapped[str]	
    Banco:Mapped[str]	
    Agencia:Mapped[str]	
    Conta:Mapped[str]	
    CetipConta:Mapped[str]	
    CetipMiolo:Mapped[str]	
    Alias:Mapped[str]	
    ISIN:Mapped[str]	
    Benchmark:Mapped[str]	
    digito:Mapped[str]	
    CetipDigito:Mapped[str]	
    TipoInvestidor:Mapped[str]	
    TipoCondominio:Mapped[str]
    SubTipo:Mapped[str]	
    Segmento:Mapped[str]	
    BenchmarkPlano:Mapped[str]	
    IncentivoFiscal:Mapped[bool]	
    PassivoRestrito:Mapped[bool]	
    Interno:Mapped[bool]	
    FIC:Mapped[bool]	
    ETF:Mapped[bool]
    Derivativos:Mapped[bool]	
    Descoberto:Mapped[bool]	
    Adaptado4661:Mapped[bool]
    Adaptado3922:Mapped[bool]
    Adaptado4444:Mapped[bool]	
    Abertura:Mapped[bool]
    DataInicioMai:Mapped[datetime.datetime]		
    DataFimMai:Mapped[datetime.datetime]		
    idBolsa:Mapped[int]	
    idMoeda:Mapped[int]	
    Alavancagem:Mapped[float]
    TaxaPerformance:Mapped[float]
    TaxaAdministracao:Mapped[float]
    __tablename__ = "Fundo"
    __table_args__ = {'extend_existing': True}
    __db__ = app.db
    __pk__ = ['IDFundo']
    __nn__ = ['Nome','CGC','Alias']
    __nnbl__ = []
    __nnint__ = []
    __nndbl__ = []
    __nndt__ = []
    __unics__ = ['CGC','Nome','Alias'] 
    __fks__ = {} 


    
    def __init__(self,**kwargs): 
        self.IDFundo = kwargs['IDFundo'] if 'IDFundo' in kwargs else None
        self.CGC = kwargs['CGC'] if 'CGC' in kwargs else None	
        self.Nome = kwargs['Nome'] if 'Nome' in kwargs else None	
        self.AliasCota = kwargs['AliasCota'] if 'AliasCota' in kwargs else None	
        self.Tipo = kwargs['Tipo'] if 'Tipo' in kwargs else None
        self.RegraResgate = kwargs['RegraResgate'] if 'RegraResgate' in kwargs else None	
        self.RegraAplicacao = kwargs['RegraAplicacao'] if 'RegraAplicacao' in kwargs else None	
        self.Administrador = kwargs['Administrador'] if 'Administrador' in kwargs else None
        self.Banco = kwargs['Banco'] if 'Banco' in kwargs else None	
        self.Agencia = kwargs['Agencia'] if 'Agencia' in kwargs else None
        self.Conta = kwargs['Conta'] if 'Conta' in kwargs else None
        self.CetipConta = kwargs['CetipConta'] if 'CetipConta' in kwargs else None
        self.CetipMiolo = kwargs['CetipMiolo'] if 'CetipMiolo' in kwargs else None
        self.Alias = kwargs['Alias'] if 'Alias' in kwargs else None
        self.ISIN = kwargs['ISIN'] if 'ISIN' in kwargs else None
        self.Benchmark = kwargs['Benchmark'] if 'Benchmark' in kwargs else None	
        self.digito = kwargs['digito'] if 'digito' in kwargs else None	
        self.CetipDigito = kwargs['CetipDigito'] if 'CetipDigito' in kwargs else None	
        self.TipoInvestidor = kwargs['TipoInvestidor'] if 'TipoInvestidor' in kwargs else None	
        self.TipoCondominio = kwargs['TipoCondominio'] if 'TipoCondominio' in kwargs else None
        self.SubTipo = kwargs['SubTipo'] if 'SubTipo' in kwargs else None
        self.Segmento = kwargs['Segmento'] if 'Segmento' in kwargs else None
        self.BenchmarkPlano = kwargs['BenchmarkPlano'] if 'BenchmarkPlano' in kwargs else None
        self.IncentivoFiscal = kwargs['IncentivoFiscal'] if 'IncentivoFiscal' in kwargs else None
        self.PassivoRestrito = kwargs['PassivoRestrito'] if 'PassivoRestrito' in kwargs else None
        self.Interno = kwargs['Interno'] if 'Interno' in kwargs else None
        self.FIC = kwargs['FIC'] if 'FIC' in kwargs else None
        self.ETF = kwargs['ETF'] if 'ETF' in kwargs else None
        self.Derivativos = kwargs['Derivativos'] if 'Derivativos' in kwargs else None	
        self.Descoberto = kwargs['Descoberto'] if 'Descoberto' in kwargs else None
        self.Adaptado4661 = kwargs['Adaptado4661'] if 'Adaptado4661' in kwargs else None
        self.Adaptado3922 = kwargs['Adaptado3922'] if 'Adaptado3922' in kwargs else None
        self.Adaptado4444 = kwargs['Adaptado4444'] if 'Adaptado4444' in kwargs else None
        self.Abertura = kwargs['Abertura'] if 'Abertura' in kwargs else None
        self.DataInicioMai = kwargs['DataInicioMai'] if 'DataInicioMai' in kwargs else None		
        self.DataFimMai = kwargs['DataFimMai'] if 'DataFimMai' in kwargs else None		
        self.idBolsa = kwargs['idBolsa'] if 'idBolsa' in kwargs else None
        self.idMoeda = kwargs['idMoeda'] if 'idMoeda' in kwargs else None
        self.Alavancagem = kwargs['Alavancagem'] if 'Alavancagem' in kwargs else None
        self.TaxaPerformance = kwargs['TaxaPerformance'] if 'TaxaPerformance' in kwargs else None
        self.TaxaAdministracao = kwargs['TaxaAdministracao'] if 'TaxaAdministracao' in kwargs else None
    
    @orm.reconstructor 
    def init_on_load(self): # Construtor usando ORM (exmplandin do init do orm)
        self.Carteiras = []
            
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

    
    def LoadCarteiras(self,db,DataIni,DataFim):
        vv = False
        try:
            myQuery = """
            select * from Carteira
            where CGC = '""" + self.CGC + """'
            and Data >= '""" + DataIni.strftime('%Y-%m-%d') + """'
            and Data <= '""" + DataFim.strftime('%Y-%m-%d') + """'
            """
            self.Carteiras = app.pd.read_sql_query(myQuery, db.engine)
            if len(self.Carteiras)>0:
                vv = True
            db.statusquery = 'Executed'
        except Exception as e:
            db.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv

    def get_id_by_CGC(self):
        vv = False
        try:
            myQuery = """
            select IDFundo from """ + self.__tablename__ + """
            where CGC = '""" + self.CGC + """'
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                self.IDFundo = dfresult['IDFundo'].iloc[0].item() # Item() para tranformar em int nativo python... pandas devolve um numpy
                vv = True
            else:
                self.IDFundo = 0
            self._db_.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv