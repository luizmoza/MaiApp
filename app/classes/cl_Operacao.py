
from app import app
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import datetime

class cl_Operacao(app.base):
    AliasOperacao:Mapped[str] = mapped_column(primary_key=True)	
    CGC:Mapped[str]  = mapped_column(primary_key=True)	
    Administrador:Mapped[str]	
    AliasAtivo:Mapped[str]
    Estrategia:Mapped[str]	
    PuCompra:Mapped[float]		
    TaxaCompra:Mapped[float]		
    Marcacao:Mapped[str]
    Vencimento:Mapped[datetime.datetime]	
    FormulaPrecificacao:Mapped[str]	
    DataCompra:Mapped[datetime.datetime]	
    PuVencimento:Mapped[float]		
    TravaEdicao:Mapped[bool]
    MacroEstrategia:Mapped[str]	
    DataLog:Mapped[datetime.datetime]	
    __tablename__ = "Operacao"
    __table_args__ = {'extend_existing': True}
    __db__ = app.db
    __pk__ = ['AliasOperacao','CGC']
    __nn__ = ['AliasAtivo']
    __nnbl__ = []
    __nnint__ = []
    __nndbl__ = []
    __nndt__ = []
    __unics__ = [] 
    __fks__ = {} 
    
    def __init__(self,**kwargs): 
        self.AliasOperacao = kwargs['AliasOperacao'] if 'AliasOperacao' in kwargs else None
        self.CGC = kwargs['CGC'] if 'CGC' in kwargs else None
        self.Administrador = kwargs['Administrador'] if 'Administrador' in kwargs else None
        self.AliasAtivo = kwargs['AliasAtivo'] if 'AliasAtivo' in kwargs else None
        self.Estrategia = kwargs['Estrategia'] if 'Estrategia' in kwargs else None
        self.PuCompra = kwargs['PuCompra'] if 'PuCompra' in kwargs else None	
        self.TaxaCompra = kwargs['TaxaCompra'] if 'TaxaCompra' in kwargs else None
        self.Marcacao = kwargs['Marcacao'] if 'Marcacao' in kwargs else None
        self.Vencimento = kwargs['Vencimento'] if 'Vencimento' in kwargs else None
        self.FormulaPrecificacao = kwargs['FormulaPrecificacao'] if 'FormulaPrecificacao' in kwargs else None
        self.DataCompra = kwargs['DataCompra'] if 'DataCompra' in kwargs else None
        self.PuVencimento = kwargs['PuVencimento'] if 'PuVencimento' in kwargs else None
        self.TravaEdicao = kwargs['TravaEdicao'] if 'TravaEdicao' in kwargs else None
        self.MacroEstrategia = kwargs['MacroEstrategia'] if 'MacroEstrategia' in kwargs else None
        self.DataLog = kwargs['DataLog'] if 'DataLog' in kwargs else None


    def Exists(self,AliasOperacao,CGC):
        vv = False
        try:
            myQuery = """
            select aliasoperacao,cgc from """ + self.__tablename__ + """
            where aliasoperacao = '""" + AliasOperacao + """'
            and CGC = '""" + CGC + """'
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                vv = True
            else:
                vv = False
            self.__db__.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv
    
    def Delete(self,AliasOperacao,CGC):
        vv = False
        try:
            myQuery = """
            delete from """ + self.__tablename__ + """
            where aliasoperacao = '""" + AliasOperacao + """'
            and CGC = '""" + CGC + """'
            """
            if self.__db__.isConnected() == False:
                self.__db__.connect()
            self.__db__.execRawQuery(myQuery)
            if self.__db__.statusquery == 'Query Succeeded':
                self.__db__.drop()
                self.__db__.statusquery = 'Executed'
                vv = True
            else:
                self.__db__.drop()
                self.__db__.statusquery = 'Not Executed'
                vv = False
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv    

    def Load(self,AliasOperacao,CGC):
        vv = False
        try:
            myQuery = """
            select * from """ + self.__tablename__ + """
            where aliasoperacao = '""" + AliasOperacao + """'
            and CGC = '""" + CGC + """'
            """
            dfresult = app.pd.read_sql_query(myQuery, self.__db__.engine)
            if len(dfresult)>0:
                for index,row in dfresult.iterrows():
                    self.AliasOperacao = row['AliasOperacao']	
                    self.CGC = row['CGC']	
                    self.Administrador = row['Administrador']	
                    self.AliasAtivo = row['AliasAtivo']	
                    self.Estrategia = row['Estrategia']	
                    self.PuCompra = row['PuCompra']	
                    self.TaxaCompra = row['TaxaCompra']		
                    self.Marcacao = row['Marcacao']	
                    self.Vencimento = row['Vencimento']	
                    self.FormulaPrecificacao = row['FormulaPrecificacao']		
                    self.DataCompra	= row['DataCompra']		
                    self.PuVencimento	= row['PuVencimento']	
                    self.TravaEdicao = row['TravaEdicao']	
                    self.MacroEstrategia= row['MacroEstrategia']	
                    self.DataLog = row['DataLog']	
                vv = True
            else:
                vv = False
            self.__db__.statusquery = 'Executed'
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv
    
    def Update(self,Administrador,AliasAtivo,Estrategia,PuCompra,TaxaCompra,Marcacao,Vencimento,FormulaPrecificacao,DataCompra,PuVencimento,TravaEdicao,MacroEstrategia,DataLog,AliasOperacao,CGC):
        vv = False
        try:
            myQuery = """
            Update """ + self.__tablename__ + """
            set Administrador = '""" + Administrador + """', 	
            AliasAtivo = '""" + AliasAtivo + """',
            Estrategia = '""" + Estrategia + """',	
            PuCompra = '""" + PuCompra + """',	
            TaxaCompra = '""" + TaxaCompra + """',		
            Marcacao = '""" + Marcacao + """',	
            Vencimento = '""" + Vencimento + """',	
            FormulaPrecificacao = '""" + FormulaPrecificacao + """',		
            DataCompra = '""" + DataCompra + """',		
            PuVencimento = '""" + str(PuVencimento) + """',	
            TravaEdicao = '""" + str(TravaEdicao) + """',	
            MacroEstrategia = '""" + MacroEstrategia + """',	
            DataLog = '""" + DataLog.strftime('%Y-%m-%d') + """'	            
            where aliasoperacao = '""" + AliasOperacao + """'
            and CGC = '""" + CGC + """'
            """
            if self.__db__.isConnected() == False:
                self.__db__.connect()
            self.__db__.execRawQuery(myQuery)
            if self.__db__.statusquery == 'Query Succeeded':
                self.__db__.drop()
                self.__db__.statusquery = 'Executed'
                vv = True
            else:
                self.__db__.drop()
                self.__db__.statusquery = 'Not Executed'
                vv = False
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv
    
    def Insert(self,Administrador,AliasAtivo,Estrategia,PuCompra,TaxaCompra,Marcacao,Vencimento,FormulaPrecificacao,DataCompra,PuVencimento,TravaEdicao,MacroEstrategia,DataLog,AliasOperacao,CGC):
        vv = False
        try:
            myQuery = """
            Insert into """ + self.__tablename__ + """
            (Administrador,AliasAtivo,Estrategia,PuCompra,TaxaCompra,Marcacao,Vencimento,FormulaPrecificacao,DataCompra,PuVencimento,TravaEdicao,MacroEstrategia,DataLog,AliasOperacao,CGC)
            Values(            
            Administrador = '""" + Administrador + """', 	
            AliasAtivo = '""" + AliasAtivo + """',
            Estrategia = '""" + Estrategia + """',	
            PuCompra = '""" + PuCompra + """',	
            TaxaCompra = '""" + TaxaCompra + """',		
            Marcacao = '""" + Marcacao + """',	
            Vencimento = '""" + Vencimento + """',	
            FormulaPrecificacao = '""" + FormulaPrecificacao + """',		
            DataCompra = '""" + DataCompra + """',		
            PuVencimento = '""" + str(PuVencimento) + """',	
            TravaEdicao = '""" + str(TravaEdicao) + """',	
            MacroEstrategia = '""" + MacroEstrategia + """',	
            DataLog = '""" + DataLog.strftime('%Y-%m-%d') + """',	            
            aliasoperacao = '""" + AliasOperacao + """',
            CGC = '""" + CGC + """'
            )
            """
            if self.__db__.isConnected() == False:
                self.__db__.connect()
            self.__db__.execRawQuery(myQuery)
            if self.__db__.statusquery == 'Query Succeeded':
                self.__db__.drop()
                self.__db__.statusquery = 'Executed'
                vv = True
            else:
                self.__db__.drop()
                self.__db__.statusquery = 'Not Executed'
                vv = False
        except Exception as e:
            self.__db__.statusquery = 'Failed Query: %s', repr(e)
            vv = False  
        return vv