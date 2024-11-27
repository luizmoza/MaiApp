import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.append(r"../")
from app import app
from app.classes.cl_Apontamento import cl_Apontamento
from app.classes.cl_Controle import cl_Controle

print('Inicio Carga de Dados:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
Apontamento = cl_Apontamento()
Controle = cl_Controle()

def ControleExists(Cntrl):
    vv = False
    sql = """
    select * from Controle where 
    Nome = '""" + Cntrl.Nome + """'
    and Tipo = '""" + Cntrl.Tipo + """'
    and SubTipo = '""" + Cntrl.SubTipo + """'
    """
    df = app.pd.read_sql_query(sql, app.db.engine)
    if len(df)>0: 
        vv = True
        Cntrl.idControle = df['idControle'].iloc[0]
    return vv

def ApontamentoExists(Apntmnt):
    vv = False
    sql = """
    select * from Apontamento where 
    idControle = """ + str(Apntmnt.idControle) + """
    and Data = '""" + Apntmnt.Data.strftime('%Y-%m-%d') + """'
    and IDFundo = """ + str(Apntmnt.IDFundo) + """
    and Obs = '""" + Apntmnt.Obs + """'
    """
    df = app.pd.read_sql_query(sql, app.db.engine)
    if len(df)>0: 
        vv = True
        Apntmnt.idControle = df['idApontamento'].iloc[0]
    return vv

def InspecaoExists(Apntmnt):
    vv = False
    sql = """
    select * from inspecao where 
    idControle = """ + Apntmnt.idControle + """
    and idFundo = """ + Apntmnt.idFundo + """
    """
    df = app.pd.read_sql_query(sql, app.db.engine)
    if len(df)>0: 
        vv = True
        Apntmnt.idControle = df['idApontamento'].iloc[0]
    return vv

def ParseDictToDF(obj):
    dictaux = {}
    dict = app.tk.ParseObjectDict(obj)
    for key, value in dict.items():
        dictaux[key] = [value]
    return app.pd.DataFrame.from_dict(dictaux)
    

def GetDFFundosInternosAtivos():
    sql = """
    select idfundo,Alias,cgc 
    from fundo 
    where Interno = 1 
    and ((DataInicioMai > datafimmai or (datafimmai is null and DataInicioMai is not null)) 
    and datafimmai <= '""" + app.dt.now().strftime('%Y-%m-%d') + """') order by idfundo desc
    """
    return app.pd.read_sql_query(sql, app.db.engine)

def GetPLD_2():
    sql = """
    select 
    cgc,
    PL as PL_d_2 
    from carteira 
    where 
    data = '""" + app.tkdtm.date_after_work_days(app.dt.now(),-2).strftime('%Y-%m-%d') + """'
    """
    return  app.pd.read_sql_query(sql, app.db.engine)

def GetPLD_1():
    sql = """
    select 
    cgc,
    PL as PL_d_1 
    from carteira 
    where 
    data = '""" + app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d') + """'
    """
    return  app.pd.read_sql_query(sql, app.db.engine) 

def GetcotaD_1():
    sql = """
    select 
    cgc,
    cota as cota_d_1 
    from carteira 
    where data = '""" + app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d') + """'
    """
    return  app.pd.read_sql_query(sql, app.db.engine)

def GetcotaD_2():
    sql = """
    select 
    cgc
    ,cota as cota_d_2 
    from carteira 
    where data = '""" + app.tkdtm.date_after_work_days(app.dt.now(),-2).strftime('%Y-%m-%d') + """'
    """
    return  app.pd.read_sql_query(sql, app.db.engine)
    
def GetResultado_D_1():
    sql = """
    select 
    cgc,
    sum(resultado) as resultado 
    from posicao where 
    data = '""" + app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d') + """'
    group by cgc
    """
    return  app.pd.read_sql_query(sql, app.db.engine)

def GetResultadoespecifico_D_1(aliasativo,aliasoperacao,fieldname):
    sql = """
    select 
    cgc,
    sum(resultado) as '""" + fieldname + """'
    from posicao where 
    data = '""" + app.tkdtm.date_after_work_days(app.dt.now(),-2).strftime('%Y-%m-%d') + """'
    and aliasativo = '""" + aliasativo + """'
    and aliasoperacao like '%""" + aliasoperacao + """%'
    group by cgc
    """
    return app.pd.read_sql_query(sql, app.db.engine)

def GetCadastroFundo():
    sql = """
    SELECT fundo.CGC as cgc
          ,TaxaPerformance
          ,TaxaAdministracao
          ,datainiciomai
          ,datafimmai
          ,interno
          ,alias
          ,mxdtpos
      FROM Fundo
      inner join (
  select cgc,max(data) as mxdtpos
  from posicao
  group by cgc
          ) as btt
      on btt.cgc = fundo.cgc
    """
    return  app.pd.read_sql_query(sql, app.db.engine)        


def GetCustodia():
    sql = """
    select * from
    (
    SELECT mov.CGC as cgc
    ,aliasativo
    ,sum(qtd) as custodia
      FROM Mov
      inner join fundo on fundo.cgc = mov.cgc
      where datamov <= '""" + app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d') + """'
      and aliasativo <> 'SPOT#BRLOTC@REAL'
      and aliasativo <> 'RF#BRLB3@Compromissada'
      and aliasativo not like '%RF#%@TERMO%'
      and aliasativo not like 'Cota#%'
      and not (
          fundo.administrador = 'BRADESCO' 
          and datacompromisso > '""" + app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d') + """'  
          and tipoCompromisso <> 'Sem Compromisso'
          and tipoCompromisso is not null
            )
        group by mov.cgc,AliasAtivo
        ) as btt
        where custodia <> 0
    """
    return  app.pd.read_sql_query(sql, app.db.engine)       


def GetCadastroAtivos():
    sql = """
    (SELECT distinct Alias as aliasativo,emissor.Nome as Emissor,1 as PrecisaEmissor,'' as RatingEmissaoMAI,'' as ratingemissor FROM RV left join emissor on emissor.IDEmissor = rv.idEmissor)
    union 
    (SELECT distinct Alias as aliasativo,emissor.Nome as Emissor,1 as PrecisaEmissor,RatingEmissaoMAI,RatingMAI as ratingemissor FROM RF left join emissor on emissor.IDEmissor = rf.idEmissor)
    union 
    (SELECT distinct Alias as aliasativo,'' as Emissor,0 as PrecisaEmissor,'' as RatingEmissaoMAI,'' as ratingemissor FROM futuro )
    union 
    (SELECT distinct Alias as aliasativo,'' as Emissor,0 as PrecisaEmissor,'' as RatingEmissaoMAI,'' as ratingemissor FROM opcao )
    union 
    (SELECT distinct AliasCota as aliasativo,'' as Emissor,0 as PrecisaEmissor,'' as RatingEmissaoMAI,'' as ratingemissor FROM fundo )
    """
    return  app.pd.read_sql_query(sql, app.db.engine)   


def GetCustodiaAdm():
    sql = """
    SELECT posicao.cgc,operacao.aliasativo,sum(qtd) as qtd from posicao 
    inner join operacao on operacao.cgc = posicao.cgc and operacao.aliasoperacao = posicao.aliasoperacao
    where data = '""" + app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d') + """'
    and operacao.aliasativo <> 'SPOT#BRLOTC@REAL'
    and operacao.aliasativo <> 'RF#BRLB3@Compromissada'
    and operacao.aliasativo not like 'RF#%@TERMO%'
    and operacao.aliasativo not like 'Cota#%'
    group by posicao.cgc,operacao.aliasativo
    """
    return  app.pd.read_sql_query(sql, app.db.engine)   



print('Garantindo a Existencia dos Controles:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfControles = app.pd.DataFrame.from_dict({})
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Impacto de Taxa de Adm e Custodia"
Controle.Descricao = "Limita o impacto diário no valor cadastrado com uma margem de erro 10%"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Controle de Impacto"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Impacto de Taxa de Performance"
Controle.Descricao = "Limita o impacto diário no valor cadastrado com uma margem de erro 10%"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Controle de Impacto"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Impacto de Auditoria"
Controle.Descricao = "Limita o impacto diário em um valor arbitrário mocado no código"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Controle de Impacto"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Impacto de Taxa CVM"
Controle.Descricao = "Limita o impacto diário em um valor arbitrário mocado no código"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Controle de Impacto"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Impacto de Taxa Anbima"
Controle.Descricao = "Limita o impacto diário em um valor arbitrário mocado no código"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Controle de Impacto"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Impacto Outras Despesas"
Controle.Descricao = "Limita o impacto diário em um valor arbitrário mocado no código"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Controle de Impacto"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Impacto Saldo em Tesouraria"
Controle.Descricao = "Limita o impacto diário em um valor arbitrário mocado no código"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Controle de Impacto"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Impacto Ajustes Contabeis"
Controle.Descricao = "Limita o impacto diário em um valor arbitrário mocado no código"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Controle de Impacto"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Ausência de Cadastro Ativo"
Controle.Descricao = "Aponta caso haja um ativo custodiado sem cadastro no MaiApp"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Conformidade de Cadastro"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Ausência de Cadastro Emissor"
Controle.Descricao = "Aponta caso haja um ativo custodiado sem cadastro de Emissor no MaiApp"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Conformidade de Cadastro"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Ausência de cadastro de Rating de Emissão"
Controle.Descricao = "Aponta caso haja boletas de ativos de renda fixa sem rating de emissão cadastrados"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Conformidade de Cadastro"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Ausência de cadastro de Rating de Emissor"
Controle.Descricao = "Aponta caso haja boletas de ativos de renda fixa sem rating de emissão cadastrados"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Pre Trade"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Posição em RF sem Grau de Investimento"
Controle.Descricao = "Aponta caso haja boletas de ativos de renda fixa sem grau de investimento em fundos pertinentes"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Pre Trade"
Controle.Tipo = "Regulatório"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
Controle = cl_Controle()
Controle.Nome = "Diferença de Custódia"
Controle.Descricao = "Aponta caso haja diferença de custódia entre as boletas e a posição reportada da carteira do administrador"
Controle.InstrucaoNormativa = ""
Controle.SubTipo = "Controle de Impacto"
Controle.Tipo = "Interno"
if not ControleExists(Controle): Controle.insert()
dfControles = app.pd.concat([dfControles,ParseDictToDF(Controle)], ignore_index=True)
###############################################################################################
###############################################################################################
print('Fim Garantia Existencia de controles:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
print('Inicio montagem lista execucao:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfControles_internos = dfControles[dfControles['Tipo']=='Interno']
dfFundos = GetDFFundosInternosAtivos()
dfFundos['Tipo'] = 'Interno'
dfListaExecucaoControlesInternos = app.pd.merge(left=dfFundos.copy(), right=dfControles_internos.copy(),how='left',left_on=['Tipo'],right_on=['Tipo']).copy()
dfListaExecucao = app.pd.DataFrame.from_dict({})
dfListaExecucao = app.pd.concat([dfListaExecucao,dfListaExecucaoControlesInternos], ignore_index=True)
del dfListaExecucaoControlesInternos
del dfFundos
del dfControles_internos
print('Fim montagem lista execucao:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
###############################################################################################

###############################################################################################
############################## Inicio dos Controles ##########################################

dfPLD_2 = GetPLD_2()
print('carregando pld-2:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfPLD_1 = GetPLD_1()
print('carregando pld-1:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfcotaD_1 = GetcotaD_1()
print('carregando cotad-1:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfcotaD_2 = GetcotaD_2()
print('carregando cotad-2:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfResultado_D_1 = GetResultado_D_1()
print('carregando resultadod-1:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfCadastroFundo = GetCadastroFundo()
print('carregando cadastro:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfCustodia = GetCustodia()
print('carregando custodia:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfCadastro = GetCadastroAtivos()
print('carregando Cadastro Ativos:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfCustodiaAdm = GetCustodiaAdm()
print('carregando Custodia Adm:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))

dfCadastroFundointernoativo = dfCadastroFundo[dfCadastroFundo['datainiciomai'].isna()==False].copy()
dfCadastroFundointernoativo = dfCadastroFundointernoativo[ app.pd.to_datetime(dfCadastroFundointernoativo['datainiciomai'])!=app.pd.to_datetime('1900-01-01')]
dfCadastroFundointernoativo = dfCadastroFundointernoativo[ app.pd.to_datetime(dfCadastroFundointernoativo['datainiciomai'])!=app.pd.to_datetime('1899-12-30')]
dfCadastroFundointernoativo = dfCadastroFundointernoativo[ dfCadastroFundointernoativo['interno']==True]
dfCadastroFundointernoativo = dfCadastroFundointernoativo[ 
                                                           (app.pd.to_datetime(dfCadastroFundointernoativo['datafimmai'])==app.pd.to_datetime('1899-12-30')) |
                                                           (app.pd.to_datetime(dfCadastroFundointernoativo['datafimmai'])==app.pd.to_datetime('1900-01-01'))
                                                         ]

dfCadastroFundointernoativo = dfCadastroFundointernoativo[['cgc','alias','mxdtpos']].copy()
dfCustodia = app.pd.merge(left=dfCustodia.copy(), right=dfCadastro.copy(),how='left',left_on=['aliasativo'],right_on=['aliasativo']).copy()
dfCustodia = app.pd.merge(left=dfCustodia.copy(), right=dfCustodiaAdm.copy(),how='left',left_on=['cgc','aliasativo'],right_on=['cgc','aliasativo']).copy()
dfCustodia.loc[dfCustodia['Emissor'].isna(),'Emissor']=''

dfPrecisaCadastroAtivo = dfCustodia[dfCustodia['PrecisaEmissor'].isna()].copy()

dfCustodia['RatingEmissaoMAI'] = dfCustodia['RatingEmissaoMAI'].fillna('')
dfCustodia['ratingemissor'] = dfCustodia['ratingemissor'].fillna('')

listratingsmai = ['AAA','AA','A','BBB','BB','B','CCC','CC','C']
listratingsmaigrauinvestimentoEmissao = ['AAA','AA','A','BBB']
dfCustodiaSemRatingEmissaoMai = dfCustodia[(dfCustodia['RatingEmissaoMAI'].isin(listratingsmai)==False) & (app.tkstr.left(dfCustodia['aliasativo'].str,3)=='RF#') ].copy()
dfCustodiaSemRatingEmissorMai = dfCustodia[(dfCustodia['ratingemissor'].isin(listratingsmai)==False) & (app.tkstr.left(dfCustodia['aliasativo'].str,3)=='RF#')].copy()
dfCustodiaSemGrauInvEmissaoMai = dfCustodia[(dfCustodia['RatingEmissaoMAI'].isin(listratingsmaigrauinvestimentoEmissao)==False) & (app.tkstr.left(dfCustodia['aliasativo'].str,3)=='RF#')].copy()
dfCustodiaSemGrauInvEmissorMai = dfCustodia[(dfCustodia['ratingemissor'].isin(listratingsmaigrauinvestimentoEmissao)==False) & (app.tkstr.left(dfCustodia['aliasativo'].str,3)=='RF#')].copy()

dfCustodiaSemRatingEmissaoMai = dfCustodiaSemRatingEmissaoMai[
                                                                (app.tkstr.left(dfCustodiaSemRatingEmissaoMai['aliasativo'].str,12)!='RF#BRLB3@LFT')&
                                                                (app.tkstr.left(dfCustodiaSemRatingEmissaoMai['aliasativo'].str,12)!='RF#BRLB3@LTN')&
                                                                (app.tkstr.left(dfCustodiaSemRatingEmissaoMai['aliasativo'].str,12)!='RF#BRLB3@NTN')
                                                                ].copy()

dfCustodiaSemRatingEmissorMai = dfCustodiaSemRatingEmissorMai[
                                                                (app.tkstr.left(dfCustodiaSemRatingEmissorMai['aliasativo'].str,12)!='RF#BRLB3@LFT')&
                                                                (app.tkstr.left(dfCustodiaSemRatingEmissorMai['aliasativo'].str,12)!='RF#BRLB3@LTN')&
                                                                (app.tkstr.left(dfCustodiaSemRatingEmissorMai['aliasativo'].str,12)!='RF#BRLB3@NTN')
                                                                ].copy()

dfCustodiaSemGrauInvEmissaoMai = dfCustodiaSemGrauInvEmissaoMai[
                                                                (app.tkstr.left(dfCustodiaSemGrauInvEmissaoMai['aliasativo'].str,12)!='RF#BRLB3@LFT')&
                                                                (app.tkstr.left(dfCustodiaSemGrauInvEmissaoMai['aliasativo'].str,12)!='RF#BRLB3@LTN')&
                                                                (app.tkstr.left(dfCustodiaSemGrauInvEmissaoMai['aliasativo'].str,12)!='RF#BRLB3@NTN')
                                                                ].copy()

dfCustodiaSemGrauInvEmissorMai = dfCustodiaSemGrauInvEmissorMai[
                                                                (app.tkstr.left(dfCustodiaSemGrauInvEmissorMai['aliasativo'].str,12)!='RF#BRLB3@LFT')&
                                                                (app.tkstr.left(dfCustodiaSemGrauInvEmissorMai['aliasativo'].str,12)!='RF#BRLB3@LTN')&
                                                                (app.tkstr.left(dfCustodiaSemGrauInvEmissorMai['aliasativo'].str,12)!='RF#BRLB3@NTN')
                                                                ].copy()

dfCustodiaSemRatingEmissaoMai = app.pd.merge(left=dfCustodiaSemRatingEmissaoMai.copy(), right=dfCadastroFundointernoativo.copy(),how='inner',left_on=['cgc'],right_on=['cgc']).copy()
dfCustodiaSemRatingEmissorMai = app.pd.merge(left=dfCustodiaSemRatingEmissorMai.copy(), right=dfCadastroFundointernoativo.copy(),how='inner',left_on=['cgc'],right_on=['cgc']).copy()
dfCustodiaSemGrauInvEmissaoMai = app.pd.merge(left=dfCustodiaSemGrauInvEmissaoMai.copy(), right=dfCadastroFundointernoativo.copy(),how='inner',left_on=['cgc'],right_on=['cgc']).copy()
dfCustodiaSemGrauInvEmissorMai = app.pd.merge(left=dfCustodiaSemGrauInvEmissorMai.copy(), right=dfCadastroFundointernoativo.copy(),how='inner',left_on=['cgc'],right_on=['cgc']).copy()


dfCustodiaSemRatingEmissaoMai = dfCustodiaSemRatingEmissaoMai[['cgc','aliasativo','alias','RatingEmissaoMAI','ratingemissor']].copy()
dfCustodiaSemRatingEmissorMai = dfCustodiaSemRatingEmissorMai[['cgc','aliasativo','alias','RatingEmissaoMAI','ratingemissor']].copy()
dfCustodiaSemGrauInvEmissaoMai = dfCustodiaSemGrauInvEmissaoMai[['cgc','aliasativo','alias','RatingEmissaoMAI','ratingemissor']].copy()
dfCustodiaSemGrauInvEmissorMai = dfCustodiaSemGrauInvEmissorMai[['cgc','aliasativo','alias','RatingEmissaoMAI','ratingemissor']].copy()



dfPrecisaEmissorENaoTem = dfCustodia[(dfCustodia['Emissor']=='') & (dfCustodia['PrecisaEmissor']==1)].copy()
dfPrecisaEmissorENaoTem = app.pd.merge(left=dfPrecisaEmissorENaoTem.copy(), right=dfCadastroFundointernoativo.copy(),how='inner',left_on=['cgc'],right_on=['cgc']).copy()

dfCustodia = app.pd.merge(left=dfCustodia.copy(), right=dfCadastroFundointernoativo.copy(),how='inner',left_on=['cgc'],right_on=['cgc']).copy()
dfCustodia['qtd'] = dfCustodia['qtd'].fillna(0)
dfCustodia['dif'] = dfCustodia['qtd']-dfCustodia['custodia']
dfCustodia_divergente = dfCustodia[abs(dfCustodia['dif'])>0.01]


dfPrecisaCadastroAtivo = dfPrecisaCadastroAtivo[dfPrecisaCadastroAtivo['cgc']!='11702084000121']
dfPrecisaCadastroAtivo = dfPrecisaCadastroAtivo[dfPrecisaCadastroAtivo['cgc']!='13107003000170']
dfPrecisaEmissorENaoTem = dfPrecisaEmissorENaoTem[dfPrecisaEmissorENaoTem['alias']!='Pascal']
dfPrecisaEmissorENaoTem = dfPrecisaEmissorENaoTem[dfPrecisaEmissorENaoTem['alias']!='Saint German']
dfCustodia_divergente = dfCustodia_divergente[dfCustodia_divergente['alias']!='Pascal']
dfCustodia_divergente = dfCustodia_divergente[dfCustodia_divergente['alias']!='Saint German']


del dfCadastro
del dfCustodia
del dfCadastroFundointernoativo


dfListaExecucao = app.pd.merge(left=dfListaExecucao.copy(), right=dfPLD_2.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
dfListaExecucao = app.pd.merge(left=dfListaExecucao.copy(), right=dfPLD_1.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
dfListaExecucao = app.pd.merge(left=dfListaExecucao.copy(), right=dfcotaD_1.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
dfListaExecucao = app.pd.merge(left=dfListaExecucao.copy(), right=dfcotaD_2.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
dfListaExecucao = app.pd.merge(left=dfListaExecucao.copy(), right=dfResultado_D_1.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
dfListaExecucao = app.pd.merge(left=dfListaExecucao.copy(), right=dfCadastroFundo.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()

del dfPLD_2
del dfPLD_1
del dfcotaD_1
del dfcotaD_2
del dfResultado_D_1

dfListaExecucao['PL_d_2'] = dfListaExecucao['PL_d_2'].fillna(0)
dfListaExecucao['PL_d_1'] = dfListaExecucao['PL_d_1'].fillna(0)
dfListaExecucao['cota_d_2'] = dfListaExecucao['cota_d_2'].fillna(0)
dfListaExecucao['cota_d_1'] = dfListaExecucao['cota_d_1'].fillna(0)
dfListaExecucao['resultado'] = dfListaExecucao['resultado'].fillna(0)
dfListaExecucao = dfListaExecucao[dfListaExecucao['PL_d_2']!=0]
dfListaExecucao = dfListaExecucao[dfListaExecucao['PL_d_1']!=0]
dfListaExecucao = dfListaExecucao[dfListaExecucao['resultado']!=0]
dfListaExecucao = dfListaExecucao[dfListaExecucao['cota_d_2']!=0]
dfListaExecucao = dfListaExecucao[dfListaExecucao['cota_d_1']!=0]
dfListaExecucao['rent'] = dfListaExecucao['cota_d_1']/dfListaExecucao['cota_d_2']-1
dfListaExecucao['rent'] = dfListaExecucao['rent'].fillna(0)
dfListaExecucao['resultado_Cota'] = dfListaExecucao['rent']*dfListaExecucao['PL_d_2']
dfListaExecucao['Batido?'] = abs(dfListaExecucao['resultado_Cota']-dfListaExecucao['resultado'])<100
dfListaExecucao =dfListaExecucao[ dfListaExecucao['Batido?']==True]


cntrl = "Impacto de Taxa de Adm e Custodia"
SubTipo = "Controle de Impacto"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfResultadoEspecifico_Taxa_Administracao = GetResultadoespecifico_D_1('SPOT#BRLOTC@REAL','Administra','Administracao')
dfResultadoEspecifico_Taxa_Custoodia = GetResultadoespecifico_D_1('SPOT#BRLOTC@REAL','Cust%dia','Custodia')
dfList = app.pd.merge(left=dfList.copy(), right=dfResultadoEspecifico_Taxa_Administracao.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
dfList = app.pd.merge(left=dfList.copy(), right=dfResultadoEspecifico_Taxa_Custoodia.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
del dfResultadoEspecifico_Taxa_Administracao
del dfResultadoEspecifico_Taxa_Custoodia
dfList['Administracao'] = dfList['Administracao'].fillna(0)
dfList['Custodia'] = dfList['Custodia'].fillna(0)
dfList['ResultadoAdm'] = dfList['Administracao']+dfList['Custodia']
dfList['ImpactoAdm'] = abs(dfList['ResultadoAdm']/dfList['PL_d_2'])

dfList_controle_Taxa_adm = dfList[dfList['ImpactoAdm']>dfList['TaxaAdministracao']].copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))


cntrl = "Impacto de Taxa de Performance"
SubTipo = "Controle de Impacto"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfResultadoEspecifico = GetResultadoespecifico_D_1('SPOT#BRLOTC@REAL','Perform','Perform')
dfList = app.pd.merge(left=dfList.copy(), right=dfResultadoEspecifico.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
del dfResultadoEspecifico
dfList['Perform'] = dfList['Perform'].fillna(0)
dfList['Perform'] = abs(dfList['Perform']/dfList['PL_d_2'])

dfList_controle_Taxa_perform = dfList[dfList['Perform']>0.001*dfList['TaxaPerformance']].copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))


cntrl = "Impacto de Auditoria"
SubTipo = "Controle de Impacto"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfResultadoEspecifico = GetResultadoespecifico_D_1('SPOT#BRLOTC@REAL','Auditoria','Auditoria')
dfList = app.pd.merge(left=dfList.copy(), right=dfResultadoEspecifico.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
del dfResultadoEspecifico
dfList['Auditoria'] = dfList['Auditoria'].fillna(0)
dfList['ImpactoAuditoria'] = abs(dfList['Auditoria']/dfList['PL_d_2'])

dfList_controle_auditoria = dfList[dfList['ImpactoAuditoria']>0.001].copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))


cntrl = "Impacto de Taxa CVM"
SubTipo = "Controle de Impacto"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfResultadoEspecifico = GetResultadoespecifico_D_1('SPOT#BRLOTC@REAL','cvm','cvm')
dfList = app.pd.merge(left=dfList.copy(), right=dfResultadoEspecifico.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
del dfResultadoEspecifico
dfList['cvm'] = dfList['cvm'].fillna(0)
dfList['Impactocvm'] = abs(dfList['cvm']/dfList['PL_d_2'])

dfList_controle_taxacvm = dfList[dfList['Impactocvm']>0.0001].copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))


cntrl = "Impacto de Taxa Anbima"
SubTipo = "Controle de Impacto"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfResultadoEspecifico = GetResultadoespecifico_D_1('SPOT#BRLOTC@REAL','Anbima','Anbima')
dfList = app.pd.merge(left=dfList.copy(), right=dfResultadoEspecifico.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
del dfResultadoEspecifico
dfList['Anbima'] = dfList['Anbima'].fillna(0)
dfList['ImpactoAnbima'] = abs(dfList['Anbima']/dfList['PL_d_2'])

dfList_controle_taxaAnbima = dfList[dfList['ImpactoAnbima']>0.0001].copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))


cntrl = "Impacto Outras Despesas"
SubTipo = "Controle de Impacto"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfResultadoEspecifico = GetResultadoespecifico_D_1('SPOT#BRLOTC@REAL','Outras Despesas','OutrasDespesas')
dfList = app.pd.merge(left=dfList.copy(), right=dfResultadoEspecifico.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
del dfResultadoEspecifico
dfList['OutrasDespesas'] = dfList['OutrasDespesas'].fillna(0)
dfList['ImpactoOutrasDespesas'] = abs(dfList['OutrasDespesas']/dfList['PL_d_2'])

dfList_controle_OutrasDespesas = dfList[dfList['ImpactoOutrasDespesas']>0.0001].copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))


cntrl = "Impacto Saldo em Tesouraria"
SubTipo = "Controle de Impacto"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfResultadoEspecifico = GetResultadoespecifico_D_1('SPOT#BRLOTC@REAL','Saldo em Tesouraria','Tesouraria')
dfList = app.pd.merge(left=dfList.copy(), right=dfResultadoEspecifico.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
del dfResultadoEspecifico
dfList['Tesouraria'] = dfList['Tesouraria'].fillna(0)
dfList['ImpactoTesouraria'] = abs(dfList['Tesouraria']/dfList['PL_d_2'])

dfList_controle_Tesouraria= dfList[dfList['ImpactoTesouraria']>0.00001].copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))


cntrl = "Impacto Ajustes Contabeis"
SubTipo = "Controle de Impacto"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfResultadoEspecifico = GetResultadoespecifico_D_1('SPOT#BRLOTC@REAL','Ajuste Contábil','AjustesContabeis')
dfList = app.pd.merge(left=dfList.copy(), right=dfResultadoEspecifico.copy(),how='left',left_on=['cgc'],right_on=['cgc']).copy()
del dfResultadoEspecifico
dfList['AjustesContabeis'] = dfList['AjustesContabeis'].fillna(0)
dfList['ImpactoAjustesContabeis'] = abs(dfList['AjustesContabeis']/dfList['PL_d_2'])

dfList_controle_AjustesContabeis= dfList[dfList['ImpactoAjustesContabeis']>0.0001].copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))



cntrl = "Ausência de Cadastro Ativo"
SubTipo = "Conformidade de Cadastro"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfList = app.pd.merge(left=dfList.copy(), right=dfPrecisaCadastroAtivo.copy(),how='inner',left_on=['cgc'],right_on=['cgc']).copy()
del dfPrecisaCadastroAtivo

dfList_controle_ausenciacadastroativo = dfList.copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))


cntrl = "Ausência de Cadastro Emissor"
SubTipo = "Conformidade de Cadastro"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfList = app.pd.merge(left=dfList.copy(), right=dfPrecisaEmissorENaoTem.copy(),how='inner',left_on=['cgc'],right_on=['cgc']).copy()
del dfPrecisaEmissorENaoTem

dfList_controle_ausenciacadastroEmissor = dfList.copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))


cntrl = "Ausência de cadastro de Rating de Emissão"
SubTipo = "Conformidade de Cadastro"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfList = app.pd.merge(left=dfList.copy(), right=dfCustodiaSemRatingEmissaoMai.copy(),how='inner',left_on=['cgc'],right_on=['cgc']).copy()
del dfCustodiaSemRatingEmissaoMai
dfList_controle_ausenciaratingEmissao = dfList.copy()
print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))


cntrl = "Ausência de cadastro de Rating de Emissor"
SubTipo = "Conformidade de Cadastro"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfList = app.pd.merge(left=dfList.copy(), right=dfCustodiaSemRatingEmissorMai.copy(),how='inner',left_on=['cgc'],right_on=['cgc']).copy()
del dfCustodiaSemRatingEmissorMai

dfList_controle_ausenciaratingEmissor = dfList.copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))

cntrl = "Diferença de Custódia"
SubTipo = "Controle de Impacto"
Tipo = "Interno"
print('Inicio Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfList = dfListaExecucao[(dfListaExecucao['Nome'] == cntrl) & (dfListaExecucao['SubTipo'] == SubTipo) & (dfListaExecucao['Tipo'] == Tipo)].copy()
dfList = app.pd.merge(left=dfList.copy(), right=dfCustodia_divergente.copy(),how='inner',left_on=['cgc'],right_on=['cgc']).copy()
del dfCustodia_divergente

dfList_controle_divergenciacustodia = dfList.copy()

print('Fim Controle ' + cntrl + ' :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))

###############################################################################################
############################## Fim dos Controles ##########################################

############################## Fim dos Controles Internos...##########################################
# aqui  o ideal seria pegar a lista de execução de tudoo que não intero se existir inspeção vai fundo...
############################## Fim dos Controles Internos...##########################################


###############################################################################################
############################## Carga Apontamentos... ##########################################
print('Carga de Apontamentos na Base:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))

del dfControles
del dfCustodiaAdm
del Controle
del cntrl
del listratingsmai
del listratingsmaigrauinvestimentoEmissao
del SubTipo
del Tipo


dfList = app.pd.DataFrame({})

dfList_controle_ausenciacadastroativo['Rotolo'] = 'ImpactoAjustesContabeis'
dfList_controle_AjustesContabeis['Limite'] = '0.0001'
dfList_controle_AjustesContabeis['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_AjustesContabeis['OBS'] = 'Ajustes Contábeis não podem superar um impact superior a 1bps em um dia'
dfList_controle_AjustesContabeis['idInspecao'] = 0
dfList_controle_AjustesContabeis = dfList_controle_AjustesContabeis.rename(columns={
    "ImpactoAjustesContabeis":'ValorMetrica',
    "idfundo":'idFundo'
    }).copy()
dfList = dfList_controle_AjustesContabeis[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite']].copy()
del dfList_controle_AjustesContabeis


dfList_controle_auditoria['Rotolo'] = 'ImpactoAuditoria'
dfList_controle_auditoria['Limite'] = '0.0001'
dfList_controle_auditoria['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_auditoria['OBS'] = 'Gastos com auditoria não podem superar um impact superior a 1bps em um dia'
dfList_controle_auditoria['idInspecao'] = 0
dfList_controle_auditoria = dfList_controle_auditoria.rename(columns={
    "ImpactoAuditoria":'ValorMetrica',
    "idfundo":'idFundo'
    }).copy()
dfList = app.pd.concat([dfList,dfList_controle_auditoria[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite','Rotolo','Alias']].copy()], ignore_index=True)
del dfList_controle_auditoria


dfList_controle_ausenciacadastroativo['Rotolo'] = 'AusenciaCadastroAtivo'
dfList_controle_ausenciacadastroativo['Limite'] = '0'
dfList_controle_ausenciacadastroativo['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_ausenciacadastroativo['idInspecao'] = 0
dfList_controle_ausenciacadastroativo['ValorMetrica'] = 1
dfList_controle_ausenciacadastroativo = dfList_controle_ausenciacadastroativo.rename(columns={
    "aliasativo":'OBS',
    "idfundo":'idFundo'
    }).copy()
dfList = app.pd.concat([dfList,dfList_controle_ausenciacadastroativo[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite','Rotolo','Alias']].copy()], ignore_index=True)
del dfList_controle_ausenciacadastroativo


dfList_controle_ausenciacadastroEmissor['Rotolo'] = 'AusenciaCadastroEmissor'
dfList_controle_ausenciacadastroEmissor['Limite'] = '0'
dfList_controle_ausenciacadastroEmissor['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_ausenciacadastroEmissor['idInspecao'] = 0
dfList_controle_ausenciacadastroEmissor['ValorMetrica'] = 1
dfList_controle_ausenciacadastroEmissor = dfList_controle_ausenciacadastroEmissor.rename(columns={
    "aliasativo":'OBS',
    "idfundo":'idFundo'
    }).copy()
dfList = app.pd.concat([dfList,dfList_controle_ausenciacadastroEmissor[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite','Rotolo','Alias']].copy()], ignore_index=True)
del dfList_controle_ausenciacadastroEmissor

dfList_controle_ausenciaratingEmissao['Rotolo'] = 'AusenciaRatingEmissao'
dfList_controle_ausenciaratingEmissao['Limite'] = '0'
dfList_controle_ausenciaratingEmissao['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_ausenciaratingEmissao['idInspecao'] = 0
dfList_controle_ausenciaratingEmissao['ValorMetrica'] = 1
dfList_controle_ausenciaratingEmissao = dfList_controle_ausenciaratingEmissao.rename(columns={
    "aliasativo":'OBS',
    "idfundo":'idFundo'
    }).copy()
dfList = app.pd.concat([dfList,dfList_controle_ausenciaratingEmissao[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite','Rotolo','Alias']].copy()], ignore_index=True)
del dfList_controle_ausenciaratingEmissao

dfList_controle_ausenciaratingEmissor['Rotolo'] = 'AusenciaRatingEmissor'
dfList_controle_ausenciaratingEmissor['Limite'] = '0'
dfList_controle_ausenciaratingEmissor['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_ausenciaratingEmissor['idInspecao'] = 0
dfList_controle_ausenciaratingEmissor['ValorMetrica'] = 1
dfList_controle_ausenciaratingEmissor = dfList_controle_ausenciaratingEmissor.rename(columns={
    "aliasativo":'OBS',
    "idfundo":'idFundo'
    }).copy()
dfList = app.pd.concat([dfList,dfList_controle_ausenciaratingEmissor[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite','Rotolo','Alias']].copy()], ignore_index=True)
del dfList_controle_ausenciaratingEmissor

dfList_controle_OutrasDespesas['Rotolo'] = 'ImpactoOutrasDespesas'
dfList_controle_OutrasDespesas['Limite'] = '0.001'
dfList_controle_OutrasDespesas['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_OutrasDespesas['OBS'] = 'Gastos com outras despesas não podem superar um impact superior a 1bps em um dia'
dfList_controle_OutrasDespesas['idInspecao'] = 0
dfList_controle_OutrasDespesas = dfList_controle_OutrasDespesas.rename(columns={
    "ImpactoOutrasDespesas":'ValorMetrica',
    "idfundo":'idFundo'
    }).copy()
dfList = app.pd.concat([dfList,dfList_controle_OutrasDespesas[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite','Rotolo','Alias']].copy()], ignore_index=True)
del dfList_controle_OutrasDespesas

dfList_controle_Taxa_adm['Rotolo'] = 'ImpactoTaxaAdm'
dfList_controle_Taxa_adm['Limite'] = '0'
dfList_controle_Taxa_adm['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_Taxa_adm['OBS'] = 'Gastos com taxa adm não podem superar um impact superior o valor cadastrado'
dfList_controle_Taxa_adm['idInspecao'] = 0
dfList_controle_Taxa_adm = dfList_controle_Taxa_adm.rename(columns={
    "ImpactoAdm":'ValorMetrica',
    "idfundo":'idFundo'
    }).copy()
dfList = app.pd.concat([dfList,dfList_controle_Taxa_adm[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite','Rotolo','Alias']].copy()], ignore_index=True)
del dfList_controle_Taxa_adm

dfList_controle_Taxa_perform['Rotolo'] = 'ImpactoTaxaPerform'
dfList_controle_Taxa_perform['Limite'] = '0.001'
dfList_controle_Taxa_perform['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_Taxa_perform['OBS'] = 'Gastos com taxa perform não podem superar um impact superior 10bps multiplicado pela a TaxaPerformance cadastrada'
dfList_controle_Taxa_perform['idInspecao'] = 0
dfList_controle_Taxa_perform = dfList_controle_Taxa_perform.rename(columns={
    "Perform":'ValorMetrica',
    "idfundo":'idFundo'
    }).copy()
dfList = app.pd.concat([dfList,dfList_controle_Taxa_perform[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite','Rotolo','Alias']].copy()], ignore_index=True)
del dfList_controle_Taxa_perform

dfList_controle_taxaAnbima['Rotolo'] = 'ImpactoTaxaAnbima'
dfList_controle_taxaAnbima['Limite'] = '0.0001'
dfList_controle_taxaAnbima['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_taxaAnbima['OBS'] = 'Gastos com taxa anbima não podem superar um impact superior a 1bp'
dfList_controle_taxaAnbima['idInspecao'] = 0
dfList_controle_taxaAnbima = dfList_controle_taxaAnbima.rename(columns={
    "ImpactoAnbima":'ValorMetrica',
    "idfundo":'idFundo'
    }).copy()
dfList = app.pd.concat([dfList,dfList_controle_taxaAnbima[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite','Rotolo','Alias']].copy()], ignore_index=True)
del dfList_controle_taxaAnbima

dfList_controle_taxacvm['Rotolo'] = 'ImpactoTaxaCVM'
dfList_controle_taxacvm['Limite'] = '0.0001'
dfList_controle_taxacvm['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_taxacvm['OBS'] = 'Gastos com taxa cvm não podem superar um impact superior a 1bp'
dfList_controle_taxacvm['idInspecao'] = 0
dfList_controle_taxacvm = dfList_controle_taxacvm.rename(columns={
    "Impactocvm":'ValorMetrica',
    "idfundo":'idFundo'
    }).copy()
dfList = app.pd.concat([dfList,dfList_controle_taxacvm[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite','Rotolo','Alias']].copy()], ignore_index=True)
del dfList_controle_taxacvm

dfList_controle_Tesouraria['Rotolo'] = 'ImpactoTesouraria'
dfList_controle_Tesouraria['Limite'] = '0.00001'
dfList_controle_Tesouraria['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_Tesouraria['OBS'] = 'Impacto de saldo em tesouraria tem que ser desprezível'
dfList_controle_Tesouraria['idInspecao'] = 0
dfList_controle_Tesouraria = dfList_controle_Tesouraria.rename(columns={
    "ImpactoTesouraria":'ValorMetrica',
    "idfundo":'idFundo'
    }).copy()
dfList = app.pd.concat([dfList,dfList_controle_Tesouraria[['idFundo','idControle','idInspecao','OBS','Data','ValorMetrica','Limite','Rotolo','Alias']].copy()], ignore_index=True)
del dfList_controle_Tesouraria

dfList_controle_divergenciacustodia['Rotolo'] = 'difCustodia'
dfList_controle_divergenciacustodia['Limite'] = '0.1'
dfList_controle_divergenciacustodia['Data'] = app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
dfList_controle_divergenciacustodia['idInspecao'] = 0
dfList_controle_divergenciacustodia = dfList_controle_divergenciacustodia.rename(columns={
    "dif":'ValorMetrica',
    "aliasativo":'OBS',
    "idfundo":'idFundo'
    }).copy()

dfList_controle_divergenciacustodia['qtd'] = dfList_controle_divergenciacustodia['qtd'].apply(lambda x: f'{x:.2f}')
dfList_controle_divergenciacustodia['custodia'] = dfList_controle_divergenciacustodia['custodia'].apply(lambda x: f'{x:.2f}')
dfList_controle_divergenciacustodia['OBS'] = dfList_controle_divergenciacustodia['OBS'] + ' out: ' + dfList_controle_divergenciacustodia['qtd'] + ' vs Mai: ' + dfList_controle_divergenciacustodia['custodia']
dfList = app.pd.concat([dfList,dfList_controle_divergenciacustodia[['idFundo','idControle','idInspecao','Rotolo','Alias','OBS','Data','ValorMetrica','Limite']].copy()], ignore_index=True)
del dfList_controle_divergenciacustodia


#del dfList['Alias']
#del dfList['Rotolo']
del dfListaExecucao
del dfCadastroFundo


bodyhtmltable = dfList[['Data','Alias','Rotolo','OBS']].to_html()

outlook = app.win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'mozaic.lmoza@terceiros.mag.com.br;mmmachado@mag.com.br;afarruda@mag.com.br'
mail.Subject = 'Lista de Apontamentos com data base ' + app.tkdtm.date_after_work_days(app.dt.now(),-1).strftime('%Y-%m-%d')
conteudo =  """<p> Segue lista de apontamentos de controles internos gerados automaticamente pelo MaiApp: </p>
            <div>""" + bodyhtmltable + """</div>
            <p>Caso entenda que algum elemento desta lista seja um "False Call" fique à vontade para responde este email</p>
            <p>Este email tem como objetivo sanear as bases e calibrar o processo de batimento de carteiras e processamento contábil gerencial</p>
            <p>Na segunda fase do projeto esta lista será disposta em uma tela do Mai APP e será parte de um fluxo de "feito conferido" </p>
            """           
mail.HTMLBody = f'''
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            {app.tkEmail.css}
        </head>
        <body>
            <section class="email">
                {conteudo}
            </section>
        </body>
    </html>
    '''        
mail.Send()
i=0
for index,row in dfList.iterrows():
    i = i+1
    print ('{:.2f}'.format(i/len(dfList)*100)+'%')
    Apontamento = cl_Apontamento()
    Apontamento.Data = app.pd.to_datetime(row['Data'],errors='coerce')
    Apontamento.IDFundo = row['idFundo']
    Apontamento.idControle = row['idControle']
    Apontamento.idInspecao = row['idInspecao']
    Apontamento.Obs = app.tkstr.left(row['OBS'],50)
    Apontamento.Limite = row['Limite']
    Apontamento.ValorMetrica = row['ValorMetrica']
    Apontamento.Status = 'Alerta'
    if not ApontamentoExists(Apontamento): 
        Apontamento.insert()

    



############################## Fim dos Controles ##########################################
###############################################################################################

print('Fim Carga Apontamentos:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))








