from app import app
import math

class cl_tkDict:
    def __init__(self):
            self.db = app.db
            self.DictOperacoes = {}
            self.DictEstrategias = {}
            self.DictFundos = {}
            self.DictBolsas = {}
            self.DictidBolsa = {}
            self.DictMoedas = {}
            self.DictRF = {}
            self.DictRV = {}
            self.DictEmissor = {}
            self.DictCorretora = {}
            self.DictDistribuidor = {}
            self.DictCotista = {}
            self.DictCodRefCotistaFundo = {}
            self.DictOpcao = {}
            self.DictFuturo = []
            self.DictMov = {}
            self.DictBuscarAtivos = {}
            self.DictFundosDaCasa = {}
            self.DictCotistaByCGC = {}
            self.DictDistribuidorSimples = {}
            self.DictTipoMercadoriaOpcao = {}
            self.DictTipoMercadoriaFuturo = {}
            self.DictTipoRV = {}
            self.DictTipoRF = {}
            self.DictIDTipoMercadoriaOpcao = {}
            self.DictIDTipoMercadoriaFuturo = {}
            self.DictIDTipoRV = {}
            self.DictIDTipoRF = {}
            self.DictIDTrader = {}
            self.DictTrader = {}
            self.DictIDContraparte = {}
            self.DictContraparte = {}
            self.DictIDEstrat = {}
            self.DictEstrat = {}
            self.DictMacroEstrat = {}
            self.DictCGCToAlias = {}
            self.DictListaEmissor = {}
            self.DictIDEmissor = {}
            self.DictIDCodRefCotistaFundo = {}
            self.DictIDFundo = {}
            self.DictPassivo = {}
            self.DictIDFundoWithInterno = {}
            self.dfListaPassivo={}
            self.DictCGCFundoid={}
            self.DictEstratFull={}
            self.DictRateio={}
            self.DictListRateio={}
            self.DictEstratID={}
            self.DictMacroEstratID={}
            self.DictCGCFundoidCGC={}
            

############################################# Inicio do ListLoaders #################################################

    def LoadDictTipoRF(self,srch):
         query = "select idTipoRF,Nome from TipoRF where Nome like '%" + srch + "%' order by Nome asc"
         self.DictTipoRF = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictTipoRF[row["Nome"]] = row["idTipoRF"]
             return True
         else:
             return False


    def LoadDictRateio(self):
        vv = False    
        try:
            query = "select lista,cgc,ordem,idFundolista from fundolista order by lista,ordem asc"
            df = app.pd.read_sql(query,self.db.engine)
            self.DictRateio = df.to_dict('records')
            vv = True    
        except:
            vv = False    
        return vv
    
    def LoadDictListRateio(self):
        vv = False    
        try:
            query = "select distinct lista from fundolista"
            df = app.pd.read_sql(query,self.db.engine)
            self.DictListRateio = df.to_dict('records')
            vv = True    
        except:
            vv = False    
        return vv
         

    def LoadDictIDTipoRF(self,srch):
         query = "select idTipoRF,Nome from TipoRF where Nome like '%" + srch + "%' order by Nome asc"
         self.DictIDTipoRF = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDTipoRF[row["idTipoRF"]] = row["Nome"]
             return True
         else:
             return False
         
    def LoadDictTrader(self,srch):
         query = "select idTrader,Nome from Trader where Nome like '%" + srch + "%' order by Nome asc"
         self.DictTrader = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictTrader[row["Nome"]] = row["idTrader"]
             return True
         else:
             return False
         
    def LoadDictTraderID(self,srch):
         query = "select idTrader,Nome from Trader where Nome like '%" + srch + "%' order by Nome asc"
         self.DictTrader = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictTrader[row["idTrader"]] = row["Nome"]
             return True
         else:
             return False
         
    
    def LoadDictIDTrader(self,srch):
         query = "select idTrader,Nome from Trader where Nome like '%" + srch + "%' order by Nome asc"
         self.DictIDTrader = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDTrader[row["idTrader"]] = row["Nome"]
             return True
         else:
             return False

    def LoadDictContraparte(self,srch):
         query = "select idCorretora,Nome from Contraparte where Nome like'%" + srch + "%' order by Nome asc"
         self.DictContraparte = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictContraparte[row["Nome"]] = row["idCorretora"]
             return True
         else:
             return False

    def LoadDictIDContraparte(self,srch):
         query = "select idCorretora,Nome from Contraparte where Nome like'%" + srch + "%' order by Nome asc"
         self.DictIDContraparte = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDContraparte[row["idCorretora"]] = row["Nome"]
             return True
         else:
             return False

    def LoadDictMacroEstrat(self,srch):
         query = "select distinct Grupo from Estrategia where Nome like'%" + srch + "%'"
         self.DictMacroEstrat = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictMacroEstrat[row["Grupo"]] = 1
             return True
         else:
             return False
    
    def LoadDictEstrat(self,srch):
         query = "select idEstrategia,Grupo+'#'+Nome as Nome from Estrategia where Nome like '%" + srch + "%' order by Nome asc"
         self.DictEstrat = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictEstrat[row["Nome"]] = row["idEstrategia"]
             return True
         else:
             return False

    def LoadDictEstratID(self,srch):
         query = "select idEstrategia,Nome from Estrategia where Nome like '%" + srch + "%' order by Nome asc"
         self.DictEstrat = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictEstratID[row["idEstrategia"]] = row["Nome"]
             return True
         else:
             return False
    
    def LoadDictMacroEstratID(self,srch):
         query = "select idEstrategia,Grupo from Estrategia where Nome like '%" + srch + "%' order by Nome asc"
         self.DictEstrat = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictMacroEstratID[row["idEstrategia"]] = row["Grupo"]
             return True
         else:
             return False
         

    def LoadDictEstratFull(self,srch):
         query = "select idEstrategia,Grupo,Nome from Estrategia where Nome like '%" + srch + "%' order by Nome asc"
         self.DictEstratFull = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 if row['Grupo'] not in self.DictEstratFull: self.DictEstratFull[row['Grupo']] = {}
                 self.DictEstratFull[row["Grupo"]][row["Nome"]] = row["idEstrategia"]
             return True
         else:
             return False
         

    def LoadDictIDEstrat(self,srch):
         query = "select idEstrategia,Grupo+'#'+nome as Nome from Estrategia where Nome like '%" + srch + "%' order by Nome asc"
         self.DictIDEstrat = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDEstrat[row["idEstrategia"]] = row["Nome"]
             return True
         else:
             return False
    
    def LoadDictIDCodRefCotistaFundo(self,srch):
         query = "select idCodRefCotistaFundo,Codigo from CodRefCotistaFundo where idFundo like " + srch + " order by Codigo asc"
         self.DictIDCodRefCotistaFundo = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDCodRefCotistaFundo[row["Codigo"]] = row["idCodRefCotistaFundo"]
             return True
         else:
             return False

    def LoadDictIDFundo(self,srch):
         query = "select idfundo,Alias from fundo where (DataInicioMai > datafimmai or (datafimmai is null and DataInicioMai is not null) and datafimmai <= '" + srch.strftime('%Y-%m-%d') + "') order by idfundo desc"
         self.DictIDFundo = {}
         df = app.pd.read_sql(query,self.db.engine)
         self.DictIDFundo["N/A"] = -1
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDFundo[row["Alias"]] = row["idfundo"]
             return True
         else:
             return False

    def LoadDictIDFundoWithInterno(self,srch):
         query = "select idfundo,Alias from fundo where Interno = 1 and ((DataInicioMai > datafimmai or (datafimmai is null and DataInicioMai is not null)) and datafimmai <= '" + srch.strftime('%Y-%m-%d') + "') order by idfundo desc"
         self.DictIDFundo = {}
         df = app.pd.read_sql(query,self.db.engine)
         self.DictIDFundo["N/A"] = -1
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDFundoWithInterno[row["Alias"]] = row["idfundo"]
             return True
         else:
             return False

    def LoadDictCGCFundo(self,srch):
         query = "select cgc,alias from fundo where (DataInicioMai > datafimmai or (datafimmai is null and DataInicioMai is not null)) and datafimmai <= '" + srch.strftime('%Y-%m-%d') + "' order by alias asc"
         self.DictIDFundo = {}
         df = app.pd.read_sql(query,self.db.engine)
         self.DictIDFundo["N/A"] = -1
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDFundo[row["cgc"]] = row["alias"]
             return True
         else:
             return False


    def LoadDictCGCFundoid(self,srch):
         query = "select CGC,idFundo,Alias from fundo where (DataInicioMai > datafimmai or (datafimmai is null and DataInicioMai is not null)) and (datafimmai is null or datafimmai <= '" + srch.strftime('%Y-%m-%d') + "') order by alias asc"
         self.DictCGCFundoid = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
                 self.DictCGCFundoid = df.set_index('idFundo').to_dict('index')
                 return True
         else:
             return False

    def LoadDictCGCFundoidCGC(self,srch):
         query = "select CGC,idFundo,Alias from fundo where (DataInicioMai > datafimmai or (datafimmai is null and DataInicioMai is not null)) and (datafimmai is null or datafimmai <= '" + srch.strftime('%Y-%m-%d') + "') order by alias asc"
         self.DictCGCFundoidCGC = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
                 self.DictCGCFundoidCGC = df.set_index('CGC').to_dict('index')
                 return True
         else:
             return False
         

    def LoadDictCGCToAlias(self,srch):
         query = "select cgc,Alias from fundo where DataInicioMai > datafimmai or (datafimmai is null and DataInicioMai is not null) and datafimmai <= '" + srch.strftime('%Y-%m-%d') + "' order by alias asc"
         self.DictCGCToAlias = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictCGCToAlias[row["cgc"]] = row["Alias"]
             return True
         else:
             return False
    
    def LoadDictTipoRV(self,srch):
         query = "select idTipoRV,Nome from TipoRV where Nome like '%" + srch + "%' order by Nome asc"
         self.DictTipoRV = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictTipoRV[row["Nome"]] = row["idTipoRV"]
             return True
         else:
             return False
    
    def LoadDictIDTipoRV(self,srch):
         query = "select idTipoRV,Nome from TipoRV where Nome like '%" + srch + "%' order by Nome asc"
         self.DictIDTipoRV = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDTipoRV[row["idTipoRV"]] = row["Nome"]
             return True
         else:
             return False

    def LoadDictIDTipoRV(self,srch):
         query = "select idTipoRV,Nome from TipoRV where Nome like '%" + srch + "%' order by Nome asc"
         self.DictIDTipoRV = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDTipoRV[row["idTipoRV"]] = row["Nome"]
             return True
         else:
             return False

    def LoadDictTipoMercadoriaFuturo(self,srch):
         query = "select idTipoMercadoriaFuturo,NomeTipoMercadoriaFuturo from TipoMercadoriaFuturo where NomeTipoMercadoriaFuturo like '%" + srch + "%' order by NomeTipoMercadoriaFuturo asc"
         self.DictTipoMercadoriaFuturo = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictTipoMercadoriaFuturo[row["NomeTipoMercadoriaFuturo"]] = row["idTipoMercadoriaFuturo"]
             return True
         else:
             return False

    def LoadDictIDTipoMercadoriaFuturo(self,srch):
         query = "select idTipoMercadoriaFuturo,NomeTipoMercadoriaFuturo from TipoMercadoriaFuturo where NomeTipoMercadoriaFuturo like '%" + srch + "%' order by NomeTipoMercadoriaFuturo asc"
         self.DictIDTipoMercadoriaFuturo = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDTipoMercadoriaFuturo[row["idTipoMercadoriaFuturo"]] = row["NomeTipoMercadoriaFuturo"]
             return True
         else:
             return False

    def LoadDictTipoMercadoriaOpcao(self,srch):
         query = "select idTipoMercadoriaOpcao,NomeTipoMercadoriaOpcao from TipoMercadoriaOpcao where NomeTipoMercadoriaOpcao like '%" + srch + "%' order by NomeTipoMercadoriaOpcao asc"
         self.DictTipoMercadoriaOpcao = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictTipoMercadoriaOpcao[row["NomeTipoMercadoriaOpcao"]] = row["idTipoMercadoriaOpcao"]
             return True
         else:
             return False         
         
    def LoadDictIDTipoMercadoriaOpcao(self,srch):
         query = "select idTipoMercadoriaOpcao,NomeTipoMercadoriaOpcao from TipoMercadoriaOpcao where NomeTipoMercadoriaOpcao like '%" + srch + "%' order by NomeTipoMercadoriaOpcao asc"
         self.DictIDTipoMercadoriaOpcao = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDTipoMercadoriaOpcao[row["idTipoMercadoriaOpcao"]] = row["NomeTipoMercadoriaOpcao"]
             return True
         else:
             return False         

    def LoadDictListaIDEmissor(self,srch):
         query = "select idEmissor,Nome from Emissor where Nome like '%" + srch + "%' or cgc like '%" + srch + "%' order by Nome asc"
         self.DictIDEmissor = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictIDEmissor[row["idEmissor"]] = row["Nome"]
             return True
         else:
             return False         

    def LoadDictListaEmissor(self,srch):
         query = "select idEmissor,Nome from Emissor where Nome like '%" + srch + "%' or cgc like '%" + srch + "%' order by Nome asc"
         self.DictListaEmissor = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictListaEmissor[row["Nome"]] = row["idEmissor"]
             return True
         else:
             return False     

    def LoaddfListaPassivo(self,idFundo):
        try:
            query = """
            SELECT 
            Codigo as Codigo,
            IDCodRefCotistaFundo as idCodRefCotistaFundo,
            cotista.idCotista as idCotista,
            distribuidor.nome as NomeDistribuidor  ,
            fundo.administrador as Administrador,
            cotista.nome as NomeCotista,
            cotista.cgc as CGCCotista,
            cotista.banco as Banco,
            cotista.conta as Conta,
            cotista.digito as Agencia ,
            cotista.tipo as TipoCotista,
            fundo.cgc as CGCFundo
            FROM CodRefCotistaFundo 
            inner join Cotista on cotista.idcotista = CodRefCotistaFundo.idcotista
            inner join Fundo on Fundo.idFundo = CodRefCotistaFundo.idFundo 
            inner join Distribuidor on Distribuidor.idDistribuidor = CodRefCotistaFundo.idDistribuidor 
            where CodRefCotistaFundo.idfundo = '""" + str(idFundo) + """' 
            """
            self.dfListaPassivo = app.pd.read_sql(query,self.db.engine)
            return True
        except:
            return False  



    def LoadDictFundosDaCasa(self,srch):
         query = "select idfundo,Alias from fundo where  (datafimmai is null and DataInicioMai is not null) or ( DataInicioMai > datafimmai and datafimmai <= '" + srch.strftime('%Y-%m-%d') + "') order by alias asc"
         self.DictFundosDaCasa = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictFundosDaCasa[row["Alias"]] = row["idfundo"]
             return True
         else:
             return False     

    def LoadDictCotistaByCGC(self,srch):
         query = "select IDCotista,Nome from Cotista where cgc like '%" + srch + "%' or nome like '%" + srch + "%' order by Nome asc"
         self.DictCotistaByCGC = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictCotistaByCGC[row["Nome"]] = row["IDCotista"]
             return True
         else:
             return False     

    def LoadDictDistribuidorSimples(self,srch):
         query = "select IDDistribuidor,Nome from Distribuidor where cgc like '%" + srch + "%' order by Nome asc"
         self.DictDistribuidorSimples = {}
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             for index,row in df.iterrows():
                 self.DictDistribuidorSimples[row["Nome"]] = row["IDDistribuidor"]
             return True
         else:
             return False     

############################################# Fim do ListLoaders #################################################
############################################# Inicio dos Counts ##################################################

         
    def CountLoadDictOperacoes(self,srch):
         query = "SELECT count(aliasoperacao+'#'+cgc) as ncount FROM Operacao where aliasoperacao like '%" + srch + "%' or aliasAtivo like '%" + srch + "%' or cgc like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1     
         
    def CountLoadDictFundos(self,srch):
         query = "SELECT count(IdFundo) as ncount FROM Fundo where CGC like '%" + srch + "%' or Alias like '%" + srch + "%' or Nome like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1  

    def CountLoadDictOpcao(self,srch):
         query = "SELECT count(IdOpcao) as ncount FROM Opcao where Alias like '%" + srch + "%' or Isin like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1 
          
    def CountLoadDictFuturo(self,srch):
         query = "SELECT count(IdFuturo) as ncount FROM Futuro where Alias like '%" + srch + "%' or CodIsin like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1 

    def CountLoadDictRF(self,srch):
         query = "SELECT count(IdRF) as ncount FROM RF left join emissor on emissor.idemissor = rf.idemissor where Isin like '%" + srch + "%' or emissor.nome like '%" + srch + "%' or Alias like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1 

    def CountLoadDictRV(self,srch):
         query = "SELECT count(IdRV) as ncount FROM RV left join emissor on emissor.idemissor = rv.idemissor where Alias like '%" + srch + "%' or Isin like '%" + srch + "%'  or Emissor.nome like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1 

    def CountLoadDictEmissor(self,srch):
         query = "SELECT count(IdEmissor) as ncount FROM Emissor where Nome like '%" + srch + "%' or Grupo like '%" + srch + "%' or CGC like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1 

    def CountLoadDictCorretora(self,srch):
         query = "SELECT count(IdCorretora) as ncount FROM Contraparte where Nome like '%" + srch + "%' or CNPJ like '%" + srch + "%' or AliasMellon like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1 

    def CountLoadDictDistribuidor(self,srch):
         query = "SELECT count(IdDistribuidor) as ncount FROM Distribuidor where Nome like '%" + srch + "%' or CGC like '%" + srch + "%' or razaosocial like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1

    def CountLoadDictCotista(self,srch):
         query = "SELECT count(IdCotista) as ncount FROM Cotista where Nome like '%" + srch + "%' or CGC like '%" + srch + "%' or Tipo like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1
         
    def CountLoadDictEstrategias(self,srch):
         query = "SELECT count(idEstrategia) as ncount FROM Estrategia where Grupo like '%" + srch + "%' or Nome like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1
         
    def CountLoadDictBolsas(self,srch):
         query = "SELECT count(idBolsa) as ncount FROM Bolsa where NomeBolsa like '%" + srch + "%' "
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1

    def CountLoadDictMoedas(self,srch):
         query = "SELECT count(idMoeda) as ncount FROM Moeda where NomeMoeda like '%" + srch + "%' or CodigoIso like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1
         
    def CountLoadDictCodRefCotistaFundo(self,srch):
         query = "SELECT count(idcodrefcotistafundo) as ncount  FROM CodRefCotistaFundo inner join Fundo on CodRefCotistaFundo.idfundo = Fundo.idfundo inner join Cotista on cotista.idcotista = CodRefCotistaFundo.idcotista where codigo like '%" + srch + "%' or fundo.cgc like '%" + srch + "%' or fundo.alias like '%" + srch + "%' or cotista.nome like '%" + srch + "%'"
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1

    def CountLoadDictPassivo(self,srch,DataIni,DataFim,filter_search):
         query = "SELECT count(IdPassivo) as ncount FROM Passivo inner join codrefcotistafundo on codrefcotistafundo.idcodrefcotistafundo = passivo.idcodrefcotistafundo inner join fundo on fundo.idfundo = codrefcotistafundo.idfundo where passivo.tipo LIKE '%" + filter_search + "%' AND datamovimentacao <= '" + DataFim + "'  and datamovimentacao >= '" + DataIni + "' and (codrefcotistafundo.codigo like '%" + srch + "%' or fundo.cgc like '%" + srch + "%' or fundo.alias like '%" + srch + "%')" 
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1

    def CountLoadDictMov(self,srch, DataIni, DataFim, IdEstrategia, IdTrader, CGC):
        query = """
        SELECT count(Idmov) as ncount 
        from mov left join fundo on fundo.cgc = mov.cgc inner join estrategia on estrategia.idestrategia = mov.idestrategia
        where datamov <= '""" + DataFim + """'
        and datamov >= '""" + DataIni + """'
        and (fundo.alias like '%""" + srch + """%' or mov.aliasativo like '%""" + srch + """%')
        """
        if CGC == '00000000000000': query = query +  "and mov.CGC = '00000000000000'"
        if CGC != '00000000000000': query = query +  "and mov.CGC <> '00000000000000'"
        if int(IdEstrategia) > 0: query = query + " and mov.idestrategia = " + str(IdEstrategia) + " "
        if int(IdTrader) > 0: query = query + " and mov.idTrader = " + str(IdTrader) + " "
        df = app.pd.read_sql(query,self.db.engine)
        if len(df)>0:
            return df['ncount'].iloc[0].item()
        else:
            return -1


    def CountLoadDictBuscarAtivos(self,srch, Grupo, Tipo):
         if Grupo == "Cota": query = "SELECT count(Idfundo) as ncount  from fundo where fundo.segmento like '%" + Tipo + "%' and (fundo.alias like '%" + srch + "%' or fundo.aliascota like '%" + srch + "%') and fundo.aliascota is not null and fundo.alias <> ''"
         elif Grupo == "Opcao": query = "SELECT count(opcao.Idopcao) as ncount  from Opcao left join tipomercadoriaOpcao on tipomercadoriaOpcao.idtipomercadoriaOpcao = Opcao.idtipomercadoriaOpcao where tipomercadoriaOpcao.nometipomercadoriaOpcao like '%" + Tipo + "%' and Opcao.alias like '%" + srch + "%'"
         elif Grupo == "Futuro": query = "SELECT count(futuro.Idfuturo) as ncount  from futuro left join tipomercadoriafuturo on tipomercadoriafuturo.idtipomercadoriafuturo = futuro.idtipomercadoriafuturo  where tipomercadoriafuturo.nometipomercadoriafuturo like '%" + Tipo + "%' and futuro.alias like '%" + srch + "%'"
         elif Grupo == "RV": query = "SELECT count(rv.Idrv) as ncount from rv left join emissor on rv.idemissor = emissor.idEmissor left join tiporv on tiporv.idtiporv = rv.idtiporv  where tiporv.nome like '%" + Tipo + "%' and (emissor.nome like '%" + srch + "%' or rv.alias like '%" + srch + "%')"
         elif Grupo == "RF": query = "SELECT count(rf.Idrf) as ncount  from rf left join emissor on rf.idemissor = emissor.idEmissor left join tiporf on tiporf.idtiporf = rf.idtiporf  where tiporf.nome like '%" + Tipo + "%' and (emissor.nome like '%" + srch + "%' or rf.alias like '%" + srch + "%')"
         else: return -1
         df = app.pd.read_sql(query,self.db.engine)
         if len(df)>0:
             return df['ncount'].iloc[0].item()
         else:
             return -1




############################################# Fim do Counts ##################################################
############################################# Inicio dos Loaders ##################################################
         
    def LoadDictOperacoes(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictOperacoes(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " * FROM Operacao where aliasoperacao like '%" + srch + "%' or aliasAtivo like '%" + srch + "%' or cgc like '%" + srch + "%' order by cgc+aliasoperacao asc) as aux order by cgc+aliasoperacao desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictOperacoes = {}
        self.DictOperacoes['Lista'] = {}
        if len(df)>0:
            self.DictOperacoes['nPags'] = nPags
            self.DictOperacoes['Pag'] = Pag
            self.DictOperacoes['nPerPag'] = nPerPag
            self.DictOperacoes['nCount'] = nCount
            for index,row in df.iterrows():
              if row["CGC"] + "#" + row["AliasOperacao"] not in self.DictOperacoes['Lista']:
                 self.DictOperacoes['Lista'][row["CGC"] + "#" + row["AliasOperacao"]] = {}
                 self.DictOperacoes['Lista'][row["CGC"] + "#" + row["AliasOperacao"]]["AliasOperacao"] = row["AliasOperacao"]
                 self.DictOperacoes['Lista'][row["CGC"] + "#" + row["AliasOperacao"]]["AliasAtivo"] = row["AliasAtivo"]
                 self.DictOperacoes['Lista'][row["CGC"] + "#" + row["AliasOperacao"]]["CGC"] = row["CGC"]
                 self.DictOperacoes['Lista'][row["CGC"] + "#" + row["AliasOperacao"]]["Estrategia"] = row["Estrategia"]
                 self.DictOperacoes['Lista'][row["CGC"] + "#" + row["AliasOperacao"]]["MacroEstrategia"] = row["MacroEstrategia"]
                 self.DictOperacoes['Lista'][row["CGC"] + "#" + row["AliasOperacao"]]["Marcacao"] = row["Marcacao"]
                 self.DictOperacoes['Lista'][row["CGC"] + "#" + row["AliasOperacao"]]["Vencimento"] = row["Vencimento"]
                 self.DictOperacoes['Lista'][row["CGC"] + "#" + row["AliasOperacao"]]["DataCompra"] = row["DataCompra"]
                 self.DictOperacoes['Lista'][row["CGC"] + "#" + row["AliasOperacao"]]["TaxaCompra"] = row["TaxaCompra"]
                 self.DictOperacoes['Lista'][row["CGC"] + "#" + row["AliasOperacao"]]["Administrador"] = row["Administrador"]
            vv = True
        return vv

    def LoadDictEstrategias(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictEstrategias(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " * FROM Estrategia where Grupo like '%" + srch + "%' or Nome like '%" + srch + "%' order by idestrategia asc) as aux order by idestrategia desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictEstrategias = {}
        self.DictEstrategias['Lista'] = {}
        self.DictEstrategias['ListaGrupo'] = {}
        if len(df)>0:
            self.DictEstrategias['nPags'] = nPags
            self.DictEstrategias['Pag'] = Pag
            self.DictEstrategias['nPerPag'] = nPerPag
            self.DictEstrategias['nCount'] = nCount
            for index,row in df.iterrows():
                if row["Nome"] + "#" + row["Grupo"] not in self.DictEstrategias["Lista"]:
                    self.DictEstrategias["Lista"][row["Nome"] + "#" + row["Grupo"]] = row["IDEstrategia"]
                if row["Grupo"] not in self.DictEstrategias["ListaGrupo"]:
                    self.DictEstrategias["ListaGrupo"][row["Grupo"]] = {}
                if row["Nome"] not in self.DictEstrategias["ListaGrupo"][row["Grupo"]]: 
                    self.DictEstrategias["ListaGrupo"][row["Grupo"]][row["Nome"]] = row["IDEstrategia"]
            vv = True
        return vv


    def LoadDictMoedas(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictMoedas(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " * FROM Moeda where CodigoIso like '%" + srch + "%' or NomeMoeda like '%" + srch + "%' order by idMoeda desc) as aux order by idMoeda asc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictMoedas = {}
        self.DictMoedas['Lista'] = {}
        self.DictMoedas['Listaid'] = {}
        if len(df)>0:
            self.DictMoedas['nPags'] = nPags
            self.DictMoedas['Pag'] = Pag
            self.DictMoedas['nPerPag'] = nPerPag
            self.DictMoedas['nCount'] = nCount
            for index,row in df.iterrows():
                if row["CodigoIso"] not in self.DictMoedas["Lista"]:
                    self.DictMoedas["Lista"][row["CodigoIso"]] = row["IDMoeda"]
                if row["IDMoeda"] not in self.DictMoedas["Listaid"]:
                    self.DictMoedas["Listaid"][row["IDMoeda"]] = row["CodigoIso"]
            vv = True
        return vv

    def LoadDictBolsas(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictBolsas(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " * FROM Bolsa where NomeBolsa like '%" + srch + "%'  order by idBolsa desc) as aux order by idBolsa asc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictBolsas = {}
        self.DictBolsas['Lista'] = {}
        self.DictBolsas['Listaid'] = {}
        if len(df)>0:
            self.DictBolsas['nPags'] = nPags
            self.DictBolsas['Pag'] = Pag
            self.DictBolsas['nPerPag'] = nPerPag
            self.DictBolsas['nCount'] = nCount
            for index,row in df.iterrows():
                if row["NomeBolsa"] not in self.DictBolsas["Lista"]:
                    self.DictBolsas["Lista"][row["NomeBolsa"]] = row["IDBolsa"]
                if row["IDBolsa"] not in self.DictBolsas["Listaid"]:
                    self.DictBolsas["Listaid"][row["IDBolsa"]] = row["NomeBolsa"]
            vv = True
        return vv
    
    def LoadDictFundos(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictFundos(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " * FROM Fundo where CGC like '%" + srch + "%' or Alias like '%" + srch + "%' or Nome like '%" + srch + "%' order by IdFundo asc) as aux order by IdFundo desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictFundos = {}
        self.DictFundos['Lista'] = {}
        self.DictFundos['ListaGrupo'] = {}
        if len(df)>0:
            self.DictFundos['nPags'] = nPags
            self.DictFundos['Pag'] = Pag
            self.DictFundos['nPerPag'] = nPerPag
            self.DictFundos['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDFundo"] not in self.DictFundos["Lista"]:
                    self.DictFundos["Lista"][row["IDFundo"]] = {}
                    self.DictFundos["Lista"][row["IDFundo"]]["CGC"] = row["CGC"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Nome"] = row["Nome"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Alias"] = row["Alias"]
                    self.DictFundos["Lista"][row["IDFundo"]]["AliasCota"] = row["AliasCota"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Tipo"] = row["Tipo"]
                    self.DictFundos["Lista"][row["IDFundo"]]["IdFundo"] = row["IDFundo"]
                    self.DictFundos["Lista"][row["IDFundo"]]["RegraResgate"] = row["RegraResgate"]
                    self.DictFundos["Lista"][row["IDFundo"]]["RegraAplicacao"] = row["RegraAplicacao"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Administrador"] = row["Administrador"]
                    self.DictFundos["Lista"][row["IDFundo"]]["TaxaPerformance"] = row["TaxaPerformance"]
                    self.DictFundos["Lista"][row["IDFundo"]]["TaxaAdministracao"] = row["TaxaAdministracao"]
                    self.DictFundos["Lista"][row["IDFundo"]]["DataInicioMai"] = row["DataInicioMai"]
                    self.DictFundos["Lista"][row["IDFundo"]]["DataFimMai"] = row["DataFimMai"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Banco"] = row["Banco"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Agencia"] = row["Agencia"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Agencia"] = row["Agencia"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Conta"] = row["Conta"]
                    self.DictFundos["Lista"][row["IDFundo"]]["CetipConta"] = row["CetipConta"]
                    self.DictFundos["Lista"][row["IDFundo"]]["CetipMiolo"] = row["CetipMiolo"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Isin"] = row["ISIN"]
                    self.DictFundos["Lista"][row["IDFundo"]]["IdBolsa"] = row["idBolsa"]
                    self.DictFundos["Lista"][row["IDFundo"]]["IdMoeda"] = row["idMoeda"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Adaptado4661"] = row["Adaptado4661"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Adaptado3922"] = row["Adaptado3922"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Adaptado4444"] = row["Adaptado4444"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Benchmark"] = row["Benchmark"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Digito"] = row["digito"]
                    self.DictFundos["Lista"][row["IDFundo"]]["CetipDigito"] = row["CetipDigito"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Alavancagem"] = row["Alavancagem"]
                    self.DictFundos["Lista"][row["IDFundo"]]["ETF"] = row["ETF"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Derivativos"] = row["Derivativos"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Descoberto"] = row["Descoberto"]
                    self.DictFundos["Lista"][row["IDFundo"]]["TipoInvestidor"] = row["TipoInvestidor"]
                    self.DictFundos["Lista"][row["IDFundo"]]["PassivoRestrito"] = row["PassivoRestrito"]
                    self.DictFundos["Lista"][row["IDFundo"]]["TipoCondominio"] = row["TipoCondominio"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Interno"] = row["Interno"]
                    self.DictFundos["Lista"][row["IDFundo"]]["SubTipo"] = row["SubTipo"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Segmento"] = row["Segmento"]
                    self.DictFundos["Lista"][row["IDFundo"]]["FIC"] = row["FIC"]
                    self.DictFundos["Lista"][row["IDFundo"]]["IncentivoFiscal"] = row["IncentivoFiscal"]
                    self.DictFundos["Lista"][row["IDFundo"]]["Abertura"] = row["Abertura"]
            vv = True
        return vv

    def LoadDictRF(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictRF(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " IDRF,Alias,Codigo,Isin,emissor.nome as EmissorNome FROM RF left join emissor on emissor.idemissor = rf.idemissor where Isin like '%" + srch + "%' or emissor.nome like '%" + srch + "%' or Alias like '%" + srch + "%' order by IdRF asc) as aux order by IdRF desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictRF = {}
        self.DictRF['Lista'] = {}
        if len(df)>0:
            self.DictRF['nPags'] = nPags
            self.DictRF['Pag'] = Pag
            self.DictRF['nPerPag'] = nPerPag
            self.DictRF['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDRF"] not in self.DictRF["Lista"]:
                    self.DictRF["Lista"][row["IDRF"]] = {}
                    self.DictRF["Lista"][row["IDRF"]]["Alias"] = row["Alias"]
                    self.DictRF["Lista"][row["IDRF"]]["Codigo"] = row["Codigo"]
                    self.DictRF["Lista"][row["IDRF"]]["Isin"] = row["Isin"]
                    self.DictRF["Lista"][row["IDRF"]]["EmissorNome"] = row["EmissorNome"]
            vv = True
        return vv

    def LoadDictEmissor(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictEmissor(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " * FROM Emissor where Nome like '%" + srch + "%' or CGC like '%" + srch + "%' or Grupo like '%" + srch + "%' order by IdEmissor asc) as aux order by IdEmissor desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictEmissor = {}
        self.DictEmissor['Lista'] = {}
        if len(df)>0:
            self.DictEmissor['nPags'] = nPags
            self.DictEmissor['Pag'] = Pag
            self.DictEmissor['nPerPag'] = nPerPag
            self.DictEmissor['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDEmissor"] not in self.DictEmissor["Lista"]:
                    self.DictEmissor["Lista"][row["IDEmissor"]] = {}
                    self.DictEmissor["Lista"][row["IDEmissor"]]["IDEmissor"] = row["IDEmissor"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["Rating"] = row["Rating"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["Agencia"] = row["Agencia"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["RatingMAI"] = row["RatingMAI"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["Categoria"] = row["Categoria"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["Grupo"] = row["Grupo"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["Nome"] = row["Nome"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["cgc"] = row["cgc"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["AliasBradesco"] = row["AliasBradesco"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["AliasItau"] = row["AliasItau"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["AliasMellon"] = row["AliasMellon"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["TipoCIA"] = row["TipoCIA"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["CategoriaListagem"] = row["CategoriaListagem"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["Nacional"] = row["Nacional"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["TipoEmissor"] = row["TipoEmissor"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["RatingSeP"] = row["RatingSeP"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["RatingMoodys"] = row["RatingMoodys"]
                    self.DictEmissor["Lista"][row["IDEmissor"]]["RatingFitch"] = row["RatingFitch"]
            vv = True
        return vv


    def LoadDictCorretora(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictCorretora(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " * FROM Contraparte where Nome like '%" + srch + "%' or CNPJ like '%" + srch + "%' or AliasMellon like '%" + srch + "%' order by IdCorretora asc) as aux order by IdCorretora desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictCorretora = {}
        self.DictCorretora['Lista'] = {}
        if len(df)>0:
            self.DictCorretora['nPags'] = nPags
            self.DictCorretora['Pag'] = Pag
            self.DictCorretora['nPerPag'] = nPerPag
            self.DictCorretora['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDCorretora"] not in self.DictCorretora["Lista"]:
                    self.DictCorretora["Lista"][row["IDCorretora"]] = {}
                    self.DictCorretora["Lista"][row["IDCorretora"]]["IDCorretora"] = row["IDCorretora"]
                    self.DictCorretora["Lista"][row["IDCorretora"]]["Nome"] = row["Nome"]
                    self.DictCorretora["Lista"][row["IDCorretora"]]["CNPJ"] = row["CNPJ"]
                    self.DictCorretora["Lista"][row["IDCorretora"]]["AliasMellon"] = row["AliasMellon"]
                    self.DictCorretora["Lista"][row["IDCorretora"]]["AliasBradesco"] = row["AliasBradesco"]
                    self.DictCorretora["Lista"][row["IDCorretora"]]["AliasItau"] = row["AliasItau"]
            vv = True
        return vv

    def LoadDictDistribuidor(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictDistribuidor(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " * FROM Distribuidor where Nome like '%" + srch + "%' or CGC like '%" + srch + "%' or razaosocial like '%" + srch + "%' order by IdDistribuidor asc) as aux order by IdDistribuidor desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictDistribuidor = {}
        self.DictDistribuidor['Lista'] = {}
        if len(df)>0:
            self.DictDistribuidor['nPags'] = nPags
            self.DictDistribuidor['Pag'] = Pag
            self.DictDistribuidor['nPerPag'] = nPerPag
            self.DictDistribuidor['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDDistribuidor"] not in self.DictDistribuidor["Lista"]:
                    self.DictDistribuidor["Lista"][row["IDDistribuidor"]] = {}
                    self.DictDistribuidor["Lista"][row["IDDistribuidor"]]["IDDistribuidor"] = row["IDDistribuidor"]
                    self.DictDistribuidor["Lista"][row["IDDistribuidor"]]["Nome"] = row["Nome"]
                    self.DictDistribuidor["Lista"][row["IDDistribuidor"]]["CGC"] = row["CGC"]
                    self.DictDistribuidor["Lista"][row["IDDistribuidor"]]["RazaoSocial"] = row["RazaoSocial"]
            vv = True
        return vv

    def LoadDictCotista(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictCotista(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " * FROM Cotista where Nome like '%" + srch + "%' or CGC like '%" + srch + "%' or tipo like '%" + srch + "%' order by IdCotista asc) as aux order by IdCotista desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictCotista = {}
        self.DictCotista['Lista'] = {}
        if len(df)>0:
            self.DictCotista['nPags'] = nPags
            self.DictCotista['Pag'] = Pag
            self.DictCotista['nPerPag'] = nPerPag
            self.DictCotista['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDCotista"] not in self.DictCotista["Lista"]:                
                    self.DictCotista["Lista"][row["IDCotista"]] = {}
                    self.DictCotista["Lista"][row["IDCotista"]]["IDCotista"] = row["IDCotista"]
                    self.DictCotista["Lista"][row["IDCotista"]]["Nome"] = row["Nome"]
                    self.DictCotista["Lista"][row["IDCotista"]]["CGC"] = row["CGC"]
                    self.DictCotista["Lista"][row["IDCotista"]]["Tipo"] = row["Tipo"]
            vv = True
        return vv

    def LoadDictCodRefCotistaFundo(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictCodRefCotistaFundo(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " Codigo,cotista.nome as Cotista,fundo.alias as Fundo,IDCodRefCotistaFundo FROM CodRefCotistaFundo inner join Fundo on CodRefCotistaFundo.idfundo = Fundo.idfundo inner join Cotista on cotista.idcotista = CodRefCotistaFundo.idcotista where codigo like '%" + srch + "%' or fundo.cgc like '%" + srch + "%' or fundo.alias like '%" + srch + "%' or cotista.nome like '%" + srch + "%' order by idcodrefcotistafundo asc) as aux order by idcodrefcotistafundo desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictCodRefCotistaFundo = {}
        self.DictCodRefCotistaFundo['Lista'] = {}
        if len(df)>0:
            self.DictCodRefCotistaFundo['nPags'] = nPags
            self.DictCodRefCotistaFundo['Pag'] = Pag
            self.DictCodRefCotistaFundo['nPerPag'] = nPerPag
            self.DictCodRefCotistaFundo['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDCodRefCotistaFundo"] not in self.DictCodRefCotistaFundo["Lista"]:        
                    self.DictCodRefCotistaFundo["Lista"][row["IDCodRefCotistaFundo"]] = {}
                    self.DictCodRefCotistaFundo["Lista"][row["IDCodRefCotistaFundo"]]["IDCodRefCotistaFundo"] = row["IDCodRefCotistaFundo"]
                    self.DictCodRefCotistaFundo["Lista"][row["IDCodRefCotistaFundo"]]["Codigo"] = row["Codigo"]
                    self.DictCodRefCotistaFundo["Lista"][row["IDCodRefCotistaFundo"]]["Cotista"] = row["Cotista"]
                    self.DictCodRefCotistaFundo["Lista"][row["IDCodRefCotistaFundo"]]["Fundo"] = row["Fundo"]                    
            vv = True
        return vv

    def LoadDictOpcao(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictOpcao(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " * FROM Opcao where Alias like '%" + srch + "%' or Isin like '%" + srch + "%'  order by IdOpcao asc) as aux order by IdOpcao desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictOpcao = {}
        self.DictOpcao['Lista'] = {}
        if len(df)>0:
            self.DictOpcao['nPags'] = nPags
            self.DictOpcao['Pag'] = Pag
            self.DictOpcao['nPerPag'] = nPerPag
            self.DictOpcao['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDOpcao"] not in self.DictOpcao["Lista"]:        
                    self.DictOpcao["Lista"][row["IDOpcao"]] = {}
                    self.DictOpcao["Lista"][row["IDOpcao"]]["IDOpcao"] = row["IDOpcao"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["Alias"] = row["Alias"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["Isin"] = row["Isin"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["Codigo"] = row["Codigo"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["PrecoExercicio"] = row["PrecoExercicio"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["IdMoedaPrecoExercicio"] = row["IdMoedaPrecoExercicio"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["CodVencimento"] = row["CodVencimento"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["CodClassificarInstrumento"] = row["CodClassificarInstrumento"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["TipoOpcao"] = row["TipoOpcao"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["TipoEstilo"] = row["TipoEstilo"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["MultiplicadorContrato"] = row["MultiplicadorContrato"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["Quantidade"] = row["Quantidade"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["LoteAlocacao"] = row["LoteAlocacao"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["PremioPagoAntecip"] = row["PremioPagoAntecip"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["idBolsa"] = row["idBolsa"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["idMoeda"] = row["idMoeda"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["IdTipoMercadoriaOpcao"] = row["IdTipoMercadoriaOpcao"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["DataVencimento"] = row["DataVencimento"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["DatainicioNegociacao"] = row["DatainicioNegociacao"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["DataConclusaoNegociacao"] = row["DataConclusaoNegociacao"]
                    self.DictOpcao["Lista"][row["IDOpcao"]]["DataPosicaoAberto"] = row["DataPosicaoAberto"]              
            vv = True
        return vv

    def LoadDictFuturo(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictFuturo(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " * FROM Futuro where Alias like '%" + srch + "%' or CodIsin like '%" + srch + "%'  order by IdFuturo asc) as aux order by IdFuturo desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictFuturo = {}
        self.DictFuturo['Lista'] = {}
        if len(df)>0:
            self.DictFuturo['nPags'] = nPags
            self.DictFuturo['Pag'] = Pag
            self.DictFuturo['nPerPag'] = nPerPag
            self.DictFuturo['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDFuturo"] not in self.DictFuturo["Lista"]:        
                    self.DictFuturo["Lista"][row["IDFuturo"]] = {}
                    self.DictFuturo["Lista"][row["IDFuturo"]]["IDFuturo"] = row["IDFuturo"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["Alias"] = row["Alias"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["CodIsin"] = row["CodIsin"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["Codigo"] = row["Codigo"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["CodVencimento"] = row["CodVencimento"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["BaseData"] = row["BaseData"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["CriterioConversao"] = row["CriterioConversao"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["NumeroPontosVencimento"] = row["NumeroPontosVencimento"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["TaxaConvertPreco"] = row["TaxaConvertPreco"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["CodClassificacaoInstrumento"] = row["CodClassificacaoInstrumento"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["MultiplicadorContrato"] = row["MultiplicadorContrato"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["Quantidade"] = row["Quantidade"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["LoteAlocacao"] = row["LoteAlocacao"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["IDFuturo"] = row["IDFuturo"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["idMoeda"] = row["idMoeda"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["idBolsa"] = row["idBolsa"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["DataVencimento"] = row["DataVencimento"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["DataInicioNegociacao"] = row["DataInicioNegociacao"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["idTipoMercadoriaFuturo"] = row["idTipoMercadoriaFuturo"]
                    self.DictFuturo["Lista"][row["IDFuturo"]]["DataConclusaoNegociacao"] = row["DataConclusaoNegociacao"]            
            vv = True
        return vv

    def LoadDictRV(self,srch,Pag,nPerPag):
        vv = False
        nCount = self.CountLoadDictRV(srch)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " Alias,Codigo,Isin,QtdEmitida,Lote,idMoeda,idBolsa,idTipoRV,emissor.idEmissor,IDRV,ETF,IBOVESPA,emissor.nome as EmissorNome FROM RV left join emissor on rv.idemissor = emissor.idemissor where Alias like '%" + srch + "%' or Isin like '%" + srch + "%' or Emissor.nome like '%" + srch + "%' order by IdRV asc) as aux order by IdRV desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictRV = {}
        self.DictRV['Lista'] = {}
        if len(df)>0:
            self.DictRV['nPags'] = nPags
            self.DictRV['Pag'] = Pag
            self.DictRV['nPerPag'] = nPerPag
            self.DictRV['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDRV"] not in self.DictRV["Lista"]:        
                    self.DictRV["Lista"][row["IDRV"]] = {}
                    self.DictRV["Lista"][row["IDRV"]]["IDRV"] = row["IDRV"]
                    self.DictRV["Lista"][row["IDRV"]]["Alias"] = row["Alias"]
                    self.DictRV["Lista"][row["IDRV"]]["Codigo"] = row["Codigo"]
                    self.DictRV["Lista"][row["IDRV"]]["Isin"] = row["Isin"]
                    self.DictRV["Lista"][row["IDRV"]]["QtdEmitida"] = row["QtdEmitida"]
                    self.DictRV["Lista"][row["IDRV"]]["Lote"] = row["Lote"]
                    self.DictRV["Lista"][row["IDRV"]]["idMoeda"] = row["idMoeda"]
                    self.DictRV["Lista"][row["IDRV"]]["idBolsa"] = row["idBolsa"]
                    self.DictRV["Lista"][row["IDRV"]]["idTipoRV"] = row["idTipoRV"]
                    self.DictRV["Lista"][row["IDRV"]]["idEmissor"] = row["idEmissor"]
                    self.DictRV["Lista"][row["IDRV"]]["EmissorNome"] = row["EmissorNome"]
                    self.DictRV["Lista"][row["IDRV"]]["ETF"] = row["ETF"]
                    self.DictRV["Lista"][row["IDRV"]]["IBOVESPA"] = row["IBOVESPA"]           
            vv = True
        return vv

    def LoadDictPassivo(self,srch,DataIni,DataFim,Pag,nPerPag,filter_search):
        vv = False
        nCount = self.CountLoadDictPassivo(srch,DataIni,DataFim,filter_search)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " qtdcotas as QtdCotas,fin as Financeiro,passivo.Tipo as TipoCustom,IDPassivo,fundo.alias as Alias,DataCotizacao,DataLiquidacao,DataMovimentacao,codrefcotistafundo.codigo as CodRefCotistaFundo from Passivo inner join codrefcotistafundo on codrefcotistafundo.idcodrefcotistafundo = passivo.idcodrefcotistafundo inner join fundo on fundo.idfundo = codrefcotistafundo.idfundo where passivo.tipo LIKE '%" + filter_search + "%' AND datamovimentacao <= '" + DataFim + "'  and datamovimentacao >= '" + DataIni+ "' and (codrefcotistafundo.codigo like '%" + srch + "%' or fundo.cgc like '%" + srch + "%' or fundo.alias like '%" + srch + "%') order by IdPassivo asc) as aux order by IdPassivo desc"
        df = app.pd.read_sql(query,self.db.engine)
        self.DictPassivo = {}
        self.DictPassivo['Lista'] = {}
        if len(df)>0:
            self.DictPassivo['nPags'] = nPags
            self.DictPassivo['Pag'] = Pag
            self.DictPassivo['nPerPag'] = nPerPag
            self.DictPassivo['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDPassivo"] not in self.DictPassivo["Lista"]:        
                    self.DictPassivo["Lista"][row["IDPassivo"]] = {}
                    self.DictPassivo["Lista"][row["IDPassivo"]]["IDPassivo"] = row["IDPassivo"]
                    self.DictPassivo["Lista"][row["IDPassivo"]]["QtdCotas"] = row["QtdCotas"]
                    self.DictPassivo["Lista"][row["IDPassivo"]]["Financeiro"] = row["Financeiro"]
                    self.DictPassivo["Lista"][row["IDPassivo"]]["TipoCustom"] = row["TipoCustom"]
                    self.DictPassivo["Lista"][row["IDPassivo"]]["Alias"] = row["Alias"]
                    self.DictPassivo["Lista"][row["IDPassivo"]]["DataCotizacao"] = row["DataCotizacao"]
                    self.DictPassivo["Lista"][row["IDPassivo"]]["DataLiquidacao"] = row["DataLiquidacao"]
                    self.DictPassivo["Lista"][row["IDPassivo"]]["DataMovimentacao"] = row["DataMovimentacao"]
                    self.DictPassivo["Lista"][row["IDPassivo"]]["CodRefCotistaFundo"] = row["CodRefCotistaFundo"]         
            vv = True
        return vv    


    def LoadDictMov(self,srch, DataIni, DataFim, IdEstrategia, IdTrader, Pag, nPerPag, CGC):
        vv = False
        nCount = self.CountLoadDictMov(srch,DataIni, DataFim, IdEstrategia, IdTrader,CGC)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        query = """
        Select top """ + str(nPerPag) + """ * from (SELECT top """ + str(nPerPag * Pag) + """ mov.idmov as IDMov,qtd,pu,taxa,aliasativo,datamov,estrategia.nome+'#'+estrategia.grupo as Estrategia,fundo.Alias as AliasFundo 
        from mov left join fundo on fundo.cgc = mov.cgc inner join estrategia on estrategia.idestrategia = mov.idestrategia
        where datamov <= '""" + DataFim + """'
        and datamov >= '""" + DataIni + """'
        and (fundo.alias like '%""" + srch + """%' or mov.aliasativo like '%""" + srch + """%')
        """
        if CGC == '00000000000000': query = query +  "and mov.CGC = '00000000000000'"
        if CGC != '00000000000000': query = query +  "and mov.CGC <> '00000000000000'"
        if int(IdEstrategia) > 0: query = query + " and mov.idestrategia = " + str(IdEstrategia) + " "
        if int(IdTrader) > 0: query = query + " and mov.idTrader = " + str(IdTrader) + " "
        query = query + " order by Idmov asc) as aux order by Idmov desc"        
        df = app.pd.read_sql(query,self.db.engine)
        df.loc[df['taxa'].isna(),'taxa']=0
        self.DictMov = {}
        self.DictMov['Lista'] = {}
        if len(df)>0:
            self.DictMov['nPags'] = nPags
            self.DictMov['Pag'] = Pag
            self.DictMov['nPerPag'] = nPerPag
            self.DictMov['nCount'] = nCount
            for index,row in df.iterrows():
                if row["IDMov"] not in self.DictMov["Lista"]:        
                    self.DictMov["Lista"][row["IDMov"]] = {}
                    self.DictMov["Lista"][row["IDMov"]]["IDMov"] = row["IDMov"]
                    self.DictMov["Lista"][row["IDMov"]]["Qtd"] = row["qtd"]
                    if " DI1 " in row["aliasativo"] : self.DictMov["Lista"][row["IDMov"]]["Qtd"] = -self.DictMov["Lista"][row["IDMov"]]["Qtd"]
                    self.DictMov["Lista"][row["IDMov"]]["Pu"] = row["pu"]
                    self.DictMov["Lista"][row["IDMov"]]["Taxa"] = row["taxa"]
                    self.DictMov["Lista"][row["IDMov"]]["AliasAtivo"] = row["aliasativo"]
                    self.DictMov["Lista"][row["IDMov"]]["datamov"] = row["datamov"]
                    self.DictMov["Lista"][row["IDMov"]]["Estrategia"] = row["Estrategia"]
                    self.DictMov["Lista"][row["IDMov"]]["AliasFundo"] = row["AliasFundo"]        
        vv = True
        return vv    

    def LoadDictBuscarAtivos(self,srch,Pag,nPerPag,Grupo,Tipo):
        vv = False
        nCount = self.CountLoadDictBuscarAtivos(srch,Grupo,Tipo)
        nPags = max(math.ceil(nCount/nPerPag), 1)
        if Grupo == "Cota": query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " fundo.aliascota as codigo,Alias as Tipo,idfundo as id from fundo where fundo.segmento like '%" + Tipo + "%' and (fundo.alias like '%" + srch + "%' or fundo.aliascota like '%" + srch + "%') and fundo.aliascota is not null and fundo.alias <> '' order by Idfundo asc) as aux order by Id desc"
        elif Grupo == "Opcao": query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " Opcao.alias as codigo,tipomercadoriaopcao.nometipomercadoriaopcao as Tipo,opcao.idopcao as id from Opcao left join tipomercadoriaOpcao on tipomercadoriaOpcao.idtipomercadoriaOpcao = Opcao.idtipomercadoriaOpcao where tipomercadoriaOpcao.nometipomercadoriaOpcao like '%" + Tipo + "%' and Opcao.alias like '%" + srch + "%' order by opcao.Idopcao asc) as aux order by Id desc"
        elif Grupo == "Futuro": query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " futuro.alias as codigo,tipomercadoriafuturo.nometipomercadoriafuturo as Tipo,futuro.idfuturo as id from futuro left join tipomercadoriafuturo on tipomercadoriafuturo.idtipomercadoriafuturo = futuro.idtipomercadoriafuturo  where tipomercadoriafuturo.nometipomercadoriafuturo like '%" + Tipo + "%' and futuro.alias like '%" + srch + "%'  order by futuro.idfuturo asc) as aux order by id desc"
        elif Grupo == "RV": query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " rv.alias as codigo,Emissor.Nome as Tipo,rv.idrv as id from rv left join emissor on rv.idemissor = emissor.idEmissor left join tiporv on tiporv.idtiporv = rv.idtiporv  where tiporv.nome like '%" + Tipo + "%' and (emissor.nome like '%" + srch + "%' or rv.alias like '%" + srch + "%') order by rv.Idrv asc) as aux order by Id desc"
        elif Grupo == "RF": query = "Select top " + str(nPerPag) + " * from (SELECT top " + str(nPerPag * Pag) + " rf.alias as codigo,Emissor.Nome as Tipo,rf.idrf as id from rf left join emissor on rf.idemissor = emissor.idEmissor left join tiporf on tiporf.idtiporf = rf.idtiporf  where tiporf.nome like '%" + Tipo + "%' and (emissor.nome like '%" + srch + "%' or rf.alias like '%" + srch + "%') order by rf.Idrf asc) as aux order by Id desc"
        else: return False
        df = app.pd.read_sql(query,self.db.engine)
        self.DictBuscarAtivos = {}
        self.DictBuscarAtivos['Lista'] = {}
        if len(df)>0:
            self.DictBuscarAtivos['nPags'] = nPags
            self.DictBuscarAtivos['Pag'] = Pag
            self.DictBuscarAtivos['nPerPag'] = nPerPag
            self.DictBuscarAtivos['nCount'] = nCount
            for index,row in df.iterrows():
                if row["codigo"] not in self.DictBuscarAtivos["Lista"]:        
                    self.DictBuscarAtivos["Lista"][row["codigo"]] = {}
                    self.DictBuscarAtivos["Lista"][row["codigo"]]["Codigo"] = row["codigo"]
                    self.DictBuscarAtivos["Lista"][row["codigo"]]["Tipo"] = row["Tipo"]
            vv = True
        return vv    

    def LoadDictBuscarAtivosTotal(self,srch,Grupo,Tipo):
        vv = False
        if Grupo == "Cota": query = "Select * from (SELECT * fundo.aliascota as codigo,Alias as Tipo,idfundo as id from fundo where fundo.segmento like '%" + Tipo + "%' and (fundo.alias like '%" + srch + "%' or fundo.aliascota like '%" + srch + "%') and fundo.aliascota is not null and fundo.alias <> '' order by Idfundo asc) as aux order by Id desc"
        elif Grupo == "Opcao": query = "Select * from (SELECT * Opcao.alias as codigo,tipomercadoriaopcao.nometipomercadoriaopcao as Tipo,opcao.idopcao as id from Opcao left join tipomercadoriaOpcao on tipomercadoriaOpcao.idtipomercadoriaOpcao = Opcao.idtipomercadoriaOpcao where tipomercadoriaOpcao.nometipomercadoriaOpcao like '%" + Tipo + "%' and Opcao.alias like '%" + srch + "%' order by opcao.Idopcao asc) as aux order by Id desc"
        elif Grupo == "Futuro": query = "Select * from (SELECT top * futuro.alias as codigo,tipomercadoriafuturo.nometipomercadoriafuturo as Tipo,futuro.idfuturo as id from futuro left join tipomercadoriafuturo on tipomercadoriafuturo.idtipomercadoriafuturo = futuro.idtipomercadoriafuturo  where tipomercadoriafuturo.nometipomercadoriafuturo like '%" + Tipo + "%' and futuro.alias like '%" + srch + "%'  order by futuro.idfuturo asc) as aux order by id desc"
        elif Grupo == "RV": query = "Select * from (SELECT * rv.alias as codigo,Emissor.Nome as Tipo,rv.idrv as id from rv left join emissor on rv.idemissor = emissor.idEmissor left join tiporv on tiporv.idtiporv = rv.idtiporv  where tiporv.nome like '%" + Tipo + "%' and (emissor.nome like '%" + srch + "%' or rv.alias like '%" + srch + "%') order by rv.Idrv asc) as aux order by Id desc"
        elif Grupo == "RF": query = "Select * from (SELECT + rf.alias as codigo,Emissor.Nome as Tipo,rf.idrf as id from rf left join emissor on rf.idemissor = emissor.idEmissor left join tiporf on tiporf.idtiporf = rf.idtiporf  where tiporf.nome like '%" + Tipo + "%' and (emissor.nome like '%" + srch + "%' or rf.alias like '%" + srch + "%') order by rf.Idrf asc) as aux order by Id desc"
        else: return False
        df = app.pd.read_sql(query,self.db.engine)
        self.DictBuscarAtivos = {}
        self.DictBuscarAtivos['ListaTotal'] = {}
        if len(df)>0:
            for index,row in df.iterrows():
                if row["codigo"] not in self.DictBuscarAtivos["ListaTotal"]:        
                    self.DictBuscarAtivos["ListaTotal"][row["codigo"]] = {}
                    self.DictBuscarAtivos["ListaTotal"][row["codigo"]]["Codigo"] = str(row["codigo"])
                    self.DictBuscarAtivos["ListaTotal"][row["codigo"]]["Tipo"] = str(row["Tipo"])
            vv = True
        return vv    

