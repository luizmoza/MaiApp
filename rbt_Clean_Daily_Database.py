import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.append(r"../")
from app import app
from app.classes.cl_Opcao import cl_Opcao
from app.classes.cl_FechamentoOpcao import cl_FechamentoOpcao
#from app.classes.cl_Apontamento import cl_Apontamento
#from app.classes.cl_Controle import cl_Controle


#from app.classes.cl_Futuro import cl_Futuro
#from app.classes.cl_FechamentoFuturo import cl_FechamentoFuturo
# Futuro = cl_Futuro(**{})
# Futuro.Alias = 'Futuro#BRLB3@FUT ' + 'DAP' + ' ' + 'Q30'
# print(Futuro.Codigo)
# Futuro.IDFuturo = -1
# Futuro.get_id_alias()
# print(str(Futuro.IDFuturo))
# if Futuro.get():
#     print('O Id é :' + str(Futuro.IDFuturo))        
# else:
#     print('Não Achô!')        
    

#sys.exit('Para!')

if len(sys.argv)>1:
    data = sys.argv[1]
else:
    data = app.tkdtm.hoje
    
    
data = app.dt.strptime('2024-09-02','%Y-%m-%d')
    
# De 1 em 1h isso aqui vai passar, limpar e apontar problemas (se os apontamentos já não existerem)
    
############# Check list ##############
# Controles Básicos:
# Cadastro ok?
# fechamento para os ativos? --> Força Criação!
# Taxa de Administração + Custodia batida ?
# Taxa de Administração + Custodia batida ?
############# Check list ##############

###############################################################################################################################
########################################## Limpeza de tabelas e Expurgos ######################################################

# Agrupar e deletar movimentos antigos
# Agrupar e deletar Passivo antigos
# posições Antigas --> Limite?
# preços e fatores de risco --> Limite?

########################################## Limpeza de tabelas e Expurgos ######################################################
###############################################################################################################################
###############################################################################################################################
########################################## Boletas Automáticas  ###############################################################

# Cotas de Fundso Abertos
# Compromissadas
# Dinheiros CPR
# Termos de Ação

########################################## Limpeza de tabelas e Expurgos ######################################################
###############################################################################################################################
###############################################################################################################################
########################################## Controle de Custódia ###############################################################

# Somar Boletas Agrupando por ativo , somar posição agrupando por ativo.... comparar a quantidade.... tem que bater....
# Se não bater gera apontamento

########################################## Controle de Custódia ###############################################################
###############################################################################################################################
###############################################################################################################################
################################################## Limpeza Profunda ###########################################################
print('Iniciando Limpa Cadastros NTNs:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
app.db.connect()
app.db.execRawQuery("update operacao set aliasativo = replace(aliasativo,'NTNB','NTN-B') where aliasativo like '%NTNB%'")
app.db.execRawQuery("update operacao set aliasativo = replace(aliasativo,'NTNC','NTN-C') where aliasativo like '%NTNC%'")
app.db.execRawQuery("update operacao set aliasativo = replace(aliasativo,'NTNF','NTN-F') where aliasativo like '%NTNF%'")
app.db.execRawQuery("update posicao set aliasativo = replace(aliasativo,'NTNB','NTN-B') where aliasativo like '%NTNB%'")
app.db.execRawQuery("update posicao set aliasativo = replace(aliasativo,'NTNC','NTN-C') where aliasativo like '%NTNC%'")
app.db.execRawQuery("update posicao set aliasativo = replace(aliasativo,'NTNF','NTN-F') where aliasativo like '%NTNF%'")
app.db.execRawQuery("update rf set alias = replace(alias,'NTNB','NTN-B') where alias like '%NTNB%'")
app.db.execRawQuery("update rf set alias = replace(alias,'NTNC','NTN-C') where alias like '%NTNC%'")
app.db.execRawQuery("update rf set alias = replace(alias,'NTNF','NTN-F') where alias like '%NTNF%'")
app.db.execRawQuery("update Futuro set alias = replace(alias,'FUT#','Futuro#') where alias like 'FUT#%'")
app.db.execRawQuery("update posicao set aliasativo = replace(aliasativo,'FUT#','Futuro#') where aliasativo like 'FUT#%'")
app.db.execRawQuery("update operacao set aliasativo = replace(aliasativo,'FUT#','Futuro#') where aliasativo like 'FUT#%'")
app.db.execRawQuery("update Opcao set alias = replace(alias,'OPT#','Opcao#') where alias like 'OPT#%'")
app.db.execRawQuery("update posicao set aliasativo = replace(aliasativo,'OPT#','Opcao#') where aliasativo like 'OPT#%'")
app.db.execRawQuery("update operacao set aliasativo = replace(aliasativo,'OPT#','Opcao#') where aliasativo like 'OPT#%'")
app.db.execRawQuery("execute LimpaBoletasFracionarios")
app.db.execRawQuery("execute LimpaOperacoesDuplicadas")
app.db.execRawQuery("update operacao set AliasAtivo = 'RF#BRLB3@TERMO' where AliasAtivo like 'RF#BRLB3@TERM3%'")
app.db.drop()

# Evitar explosões.... deve ter uma maneira mais inteligente de fazer isso.....
#Set rs = mai.dbMai.Execute("update mov set qtd = 1 where aliasAtivo = 'RF#BRLB3@Compromissada' and datamov <= '" & Format(data, "yyyy-mm-dd") & "'")
#Set rs = mai.dbMai.Execute("update mov set qtd = 1 where aliasAtivo = 'SPOT#BRLOTC@REAL' and datamov < '" & Format(data, "yyyy-mm-dd") & "'")
# Evitar explosões.... deve ter uma maneira mais inteligente de fazer isso.....

app.db.drop()
################################################## Limpeza Profunda ###########################################################
###############################################################################################################################
###############################################################################################################################
################################## Acerta cadastro cotistas conta e ordem #####################################################
print('Iniciando ajuste cadastros cotistas Conta e Ordem:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dictdistribuidor = app.pd.read_sql_query("Select distinct iddistribuidor,cgc from distribuidor", app.db.engine)
dictcotistassemcgc = app.pd.read_sql_query("Select distinct codrefcotistafundo.idcotista,iddistribuidor from codrefcotistafundo inner join cotista on codrefcotistafundo.idcotista = cotista.idcotista where codrefcotistafundo.tipo = 'HB' and (cgc = '' or cgc is null)", app.db.engine)
app.db.connect()
for index, row in dictcotistassemcgc.iterrows():
#    sys.exit('Primeira Tentativa... tirar isso aqui se a query não estiver cagando a base....')
    app.db.execRawQuery("update cotista set cgc = '" + dictdistribuidor[ dictdistribuidor['iddistribuidor'] == row['iddistribuidor']]['cgc'].iloc[0] + "' where idcotista = " + str(row['idcotista']))
app.db.drop()
################################## Acerta cadastro cotistas conta e ordem #####################################################
###############################################################################################################################
###############################################################################################################################
################################ Cria fechamento de opções sintéticos > D-5 ###################################################
# Mudança de nome de opção de Ação !!!!!! ou falta de boleta de rolagem
print('Iniciando Criação Fechamentos Sintéticos Opções:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
sql = """
Select data,vl,pu,pu1,qtd,qtd1,fin,fin1,vl1,
operacao.cgc as cgc,
operacao.aliasoperacao as aliasoperacao,
data,operacao.aliasativo as aliasativo,
posicao.pu,
posicao.pu1,
operacao.marcacao 
from posicao 
inner join operacao on operacao.cgc = posicao.cgc 
and operacao.aliasoperacao = posicao.aliasoperacao 
where posicao.data >= '""" + app.dt.strftime(app.tkdtm.date_after_work_days(data, -5), "%Y-%m-%d") +  """' 
and operacao.cgc not like '%a'  
and Upper(operacao.AliasAtivo) like 'Opcao#%' 
"""
dfPusOps = app.pd.read_sql_query(sql, app.db.engine)
Opcao = cl_Opcao(**{})
FechamentoOpcao = cl_FechamentoOpcao(**{})
for index,row in dfPusOps.iterrows():
    Opcao.Alias = row['aliasativo']
    Opcao.get_id_alias()
    if Opcao.IDOpcao == 0:
#        Controle = cl_Controle(app.db)
#        Controle.Nome = "Ausência de Cadastro Opção"
#        print(Controle.Nome)
        print(row['aliasativo'])
        sys.exit('Cadastro de Preço Interrompido por ausencia de cadastro!')
#        Controle.get_id_nome(app.db)
#        if Controle.idControle == '0' :
#            Controle.idControle = app.tk.generate_guid()
#            Controle.Tipo = "Interno"
#            Controle.Subtipo = "Falha Cadastro"
#            app.db.session.add(Controle)
#        Apontamento = cl_Apontamento(app.db)
#        Apontamento.idControle = Controle.idControle
#        Apontamento.Data = row['data']
#        Apontamento.IDFundo = 0
#        Apontamento.get_id_IDFundo_idControle_data(app.db)
#        if Apontamento.idApontamento == '0':
#            Apontamento.Status = 'Warning'
#            Apontamento.ValorMetrica = 0
#            Apontamento.Obs = row['aliasativo']
#            app.db.session.add(Apontamento)
    else:
        FechamentoOpcao.idOpcao = Opcao.IDOpcao
        FechamentoOpcao.Data = row['data']
        FechamentoOpcao.get_id_data_idasset()
        if FechamentoOpcao.IDFechamentoOpcao == 0 :
            FechamentoOpcao.TipoFechamento = ''
            FechamentoOpcao.Preco = row['pu']
#            sys.exit('Para!')
            app.db.session.add(FechamentoOpcao)
            app.db.session.commit()
del dfPusOps
################################ Cria fechamento de opções sintéticos > D-5 ################################################
############################################################################################################################
############################################################################################################################
################################ Cria fechamento de Futuros sintéticos > D-5 ###############################################
################################ Cria fechamento de Futuros sintéticos > D-5 ###############################################
############################################################################################################################
############################################################################################################################
################################ Cria fechamento de RV sintéticos > D-5 ####################################################
################################ Cria fechamento de RV sintéticos > D-5 ####################################################
############################################################################################################################
############################################################################################################################
######################################## Posicao Batida Com Movimentos? ####################################################
######################################## Posicao Batida Com Movimentos? ####################################################
############################################################################################################################