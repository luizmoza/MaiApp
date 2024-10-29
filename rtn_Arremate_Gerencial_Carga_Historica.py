import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.append(r"../")
from app import app
from app.classes.cl_Gerencial import cl_Gerencial

print('Inicio Carga de Dados:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))


Gerencial = cl_Gerencial()

print('importando0:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfDadosGO = app.pd.read_excel(r"C:/Users/Luiz Moza/OneDrive/Área de Trabalho/Gerencial OAB GO D-2.xlsm", 'Base de Dados',skiprows=[0])
dfDadosGO['Carteira'] = 'OAB GO'
print('importando1:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfDadosSBOT = app.pd.read_excel(r"C:/Users/Luiz Moza/OneDrive/Área de Trabalho/Gerencial SBOT D-2.xlsm", 'Base de Dados',skiprows=[0])
dfDadosSBOT['Carteira'] = 'SBOT'
print('importando2:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfDadosSC = app.pd.read_excel(r"C:/Users/Luiz Moza/OneDrive/Área de Trabalho/Gerencial OAB SC D-2.xlsm", 'Base de Dados',skiprows=[0])
dfDadosSC['Carteira'] = 'OAB SC'
print('importando3:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfDadosBalder = app.pd.read_excel(r"C:/Users/Luiz Moza/OneDrive/Área de Trabalho/Gerencial Balder D-2.xlsm", 'Base de Dados')
dfDadosBalder['Carteira'] = 'Balder'
print('importando4:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
dfDadoscresol = app.pd.read_excel(r"C:/Users/Luiz Moza/OneDrive/Área de Trabalho/Gerencial Cresol D-2.xlsm", 'Base de Dados',skiprows=[0])
dfDadoscresol['Carteira'] = 'Cresol'
print('importando5:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))

dfDados = app.pd.concat([dfDadosGO.copy(),dfDadosSBOT.copy(),dfDadosSC.copy(),dfDadosBalder.copy(),dfDadoscresol.copy()], ignore_index=True)

del dfDadosGO
del dfDadosSBOT
del dfDadosSC
del dfDadosBalder
del dfDadoscresol

dfDados = dfDados.rename(columns={
    'Carteira':'AliasFundo',
    'Ativo':'AliasAtivo',
    'Macro Estratégia':'Macro',
    'Estrategia':'Estrat',
    'Fin D-1':'FinD1',
    'Over Carrego':'Over_Carrego',
    'Carrego Específico':'Carrego_Espec',
    'Over Carrego Específico':'Over_Carrego_Espec',
    '% Over Carrego':'Perc_Carrego',
    '% Over Carrego Específico':'Perc_Carregi_Espec',
    'Indice Específico':'Indice_Espec',
    '%PL':'Perc_PL'
    })
dfDados = dfDados[['Data','AliasFundo','Trader','AliasAtivo','Macro','Estrat','Quantidade','Fin','FinD1','Resultado','Carrego','Over_Carrego','Carrego_Espec','Over_Carrego_Espec','Perc_Carrego','Perc_Carregi_Espec','PL','Indice_Espec','Perc_PL']]


print('unBulkando:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))  

dfDados_list_aliasfundo = dfDados['AliasFundo'].drop_duplicates().reset_index().copy()
dfDados_list_dates = dfDados['Data'].drop_duplicates().reset_index().copy()
for index,row in dfDados_list_aliasfundo.iterrows():
    Gerencial.unbulk(dfDados[dfDados['AliasFundo'] == row['AliasFundo']]['Data'].min(),dfDados[dfDados['AliasFundo'] == row['AliasFundo']]['Data'].max(),row['AliasFundo'])
    print('Unbulkando Fundo:' + row['AliasFundo'] + 'Data ini: ' + dfDados[dfDados['AliasFundo'] == row['AliasFundo']]['Data'].min().strftime('%Y-%m-%d') + 'Data fim: ' + dfDados[dfDados['AliasFundo'] == row['AliasFundo']]['Data'].max().strftime('%Y-%m-%d') )

print('Bulkando:' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))

dfDados['Perc_PL'] = app.pd.to_numeric(dfDados['Perc_PL'],errors='coerce')
dfDados['PL'] = app.pd.to_numeric(dfDados['PL'],errors='coerce')
dfDados['Perc_Carregi_Espec'] = app.pd.to_numeric(dfDados['Perc_Carregi_Espec'],errors='coerce')
dfDados['Perc_Carrego'] = app.pd.to_numeric(dfDados['Perc_Carrego'],errors='coerce')
dfDados['Over_Carrego_Espec'] = app.pd.to_numeric(dfDados['Over_Carrego_Espec'],errors='coerce')
dfDados['Carrego_Espec'] = app.pd.to_numeric(dfDados['Carrego_Espec'],errors='coerce')
dfDados['Over_Carrego'] = app.pd.to_numeric(dfDados['Over_Carrego'],errors='coerce')
dfDados['Carrego'] = app.pd.to_numeric(dfDados['Carrego'],errors='coerce')
dfDados['Resultado'] = app.pd.to_numeric(dfDados['Resultado'],errors='coerce')
dfDados['FinD1'] = app.pd.to_numeric(dfDados['FinD1'],errors='coerce')
dfDados['Fin'] = app.pd.to_numeric(dfDados['Fin'],errors='coerce')
dfDados['Quantidade'] = app.pd.to_numeric(dfDados['Quantidade'],errors='coerce')

dfDados['Perc_PL'] = dfDados['Perc_PL'].fillna(0)
dfDados['PL'] = dfDados['PL'].fillna(0)
dfDados['Perc_Carregi_Espec'] = dfDados['Perc_Carregi_Espec'].fillna(0)
dfDados['Perc_Carrego'] = dfDados['Perc_Carrego'].fillna(0)
dfDados['Over_Carrego_Espec'] = dfDados['Over_Carrego_Espec'].fillna(0)
dfDados['Carrego_Espec'] = dfDados['Carrego_Espec'].fillna(0)
dfDados['Over_Carrego'] = dfDados['Over_Carrego'].fillna(0)
dfDados['Carrego'] = dfDados['Carrego'].fillna(0)
dfDados['Resultado'] = dfDados['Resultado'].fillna(0)
dfDados['FinD1'] = dfDados['FinD1'].fillna(0)
dfDados['Fin'] = dfDados['Fin'].fillna(0)
dfDados['Quantidade'] = dfDados['Quantidade'].fillna(0)

for index,row in dfDados_list_dates.iterrows():
    print('Bulkando Data: ' + row['Data'].strftime('%Y-%m-%d') + 'Status Query:' + Gerencial.__db__.statusquery + ' horário: '  + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
    Gerencial.bulk(dfDados[dfDados['Data']==row['Data']])

