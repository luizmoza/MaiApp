import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.append(r"../")
from app import app
from app.classes.cl_Mov import cl_Mov

################################################################################################################################
##################################### Coletando Dados do Pré Processamento  ##################################################
print('Buscando parametros de processamento:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
app.db.execRawQuery("update mov set AliasOperacao = '' where AliasOperacao is null")
dictNotMTM = app.pd.read_excel(r"../Novo_Gerencial.xlsm", 'Aux',skiprows=[0])
dfData = app.pd.read_excel(r"../Novo_Gerencial.xlsm", 'Dt_Param',skiprows=[0])
dfRendimentos = app.pd.read_excel(r"../Novo_Gerencial.xlsm", 'QTLink')
dflistacgcs = app.pd.read_excel(r"../Novo_Gerencial.xlsm", 'Lista_CGCs',skiprows=[0])
data = app.pd.to_datetime(dfData['Data Processamento'].iloc[0],errors='coerce')
listacgcs = []
for index,row in dflistacgcs.iterrows():
    listacgcs.append(app.tkstr.Right('0000' + str(row['Lista CGCs']),14))
dictNotMTM['NotMTMAtivo']= True
def is_valid_date(dt):
    vv = True
    try:
        year = dt.year
        month = dt.month
        day = dt.day
        day_count_for_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if year%4==0 and (year%100 != 0 or year%400==0):
            day_count_for_month[2] = 29
        return (1 <= month <= 12 and 1 <= day <= day_count_for_month[month])
    except:
        vv = False
    return vv
        
if not is_valid_date(data): 
    print('Data Não é Valida: Utilizando D-2')
    data = app.tkdtm.date_after_work_days(app.tkdtm.hoje,-2)
else:
    print('Data utilizada: ' + data.strftime('%Y-%m-%d'))  
data = app.dt.strptime(data.strftime('%Y-%m-%d'),'%Y-%m-%d')    
strlistacgcs = f'{*listacgcs,}'



#strlistacgcs = "('14550994000124')"



print('Processando ... :' + strlistacgcs)
##################################### Coletando Dados do Pré Processamento  ##################################################
################################################################################################################################
############################################### Antes de Começar ###############################################################
#Verifica se existe algum apontamento de cadastro... se existir para aqui!!
#Verifica se existe algum apontamento de pos Vs sum(mov) !! se existir para aqui!!
#Verifica se existe Apontamento False Call de Clean Dialy !! se não existir para aqui!!
#Verifica se todas as cotas de fundos em posição tem boletas (Com Estratégias associadas a elas) ou cadastro na planilha!!!!!
################################################################################################################################
######################################## Ajuste Posição Dividendos e Alugueis ##################################################


# ### Apagar essa linha quando for para rodar a vera....
#strlistacgcs = "('42494899000196','14550994000124')"
# ### Apagar essa linha quando for para rodar a vera....


def stringcontainsnumericcar(s):
    vv = False
    for x in s:
        if x.isnumeric():
            vv = True
    return vv

def stringonlyupper(s):
    vv = False
    for x in s:
        if x == x.upper():
            vv = True
    return vv

def has_special_char(text: str) -> bool:
    return any(c for c in text if not c.isalnum() and not c.isspace())


def checkposrowisunique(row) -> bool:
    sql = "select * from posicao where data = '" + row['Data'].strftime('%Y-%m-%d') + "'"
    sql = sql + " and cgc = '" + row['CGC'] + "'"
    sql = sql + " and AliasOperacao = '" + row['AliasOperacao'] + "'"
    df = app.pd.read_sql_query(sql, app.db.engine)
    if len(df)==1:
        return True
    else:
        return False


def zeraresultadolinhaposicao(row) -> bool:
    sql = "select * from posicao where data = '" + row['Data'].strftime('%Y-%m-%d') + "'"
    sql = sql + " and cgc = '" + row['CGC'] + "'"
    sql = sql + " and AliasOperacao = '" + row['AliasOperacao'] + "'"
    df = app.pd.read_sql_query(sql, app.db.engine)
    if len(df)==1:
        if app.db.isConnected() == False:app.db.connect()
        sql = "Update posicao set Resultado = 0 where data = '" + row['Data'].strftime('%Y-%m-%d') + "'"
        sql = sql + " and cgc = '" + row['CGC'] + "'"
        sql = sql + " and AliasOperacao = '" + row['AliasOperacao'] + "'"
        app.db.execRawQuery(sql) 
    else:
        return False

def inserelinhaposicao(row,k,newop) -> bool:
    sql = "select * from Posicao where data = '" + row['Data'].strftime('%Y-%m-%d') + "'"
    sql = sql + " and cgc = '" + row['CGC'] + "'"
    sql = sql + " and AliasOperacao = '" + row['AliasOperacao'] + "'"
    dfold = app.pd.read_sql_query(sql, app.db.engine)
    del dfold['IDPosicao']
    sql = "select * from Posicao where data = '" + row['Data'].strftime('%Y-%m-%d') + "'"
    sql = sql + " and cgc = '" + row['CGC'] + "'"
    sql = sql + " and AliasOperacao = '" + newop + "'"
    dfnew = app.pd.read_sql_query(sql, app.db.engine)
    if len(dfnew)==0:
        if len(dfold)==1:
                dfold['AliasOperacao'] = newop
                dfold['AliasAtivo'] = k
                dfold['Qtd'] = 0
                dfold['Pu'] = 0
                dfold['VL'] = 0
                dfold['CPR'] = 0
                dfold['Caixa'] = 0
                dfold['Qtd1'] = 0
                dfold['Pu1'] = 0
                dfold['VL1'] = 0
                dfold['CPR1'] = 0
                dfold['Caixa1'] = 0
                dfold['Fin1'] = 0
                dfold['Fin'] = 0
                dfold.to_sql('Posicao', app.db.engine, if_exists='append', index=False)
                return True
        else:
            return False
    else:
        if len(dfold)==1:
            if app.db.isConnected() == False:app.db.connect()
            sql = "update Posicao set Resultado = Resultado + '" + ("{:10.4f}".format(dfold['Resultado'].iloc[0])) + "' where data = '" + row['Data'].strftime('%Y-%m-%d') + "'"
            sql = sql + " and cgc = '" + row['CGC'] + "'"
            sql = sql + " and AliasOperacao = '" + newop + "'"
            app.db.execRawQuery(sql) 
        else:
            return False
    return True

def inserteoperacaonovasenaoexistir(row,k,newop) -> bool:
    sql = "select * from operacao where "
    sql = sql + " cgc = '" + row['CGC'] + "'"
    sql = sql + " and AliasOperacao = '" + row['AliasOperacao'] + "'"
    dfold = app.pd.read_sql_query(sql, app.db.engine)
    if len(dfold)==1:
        sql = "select * from operacao where "
        sql = sql + " cgc = '" + row['CGC'] + "'"
        sql = sql + " and AliasOperacao = '" + newop + "'"
        dfnew = app.pd.read_sql_query(sql, app.db.engine)
        if len(dfnew)==0:
            dfold['AliasOperacao'] = newop
            dfold['AliasAtivo'] = k
            dfold.to_sql('Operacao', app.db.engine, if_exists='append', index=False)
            return True
        else:
            return True
    else:
        return False



sql = """
SELECT Posicao.Data
  ,Posicao.CGC
  ,Posicao.AliasAtivo
 	  ,operacao.AliasAtivo
  ,Posicao.AliasOperacao
  ,Posicao.Qtd
  ,Posicao.Pu
  ,Posicao.VL
  ,Posicao.CPR
  ,Posicao.Caixa
  ,Posicao.Fin
  ,Posicao.Qtd1
  ,Posicao.Pu1
  ,Posicao.VL1
  ,Posicao.CPR1
  ,Posicao.Caixa1
  ,Posicao.Fin1
  ,Posicao.Resultado
  ,Posicao.CorretagemFut
  ,Posicao.CorretagemAVista
  ,Posicao.MovQtd
  ,Posicao.MovPu
  ,Posicao.Mov
  ,Posicao.Validador
  ,Posicao.Justificativa
  FROM  Posicao
  inner join operacao on operacao.cgc = posicao.cgc and operacao.AliasOperacao = posicao.AliasOperacao
  where posicao.cgc in """ + strlistacgcs + """ 
  and posicao.data = '""" + data.strftime('%Y-%m-%d') + """'
  and operacao.AliasAtivo = 'SPOT#BRLOTC@REAL'
  and (
  posicao.AliasOperacao like '%Receb%Juros%'
  or
  posicao.AliasOperacao like '%Receb%Divid%'
  or
  posicao.AliasOperacao like '%Dividendos %'
  or
  posicao.AliasOperacao like '%Empréstimo de Ações a Receber para o papel%'
  or
  posicao.AliasOperacao like '%Empr. de Ações a receber para o papel%'
  or
  posicao.AliasOperacao like '%Empr. de Ações a receber para o papel%'
  )
  and Resultado <> 0
"""
dfeventoscorporativosposicao = app.pd.read_sql_query(sql, app.db.engine)

for index,row in dfeventoscorporativosposicao.iterrows():
    saliasoperacao = row['AliasOperacao'].split()
    for k in saliasoperacao:
        vvonlyupper = stringonlyupper(k)
        vvcontainsnumeric = stringcontainsnumericcar(k)
        if vvonlyupper and vvcontainsnumeric and (not has_special_char(k)):
            k = "RV#BRLB3@" + k
            if checkposrowisunique(row):
                if 'Juros' in row['AliasOperacao']: 
                    newop='JSCP :' + k 
                elif 'Divid' in row['AliasOperacao']: 
                    newop='Dividendos :' + k 
                elif 'Empr' in row['AliasOperacao']: 
                    newop='Emprestimos :' + k 
                else: 
                    newop='EventoCorporativo :' + k 
                print('Começando Tratamento : ' + newop)
#                sys.exit('Para1')
                if inserteoperacaonovasenaoexistir(row,k,newop):
                    if inserelinhaposicao(row,k,newop):
                        if zeraresultadolinhaposicao(row):
                            print( k + 'Tratado com sucesso!')


#sys.exit('Para!')


######################################## Ajuste Posição Dividendos e Alugueis ##################################################
################################################################################################################################



############################################### Antes de Começar ###############################################################
################################################################################################################################
###############################################################################################################################
############################################### Caixa Rendimentos Quantun #####################################################
dfRendimentos['Data'] = app.pd.to_datetime(dfRendimentos['Data'],errors='coerce')
dfRendimentos = dfRendimentos.rename(columns={"Retorno":'Rent','Preço de Fechamento Não ajustados':'Pu','Código':'Codigo'}).copy()
dfRendimentos['Pu'] = dfRendimentos['Pu'].ffill()
dfRendimentos = dfRendimentos[dfRendimentos['Pu'].isna()==False]
dfPusRends = dfRendimentos[['Codigo','Data','Pu']].copy()
dfPusRends['D+1'] = app.tkdtm.date_after_work_days(dfPusRends['Data'],1)
dfPusRends = app.pd.merge(left=dfPusRends.copy(), right=dfPusRends.copy(),how='left',left_on=['Codigo','Data'],right_on=['Codigo','D+1']).copy()
dfPusRends = dfPusRends.rename(columns={"Data_x":'Data','Data_y':'D-1','Pu_x':'Pu','Pu_y':'Pu_D-1'}).copy()
dfPusRends = dfPusRends[['Data','Codigo','D-1','Pu','Pu_D-1']]
dfPusRends = dfPusRends[dfPusRends['D-1'].isna()==False]
dfPusRends['VarPu'] = dfPusRends['Pu']/dfPusRends['Pu_D-1']-1
dfPusRends['VarPu'] = dfPusRends['VarPu'].fillna(0)
del dfRendimentos['Pu']
dfRendimentos = app.pd.merge(left=dfRendimentos.copy(), right=dfPusRends.copy(),how='right',left_on=['Codigo','Data'],right_on=['Codigo','Data']).copy()
del dfPusRends
dfRendimentos['Prov'] = abs(dfRendimentos['VarPu']-dfRendimentos['Rent'])>0.000001
dfRendimentos = dfRendimentos[dfRendimentos['Prov']]
dfRendimentos['AliasAtivo'] = 'RV#BRLB3@' + dfRendimentos['Codigo']
dfRendimentos = dfRendimentos[['AliasAtivo','Data','Rent']].copy()
############################################### Caixa Rendimentos Quantun #####################################################
###############################################################################################################################
################################################################################################################################
############################################### Carga de preços da data base ###################################################
print('Iniciando Carga de preços e Multiplicadores:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
sql = """ select nome,idestrategia,grupo from estrategia """
dictEstrategias = app.pd.read_sql_query(sql, app.db.engine)
dictEstrategias = dictEstrategias.drop_duplicates(subset=['grupo','nome'],keep='last').reset_index()
if 'index' in dictEstrategias.columns: del dictEstrategias['index']
sql = """ 
select distinct Alias as AliasAtivo,Ajuste as Mltpl,preco as PUD0,pud1 as PUD_1  
FROM PrecosMTM 
where ajuste <> 0 
and data = '""" + app.dt.strftime(app.tkdtm.date_after_work_days(data, 0), "%Y-%m-%d") + """'
"""
dictPrecosMTM = app.pd.read_sql_query(sql, app.db.engine)
dictMtlpl = dictPrecosMTM[['AliasAtivo','Mltpl']].copy()
dictPuD_1 = dictPrecosMTM[['AliasAtivo','PUD_1']].copy()
dictPuD0 = dictPrecosMTM[['AliasAtivo','PUD0']].copy()
del dictPrecosMTM
sql = """ 
select distinct Alias as AliasAtivo,Ajuste as Mltpl,preco as PUD_1
FROM PrecosMTM 
where ajuste <> 0 
and data = '""" + app.dt.strftime(app.tkdtm.date_after_work_days(data, -1), "%Y-%m-%d") + """'
"""
dictPuD_1_aux = app.pd.read_sql_query(sql, app.db.engine)
dictPuD_1_aux = dictPuD_1_aux[['AliasAtivo','PUD_1']]
dictPuD_1 = app.pd.concat([dictPuD_1_aux , dictPuD_1], ignore_index=True) # append 
dictPuD_1 = dictPuD_1[dictPuD_1['PUD_1']!=0].copy()
dictPuD_1 = dictPuD_1.drop_duplicates(subset=['AliasAtivo'], keep='last').reset_index()
del dictPuD_1_aux
dictPuD_1 = dictPuD_1[dictPuD_1['PUD_1'].isna()==False].copy()
dictPuD0 = dictPuD0[dictPuD0['PUD0'].isna()==False].copy()
dictPuD_1 = dictPuD_1.rename(columns={"PUD_1": "XPUD_1"}).copy()
dictPuD0 = dictPuD0.rename(columns={"PUD0": "XPUD0"}).copy()
sql = """
Select data,vl,pu as PUD0,pu1 as PUD_1,qtd,qtd1,fin,fin1,vl1,
operacao.cgc as CGC,
operacao.aliasoperacao as AliasOperacao,
data,operacao.aliasativo as AliasAtivo,
operacao.marcacao 
from posicao 
inner join operacao on operacao.cgc = posicao.cgc 
and operacao.aliasoperacao = posicao.aliasoperacao 
where posicao.data = '""" + app.dt.strftime(app.tkdtm.date_after_work_days(data, 0), "%Y-%m-%d") +  """' 
and operacao.cgc not like '%a'  
and operacao.cgc not in ('13107003000170') 
and Upper(operacao.AliasAtivo) <> Upper('RF#BRLB3@Compromissada') 
and Upper(operacao.AliasAtivo) not like 'RF#BRLB3@TERMO%' 
and Upper(operacao.AliasAtivo) <> 'SPOT#BRLOTC@REAL'
"""
dfPusOps = app.pd.read_sql_query(sql, app.db.engine)
dfPusOps = app.pd.merge(left=dfPusOps, right=dictMtlpl,how='left',left_on=['AliasAtivo'],right_on=['AliasAtivo']).copy()
dfPusOps = app.pd.merge(left=dfPusOps, right=dictNotMTM,how='left',left_on=['AliasAtivo'],right_on=['AliasAtivo']).copy()
dfPusOps = app.pd.merge(left=dfPusOps, right=dictPuD_1,how='left',left_on=['AliasAtivo'],right_on=['AliasAtivo']).copy()
dfPusOps = app.pd.merge(left=dfPusOps, right=dictPuD0,how='left',left_on=['AliasAtivo'],right_on=['AliasAtivo']).copy()
dfPusOps.loc[dfPusOps['Mltpl'].isna(),'Mltpl']=1
dfPusOps.loc[dfPusOps['NotMTMAtivo'].isna(), 'NotMTMAtivo']=False
dfPusOps.loc[dfPusOps['marcacao']=='Curva','NotMTMAtivo']=True
del dfPusOps['marcacao']
dfPusOps = dfPusOps[(dfPusOps['PUD0'].isna() & dfPusOps['PUD_1'].isna())==False].copy()
del dictNotMTM
del dictPuD_1
del dictPuD0
dfPus = dfPusOps[dfPusOps['NotMTMAtivo']==False].copy()
dfPusOps = dfPusOps[dfPusOps['NotMTMAtivo']==True].copy()
dfPusOps.loc[dfPusOps['qtd']!=0,'PUD0'] = dfPusOps['fin']/dfPusOps['qtd']/dfPusOps['Mltpl']
dfPusOps.loc[dfPusOps['qtd1']!=0,'PUD_1'] = dfPusOps['fin1']/dfPusOps['qtd1']/dfPusOps['Mltpl']
dfPusOps = dfPusOps[['AliasAtivo','CGC','AliasOperacao','PUD_1','PUD0']].copy()







dfPus.loc[((dfPus['qtd']!=0) & (dfPus['qtd']!=1)) ,'PUD0'] = dfPus['vl']/ dfPus['qtd']/dfPus['Mltpl']
dfPus.loc[((dfPus['qtd1']!=0) & (dfPus['qtd1']!=1)) ,'PUD_1'] = dfPus['vl1']/ dfPus['qtd1']/dfPus['Mltpl']
dfPus['isFuture'] = False
dfPus['isNTNB'] = False
dfPus.loc[app.tkstr.left(dfPus['AliasAtivo'].str,7)=='Futuro#' ,'isFuture'] = True
dfPus.loc[app.tkstr.left(dfPus['AliasAtivo'].str,app.tkstr.Len(("RF#BRLB3@NTN-B ")))=="RF#BRLB3@NTN-B " ,'isNTNB'] = True
dfPus.loc[dfPus['XPUD0'].isna(),'XPUD0']=0
dfPus.loc[dfPus['XPUD_1'].isna(),'XPUD_1']=0
dfPus.loc[ (dfPus['isFuture']) & (dfPus['XPUD0']!=0) ,'PUD0'] = dfPus['XPUD0'] # Pega os preços dos Futuros das Tabelas de Fechamento (Dados Públicos)
dfPus.loc[ (dfPus['isFuture']) & (dfPus['XPUD_1']!=0) ,'PUD_1'] = dfPus['XPUD_1'] # Pega os preços dos Futuros das Tabelas de Fechamento (Dados Públicos)
dfPus.loc[ (dfPus['isNTNB']) & (dfPus['XPUD0']!=0) ,'PUD0'] = dfPus['XPUD0'] # Pega os preços das NTNBs das Tabelas de Fechamento (Dados Públicos)
dfPus.loc[ (dfPus['isNTNB']) & (dfPus['XPUD_1']!=0),'PUD_1'] = dfPus['XPUD_1'] # Pega os preços das NTNBs das Tabelas de Fechamento (Dados Públicos)
dfPus = dfPus[['AliasAtivo','CGC','PUD_1','PUD0']].drop_duplicates(keep='last').reset_index()[['AliasAtivo','CGC','PUD_1','PUD0']].copy()

dfPus = dfPus.sort_values(["PUD0", "PUD_1"],ascending = True)
dfPus = dfPus.drop_duplicates(subset=['AliasAtivo','CGC'],keep='last')
#sys.exit('Para!')



sql = """
Select distinct data,posicao.cgc,posicao.aliasoperacao,operacao.aliasativo,qtd,pu,fin,resultado 
from posicao left join operacao on operacao.aliasoperacao = posicao.aliasoperacao and posicao.cgc = operacao.cgc
where posicao.data = '""" + data.strftime('%Y-%m-%d') + """' and posicao.cgc in """ + strlistacgcs + """ order by cgc,aliasoperacao asc"""
dfPosicao = app.pd.read_sql_query(sql, app.db.engine)
sql = """
select Operacao as AliasOperacao,sum(Valor) as Caixa,CGC 
FROM Caixa where cgc in """ + strlistacgcs + """
and data = '""" + data.strftime('%Y-%m-%d') + """' 
group by Operacao,Data,CGC
"""
dfCaixaOps = app.pd.read_sql_query(sql, app.db.engine)
thismonth15 = app.dt.strptime(str(data.year) + "-" + str(data.month) + "-" + "15","%Y-%m-%d")  
lastmonth15 = app.dt.strptime(str((data + app.pd.offsets.MonthEnd(-1)).year) + "-" + str((data + app.pd.offsets.MonthEnd(-1)).month) + "-" + "15","%Y-%m-%d")   
D_1 = app.tkdtm.date_after_work_days(data, -1)
D_2 = app.tkdtm.date_after_work_days(data, -2)
if app.tkdtm.backfoward_wd(data) >= app.tkdtm.backfoward_wd(thismonth15):
    ultimacoleta = app.tkdtm.backfoward_wd(thismonth15)
else:
    ultimacoleta = app.tkdtm.backfoward_wd(lastmonth15)
proximacoleta = app.tkdtm.backfoward_wd(app.dt.strptime(str((ultimacoleta + app.pd.offsets.MonthEnd(1)).year) + "-" + str((ultimacoleta + app.pd.offsets.MonthEnd(1)).month) + "-" + "15","%Y-%m-%d"))
if app.tk.CalculaIndiceAcumulado("IPCA#ANBIMA", D_1 , D_1) == "Não Disponível": 
    ipcaprorata = app.tk.CarregaNumeroIndice("IPCA#ANBIMA", data) * (((1 + app.tk.CalculaIndiceAcumulado("IPCA#ANBIMA", D_2, D_2) / 100) ** (app.tkdtm.net_work_day(D_1, D_1) / app.tkdtm.net_work_day(ultimacoleta, proximacoleta))))
else:
    ipcaprorata = app.tk.CarregaNumeroIndice("IPCA#ANBIMA", data) * (((1 + app.tk.CalculaIndiceAcumulado("IPCA#ANBIMA", D_1, D_1) / 100) ** (app.tkdtm.net_work_day(D_1, D_1) / app.tkdtm.net_work_day(ultimacoleta, proximacoleta))))
dictMtlpl['ProRataIPCA'] = ipcaprorata
dictMtlpl['is_DAP'] = False
dictMtlpl.loc[dictMtlpl['AliasAtivo'].str.find("@FUT DAP",1)>0,'is_DAP'] = True
dictMtlpl.loc[dictMtlpl['is_DAP'],'Mltpl'] = dictMtlpl['Mltpl']*dictMtlpl['ProRataIPCA']
del dictMtlpl['ProRataIPCA']
del dictMtlpl['is_DAP']
# Só para garantir......
dictMtlpl.loc[dictMtlpl['AliasAtivo'].str.find("FUT DI1 ",1)>0,'Mltpl'] = 1
dictMtlpl.loc[dictMtlpl['AliasAtivo'].str.find("FUT IND ",1)>0,'Mltpl'] = 1
dictMtlpl.loc[dictMtlpl['AliasAtivo'].str.find("FUT WIN ",1)>0,'Mltpl'] = 0.2
dictMtlpl.loc[dictMtlpl['AliasAtivo'].str.find("FUT WDO ",1)>0,'Mltpl'] = 10
dictMtlpl.loc[dictMtlpl['AliasAtivo'].str.find("FUT DOL ",1)>0,'Mltpl'] = 50
dictMtlpl.loc[dictMtlpl['AliasAtivo'].str.find("OPD DOL ",1)>0,'Mltpl'] = 50
############################################### carga de preços da data base ###################################################
################################################################################################################################
################################################################################################################################
##################################################### Boletas Automaticas ######################################################
print('Iniciando Boletas Automaticas:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
app.db.connect()







################################### Diferença Short ##############################################
app.db.execRawQuery("Delete from Mov where datamov ='" + data.strftime('%Y-%m-%d') + "' and aliasativo like 'Cota#%' and cgc in " + strlistacgcs)
app.db.execRawQuery("Delete from Mov where datamov ='" + data.strftime('%Y-%m-%d') + "' and aliasativo like 'SPOT#BRLOTC@REAL%' and cgc in " + strlistacgcs)
app.db.execRawQuery("Delete from Mov where datamov ='" + data.strftime('%Y-%m-%d') + "' and aliasativo like '%RF#BRLB3@Compromissada%' and cgc in " + strlistacgcs)
app.db.execRawQuery("Delete from Mov where datamov ='" + data.strftime('%Y-%m-%d') + "' and aliasativo like 'RF#BRLB3@TERM%' and cgc in " + strlistacgcs)
################################### Diferença Short ##############################################







print('Limpando Boletas Automaticas:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
app.db.drop()
sql = """select cgc,aliasativo,idtrader,aliasoperacao,estrategia.Grupo as grupo,estrategia.nome as nome,sum(qtd) as QtdAtual,sum(pu*qtd) as FinAtual
from Mov inner join Estrategia on Estrategia.IDEstrategia = mov.idEstrategia
where datamov < '""" + data.strftime('%Y-%m-%d') + """'
and cgc in """ + strlistacgcs + """
and (aliasativo like 'Cota#%' or aliasativo like 'SPOT#BRLOTC@REAL%' or aliasativo like '%RF#BRLB3@Compromissada%' or aliasativo like 'RF#BRLB3@TERM%')
group by CGC,AliasAtivo,idtrader,estrategia.Grupo,estrategia.nome,AliasOperacao order by cgc,aliasativo,idtrader,grupo,nome asc 
"""
dfCustodiaAutomatica = app.pd.read_sql_query(sql, app.db.engine)
deparaestratpassada = dfCustodiaAutomatica[['aliasoperacao','cgc','grupo','nome']].copy().drop_duplicates(subset=['aliasoperacao','cgc'],keep='last').reset_index()
print('Carregando Boletas Automaticas:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfPosicao_Cota = dfPosicao[['cgc','aliasoperacao','aliasativo','qtd','fin','resultado']][app.tkstr.left(dfPosicao['aliasativo'].str,5)=="Cota#"].copy()
dfPosicao_CPR = dfPosicao[['cgc','aliasoperacao','aliasativo','qtd','fin','resultado']][app.tkstr.left(dfPosicao['aliasativo'].str,16)=="SPOT#BRLOTC@REAL"].copy()
dfPosicao_Compromissada = dfPosicao[['cgc','aliasoperacao','aliasativo','qtd','fin','resultado']][app.tkstr.left(dfPosicao['aliasativo'].str,22)=="RF#BRLB3@Compromissada"].copy()
dfPosicao_Termo = dfPosicao[['cgc','aliasoperacao','aliasativo','qtd','fin','resultado']][app.tkstr.left(dfPosicao['aliasativo'].str,13)=="RF#BRLB3@TERM"].copy()
dfPosicao_Compromissada['aliasoperacao'] = 'Compromissada'
dfPosicao_Compromissada = dfPosicao_Compromissada.groupby(['cgc','aliasoperacao','aliasativo']).agg({'qtd':'sum','fin':'sum','resultado':'sum'}).reset_index().copy()
dfPosicao_Compromissada['grupo'] = 'Compromissada'
dfPosicao_Compromissada['nome'] = 'Over'
dfPosicao_Termo['aliasoperacao'] = 'Termo'
dfPosicao_Termo = dfPosicao_Termo.groupby(['cgc','aliasoperacao','aliasativo']).agg({'qtd':'sum','fin':'sum','resultado':'sum'}).reset_index().copy()
dfPosicao_Termo['grupo'] = 'Juros Nominais'
dfPosicao_Termo['nome'] = 'Termo Ação'
dfPosicao_Cota = dfPosicao_Cota.groupby(['cgc','aliasoperacao','aliasativo']).agg({'qtd':'sum','fin':'sum','resultado':'sum'}).reset_index().copy()
dfPosicao_Cota = app.pd.merge(left=dfPosicao_Cota, right=deparaestratpassada,how='left',left_on=['aliasoperacao','cgc'],right_on=['aliasoperacao','cgc']).copy()
dfPosicao_Cota.loc[dfPosicao_Cota['grupo'].isna(),'grupo'] = 'Multimercado'
dfPosicao_Cota.loc[dfPosicao_Cota['nome'].isna(),'nome'] = 'Multimercado Inst.'
dfPosicao_CPR = app.pd.merge(left=dfPosicao_CPR, right=deparaestratpassada,how='left',left_on=['aliasoperacao','cgc'],right_on=['aliasoperacao','cgc']).copy()
dfPosicao_CPR['grupo'] = 'CPR'
dfPosicao_CPR['nome'] = 'Outras Despesas'
dfPosicao_CPR['aliasoperacao_x'] = dfPosicao_CPR['aliasoperacao'].str.upper()
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("ANBIMA",1)>0 ,'nome'] = 'Taxa Anbima'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("CETIP",1)>0 ,'nome'] = 'Taxa CETIP'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("ADMINISTRAÇÃO",1)>0 ,'nome'] = 'Taxa de Administração'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("SELIC",1)>0 ,'nome'] = 'Taxa SELIC'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("GESTÃO",1)>0 ,'nome'] = 'Taxa de Gestão'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("CVM",1)>0 ,'nome'] = 'Taxa CVM'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("CBLC",1)>0 ,'nome'] = 'Taxa CBLC'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("TESOURARIA",1)>0 ,'nome'] = 'Saldo em Tesouraria'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find('AUDITORIA',1)>0 ,'nome'] = 'Auditoria'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find('COMPENSAÇÃO DE COTAS',1)>0 ,'nome'] = 'Outras Despesas'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find('JUSTE CONTÁBIL',1)>0 ,'nome'] = 'Ajuste Contabil MAI'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("CUSTÓDIA",1)>0 ,'nome'] = 'Taxa de Custódia'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("ERFORMANCE FEE",1)>0 ,'nome'] = 'Performance FEE'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("ANCÁRIAS",1)>0 ,'nome'] = 'Bancárias'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("UDITORIA",1)>0 ,'nome'] = 'Auditoria'
dfPosicao_CPR.loc[dfPosicao_CPR['aliasoperacao_x'].str.find("ORRETAGEM",1)>0 ,'nome'] = 'Corretagem'
del dfPosicao_CPR['aliasoperacao_x']
dfPosicao_CPR.loc[dfPosicao_CPR['nome']=='Outras Despesas','aliasoperacao'] = 'Outras Despesas'
dfPosicao_CPR = dfPosicao_CPR.groupby(['cgc','aliasoperacao','aliasativo','grupo','nome']).agg({'qtd':'sum','fin':'sum','resultado':'sum'}).reset_index().copy()
dfPosicao_CPR['idtrader'] = 3
dfPosicao_Cota['idtrader'] = 3
dfPosicao_Compromissada['idtrader'] = 3
dfPosicao_Termo['idtrader'] = 3
dfPosicao_Compromissada = dfPosicao_Compromissada.rename(columns={"qtd": "qtd_comp","fin": "fin_comp","resultado": "result_comp"})
dfPosicao_Cota = dfPosicao_Cota.rename(columns={"qtd": "qtd_cota","fin": "fin_cota","resultado": "result_cota"})
dfPosicao_Termo = dfPosicao_Termo.rename(columns={"qtd": "qtd_term","fin": "fin_term","resultado": "result_term"})
dfPosicao_CPR = dfPosicao_CPR.rename(columns={"qtd": "qtd_cpr","fin": "fin_cpr","resultado": "result_cpr"})
if 'index' in dfPosicao_CPR.columns: del dfPosicao_CPR['index']
if 'index' in dfPosicao_Cota.columns: del dfPosicao_Cota['index']
if 'index' in dfPosicao_Termo.columns: del dfPosicao_Termo['index']
if 'index' in dfPosicao_Compromissada.columns: del dfPosicao_Compromissada['index']
dfCustodiaAutomatica = app.pd.merge(left=dfCustodiaAutomatica, right=dfPosicao_CPR,how='outer',left_on=['aliasoperacao','cgc','aliasativo','idtrader','grupo','nome'],right_on=['aliasoperacao','cgc','aliasativo','idtrader','grupo','nome']).copy()
dfCustodiaAutomatica = app.pd.merge(left=dfCustodiaAutomatica, right=dfPosicao_Cota,how='outer',left_on=['aliasoperacao','cgc','aliasativo','idtrader','grupo','nome'],right_on=['aliasoperacao','cgc','aliasativo','idtrader','grupo','nome']).copy()
dfCustodiaAutomatica = app.pd.merge(left=dfCustodiaAutomatica, right=dfPosicao_Termo,how='outer',left_on=['aliasoperacao','cgc','aliasativo','idtrader','grupo','nome'],right_on=['aliasoperacao','cgc','aliasativo','idtrader','grupo','nome']).copy()
dfCustodiaAutomatica = app.pd.merge(left=dfCustodiaAutomatica, right=dfPosicao_Compromissada,how='outer',left_on=['aliasoperacao','cgc','aliasativo','idtrader','grupo','nome'],right_on=['aliasoperacao','cgc','aliasativo','idtrader','grupo','nome']).copy()
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['QtdAtual'].isna(),'QtdAtual']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['FinAtual'].isna(),'FinAtual']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['qtd_cpr'].isna(),'qtd_cpr']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['qtd_term'].isna(),'qtd_term']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['qtd_comp'].isna(),'qtd_comp']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['qtd_cota'].isna(),'qtd_cota']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['fin_cpr'].isna(),'fin_cpr']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['fin_term'].isna(),'fin_term']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['fin_comp'].isna(),'fin_comp']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['fin_cota'].isna(),'fin_cota']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['result_cpr'].isna(),'result_cpr']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['result_term'].isna(),'result_term']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['result_comp'].isna(),'result_comp']=0
dfCustodiaAutomatica.loc[dfCustodiaAutomatica['result_cota'].isna(),'result_cota']=0
# Dinheiros PU = 1 D_1 e D0.... qtd é o financeiro... resultado vai pro caixa.... boleta só acerta a posição
dfCustodiaAutomatica['qtd_cpr'] = dfCustodiaAutomatica['fin_cpr']
dfCustodiaAutomatica['qtd_term'] = dfCustodiaAutomatica['fin_term']
dfCustodiaAutomatica['qtd_comp'] = dfCustodiaAutomatica['fin_comp']
# Dinheiros PU = 1 D_1 e D0.... qtd é o financeiro... resultado vai pro caixa.... boleta só acerta a posição
dfCustodiaAutomatica['qtd'] = dfCustodiaAutomatica['qtd_cpr']+dfCustodiaAutomatica['qtd_term']+dfCustodiaAutomatica['qtd_comp']+dfCustodiaAutomatica['qtd_cota']
dfCustodiaAutomatica['fin'] = dfCustodiaAutomatica['fin_cpr']+dfCustodiaAutomatica['fin_term']+dfCustodiaAutomatica['fin_comp']+dfCustodiaAutomatica['fin_cota']
dfCustodiaAutomatica['resultado'] = dfCustodiaAutomatica['result_cpr']+dfCustodiaAutomatica['result_term']+dfCustodiaAutomatica['result_comp']+dfCustodiaAutomatica['result_cota']
del dfCustodiaAutomatica['qtd_cpr']
del dfCustodiaAutomatica['fin_cpr']
del dfCustodiaAutomatica['result_cpr']
del dfCustodiaAutomatica['qtd_term']
del dfCustodiaAutomatica['fin_term']
del dfCustodiaAutomatica['result_term']
del dfCustodiaAutomatica['qtd_comp']
del dfCustodiaAutomatica['fin_comp']
del dfCustodiaAutomatica['result_comp']
del dfCustodiaAutomatica['qtd_cota']
del dfCustodiaAutomatica['fin_cota']
del dfCustodiaAutomatica['result_cota']
dfCustodiaAutomatica['delta_qtd'] = dfCustodiaAutomatica['qtd'] - dfCustodiaAutomatica['QtdAtual']
dfCustodiaAutomatica['delta_fin'] = dfCustodiaAutomatica['fin'] - dfCustodiaAutomatica['FinAtual']
dfCustodiaAutomatica['Pu_Bol'] = 1
dfCustodiaAutomatica.loc[(app.tkstr.left(dfCustodiaAutomatica['aliasativo'].str,12)=='Cota#BRLOTC@'),'Pu_Bol'] = dfCustodiaAutomatica['fin']/dfCustodiaAutomatica['qtd']
dfCustodiaAutomatica['Qtd_Bol'] = dfCustodiaAutomatica['delta_qtd']
dfCaixaBoletaAutomatica = dfCustodiaAutomatica[['cgc','aliasativo','aliasoperacao','idtrader','grupo','nome','resultado']].copy()
dfCaixaBoletaAutomatica = dfCaixaBoletaAutomatica[dfCaixaBoletaAutomatica['resultado']!=0]
dfCustodiaAutomatica = app.pd.merge(left=dfCustodiaAutomatica, right=dictEstrategias,how='left',left_on=['grupo','nome'],right_on=['grupo','nome']).copy()
dfCustodiaAutomatica = dfCustodiaAutomatica[['idtrader','Qtd_Bol','Pu_Bol','aliasoperacao','cgc','idestrategia','aliasativo']].copy()
dfCustodiaAutomatica = dfCustodiaAutomatica.rename(columns={  "Qtd_Bol": "Qtd",
                                                "Pu_Bol": "Pu",
                                                "aliasoperacao": "AliasOperacao",
                                                "aliasativo": "AliasAtivo",
                                                "cgc": "CGC",
                                                "idestrategia":"idEstrategia",
                                                "idtrader": "idTrader"})
dfCustodiaAutomatica['idCorretora'] = 38
dfCustodiaAutomatica['DataMov'] = data
dfCustodiaAutomatica['Marcacao'] = 'MTM'
dfCustodiaAutomatica['DataCotizacao'] = data
dfCustodiaAutomatica['DataLiquidacao'] = data
dfCustodiaAutomatica['UltimoAlterador'] = 'Boleta Automatica'
dfCustodiaAutomatica['Corretagem'] = 0
dfCustodiaAutomatica['Taxa'] = 0
dfCustodiaAutomatica['PuCompromisso'] = 0
dfCustodiaAutomatica['TipoCompromisso'] = ''
dfCustodiaAutomatica['Grupo'] = ''
dfCustodiaAutomatica.loc[app.tkstr.left(dfCustodiaAutomatica['AliasAtivo'].str,5)=='Cota#','Grupo'] = 'Cota'
dfCustodiaAutomatica.loc[app.tkstr.left(dfCustodiaAutomatica['AliasAtivo'].str,3)=='RV#','Grupo'] = 'RV'
dfCustodiaAutomatica.loc[app.tkstr.left(dfCustodiaAutomatica['AliasAtivo'].str,3)=='RF#','Grupo'] = 'RF'
dfCustodiaAutomatica.loc[app.tkstr.left(dfCustodiaAutomatica['AliasAtivo'].str,5)=='SPOT#','Grupo'] = 'SPOT'
dfCustodiaAutomatica.loc[app.tkstr.left(dfCustodiaAutomatica['AliasAtivo'].str,5)=='SWAP#','Grupo'] = 'SWAP'
dfCustodiaAutomatica = dfCustodiaAutomatica[(dfCustodiaAutomatica['Qtd']!=0) | (app.tkstr.left(dfCustodiaAutomatica['AliasAtivo'].str,12)=='Cota#BRLOTC@')]




#dfCustodiaAutomatica = dfCustodiaAutomatica[dfCustodiaAutomatica['CGC']=='20833940000179'] 
#sys.exit('PAra!')


################################### Diferença Short ##############################################
Mov = cl_Mov(**{})
Mov.bulk(dfCustodiaAutomatica)
################################### Diferença Short ##############################################



##################################################### Boletas Automaticas ######################################################
################################################################################################################################
################################################################################################################################
############################################### Carga da Custodia e das Boletas D0 #############################################
print('Iniciando carga de Boletas:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))

dictMtlpl = dictMtlpl.drop_duplicates(subset=['AliasAtivo'],keep='last').reset_index()
dfPus = dfPus.drop_duplicates(subset=['AliasAtivo', 'CGC'],keep='last').reset_index()
dfPusOps = dfPusOps.drop_duplicates(subset=['AliasAtivo', 'CGC','AliasOperacao'],keep='last').reset_index()
if 'index' in dfPus.columns: del dfPus['index']
if 'index' in dfPusOps.columns: del dfPusOps['index']
if 'index' in dictMtlpl.columns: del dictMtlpl['index']
############################################### Para Pegar O Valor que cai no caixa de juros e amortizações ####################
dfPosRF = dfPosicao[(app.tkstr.left(dfPosicao['aliasativo'].str,3)=='RF#')].copy()
dfCaixaOps = app.pd.merge(left=dfPosRF.rename(columns={"aliasoperacao": "AliasOperacao","aliasativo": "AliasAtivo","cgc": "CGC"}).copy(), right=dfCaixaOps,how='inner',left_on=['AliasOperacao','CGC'],right_on=['AliasOperacao','CGC']).copy()
del dfPosRF
dfCaixaOps.loc[dfCaixaOps['qtd'].isna(),'qtd'] = 1
dfCaixaOps.loc[dfCaixaOps['qtd']==0,'qtd'] = 1
dfCaixaOps['Caixa_por_Contrato'] = dfCaixaOps['Caixa']/dfCaixaOps['qtd']
dfCaixaOps.loc[dfCaixaOps['AliasAtivo']=='RF#BRLB3@Compromissada','Caixa_por_Contrato'] = 0
dfCaixaOps = dfCaixaOps[['AliasAtivo','CGC','Caixa_por_Contrato']].copy()
dfCaixaOps.loc[dfCaixaOps['Caixa_por_Contrato'].isna(),'Caixa_por_Contrato'] = 0
dfCaixaOps = dfCaixaOps[dfCaixaOps['Caixa_por_Contrato']!=0]
dfCaixaOps = dfCaixaOps.groupby(['CGC','AliasAtivo']).agg({'Caixa_por_Contrato':'sum'}).reset_index().copy()
### Inseguro se precisa ou não....... assumindo que não precisa....
#### Acho que para ficar bom tem que tirar o financeiro movimentado.... o problema são as operações a termo...
dfCaixaOps['Caixa_por_Contrato'] = 0
#### Acho que para ficar bom tem que tirar o financeiro movimentado.... o problema são as operações a termo...
### Inseguro se precisa ou não....... assumindo que não precisa....
############################################### Para Pegar O Valor que cai no caixa de juros e amortizações ####################
sql = """select CGC,AliasAtivo,idtrader,AliasOperacao,estrategia.Grupo as Grupo,estrategia.nome as Nome,sum(qtd) as Qtd,sum(pu*qtd) as Fin
from Mov inner join Estrategia on Estrategia.IDEstrategia = mov.idEstrategia
where datamov <= '""" + D_1.strftime('%Y-%m-%d') + """'
and cgc in """ + strlistacgcs + """
group by CGC,AliasAtivo,idtrader,estrategia.Grupo,estrategia.nome,AliasOperacao order by cgc,aliasativo,idtrader,grupo,nome asc 
"""
dfCustodiaD_1 = app.pd.read_sql_query(sql, app.db.engine)
dfCustodiaD_1 = app.pd.merge(left=dfCustodiaD_1, right=dfCaixaOps,how='left',left_on=['AliasAtivo','CGC'],right_on=['AliasAtivo','CGC']).copy()
############################################### Para Pegar O Valor que cai no caixa de juros e amortizações ####################
dfCustodiaD_1['Caixa'] = 0
dfCustodiaD_1.loc[dfCustodiaD_1['Caixa_por_Contrato'].isna()==False,'Caixa'] = dfCustodiaD_1['Qtd']*dfCustodiaD_1['Caixa_por_Contrato']
del dfCustodiaD_1['Caixa_por_Contrato']
############################################### Para Pegar O Valor que cai no caixa de juros e amortizações ####################
dfCustodiaD_1.loc[dfCustodiaD_1['Caixa'].isna(),'Caixa'] = 0 
dfCustodiaD_1.loc[dfCustodiaD_1['AliasAtivo'].str.find("Opcao#",1)>0,'Caixa'] = 0
dfCustodiaD_1.loc[dfCustodiaD_1['AliasAtivo'].str.find("RV#",1)>0,'Caixa'] = 0
dfCustodiaD_1.loc[dfCustodiaD_1['AliasAtivo'].str.find("Futuro#",1)>0,'Caixa'] = 0
dfCustodiaD_1 = app.pd.merge(left=dfCustodiaD_1, right=dfPus,how='left',left_on=['AliasAtivo','CGC'],right_on=['AliasAtivo','CGC']).copy()
dfCustodiaD_1 = app.pd.merge(left=dfCustodiaD_1, right=dfPusOps.rename(columns={"PUD_1": "PUD_1_Op","PUD0": "PUD0_Op"}).copy()[['AliasOperacao','CGC',"PUD_1_Op","PUD0_Op"]].copy(),how='left',left_on=['AliasOperacao','CGC'],right_on=['AliasOperacao','CGC']).copy()
dfCustodiaD_1 = app.pd.merge(left=dfCustodiaD_1, right=dictMtlpl,how='left',left_on=['AliasAtivo'],right_on=['AliasAtivo']).copy()
dfCustodiaD_1.loc[dfCustodiaD_1['PUD_1_Op'].isna()==False,'PUD_1'] = dfCustodiaD_1['PUD_1_Op']
dfCustodiaD_1.loc[dfCustodiaD_1['PUD0_Op'].isna()==False,'PUD0'] = dfCustodiaD_1['PUD0_Op']
dfCustodiaD_1.loc[dfCustodiaD_1['Mltpl'].isna(),'Mltpl'] = 1
del dfCustodiaD_1['PUD_1_Op']
del dfCustodiaD_1['PUD0_Op']
dfCustodiaD_1.loc[ # Zera resultado por contrato outlier de renda fixa (por movimento)
                  (dfCustodiaD_1['AliasAtivo'].str.find("RF#",1)>0) & 
                  (dfCustodiaD_1['AliasAtivo'].str.find("Compromissada",1)<=0) &
                  (dfCustodiaD_1['Qtd'] != 0) &
                  (dfCustodiaD_1['Caixa'] != 0) &
                  ((abs(((dfCustodiaD_1['PUD0']-dfCustodiaD_1['PUD_1'])*dfCustodiaD_1['Qtd']*dfCustodiaD_1['Mltpl'])+dfCustodiaD_1['Caixa']) /dfCustodiaD_1['Qtd']) > 10)
                 ,'Caixa'] = 0
dfCustodiaD_1.loc[dfCustodiaD_1['PUD0'].isna(),'PUD0'] = 1
dfCustodiaD_1.loc[dfCustodiaD_1['PUD_1'].isna(),'PUD_1'] = 1
dfCustodiaD_1['fin'] = dfCustodiaD_1['Qtd']*dfCustodiaD_1['PUD0']*dfCustodiaD_1['Mltpl'] 
dfCustodiaD_1['fin_1'] = dfCustodiaD_1['Qtd']*dfCustodiaD_1['PUD_1']*dfCustodiaD_1['Mltpl'] 
#################################### Ajuste de Eventos corporativos nas Ações e Fiis #################################################
dfCustodiaD_1.loc[dfCustodiaD_1['AliasAtivo'].str.find("RV#",1)>0,'Caixa']=0
dfRendimentos = dfRendimentos[dfRendimentos['Data'] == data]
dfCustodiaD_1 = app.pd.merge(left=dfCustodiaD_1, right=dfRendimentos,how='left',left_on=['AliasAtivo'],right_on=['AliasAtivo']).copy()
dfCustodiaD_1.loc[dfCustodiaD_1['Rent'].isna()==False,'Caixa'] = dfCustodiaD_1['Qtd']*dfCustodiaD_1['PUD_1']*dfCustodiaD_1['Rent'] - ((dfCustodiaD_1['PUD0'] + (dfCustodiaD_1['Caixa'] / dfCustodiaD_1['Qtd'])) - dfCustodiaD_1['PUD_1']) * dfCustodiaD_1['Qtd'] * dfCustodiaD_1['Mltpl']
del dfCustodiaD_1['Rent']
#################################### Ajuste de Eventos corporativos nas Ações e Fiis #################################################
dfCustodiaD_1['Resultado'] = ((dfCustodiaD_1['PUD0'] + (dfCustodiaD_1['Caixa'] / dfCustodiaD_1['Qtd'])) - dfCustodiaD_1['PUD_1']) * dfCustodiaD_1['Qtd'] * dfCustodiaD_1['Mltpl']
dfCustodiaD_1.loc[dfCustodiaD_1['Resultado'].isna(),'Resultado']=0
dfCustodiaD_1.loc[dfCustodiaD_1['AliasAtivo']=='SPOT#BRLOTC@REAL','Resultado']=0
dfCustodiaD_1['D+X']=-1
sql = """select CGC,AliasAtivo,idtrader,AliasOperacao,estrategia.Grupo as Grupo,estrategia.nome as Nome,sum(qtd) as Qtd,sum(pu*qtd) as fin
from Mov inner join Estrategia on Estrategia.IDEstrategia = mov.idEstrategia
where datamov = '""" + data.strftime('%Y-%m-%d') + """'
and cgc in """ + strlistacgcs + """
group by CGC,AliasAtivo,idtrader,AliasOperacao,estrategia.Grupo,estrategia.nome order by cgc,aliasativo,idtrader,grupo,nome asc 
"""
dfMovsD0 = app.pd.read_sql_query(sql, app.db.engine)
dfMovsD0['D+X']=0
dfMovsD0['Caixa'] = 0
dfMovsD0['DayTrade']=False
dfMovsD0.loc[(dfMovsD0['Qtd']==0)&(dfMovsD0['fin']!=0),'DayTrade'] = True
dfMovsD0 = app.pd.merge(left=dfMovsD0, right=dfPus,how='left',left_on=['AliasAtivo','CGC'],right_on=['AliasAtivo','CGC']).copy()
dfMovsD0 = app.pd.merge(left=dfMovsD0, right=dictMtlpl,how='left',left_on=['AliasAtivo'],right_on=['AliasAtivo']).copy()
dfMovsD0['PUD_1'] = 1
dfMovsD0.loc[dfMovsD0['Mltpl'].isna(),'Mltpl'] = 1
dfMovsD0.loc[dfMovsD0['Qtd']!=0 ,'PUD_1'] = dfMovsD0['fin']/dfMovsD0['Qtd']
dfMovsD0.loc[dfMovsD0['Qtd']==0 ,'PUD_1'] = dfMovsD0['fin']
dfMovsD0.loc[dfMovsD0['PUD0'].isna(),'PUD0'] = 1
dfMovsD0.loc[dfMovsD0['PUD_1'].isna(),'PUD_1'] = 1
dfMovsD0.loc[dfMovsD0['DayTrade'],'Caixa'] = dfMovsD0['fin']*dfMovsD0['Mltpl']
dfMovsD0['fin'] = dfMovsD0['Qtd']*dfMovsD0['PUD0']*dfMovsD0['Mltpl'] 
dfMovsD0['fin_1'] = dfMovsD0['Qtd']*dfMovsD0['PUD_1']*dfMovsD0['Mltpl'] 
dfCaixaBoletaAutomatica = dfCaixaBoletaAutomatica.rename(columns={"cgc": "CGC","aliasativo": "AliasAtivo","grupo": "Grupo","nome": "Nome","aliasoperacao": "AliasOperacao",'resultado':'CaixaBoletasAutomaticas'})
dfMovsD0 = app.pd.merge(left=dfMovsD0, right=dfCaixaBoletaAutomatica,how='left',left_on=['AliasOperacao','AliasAtivo','CGC','idtrader','Grupo','Nome'],right_on=['AliasOperacao','AliasAtivo','CGC','idtrader','Grupo','Nome']).copy()
dfMovsD0.loc[dfMovsD0['CaixaBoletasAutomaticas'].isna() == False, 'PUD0'] = 1
dfMovsD0.loc[dfMovsD0['CaixaBoletasAutomaticas'].isna(),'CaixaBoletasAutomaticas']=0
dfMovsD0['Caixa'] = dfMovsD0['Caixa'] + dfMovsD0['CaixaBoletasAutomaticas']
del dfMovsD0['CaixaBoletasAutomaticas']
dfMovsD0['Resultado'] = ((dfMovsD0['PUD0'] + (dfMovsD0['Caixa'] / dfMovsD0['Qtd'])) - dfMovsD0['PUD_1']) * dfMovsD0['Qtd'] * dfMovsD0['Mltpl']
dfMovsD0.loc[dfMovsD0['Resultado'].isna(),'Resultado']=0
dfMovsD0.loc[dfMovsD0['DayTrade'],'Resultado']=-dfMovsD0['Caixa']
dfFinal = app.pd.concat([dfCustodiaD_1.copy(), dfMovsD0.copy()], ignore_index=True) # append 
dfFinal = dfFinal[['CGC','AliasAtivo','idtrader','Grupo','Nome','Qtd','PUD_1','PUD0','fin_1','fin','Caixa','Mltpl','Resultado','D+X']]
dfFinal.loc[dfFinal['Resultado'].isna(),'Resultado'] = 0
dfFinal.loc[dfFinal['fin'].isna(),'fin'] = 0
dfFinal.loc[dfFinal['Qtd'].isna(),'Qtd'] = 0
dfFinal.loc[dfFinal['Resultado'].isna(),'Resultado'] = 0
dfFinal.loc[dfFinal['Caixa'].isna(),'Caixa'] = 0
dfFinal.loc[(app.tkstr.left(dfFinal['AliasAtivo'].str,12)=='Cota#BRLOTC@') & (dfFinal['D+X']==0) ,'Resultado'] = dfFinal['Caixa']
dfFinal.loc[(app.tkstr.left(dfFinal['AliasAtivo'].str,12)=='Cota#BRLOTC@') & (dfFinal['D+X']==-1) ,'Resultado'] = 0
dfFinal.loc[(app.tkstr.left(dfFinal['AliasAtivo'].str,13)=='Futuro#BRLB3@'),'fin'] = 0
dfFinal.loc[(app.tkstr.left(dfFinal['AliasAtivo'].str,13)=='Futuro#BRLB3@'),'fin_1'] = 0
dfFinal = dfFinal[(dfFinal['Qtd']!=0)|(dfFinal['fin']!=0)|(dfFinal['Resultado']!=0)]
dfFinal['CGC'] = '00000'+dfFinal['CGC']
dfFinal['CGC'] = dfFinal['CGC'].str[-14:]
dfFinal.to_excel(r"../Current_PreGerencial.xlsx", index=False)
############################################### Carga da Custodia e das Boletas D0 #############################################
################################################################################################################################
print('Fim Pre Gerencial:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))

