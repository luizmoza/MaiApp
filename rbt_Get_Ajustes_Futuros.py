import sys
import warnings
warnings.filterwarnings("ignore")
sys.path.append(r"../")
from app import app
from app.classes.cl_Futuro import cl_Futuro
from app.classes.cl_FechamentoFuturo import cl_FechamentoFuturo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
#https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.70/win64/chromedriver-win64.zip
#https://www.youtube.com/watch?v=BnY4PZyL9cg


if len(sys.argv)>1:
    data = sys.argv[1]
else:
    data = app.tkdtm.hoje
      

###############################################################################################################################
########################################## Ajustes de Futuros Pregão ##########################################################
print('Iniciando Carga dos Ajustes de Futuros :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))
D_20 = app.tkdtm.date_after_work_days(data,-5)
while data >= D_20:
    
    data = app.tkdtm.date_after_work_days(data,-1)
    print('Carregando dados de :' + data.strftime('%Y-%m-%d'))
    service = Service(executable_path=r'./chromedriver.exe')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-ajustes-do-pregao-ptBR.asp');
    time.sleep(5)
    driver.find_element(By.ID, "dData1").clear()
    driver.find_element(By.ID, "dData1").send_keys(data.strftime('%d/%m/%Y'))
    all_options = driver.find_elements(By.TAG_NAME,'button')
    for option in all_options:
        option.click()
    
    table = driver.find_element(By.ID, "tblDadosAjustes")
    dfAjustes = app.pd.read_html(table.get_attribute('outerHTML').replace('.','').replace(',','.'))[0].copy()
    dfAjustes['data'] = data
    dfAjustes = dfAjustes.rename(columns={ 'Vencimento':'Sufixo', 
                                           'Preço de ajuste anterior':'PUD_1',
                                           'Preço de ajuste Atual':'PUD0', 
                                           'Variação':'Ajuste',
                                           'Valor do ajuste por contrato (R$)':'Ajuste_pContrato'}).copy()
    driver.quit()
    
    Futuro = cl_Futuro(**{})
    for index,row in dfAjustes.iterrows(): 
        Futuro.Alias = 'Futuro#BRLB3@FUT ' + app.tkstr.left(row['Mercadoria'],row['Mercadoria'].find(' - ')) + ' ' + row['Sufixo']
        Futuro.IDFuturo = -1
        Futuro.get_id_alias()
        if Futuro.get():
            print('Carregando: FUT ' + app.tkstr.left(row['Mercadoria'],row['Mercadoria'].find(' - ')) + ' ' + row['Sufixo'] + ' ...... O Id é :' + str(Futuro.IDFuturo) + ' Data: ' + data.strftime('%Y-%m-%d'))


            # Ajuste BTG Rymer
            sql = """
            update posicao set pu = '""" + "{:10.4f}".format(row['PUD0']) + """',pu1 = '""" + "{:10.4f}".format(row['PUD_1']) + """'
            where cgc in (SELECT CGC FROM Fundo where administrador = 'BTG PACTUAL' and Interno = 1)
            and data = '""" +  row['data'].strftime('%Y-%m-%d') +  """'
            and aliasativo =  'Futuro#BRLB3@""" + 'FUT ' + app.tkstr.left(row['Mercadoria'],row['Mercadoria'].find(' - ')) + ' ' + row['Sufixo'] + """'        
            """
            app.db.execRawQuery(sql)
            # Ajuste BTG Rymer



            FechamentoFuturo = cl_FechamentoFuturo(**{})
            FechamentoFuturo.IDFechamentoFuturo = -1
            FechamentoFuturo.idFuturo = Futuro.IDFuturo
            FechamentoFuturo.Data = app.pd.to_datetime(row['data'])
            if FechamentoFuturo.get_id_data_idasset():
                if FechamentoFuturo.get():
                        FechamentoFuturo.IDFuturo = Futuro.IDFuturo
                        FechamentoFuturo.Data = app.pd.to_datetime(row['data'])
                        FechamentoFuturo.Ticker = 'FUT ' + app.tkstr.left(row['Mercadoria'],row['Mercadoria'].find(' - ')) + ' ' + row['Sufixo']
                        FechamentoFuturo.PuD0 = row['PUD0']
                        FechamentoFuturo.PuD1 = row['PUD_1']
                        FechamentoFuturo.Variacao = row['Ajuste']
                        FechamentoFuturo.Ajuste = row['Ajuste_pContrato']
                        FechamentoFuturo.PuFechamento = 0
                        FechamentoFuturo.set()
            else:
                FechamentoFuturo = cl_FechamentoFuturo(**{})
                FechamentoFuturo.idFuturo = Futuro.IDFuturo
                FechamentoFuturo.Data = app.pd.to_datetime(row['data'])
                FechamentoFuturo.Ticker = 'FUT ' + app.tkstr.left(row['Mercadoria'],row['Mercadoria'].find(' - ')) + ' ' + row['Sufixo']
                FechamentoFuturo.PuD0 = row['PUD0']
                FechamentoFuturo.PuD1 = row['PUD_1']
                FechamentoFuturo.Variacao = row['Ajuste']
                FechamentoFuturo.Ajuste = row['Ajuste_pContrato']
                FechamentoFuturo.PuFechamento = 0
                FechamentoFuturo.insert()
    
    del driver
    del service
    del options
    del dfAjustes

print('Fim Carga dos Ajustes de Futuros :' + app.dt.now().strftime('%Y-%m-%d %H:%M:%S'))

########################################## Ajustes de Futuros Pregão ##########################################################
###############################################################################################################################