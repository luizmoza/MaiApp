
from app import app

class cl_Gerencial():
    __tablename__ = "Gerencial"
    __db__ = app.db
    __pk__ = []
    __nn__ = []
    __nnbl__ = []
    __nnint__ = []
    __nndbl__ = []
    __nndt__ = []
    __unics__ = [] 
    __fks__ = {} 

    def __init__(self,**kwargs): 
        self.Data = kwargs['Data'] if 'Data' in kwargs else None
        self.AliasFundo = kwargs['AliasFundo'] if 'AliasFundo' in kwargs else None
        self.Trader = kwargs['Trader'] if 'Trader' in kwargs else None
        self.AliasAtivo = kwargs['AliasAtivo'] if 'AliasAtivo' in kwargs else None
        self.Macro = kwargs['Macro'] if 'Macro' in kwargs else None
        self.Estrat = kwargs['Estrat'] if 'Estrat' in kwargs else None
        self.Indice_Espec = kwargs['Indice_Espec'] if 'Indice_Espec' in kwargs else None
        self.Quantidade = kwargs['Quantidade'] if 'Quantidade' in kwargs else None
        self.Fin = kwargs['Fin'] if 'Fin' in kwargs else None
        self.FinD1 = kwargs['FinD1'] if 'FinD1' in kwargs else None
        self.Resultado = kwargs['Resultado'] if 'Resultado' in kwargs else None
        self.Carrego = kwargs['Carrego'] if 'Carrego' in kwargs else None
        self.Over_Carrego = kwargs['Over_Carrego'] if 'Over_Carrego' in kwargs else None
        self.Carrego_Espec = kwargs['Carrego_Espec'] if 'Carrego_Espec' in kwargs else None
        self.Over_Carrego_Espec = kwargs['Over_Carrego_Espec'] if 'Over_Carrego_Espec' in kwargs else None
        self.Perc_Carrego = kwargs['Perc_Carrego'] if 'Perc_Carrego' in kwargs else None
        self.Perc_Carregi_Espec = kwargs['Perc_Carregi_Espec'] if 'Perc_Carregi_Espec' in kwargs else None
        self.PL = kwargs['PL'] if 'PL' in kwargs else None
        self.Perc_PL = kwargs['Perc_PL'] if 'Perc_PL' in kwargs else None
    
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

    def unbulk(self,dataini,datafim,aliasfundo): # Usa os dados do próprio objeto
        sql = """
        delete from Gerencial 
        where data >= '""" + dataini.strftime('%Y-%m-%d')  +  """'
        and data <= '""" + datafim.strftime('%Y-%m-%d') +  """'
        and aliasfundo = '""" + aliasfundo +  """'
        """
        return self.__db__.execRawQuery(sql)

    def load(self,dataini,datafim,aliasfundo):
        sql = """ select * from Gerencial 
        where data >= '""" + dataini.strftime('%Y-%m-%d')  +  """'
        and data <= '""" + datafim.strftime('%Y-%m-%d') +  """'
        and aliasfundo = '""" + aliasfundo +  """'
        """
        return app.pd.read_sql_query(sql, app.db.engine)

#################################################################Métodos Génericos#############################################################
###############################################################################################################################################
