from app import app
import os
import glob
import time

class cl_tk:
    def __init__(self):
        self.server_path = 'localhost:5000'
        self.db = app.db
        self.root = str(app.pathlib.Path().resolve())
        self.PathFileDashboard = self.root +  r"\app"
        self.PathProfileImages = self.root +  r"\app\static\images\UserProfile"

    def generate_guid(self):
         query = """SELECT NEWID() as id"""
         AUX = app.pd.read_sql(query,self.db.engine)
         return AUX['id'][0]

    def calcula_acumulado_grupos(self,df_grupo):
        df_grupo_calculado = df_grupo.sort_values(by = 'Data', ascending = True)
        rent = list(df_grupo_calculado['rent'])
        rent_acum = list(df_grupo_calculado['rent_acum'])
        if rent_acum[0] == 0.0:
            rent_acum[0] = 1 / (1+rent[0])
        for i in range(1, len(rent)):
            if rent_acum[i-1]<0: rent_acum[i] = ((1 - rent[i]) * rent_acum[i-1])
            else:rent_acum[i] = ((1 + rent[i]) * rent_acum[i-1])
        df_grupo_calculado['rent_acum'] = rent_acum
        return df_grupo_calculado       

    def Calcula_Acumulado_lst_groups(self,df,lst):
        df = df.groupby(by = lst)
        resultado = df.apply(self.calcula_acumulado_grupos)
        return resultado
    
    def ParseObjectDict(self,obj): 
        dict = app.copy.deepcopy(obj.__dict__)
        a = dict.pop(next(iter(dict))) ## Tira o tipo do objeto da primeira posição do dicionário
        a = {}
        for keys, values in dict.items(): ## Limpa Nulos
            if values is not None:
                a[keys] = values
        return a
    
    def ParseNewObjectDict(self,obj):
        dict = app.copy.deepcopy(obj.__dict__)
        a = dict.pop(next(iter(dict)))## Tira o tipo do objeto da primeira posição do dicionário
        del dict[obj.__pk__[0]] 
        a = {}
        for keys, values in dict.items(): ## Limpa Nulos
            if values is not None:
                a[keys] = values
        return a

    def GetIdObject(self,obj):
        return getattr(self,obj.__pk__[0])

    def GetIdObjectDict(self,dict):
        i=0
        for keys, values in dict.items(): #assumindo que o ID da Tabela é o primeiro da lista!(depois da tag do objeto)
            i = i+1
            if i==2: return values

    def cria_pasta_se_nao_existe(self,pasta):
        if not os.path.exists(pasta):
            os.mkdir(pasta)

    def deleta_pasta(self,pasta):
        if os.path.exists(pasta):
            if len(self.monta_arr_arquivos(pasta)) > 0:
                self.formata_pasta(pasta)
            os.rmdir(pasta)

    def deleta_arquivos_pasta(self,pasta):
        if os.path.exists(pasta):
            for arquivo in self.monta_arr_arquivos(pasta):
                if os.path.isfile(arquivo):
                    os.unlink(arquivo)

    def formata_pasta(self,caminho):
        if os.path.isfile(caminho):
            os.unlink(caminho)
        elif os.path.isdir(caminho):
            for item in glob.glob(os.path.join(caminho, '*')):
                self.formata_pasta(item)
            os.rmdir(caminho)

    def deleta_arquivo(self,arquivo):
        if os.path.isfile(arquivo):
            os.unlink(arquivo)

    def monta_arr_arquivos(self,pasta):
        if os.path.exists(pasta):
            return glob.glob(os.path.join(pasta, '*'))

    def monta_dict_arquivos(self,pasta):
        arr_arquivos = self.monta_arr_arquivos(pasta)
        arquivo_info = {}
        for arquivo in arr_arquivos:
            arquivo_info[arquivo] = {
                'size': os.path.getsize(arquivo),
                'modified': time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(os.path.getmtime(arquivo))),
                'url': os.path.join(WWW, arquivo.replace("\\", "/"))
            }
        return arquivo_info
    
    def format_date_sql(date_sql):
        ano = date_sql[6:]
        mes = date_sql[3:-5]
        dia = date_sql[: -8]
        return f"{ano}-{mes}-{dia}"

    def format_date_sql_from_timestamp(dt):
        date_sql = dt.strftime('%d/%m/%Y')
        ano = date_sql[6:]
        mes = date_sql[3:-5]
        dia = date_sql[: -8]
        return f"{ano}-{mes}-{dia}"

    def round_up(number, precision=2):
        fig = int('1' + '0' * precision)
        return round(number * fig) / fig

    def exists_in_arr(self, arr, s):
        return s in arr

    def exists_in_dict(self, my_dict, s):
        return s in my_dict

    def remove_numeric_keys(self, my_dict):
        return {k: v for k, v in my_dict.items() if not isinstance(k, (int, float))}
    
    def CarregaNumeroIndice(self,Indice,data):
        sql = """
        Select numeroindice
        from Fechamentoindice inner join indice on fechamentoindice.idindice = indice.idindice 
        where data = '""" + data.strftime('%Y-%m-%d') + """'  and NomeIndice = '""" + Indice + """' order by idfechamentoindice asc """    
        df = app.pd.read_sql_query(sql, app.db.engine)
        df = df.drop_duplicates(keep='last')
        return app.pd.to_numeric(df['numeroindice'].iloc[0])
        

    def CalculaIndiceAcumulado(self,indice,dataini,datafim,perc=0,aditivo=0):
        if aditivo != 0 : 
            aditivo = ((1 + aditivo)**(1 / 252)) - 1
        if perc == 0: perc = 1
        CarregaindiceAcumulado = 1
        sql = """
        Select data,taxa as valor 
        from Fechamentoindice inner join indice on fechamentoindice.idindice = indice.idindice 
        where data >= '""" + dataini.strftime('%Y-%m-%d') + """' 
        and data <= '""" + datafim.strftime('%Y-%m-%d') +  """' and NomeIndice = '""" + indice + """' order by data asc"""
        df = app.pd.read_sql_query(sql, app.db.engine)
        existemvaloresparadatainicial = False
        existemvaloresparadatafinal = False
        for index, row in df.iterrows():
            if not (row["valor"] is None): CarregaindiceAcumulado = CarregaindiceAcumulado * (1 + ((row["valor"]) * perc) + aditivo)
            if not (row["data"] is None):
                if app.pd.to_datetime(row["data"]) == app.pd.to_datetime(dataini): existemvaloresparadatainicial = True
                if app.pd.to_datetime(row["data"]) == app.pd.to_datetime(datafim): existemvaloresparadatafinal = True
        if existemvaloresparadatafinal and existemvaloresparadatainicial:
            return  CarregaindiceAcumulado - 1
        else:
            return  "Não Disponível"
        
    def CarregaindiceCompostoAcumulado(self,Indice,dataini,datafim,perc = 1,aditivo = 0,Indice2 = None,perc2 = 1,aditivo2 = 0,Indice3 = None,perc3 = 1,aditivo3 = 0):
        if aditivo3 == None : aditivo3 = 0
        if aditivo2 == None : aditivo2 = 0
        if perc3 == None : perc3 = 1
        if perc2 == None : perc2 = 1
        if Indice2 == None : Indice2 = ''
        if Indice3 == None : Indice3 = ''
        if aditivo != 0 :aditivo = ((1 + aditivo) ** (1 / 252)) - 1
        if aditivo2 != 0: aditivo2 = ((1 + aditivo2) ** (1 / 252)) - 1
        if aditivo3 != 0 : aditivo3 = ((1 + aditivo3) ** (1 / 252)) - 1
        if perc == 0:  
            if perc2 == 0: 
                if perc3 == 0 : perc = 1
        sql = """ 
        Select 
        Data,
        indice.nomeindice as indice,
        taxa as valor 
        from Fechamentoindice 
        inner join indice on fechamentoindice.idindice = indice.idindice 
        where Data >= '""" + dataini.strftime('%Y-%m-%d') + """' 
        and Data <= '""" + datafim.strftime('%Y-%m-%d') + """' 
        and NomeIndice in ('""" + Indice + """',"""
        if not Indice2 is None: sql = sql + """'"""  + Indice2 + """',""" 
        if not Indice3 is None: sql = sql + """'"""  + Indice3 + """',""" 
        sql = app.tkstr.left(sql,app.tkstr.Len(sql)-1)
        sql = sql + """)"""
        df = app.pd.read_sql_query(sql, app.db.engine)
        dfindice1 = df[df['indice']==Indice].copy()
        dfindice2 = df[df['indice']==Indice2].copy()
        dfindice2 = dfindice2.rename(columns={'valor':'valor2','indice':'indice2','indice':'indice2'}).copy()
        dfindice3 = df[df['indice']==Indice3].copy()
        dfindice3 = dfindice3.rename(columns={'valor':'valor3','indice':'indice3','indice':'indice3'}).copy()
        df = app.pd.merge(left=dfindice1, right=dfindice2,how='left',left_on=['Data'],right_on=['Data']).copy()
        df = app.pd.merge(left=df, right=dfindice3,how='left',left_on=['Data'],right_on=['Data']).copy()
        df['valor2'] = df['valor2'].fillna(0) 
        df['valor3'] = df['valor3'].fillna(0) 
        df['valor'] = df['valor'].fillna(0) 
        del dfindice1
        del dfindice3
        del dfindice2
        df['rent'] = (((app.pd.to_numeric(df['valor']) + aditivo) * perc) + ((app.pd.to_numeric(df['valor2']) + aditivo2) * perc2) + (((app.pd.to_numeric(df['valor3'])) + aditivo3) * perc3))
        df['rent_acum'] = 0
        df['DSC_CONTA'] = 'IndiceComposto'
        dfcalc = self.Calcula_Acumulado_lst_groups(df,['DSC_CONTA'])
        return  dfcalc[ app.pd.to_datetime(dfcalc['Data']) == app.pd.to_datetime(datafim) ]['rent'].iloc[0]


    def CarregaindiceCompostoAcumulado_full(self,Indice,dataini,datafim,perc = 1,aditivo = 0,Indice2 = None,perc2 = 1,aditivo2 = 0,Indice3 = None,perc3 = 1,aditivo3 = 0):
        
        if aditivo3 == None : aditivo3 = 0
        if aditivo2 == None : aditivo2 = 0
        if perc3 == None : perc3 = 1
        if perc2 == None : perc2 = 1
        if Indice2 == None : Indice2 = ''
        if Indice3 == None : Indice3 = ''
        
        if aditivo != 0 :aditivo = ((1 + aditivo) ** (1 / 252)) - 1
        if aditivo2 != 0: aditivo2 = ((1 + aditivo2) ** (1 / 252)) - 1
        if aditivo3 != 0 : aditivo3 = ((1 + aditivo3) ** (1 / 252)) - 1
        if perc == 0:  
            if perc2 == 0: 
                if perc3 == 0 : perc = 1
        sql = """ 
        Select 
        Data,
        indice.nomeindice as indice,
        taxa as valor 
        from Fechamentoindice 
        inner join indice on fechamentoindice.idindice = indice.idindice 
        where Data >= '""" + dataini.strftime('%Y-%m-%d') + """' 
        and Data <= '""" + datafim.strftime('%Y-%m-%d') + """' 
        and NomeIndice in ('""" + Indice + """',"""
        if not Indice2 is None: sql = sql + """'"""  + Indice2 + """',""" 
        if not Indice3 is None: sql = sql + """'"""  + Indice3 + """',""" 
        sql = app.tkstr.left(sql,app.tkstr.Len(sql)-1)
        sql = sql + """)"""
        df = app.pd.read_sql_query(sql, app.db.engine)
        dfindice1 = df[df['indice']==Indice].copy()
        dfindice2 = df[df['indice']==Indice2].copy()
        dfindice2 = dfindice2.rename(columns={'valor':'valor2','indice':'indice2','indice':'indice2'}).copy()
        dfindice3 = df[df['indice']==Indice3].copy()
        dfindice3 = dfindice3.rename(columns={'valor':'valor3','indice':'indice3','indice':'indice3'}).copy()
        df = app.pd.merge(left=dfindice1, right=dfindice2,how='left',left_on=['Data'],right_on=['Data']).copy()
        df = app.pd.merge(left=df, right=dfindice3,how='left',left_on=['Data'],right_on=['Data']).copy()
        df['valor2'] = df['valor2'].fillna(0) 
        df['valor3'] = df['valor3'].fillna(0) 
        df['valor'] = df['valor'].fillna(0) 
        del dfindice1
        del dfindice3
        del dfindice2
        df['rent'] = (((app.pd.to_numeric(df['valor']) + aditivo) * perc) + ((app.pd.to_numeric(df['valor2']) + aditivo2) * perc2) + (((app.pd.to_numeric(df['valor3'])) + aditivo3) * perc3))
        df['rent_acum'] = 0
        df['DSC_CONTA'] = 'IndiceComposto'
        dfcalc = self.Calcula_Acumulado_lst_groups(df,['DSC_CONTA'])
        return  dfcalc



    def IndiceValido(self,Indice):
        sql = """
        Select 
        nomeindice
        from indice 
        where NomeIndice in ('""" + Indice + """')"""
        df = app.pd.read_sql_query(sql, app.db.engine)
        return len(df)>0

    def ReconheceFuncao(self,s):
        if app.tkstr.Instr(1, s, "(") > 0 :
            return app.tkstr.Left(s, app.tkstr.Instr(1, s, "(") - 1)
        else:
            return "Erro"


    def MontaDictArgumentosFuncao(self,s): 
        s = s.upper()
        dict = {}
        if app.tkstr.Instr(1, s, "=") != 0: return dict
        if app.tkstr.Instr(1, s, "=") == 0:
            if app.tkstr.Instr(1, s, "(") > 0:
                if app.tkstr.Instr(1, s, ")") > 0:
                    func = app.tkstr.Left(s, app.tkstr.Instr(1, s, "("))
                    s = app.tkstr.Right(s, app.tkstr.Len(s) - app.tkstr.Instr(1, s, "(")-1)
                    s = app.tkstr.Left(s, app.tkstr.Instr(1, s, ")"))
                    ssplit = s.split(";")
                    dict[0] = func
                    i=0
                    for k in ssplit:
                        i=i+1
                        dict[i] = k
        return dict

    def CalculaIndiceAcumuladoFormula(self,s,dataini,datafim):
        s = s.upper()
        Indice = None
        perc = 1
        aditivo = 0
        Indice2 = None
        perc2 = 1
        aditivo2 = 0
        Indice3 = None
        perc3 = 1
        aditivo3 = 0
        if app.tkstr.Instr(1, s, " ") != 0 : return 'Erro de Formula1'
        if app.tkstr.Instr(1, s, "(") != 0 and app.tkstr.Instr(1, s, ")") == 0 : return 'Erro de Formula2'
        if app.tkstr.Instr(1, s, "(") == 0 and app.tkstr.Instr(1, s, ")") != 0 : return 'Erro de Formula3'

        if self.IndiceValido(s):
            aditivo3 = None
            aditivo2 = None
            perc3 = None
            perc2 = None
            Indice3 = None
            Indice2 = None
            Indice = s
        else:
            dict = self.MontaDictArgumentosFuncao(s)
            if dict[0] == 'BENCHCOMPOSTO':
                if 1 in dict : Indice = dict[1]
                if 2 in dict : perc = dict[2]
                if 3 in dict : aditivo = dict[3]
                if 4 in dict : Indice2 = dict[4]
                if 5 in dict : perc2 = dict[5]
                if 6 in dict : aditivo2 = dict[6]
                if 7 in dict : Indice3 = dict[7]
                if 8 in dict : perc3 = dict[8]
                if 9 in dict : aditivo3 = dict[9]
            else:
                return 'erro! Formula!'
            
        if type(perc) == str:
            perc = perc.replace(',','.')
            if app.tkstr.Right(perc, 1) == "%" : 
                perc = app.pd.to_numeric(app.tkstr.Left(perc, app.tkstr.Len(perc) - 1)) / 100     
            else:
                perc = app.pd.to_numeric(perc)

        if type(aditivo) == str:
            aditivo = aditivo.replace(',','.')
            if app.tkstr.Right(aditivo, 1) == "%" : 
                aditivo = app.pd.to_numeric(app.tkstr.Left(aditivo, app.tkstr.Len(aditivo) - 1)) / 100       
            else:
                aditivo = app.pd.to_numeric(aditivo) 

        if type(perc2) == str:
            perc2 = perc2.replace(',','.')
            if app.tkstr.Right(perc2, 1) == "%" : 
                perc2 = app.pd.to_numeric(app.tkstr.Left(perc2, app.tkstr.Len(perc2) - 1)) / 100
            else:
                perc2 = app.pd.to_numeric(perc2) 

        if type(aditivo2) == str:
            aditivo2 = aditivo2.replace(',','.')
            if app.tkstr.Right(aditivo2, 1) == "%" : 
                aditivo2 = app.pd.to_numeric(app.tkstr.Left(aditivo2, app.tkstr.Len(aditivo2) - 1)) / 100
            else:
                aditivo2 = app.pd.to_numeric(aditivo2)

        if type(perc3) == str:
            perc3 = perc3.replace(',','.')
            if app.tkstr.Right(perc3, 1) == "%" : 
                perc3 = app.pd.to_numeric(app.tkstr.Left(perc3, app.tkstr.Len(perc3) - 1)) / 100
            else:
                perc3 = app.pd.to_numeric(perc3) 

        if type(aditivo3) == str:
            aditivo3 = aditivo3.replace(',','.')
            if app.tkstr.Right(aditivo3, 1) == "%" : 
                aditivo3 = app.pd.to_numeric(app.tkstr.Left(aditivo3, app.tkstr.Len(aditivo3) - 1)) / 100
            else:
                aditivo3 = app.pd.to_numeric(aditivo3)

        return self.CarregaindiceCompostoAcumulado(Indice, dataini, datafim, perc, aditivo, Indice2, perc2, aditivo2, Indice3, perc3, aditivo3)



        

