from app import app
from app.classes.cl_Usuario import cl_Usuario
from app.classes.cl_RF import cl_RF
from app.classes.cl_Fluxo import cl_Fluxo
from flask import render_template as render_template
from flask import Markup as Markup
import json

@app.route("/Cadastro/RF")
def CadastroRF():
    Usuario = cl_Usuario(**{}) 
    if Usuario.Auth_napi(app.session) == False : render_template('Login.html')
    fotopath = app.defaultfotopath
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.png'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.png'
    if app.tkfm.file_exists(app.tk.PathProfileImages + app.sep + 'Profile' + str(Usuario.idUsuario) +  '.jpg'): fotopath = app.fotopath + str(Usuario.idUsuario) +  '.jpg'
    htmlheader = app.codecs.open(app.path + app.headerpath,encoding='UTF-8').read()
    htmlSideBar = app.codecs.open(app.path + app.sidebarpath,encoding='UTF-8').read()
    jsonData = {}
    if app.tkDict.LoadDictBolsas('',1,10000):
        if app.tkDict.LoadDictMoedas('',1,10000):
            if app.tkDict.LoadDictTipoRF(""):
                        if app.tkDict.LoadDictListaEmissor(""):
                            jsonData = {
                                        'ListaBolsa':app.tkDict.DictBolsas["Listaid"],
                                        'ListaMoeda': app.tkDict.DictMoedas["Listaid"],
                                        'ListaTipoMercadoriaRF': app.tkDict.DictTipoRF,
                                        'ListaDictEmissor': app.tkDict.DictListaEmissor,
                                        }
    return render_template('CadastroRendaFixa.html',
                           Header = app.Markup(htmlheader), 
                           SideBar = app.Markup(htmlSideBar) ,
                           picture = fotopath,
                           HeaderUserName = str(Usuario.Nome),
                           jsnDt = jsonData,
                           Usuario_Email = app.session['Usuario_Email'],
                           Usuario_Id = str(app.session['Usuario_Id']),
                           Usuario_Auth = str(app.session['Usuario_Auth'])
                           )
    
@app.route("/Cadastro/RF/Update",methods = ['POST'])
def CadastroRFUpdate():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                

                 
            RF = cl_RF(**{}) 
            if RF.read(app.request.form['IDRF']):
                
                RF.Eventos = json.loads(app.request.form['Events'])
                RF.Situacao= ''
                RF.TipoEmissao= ''
                RF.Garantia= ''
                RF.Classe= ''
                RF.Qtd= ''
                RF.QtdEmitida= ''
                RF.ValorNominalAtual= ''
                RF.TipoCorrecao= ''
                RF.Indexacao= app.request.form['Indexacao']
                RF.DefasagemIndice= app.request.form['DefasagemIndice']
                RF.Alias= app.request.form['Alias']
                RF.Codigo= app.request.form['Codigo']
                RF.Isin= app.request.form['Isin']
                RF.Indice= app.request.form['Indice']
                RF.DUouDC= app.request.form['DUouDC']
                RF.AgenteFiduciario= app.request.form['AgenteFiduciario']
                RF.CoordenadorLider= app.request.form['CoordenadorLider']
                RF.DiasAno= app.request.form['DiasAno']
                RF.RatingEmissao= app.request.form['RatingEmissao']
                RF.AgenciaRatingEmissao= app.request.form['AgenciaRatingEmissao']
                RF.RatingEmissaoMAI= app.request.form['RatingEmissaoMAI']
                RF.idBolsa= app.request.form['idBolsa']
                RF.idMoeda= app.request.form['idMoeda']
                RF.idEmissor= app.request.form['idEmissor']
                RF.idTipoRF= app.request.form['idTipoRF']
                RF.Emissao= app.request.form['Emissao']
                RF.DataInicioRentabilidade= app.request.form['DataInicioRentabilidade']
                RF.Vencimento= app.request.form['Vencimento']
                RF.Carencia= app.request.form['Carencia']
                RF.CarenciaJuros= ''
                RF.AditivoIndice =  app.request.form['AditivoIndice']
                RF.PercIndice =  app.request.form['PercIndice']
                RF.ValorNominalEmissao= app.tkstr.brl_float_string_to_db(app.request.form['ValorNominalEmissao'])
                RF.RegistroCVM= app.tkstr.strtobool(app.request.form['RegistroCVM'])
                RF.Coobrigacao= app.tkstr.strtobool(app.request.form['Coobrigacao'])
                RF.EmDefault= app.tkstr.strtobool(app.request.form['EmDefault'])
                RF.IncorporaJuros= app.tkstr.strtobool(app.request.form['IncorporaJuros'])
                RF.Incentivada= app.tkstr.strtobool(app.request.form['Incentivada'])
                RF.ResgateAntecipado= app.tkstr.strtobool(app.request.form['ResgateAntecipado'])

                if RF.clear_db_events() == False: return app.json.dumps({"resposta" : "Erro ao limpar fluxo"}, ensure_ascii=False).encode('utf-8', 'ignore')
                if RF.insert_events() == False: return app.json.dumps({"resposta" : "Erro ao gravar fluxo"}, ensure_ascii=False).encode('utf-8', 'ignore')

                if RF.set():
                    return app.json.dumps({"resposta" : "RF Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/RF/Insert",methods = ['POST'])
def CadastroRFInsert():
    if app.request.method == 'POST':
        try:
            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            RF = cl_RF(**{})
            RF.Eventos = json.loads(app.request.form['Events'])
            RF.Situacao= ''
            RF.TipoEmissao= ''
            RF.Garantia= ''
            RF.Classe= ''
            RF.Qtd= ''
            RF.QtdEmitida= ''
            RF.ValorNominalAtual= ''
            RF.TipoCorrecao= ''
            RF.Indexacao= app.request.form['Indexacao']
            RF.DefasagemIndice= app.request.form['DefasagemIndice']
            RF.Alias= app.request.form['Alias']
            RF.Codigo= app.request.form['Codigo']
            RF.Isin= app.request.form['Isin']
            RF.Indice= app.request.form['Indice']
            RF.DUouDC= app.request.form['DUouDC']
            RF.AgenteFiduciario= app.request.form['AgenteFiduciario']
            RF.CoordenadorLider= app.request.form['CoordenadorLider']
            RF.DiasAno= app.request.form['DiasAno']
            RF.RatingEmissao= app.request.form['RatingEmissao']
            RF.AgenciaRatingEmissao= app.request.form['AgenciaRatingEmissao']
            RF.RatingEmissaoMAI= app.request.form['RatingEmissaoMAI']
            RF.idBolsa= app.request.form['idBolsa']
            RF.idMoeda= app.request.form['idMoeda']
            RF.idEmissor= app.request.form['idEmissor']
            RF.idTipoRF= app.request.form['idTipoRF']
            RF.Emissao= app.request.form['Emissao']
            RF.DataInicioRentabilidade= app.request.form['DataInicioRentabilidade']
            RF.Vencimento= app.request.form['Vencimento']
            RF.Carencia= app.request.form['Carencia']
            RF.CarenciaJuros= ''
            RF.AditivoIndice=  app.request.form['AditivoIndice']
            RF.PercIndice=  app.request.form['PercIndice']
            RF.ValorNominalEmissao= app.tkstr.brl_float_string_to_db(app.request.form['ValorNominalEmissao'])
            RF.RegistroCVM= app.tkstr.strtobool(app.request.form['RegistroCVM'])
            RF.Coobrigacao= app.tkstr.strtobool(app.request.form['Coobrigacao'])
            RF.EmDefault= app.tkstr.strtobool(app.request.form['EmDefault'])
            RF.IncorporaJuros= app.tkstr.strtobool(app.request.form['IncorporaJuros'])
            RF.Incentivada= app.tkstr.strtobool(app.request.form['Incentivada'])
            RF.ResgateAntecipado= app.tkstr.strtobool(app.request.form['ResgateAntecipado'])
            if RF.insert_full():
                return app.json.dumps({"resposta" : "RF Gravado com Sucesso"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:               
                return app.json.dumps({"resposta" : "Erro ao gravar dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao Gravar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/RF/Delete",methods = ['POST'])
def CadastroRFDelete():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                

            RF = cl_RF(**{})
            if RF.read(app.request.form['IDRF']):
               if RF.remove():
                    if RF.clear_db_events() == False: return app.json.dumps({"resposta" : "Erro ao limpar fluxo"}, ensure_ascii=False).encode('utf-8', 'ignore')
                    return app.json.dumps({"resposta" : "Deletado Com Sucesso!"}, ensure_ascii=False).encode('utf-8', 'ignore')
               else:
                    return app.json.dumps({"resposta" : "Erro ao Deletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                 return app.json.dumps({"resposta" : "Erro ao Deletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
                
        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro Ao deletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')

@app.route("/Cadastro/RF/Search",methods = ['POST'])
def CadastroRFSeach():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                Pag= app.pd.to_numeric(app.request.form['Pag'])
                nPerPag = app.pd.to_numeric(app.request.form['nPerPag'])
                if app.tkDict.LoadDictRF(app.request.form['Search'],Pag,nPerPag):
                     return app.json.dumps({"resposta" : "Ok","Dados":app.tkDict.DictRF}, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro Ao Coletar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')    

@app.route("/Cadastro/RF/Load",methods = ['POST'])
def CadastroRFLoad():
        if app.request.method == 'POST':
            try:

                Usuario = cl_Usuario(**{}) 
                if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
                
                RF = cl_RF(**{})
                if RF.read(app.request.form['IDRF']):
                    RF.get_events()
                    return app.json.dumps({"resposta" : "Ok","Dados": RF.__dict__ }, ensure_ascii=False, default=str).encode('utf-8', 'ignore')
                else:
                    return app.json.dumps({"resposta" : "Erro ao Carregar Dados"}, ensure_ascii=False).encode('utf-8', 'ignore')                   
                    
            except Exception as e: 
                print(e)
                return app.json.dumps({"resposta" : "Erro Ao Coletar Dados: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
        else:
            return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                   


@app.route("/Cadastro/RF/MontaFluxoBullet",methods = ['POST'])
def GravaFluxo():
    if app.request.method == 'POST':
        try:

            Usuario = cl_Usuario(**{}) 
            if Usuario.Auth_api(app.request) == False : return app.json.dumps({"resposta" : "Falha na Autenticação"}, ensure_ascii=False).encode('utf-8', 'ignore')                
            

            RF = cl_RF(**{})

            if app.tkstr.ValidDate(app,app.request.form['DataVencimento']) == False:
                return app.json.dumps({"resposta" : "DataVencimento Invalida!!"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                RF.Vencimento = app.dt.strptime(app.request.form['DataVencimento'],'%Y-%m-%d')

            if app.tkstr.ValidDate(app,app.request.form['DataEmissao']) == False:
                return app.json.dumps({"resposta" : "DataEmissao Invalida!!"}, ensure_ascii=False).encode('utf-8', 'ignore')
            else:
                RF.Emissao = app.dt.strptime(app.request.form['DataEmissao'],'%Y-%m-%d')

            if app.tkstr.ValidDate(app,app.request.form['DataInicioRentabilidade']) == False:
                RF.DataInicioRentabilidade = RF.Emissao
            else:
                if RF.Emissao < app.dt.strptime(app.request.form['DataInicioRentabilidade'],'%Y-%m-%d'):
                    RF.DataInicioRentabilidade = app.dt.strptime(app.request.form['DataInicioRentabilidade'],'%Y-%m-%d')

            RF.AditivoIndice = 0
            RF.PercIndice = 0
            RF.DiasAno = 252
            if app.request.form['AditivoIndice'] != '' and app.request.form['AditivoIndice'] != 0:
                 RF.AditivoIndice = app.pd.to_numeric(app.request.form['AditivoIndice'],errors='coerce')
            if app.request.form['PercIndice'] != '' and app.request.form['PercIndice'] != 0:
                 RF.PercIndice = app.pd.to_numeric(app.request.form['PercIndice'],errors='coerce')

            if app.request.form['DiasAno'] != '' and app.request.form['DiasAno'] != 0:
                 RF.DiasAno = app.pd.to_numeric(app.tkstr.brl_float_string_to_db(app.request.form['DiasAno']),errors='coerce')

            if app.request.form['Indice'] not in ('CDI','IPCA','IGP-M','PRE'):
                return app.json.dumps({"resposta" : "Indice Invalido para essa Operação!!"}, ensure_ascii=False).encode('utf-8', 'ignore')
            

            FluxoAll = []
            if app.request.form['Indice']=="CDI":
                if app.request.form['Indexacao'] == "% do Indice":
                    FluxoAll.append({
                                'Data' : app.request.form['DataVencimento'],
                                'Indice' : app.request.form['Indice'],
                                'ValorLiq' : 0,
                                'TipoEvento' : 'Juros',
                                'PercEvento' : 0,
                                'ValorLiq' : 0,
                                'TipoIncidencia' : '%VNE',
                                'idRf':-1
                            })
                    FluxoAll.append({
                                'Data' : app.request.form['DataVencimento'],
                                'Indice' : app.request.form['Indice'],
                                'ValorLiq' : 0,
                                'TipoEvento' : 'Amortização',
                                'PercEvento' : 1,
                                'ValorLiq' : 0,
                                'TipoIncidencia' : '%VNE'
                            })
                elif app.request.form['Indexacao'] == "Indice + Spread":
                    FluxoAll.append({
                                'Data' : app.request.form['DataVencimento'],
                                'Indice' : app.request.form['Indice'],
                                'ValorLiq' : 0,
                                'TipoEvento' : 'Juros',
                                'PercEvento' : pow((1 + RF.AditivoIndice),(app.tkdtm.net_work_day(RF.DataInicioRentabilidade, RF.Vencimento) / RF.DiasAno)) - 1,
                                'ValorLiq' : 0,
                                'TipoIncidencia' : '%VNE',
                                'idRf':-1
                            })
                    FluxoAll.append({
                                'Data' : app.request.form['DataVencimento'],
                                'Indice' : app.request.form['Indice'],
                                'ValorLiq' : 0,
                                'TipoEvento' : 'Amortização',
                                'PercEvento' : 1,
                                'ValorLiq' : 0,
                                'TipoIncidencia' : '%VNE'
                            })
            elif app.request.form['Indice']=="IPCA" or app.request.form['Indice']=="IGP-M" :
                FluxoAll.append({
                            'Data' : app.request.form['DataVencimento'],
                            'Indice' : app.request.form['Indice'],
                            'ValorLiq' : 0,
                            'TipoEvento' : 'Juros',
                            'PercEvento' : pow((1 + RF.AditivoIndice),(app.tkdtm.net_work_day(RF.DataInicioRentabilidade, RF.Vencimento) / RF.DiasAno)) - 1,
                            'ValorLiq' : 0,
                            'TipoIncidencia' : '%VNA',
                            'idRf':-1
                        })
                FluxoAll.append({
                            'Data' : app.request.form['DataVencimento'],
                            'Indice' : app.request.form['Indice'],
                            'ValorLiq' : 0,
                            'TipoEvento' : 'Amortização',
                            'PercEvento' : 1,
                            'ValorLiq' : 0,
                            'TipoIncidencia' : '%VNA'
                        })
            elif app.request.form['Indice']=="PRE":
                FluxoAll.append({
                            'Data' : app.request.form['DataVencimento'],
                            'Indice' : app.request.form['Indice'],
                            'ValorLiq' : 0,
                            'TipoEvento' : 'Juros',
                            'PercEvento' : pow((1 + RF.AditivoIndice),(app.tkdtm.net_work_day(RF.DataInicioRentabilidade, RF.Vencimento) / RF.DiasAno)) - 1,
                            'ValorLiq' : 0,
                            'TipoIncidencia' : '%VNE',
                            'idRf':-1
                        })
                FluxoAll.append({
                            'Data' : app.request.form['DataVencimento'],
                            'Indice' : app.request.form['Indice'],
                            'ValorLiq' : 0,
                            'TipoEvento' : 'Amortização',
                            'PercEvento' : 1,
                            'ValorLiq' : 0,
                            'TipoIncidencia' : '%VNE'
                        })

            return app.json.dumps({"resposta" : "Ok","Eventos":FluxoAll}, ensure_ascii=False).encode('utf-8', 'ignore')

        except Exception as e: 
            print(e)
            return app.json.dumps({"resposta" : "Erro na Montage: " + str(e)}, ensure_ascii=False).encode('utf-8', 'ignore')
    else:
        return app.json.dumps({"resposta" : "Request Invalida"}, ensure_ascii=False).encode('utf-8', 'ignore')                
