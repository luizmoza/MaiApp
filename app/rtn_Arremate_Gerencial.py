import sys
import warnings
import codecs
warnings.filterwarnings("ignore")
sys.path.append(r"../")
from app import app
from app.classes.cl_Gerencial import cl_Gerencial

print('Inicio Carga de Dados:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
Gerencial = cl_Gerencial()
dfDados = app.pd.read_excel(r"../Novo_Gerencial.xlsm", 'Dados',skiprows=[0])
dfData = app.pd.read_excel(r"../Novo_Gerencial.xlsm", 'Dt_Param',skiprows=[0])
data = app.dt.strptime(dfData['Data Processamento'].iloc[0].strftime('%Y-%m-%d'),'%Y-%m-%d')
dflistacgcs = app.pd.read_excel(r"../Novo_Gerencial.xlsm", 'Lista_CGCs',skiprows=[0])
listacgcs = []
for index,row in dflistacgcs.iterrows():listacgcs.append(app.tkstr.Right('0000' + str(row['Lista CGCs']),14))
Data = app.pd.to_datetime(data,errors='coerce')
data = app.dt.strptime(data.strftime('%Y-%m-%d'),'%Y-%m-%d')    
strlistacgcs = f'{*listacgcs,}'
dfDados = dfDados.drop(dfDados.columns[26],axis=1)
dfDados = dfDados.drop(dfDados.columns[25],axis=1)
dfDados = dfDados.drop(dfDados.columns[24],axis=1)
dfDados = dfDados.drop(dfDados.columns[23],axis=1)
dfDados = dfDados.drop(dfDados.columns[8],axis=1)
dfDados = dfDados.drop(dfDados.columns[7],axis=1)
dfDados = dfDados.drop(dfDados.columns[6],axis=1)
dfDados = dfDados.drop(dfDados.columns[5],axis=1)
dfDados = dfDados.drop(dfDados.columns[4],axis=1)
dfDados = dfDados.drop(dfDados.columns[3],axis=1)
dfDados = dfDados.drop(dfDados.columns[2],axis=1)
dfDados = dfDados.drop(dfDados.columns[1],axis=1)
dfDados = dfDados.drop(dfDados.columns[0],axis=1)
del dfData
dfDados = app.tkstr.FormatdfCNPJCol(dfDados,'CGC.1')
dfDados = dfDados.groupby(['CGC.1','Ativo.1','Trader','Grupo','Estrat']).agg({
                                                                               'Qtd.1':'sum',
                                                                               'Fin D-1':'sum',
                                                                               'Fin D0':'sum',
                                                                               'Caixa':'sum',
                                                                               'Mltp':'sum',
                                                                               'Result':'sum',
                                                                               'PuD0':'mean',
                                                                               'Pu D-1':'mean',
                                                                               'D+X':'mean'
                                                                                }).reset_index().copy()
dfDados_Fut = dfDados[dfDados['Ativo.1'].str.find("uturo#BRL",1)>0].copy()
dfDados_n_Fut = dfDados[dfDados['Ativo.1'].str.find("uturo#BRL",0)<=0].copy()
dfDados_Fut_FinD0 = dfDados_Fut.groupby(['CGC.1']).agg({'Fin D0':'sum'}).reset_index().copy()
dfDados_Fut_FinD0 = dfDados_Fut_FinD0[dfDados_Fut_FinD0['Fin D0'] != 0].copy()
for index,row in dfDados_Fut_FinD0.iterrows():
    dfDados_n_Fut = app.pd.concat(
        [dfDados_n_Fut,app.pd.DataFrame.from_dict(
            {
            'CGC.1':[row['CGC.1']],
            'Ativo.1':['SPOT#BRLOTC@REAL'],
            'Trader':[3],
            'Grupo':['CPR'],
            'Estrat':['Outras Despesas'],
            'Qtd.1':[row['Fin D0']],
            'Pu D-1':[1],
            'PuD0':[1],
            'Fin D-1':[row['Fin D0']],
            'Fin D0':[row['Fin D0']],
            'Caixa':[0],
            'Mltp':[1],
            'Result':[0],
            'D+X':[0],
            }
            )
            ], ignore_index=True)
dfDados_Fut['Fin D0'] = 0    
dfDados_Fut['Fin D-1'] = 0    
dfDados = app.pd.concat([dfDados_n_Fut.copy(),dfDados_Fut.copy()], ignore_index=True).copy()
del dfDados_Fut_FinD0
del dfDados_n_Fut
del dfDados_Fut
sql = """ select idTrader,Nome as Trader from trader"""
dfTraders = app.pd.read_sql_query(sql, app.db.engine)
sql = """ select 
carteira.CGC,
Alias as AliasFundo,
benchmark,
carteira.pl  as PL
from Fundo inner join carteira on carteira.cgc = fundo.cgc
where carteira.data = '""" + data.strftime('%Y-%m-%d') + """'
"""
dfFundos = app.pd.read_sql_query(sql, app.db.engine)
dfDados = dfDados.rename(columns={
    'CGC.1':'CGC',
    'Ativo.1':'AliasAtivo',
    'Trader':'idTrader',
    'Grupo':'Macro', 
    'Estrat':'Estrat', 
    'Qtd.1':'Quantidade', 
    'Pu D-1':'PuD_1',
    'PuD0':'PuD0',
    'Fin D-1':'FinD1_Aux',
    'Fin D0':'Fin', 
    'Caixa':'Caixa',
    'Mltp':'Mltp',
    'Result':'Resultado', 
    'D+X':'DX'
    }).copy()
dfDados['Data'] = data
dfDados['CGC'] = app.pd.to_numeric(dfDados['CGC']).astype('Int64').astype('str')
dfDados['CGC'] = dfDados['CGC'].apply(lambda x: app.tkstr.right('0000' + x ,14)) 
dfDados = app.pd.merge(left=dfDados, right=dfTraders,how='left',left_on=['idTrader'],right_on=['idTrader']).copy()
dfDados = app.pd.merge(left=dfDados, right=dfFundos,how='left',left_on=['CGC'],right_on=['CGC']).copy()
del dfTraders
del dfFundos
sql = """ select AliasAtivo,AliasFundo,Trader,Macro,Estrat,sum(Fin) as FinD1 
from Gerencial
where data = '""" + app.tkdtm.date_after_work_days(data,-1).strftime('%Y-%m-%d') + """'
group by AliasAtivo,AliasFundo,Trader,Macro,Estrat
"""
dfDadoD_1 = app.pd.read_sql_query(sql, app.db.engine)
dfDadoD_1.loc[dfDadoD_1['Trader']=='3','Trader'] = 'Claudio'
dfDadoD_1.loc[dfDadoD_1['Trader']=='0','Trader'] = 'Claudio'
print('Fim Carga de Dados:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfDados = dfDados[['AliasFundo', 'AliasAtivo','Trader', 'Macro', 'Estrat', 'Quantidade','FinD1_Aux', 'Fin', 'Caixa', 'Mltp', 'Resultado', 'PuD0', 'PuD_1', 'DX', 'Data','CGC' , 'idTrader', 'benchmark', 'PL']].copy()
dfDados = app.pd.merge(left=dfDados, right=dfDadoD_1,how='left',left_on=['AliasFundo','AliasAtivo','Trader','Macro','Estrat'],right_on=['AliasFundo','AliasAtivo','Trader','Macro','Estrat']).copy()
dfDados['FinD1'] = dfDados['FinD1'].fillna(0)
del dfDadoD_1
dfaux = dfDados[['benchmark','AliasFundo']].drop_duplicates().reset_index().copy()
dfaux = app.pd.concat([dfaux.copy(), app.pd.DataFrame.from_dict({'benchmark':['CDI'],'AliasFundo':['Generic']})], ignore_index=True) # append 
dfaux.loc[dfaux['benchmark']=='','benchmark'] = 'CDI'
dfaux.loc[dfaux['benchmark'].isna(),'benchmark'] = 'CDI'
dfaux['IndiceAcumulado'] = dfaux['benchmark'].apply(lambda x: app.tk.CalculaIndiceAcumuladoFormula(x,data,data)) 
dfDados['Indice_Espec'] = 'CDI'
dfaux['IndiceAcumuladoEspecifico'] = dfaux['IndiceAcumulado']
dfDados.loc[dfDados['benchmark'].isna(),'benchmark'] = 'CDI'
dfDados.loc[dfDados['benchmark'] == '','benchmark'] = 'CDI'
dfDados = app.pd.merge(left=dfDados.copy(), right=dfaux[['benchmark','AliasFundo','IndiceAcumulado']].copy(),how='left',left_on=['benchmark','AliasFundo'],right_on=['benchmark','AliasFundo']).copy()
dfaux = dfaux.rename(columns={'benchmark':'Indice_Espec'}).copy()
dfaux = dfaux[['Indice_Espec','IndiceAcumuladoEspecifico']].copy()
dfaux = dfaux.drop_duplicates().reset_index()
dfDados = app.pd.merge(left=dfDados.copy(), right=dfaux[['Indice_Espec','IndiceAcumuladoEspecifico']].copy(),how='left',left_on=['Indice_Espec'],right_on=['Indice_Espec']).copy()
del dfaux
dfDados['Carrego'] = dfDados['IndiceAcumulado'] * dfDados['FinD1'] 
dfDados['Carrego_Espec'] = dfDados['IndiceAcumuladoEspecifico'] * dfDados['FinD1'] 
dfDados['Over_Carrego'] = dfDados['Resultado']-dfDados['Carrego'] 
dfDados['Over_Carrego_Espec'] = dfDados['Resultado']-dfDados['Carrego'] 
dfDados['Perc_Carrego'] = dfDados['Resultado']/dfDados['Carrego'] 
dfDados['Perc_Carregi_Espec'] = dfDados['Resultado']/dfDados['Carrego'] 
dfDados['Perc_PL'] = dfDados['Resultado']/dfDados['PL'] 
dfDados = dfDados.fillna(0)
dfDados.loc[(dfDados['Perc_Carrego']==app.np.inf)|(dfDados['Perc_Carrego']==-app.np.inf),'Perc_Carrego'] = 0
dfDados.loc[(dfDados['Perc_Carregi_Espec']==app.np.inf)|(dfDados['Perc_Carregi_Espec']==-app.np.inf),'Perc_Carregi_Espec'] = 0

print('unBulkando ' + data.strftime('%Y-%m-%d') + ' : ' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfDados = dfDados[['Data','AliasFundo','Trader','AliasAtivo','Macro','Estrat','Quantidade','Fin','FinD1','Resultado','Carrego','Over_Carrego','Carrego_Espec','Over_Carrego_Espec','Perc_Carrego','Perc_Carregi_Espec','PL','Indice_Espec','Perc_PL']]
dfDados_list_aliasfundo = dfDados['AliasFundo'].drop_duplicates().reset_index().copy()
dfDados_list_aliasfundo = dfDados_list_aliasfundo[dfDados_list_aliasfundo['AliasFundo']!=0].copy()
for index,row in dfDados_list_aliasfundo.iterrows():Gerencial.unbulk(
                                                                        dfDados[dfDados['AliasFundo'] == row['AliasFundo']]['Data'].min(),
                                                                        dfDados[dfDados['AliasFundo'] == row['AliasFundo']]['Data'].max(),
                                                                        row['AliasFundo']
                                                                    )
print('Bulkando Data ' + data.strftime('%Y-%m-%d') + ' : ' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
Gerencial.bulk(dfDados)

del dfDados
DataInicio12meses = app.tkdtm.last_workday_last_month(data)
DataInicio12meses = app.tkdtm.last_workday_last_month(DataInicio12meses)
DataInicio12meses = app.tkdtm.last_workday_last_month(DataInicio12meses)
DataInicio12meses = app.tkdtm.last_workday_last_month(DataInicio12meses)
DataInicio12meses = app.tkdtm.last_workday_last_month(DataInicio12meses)
DataInicio12meses = app.tkdtm.last_workday_last_month(DataInicio12meses)
DataInicio12meses = app.tkdtm.last_workday_last_month(DataInicio12meses)
DataInicio12meses = app.tkdtm.last_workday_last_month(DataInicio12meses)
DataInicio12meses = app.tkdtm.last_workday_last_month(DataInicio12meses)
DataInicio12meses = app.tkdtm.last_workday_last_month(DataInicio12meses)
DataInicio12meses = app.tkdtm.last_workday_last_month(DataInicio12meses)
DataInicio12meses = app.tkdtm.last_workday_last_month(DataInicio12meses)
print('Montando Report ' + data.strftime('%Y-%m-%d') + ' : ' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
sql = """
SELECT Data,carteira.CGC,fundo.Alias as AliasFundo,PL,Cota,fundo.benchmark as bench
FROM Carteira inner join fundo on fundo.cgc = Carteira.cgc
where carteira.cgc in """ + strlistacgcs + """
"""
print('Inicio Carga de Dados Casrteiras:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfCarteiras = app.pd.read_sql_query(sql, app.db.engine)
dfdeparaBench =dfCarteiras[['AliasFundo','bench']].copy()
dfdeparaBench = dfdeparaBench.drop_duplicates().reset_index()
dfCarteiras['Data'] = app.pd.to_datetime(dfCarteiras['Data'])
dfCarteiras['D_1'] = app.tkdtm.date_after_work_days(dfCarteiras['Data'],-1)
dfCarteiras_D_1 = dfCarteiras[['Data','Cota','AliasFundo']].copy()
dfCarteiras_D_1 = dfCarteiras_D_1.rename(columns={'Cota':'Cota_D_1','Data':'D_1'}).copy()
dfCarteiras = app.pd.merge(left=dfCarteiras.copy(), right=dfCarteiras_D_1.copy(),how='left',left_on=['D_1','AliasFundo'],right_on=['D_1','AliasFundo']).copy()
dfCarteiras['bps_total'] = (dfCarteiras['Cota']/dfCarteiras['Cota_D_1']-1)*10000
dfCarteiras['bps_total'] = dfCarteiras['bps_total'].fillna(0)
del dfCarteiras_D_1
dfdeparacgcsalias = dfCarteiras[['CGC','AliasFundo']].drop_duplicates().reset_index()
dfCarteiras = dfCarteiras[['Data','AliasFundo','bps_total']]
listaaliasfundo = []
for index,row in dfdeparacgcsalias.iterrows():listaaliasfundo.append(row['AliasFundo'])
strlistaaliasfundo = f'{*listaaliasfundo,}'

print('Limpeza Base:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
app.db.execRawQuery("update Gerencial set macro = 'Crédito' where macro = 'Credito'")
app.db.execRawQuery("update Gerencial set macro = 'Dólar' where macro = 'Dolar'")
app.db.execRawQuery("update Gerencial set macro = 'CPR' where macro = '0'")
app.db.execRawQuery("update Gerencial set estrat = 'Outras Despesas' where Nome = '0'")
app.db.execRawQuery("update Gerencial set estrat = 'Implícita' where estrat = 'Implicita'")
app.db.execRawQuery("update Gerencial set estrat = 'Inclinação' where estrat = 'Inclinacao'")
app.db.execRawQuery("update Gerencial set estrat = 'Termo Ação' where estrat = 'Termo Acao'")
app.db.execRawQuery("update Gerencial set estrat = 'Bancário' where estrat = 'Bancario'")
app.db.execRawQuery("update Gerencial set estrat = 'Renda Fixa - Crédito' where estrat = 'Renda Fixa - Credito'")
app.db.execRawQuery("update Gerencial set estrat = 'Outras Despesas' where estrat = 'Compra de Acoes [D+1]'")
app.db.execRawQuery("update Gerencial set estrat = 'Outras Despesas' where estrat = 'Compra de Acoes [D+2]'")
app.db.execRawQuery("update Gerencial set estrat = 'Outras Despesas' where estrat = 'Compra de Ações [D+1]'")
app.db.execRawQuery("update Gerencial set estrat = 'Outras Despesas' where estrat = 'Compra de Ações [D+2]'")
app.db.execRawQuery("update Gerencial set estrat = 'Outras Despesas' where estrat = 'Venda de Acoes [D+1]'")
app.db.execRawQuery("update Gerencial set estrat = 'Outras Despesas' where estrat = 'Venda de Acoes [D+2]'")
app.db.execRawQuery("update Gerencial set estrat = 'Outras Despesas' where estrat = 'Venda de Ações [D+1]'")
app.db.execRawQuery("update Gerencial set estrat = 'Outras Despesas' where estrat = 'Venda de Ações [D+2]'")

sql = """
SELECT Data,AliasFundo,Trader,AliasAtivo,Macro,Estrat,Fin,FinD1,Resultado,Carrego,Carrego_Espec,PL,Indice_Espec,Perc_PL
FROM Gerencial
where aliasfundo in """ + strlistaaliasfundo + """
and data >= '""" + DataInicio12meses.strftime('%Y-%m-%d') + """'
"""

print('Inicio Carga de Dados Gerencial:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfDados = app.pd.read_sql_query(sql, app.db.engine)

dfDados['bps_Carrego_total'] = dfDados['Carrego']/dfDados['FinD1']*10000
dfDados['bps_Carrego_espec_total'] = dfDados['Carrego_Espec']/dfDados['FinD1']*10000 
dfDados['bps_Carrego_total'] = dfDados['bps_Carrego_total'].fillna(0)
dfDados['bps_Carrego_espec_total'] = dfDados['bps_Carrego_espec_total'].fillna(0)   
dfDados['Data'] = app.pd.to_datetime(dfDados['Data'])
dfDados = app.pd.merge(left=dfDados.copy(), right=dfCarteiras.copy(),how='left',left_on=['Data','AliasFundo'],right_on=['Data','AliasFundo']).copy()
del dfCarteiras
dfDados_subtotal = dfDados[['AliasFundo','Data','Resultado','FinD1']].copy()
dfDados_subtotal = dfDados_subtotal.groupby(['AliasFundo','Data']).agg({'Resultado':'sum','FinD1':'sum'}).reset_index().copy()
dfDados_subtotal = dfDados_subtotal[['AliasFundo','Data','Resultado','FinD1']].copy()
dfDados_subtotal = dfDados_subtotal.rename(columns={'Resultado':'Resultado_total'}).copy()
dfDados_subtotal = dfDados_subtotal.rename(columns={'FinD1':'FinD1_total'}).copy()
dfDados = app.pd.merge(left=dfDados.copy(), right=dfDados_subtotal.copy(),how='left',left_on=['Data','AliasFundo'],right_on=['Data','AliasFundo']).copy()
del dfDados_subtotal
dfDados['perc_resultado'] = dfDados['Resultado']/dfDados['Resultado_total']
dfDados['perc_posD1'] = dfDados['FinD1']/dfDados['FinD1_total']
dfDados['bps'] = dfDados['bps_total'] * dfDados['perc_resultado'] 
dfDados['bps_carrego'] = dfDados['bps_Carrego_total'] * dfDados['perc_posD1'] 
dfDados['bps_Carrego_espec'] = dfDados['bps_Carrego_espec_total'] * dfDados['perc_posD1'] 
dfDados['bps_ob'] = dfDados['bps'] - dfDados['bps_carrego']
dfDados['bps_ob_esp'] = dfDados['bps'] - dfDados['bps_Carrego_espec']
dfDados = dfDados[[
                'Data',
                'AliasFundo',
                'Trader',
                'AliasAtivo',
                'Macro',
                'Estrat',
                'Fin',
                'FinD1',
                'Resultado',
                'Carrego',
                'Carrego_Espec',
                'PL',
                'bps',
                'bps_carrego',
                'bps_Carrego_espec',
                'bps_ob',
                'bps_ob_esp'
                ]].copy()

dfDados['Mes'] = dfDados['Data'].dt.month
dfDados['Ano'] = dfDados['Data'].dt.year
dfDados['Data'] = dfDados['Data'].dt.strftime('%Y-%m-%d')
dfDados = dfDados[dfDados['Ano'] == data.year].copy()
dfDados = dfDados[app.pd.to_datetime(dfDados['Data'])>=app.pd.to_datetime(app.dt.strptime('2024-10-01','%Y-%m-%d'))]
del dfDados['PL']
for index,row in dfdeparaBench.iterrows():
    json_deparaBench = dfdeparaBench.to_json(orient="records")
    json_Dados = dfDados[dfDados['AliasFundo']==row['AliasFundo']].copy().to_json(orient="records")
    print('Inicio Montagem Report HTMLs:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
    if app.tkfm.file_exists(r"../app/templates/Pivot_Table_Template_Individual.html"): 
        pagebody = codecs.open(r"../app/templates/Pivot_Table_Template_Individual.html", encoding="utf-8", errors='xmlcharrefreplace' ).read()
        pagebody = pagebody.replace('{{ Dados }}',json_Dados)
        pagebody = pagebody.replace('{{ AnoBase }}',str(data.year))
        pagebody = pagebody.replace('{{ Fundo }}',row['AliasFundo'])
        pagebody = pagebody.replace('{{ DataBase }}',data.strftime('%Y-%m-%d'))
        pagebody = pagebody.replace('{{ Benchmark }}',row['bench'])
        with open(r"Z:/Banco de Dados/Python/app/ReportsGerencial/Gerencial_" + row['AliasFundo'] + "_" + str(data.year) + ".html", 'w', encoding="utf-8", errors='xmlcharrefreplace' ) as f: f.write(pagebody)   
    else:
        print('Erro ao Carregar Template')
print('Fim Montagem Report HTML:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))









